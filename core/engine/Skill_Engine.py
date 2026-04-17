import random
from copy import deepcopy
from pathlib import Path

from core.llm.ai_client import ask_ai
from core.rag.rag_engine import search
from services.prompt_loader import compress_docs, render_prompt


class SkillValidationError(ValueError):
    pass


class SafeDict(dict):
    def __missing__(self, key):
        return ""


class SkillEngine:
    def __init__(self, skill_yaml, base_dir=None):
        self.skill = skill_yaml
        self.base_dir = Path(base_dir or Path(__file__).resolve().parents[2])
        self.handlers = {
            "normalize_input": self.normalize_input,
            "enrich_context": self.enrich_context,
            "build_prompt": self.build_prompt,
            "assemble_result": self.assemble_result,
        }

    def run(self, input_data, history=None):
        state = deepcopy(input_data)
        state["history"] = deepcopy(history or [])
        state.setdefault("references", [])
        state.setdefault("analysis", "")
        state.setdefault("summary", "")

        for node in self.skill.get("workflow", []):
            state = self.execute(node, state)
            if node.get("id") == "preprocess":
                self.validate_schema(
                    state,
                    self.skill.get("input_schema", {}),
                    label="input",
                )

        if "preprocess" not in {node.get("id") for node in self.skill.get("workflow", [])}:
            self.validate_schema(
                state,
                self.skill.get("input_schema", {}),
                label="input",
            )

        result = state.get("result")
        self.validate_schema(
            result,
            self.skill.get("output_schema", {}),
            label="output",
        )
        return result

    def execute(self, node, state):
        node_type = node.get("type")

        if node_type == "transform":
            handler_name = node.get("handler")
            handler = self.handlers.get(handler_name)
            if handler is None:
                raise SkillValidationError(f"Unknown handler: {handler_name}")
            return handler(node, state)

        if node_type == "llm":
            return self.handle_llm(node, state)

        raise SkillValidationError(f"Unknown node type: {node_type}")

    def handle_llm(self, node, state):
        prompt_key = node.get("prompt_key", "prompt")
        output_key = node.get("output_key", "output")
        mode_key = node.get("mode_key")
        mode = state.get(mode_key) if mode_key else node.get("mode", "generate")
        prompt = state.get(prompt_key, "").strip()

        if not prompt:
            raise SkillValidationError(f"LLM node requires non-empty prompt at '{prompt_key}'")

        state[output_key] = ask_ai(
            prompt=prompt,
            history=state.get("history"),
            mode=mode or "generate",
        )
        return state

    def normalize_input(self, node, state):
        defaults = node.get("defaults", {})
        for key, value in defaults.items():
            state.setdefault(key, value)

        for key, value in list(state.items()):
            if isinstance(value, str):
                state[key] = value.strip()

        state["llm_mode"] = state.get("llm_mode") or ("optimize" if state.get("history") else "generate")
        state["prompt_type"] = state.get("prompt_type") or "rag"
        state["theme"] = state.get("theme") or "未命名校园活动"
        state["type_"] = state.get("type_") or "综合活动"
        state["target_audience"] = state.get("target_audience") or "校内学生"
        state["goal_priority"] = state.get("goal_priority") or "参与度"
        state["duration"] = state.get("duration") or 2
        state["venue_type"] = state.get("venue_type") or "室内"
        return state

    def enrich_context(self, node, state):
        prompt_type = state.get("prompt_type")
        state["references"] = []
        state["analysis"] = ""
        state["summary"] = ""
        state["example"] = ""

        if prompt_type == "fewshot":
            example = self.pick_example()
            state["example"] = example
            state["references"] = ["fewshot-example"]
            return state

        if prompt_type != "rag":
            return state

        query_template = node.get("query_template", "{theme} {type_} 校园活动")
        analysis_template = node.get(
            "analysis_prompt_template",
            "分析这个活动的关键策划要点：\n主题：{theme}\n类型：{type_}\n预算：{budget}\n人数：{person}\n列出5条关键点",
        )
        top_k = int(node.get("top_k", 2))
        doc_char_limit = int(node.get("doc_char_limit", 500))

        query = query_template.format_map(SafeDict(state))
        analysis_prompt = analysis_template.format_map(SafeDict(state))

        docs = search(query, k=top_k)
        docs = [doc[:doc_char_limit] for doc in docs]

        state["references"] = docs
        if docs:
            state["summary"] = compress_docs(docs)
        state["analysis"] = ask_ai(analysis_prompt)
        return state

    def build_prompt(self, node, state):
        template_map = node.get(
            "templates",
            {
                "role": "role.txt",
                "step": "step.txt",
                "fewshot": "fewshot.txt",
                "rag": "rag.txt",
            },
        )
        prompt_type = state.get("prompt_type", "rag")
        template_name = template_map.get(prompt_type)
        if not template_name:
            raise SkillValidationError(f"Unsupported prompt_type: {prompt_type}")

        payload = {
            "theme": state.get("theme", ""),
            "type": state.get("type_", ""),
            "type_": state.get("type_", ""),
            "budget": state.get("budget", 0),
            "person": state.get("person", 0),
            "duration": state.get("duration", ""),
            "venue_type": state.get("venue_type", ""),
            "target_audience": state.get("target_audience", ""),
            "goal_priority": state.get("goal_priority", ""),
            "goal_prior": state.get("goal_priority", ""),
            "prompt_type": prompt_type,
            "analysis": state.get("analysis", ""),
            "summary": state.get("summary", ""),
            "example": state.get("example", ""),
        }
        state["prompt"] = render_prompt(template_name, payload)
        state["strategy"] = prompt_type
        return state

    def assemble_result(self, node, state):
        state["result"] = {
            "plan_markdown": state.get("plan_markdown", "").strip(),
            "strategy": state.get("strategy", state.get("prompt_type", "rag")),
            "analysis": state.get("analysis", "").strip(),
            "summary": state.get("summary", "").strip(),
            "references": state.get("references", []),
        }
        return state

    def pick_example(self):
        data_dir = self.base_dir / "data"
        candidates = sorted(
            path for path in data_dir.iterdir()
            if path.is_file() and path.suffix == ".txt"
        )
        if not candidates:
            return ""

        choice = random.choice(candidates)
        return choice.read_text(encoding="utf-8")

    def validate_schema(self, data, schema, label):
        if not schema:
            return
        self._validate_by_type(data, schema, path=label)

    def _validate_by_type(self, data, schema, path):
        expected = schema.get("type")
        if expected is None:
            return

        if expected == "object":
            if not isinstance(data, dict):
                raise SkillValidationError(f"{path} must be an object")

            required = schema.get("required", [])
            for key in required:
                if key not in data or data[key] in (None, ""):
                    raise SkillValidationError(f"{path}.{key} is required")

            properties = schema.get("properties", {})
            for key, value in data.items():
                subschema = properties.get(key)
                if subschema:
                    self._validate_by_type(value, subschema, f"{path}.{key}")
            return

        if expected == "array":
            if not isinstance(data, list):
                raise SkillValidationError(f"{path} must be an array")
            item_schema = schema.get("items")
            if item_schema:
                for index, item in enumerate(data):
                    self._validate_by_type(item, item_schema, f"{path}[{index}]")
            return

        if expected == "string":
            if not isinstance(data, str):
                raise SkillValidationError(f"{path} must be a string")
            return

        if expected == "integer":
            if not isinstance(data, int) or isinstance(data, bool):
                raise SkillValidationError(f"{path} must be an integer")
            return

        if expected == "number":
            if not isinstance(data, (int, float)) or isinstance(data, bool):
                raise SkillValidationError(f"{path} must be a number")
            return

        if expected == "boolean":
            if not isinstance(data, bool):
                raise SkillValidationError(f"{path} must be a boolean")
