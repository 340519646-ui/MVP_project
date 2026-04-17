# Campus Event Planner AI

<!-- Badges -->
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 校园活动策划 AI 助手 - 基于多策略 Prompt 与 RAG 增强的活动策划生成系统

---

## 📋 Table of Contents

- [项目概述](#项目概述)
- [核心功能](#核心功能)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [开发指南](#开发指南)
- [技术重构规划](#技术重构规划)
- [贡献指南](#贡献指南)

---

## 项目概述

`Campus Event Planner AI` 是一款基于大语言模型的校园活动策划生成工具。用户通过输入活动主题、类型、预算等参数，即可获得一份结构完整、可执行的校园活动策划方案。

### 核心价值

| 维度 | 说明 |
|------|------|
| 🎯 **输入** | 活动主题、类型、预算、人数、时长、场地、目标人群 |
| 📄 **输出** | 活动背景、目标、创意、流程、人员分工、预算明细、风险预案、宣传方案 |
| ⚡ **特色** | 多策略 Prompt 切换、RAG 知识增强、多轮优化迭代 |

---

## 核心功能

### 支持的 Prompt 策略

| 策略 | 描述 | 适用场景 |
|------|------|---------|
| `role` | 角色扮演式 Prompt | 快速生成、结构化输出 |
| `step` | 步骤分解式 Prompt | 复杂活动、详细策划 |
| `fewshot` | 示例引导式 Prompt | 需要参考案例的风格 |
| `rag` | 知识增强式 Prompt | 需要结合历史案例 |

### 多轮优化

支持在生成策划案后，根据反馈进行多轮优化：

1. 生成初版策划案
2. 输入修改需求（如"增加互动环节"、"优化预算分配"）
3. AI 基于上下文进行针对性优化

---

## 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         Streamlit 前端                            │
│                      (app/app.py)                                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       服务编排层                                  │
│  planner_service │ prompt_loader │ prompts_choice │ skill_service │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       核心业务层                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ Planner │  │ LLM     │  │ Skill   │  │ RAG     │             │
│  │         │  │ Client  │  │ Engine  │  │ Engine  │             │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       外部依赖                                    │
│     DeepSeek API      │    FAISS Index    │   文件系统           │
└─────────────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术选型 |
|------|---------|
| **前端** | Streamlit >= 1.30.0 |
| **LLM** | OpenAI SDK + DeepSeek API |
| **RAG** | FAISS + Sentence-Transformers |
| **模板引擎** | Jinja2 |
| **配置管理** | YAML |

---

## 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd mvp

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 OPENAI_API_KEY

# 5. 启动应用
streamlit run app/app.py
streamlit run app/skill.py
```

### 环境变量配置

创建 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com
LOG_LEVEL=INFO
```

---

## 项目结构

```
mvp/
├── app/                          # Streamlit 应用
│   └── app.py                    # 主应用入口
├── core/                         # 核心业务层
│   ├── engine/                   # 技能引擎
│   │   ├── Skill_Engine.py       # 核心引擎
│   │   └── Skill_rag.py          # RAG 技能
│   ├── llm/                      # LLM 客户端
│   │   └── ai_client.py          # AI 调用封装
│   ├── planner/                  # 策划逻辑
│   │   └── planner.py
│   └── rag/                      # RAG 检索
│       └── rag_engine.py
├── services/                     # 服务编排层
│   ├── planner_service.py        # 策划服务
│   ├── prompt_loader.py          # 模板加载
│   ├── prompts_choice.py         # 策略选择
│   └── skill_service.py          # 技能服务
├── skill/                        # 技能配置
│   └── Skill_definition.yaml     # 工作流配置
├── prompts/                      # Prompt 模板
│   ├── role.txt
│   ├── step.txt
│   ├── fewshot.txt
│   ├── rag.txt
│   └── prompts.yaml
├── data/                         # 示例数据
│   └── *.txt
├── model/                        # 嵌入向量模型
├── test/                         # 测试文件
├── REMAKE.md                     # 重构规划
├── requirements.txt              # 依赖清单
└── .env.example                 # 环境变量示例
```

---

## 配置说明

### Skill 工作流配置

编辑 `skill/Skill_definition.yaml` 来自定义工作流：

```yaml
skill_name: campus_event_planner
version: 1.0.0

workflow:
  - id: preprocess
    type: transform
    handler: normalize_input
    defaults:
      prompt_type: rag
      duration: 2

  - id: enrich_context
    type: transform
    handler: enrich_context
    top_k: 2
    doc_char_limit: 500

  - id: build_prompt
    type: transform
    handler: build_prompt
    templates:
      role: role.txt
      step: step.txt
      fewshot: fewshot.txt
      rag: rag.txt

  - id: generate_plan
    type: llm
    prompt_key: prompt
    output_key: plan_markdown
```

### Prompt 模板变量

支持的模板变量：

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `theme` | string | 活动主题 |
| `type_` | string | 活动类型 |
| `budget` | number | 预算范围 |
| `person` | integer | 参与人数 |
| `duration` | number | 活动时长 |
| `venue_type` | string | 场地类型 |
| `target_audience` | string | 目标人群 |
| `goal_priority` | string | 核心目标 |

---

## 开发指南

### 添加新的 Prompt 策略

1. 在 `prompts/` 目录创建新的模板文件（如 `cot.txt`）
2. 在 `Skill_definition.yaml` 的 `templates` 中注册
3. 在 `app.py` 的 `selectbox` 选项中添加新策略

```python
prompt_type = st.selectbox(
    "生成策略",
    ["role", "step", "fewshot", "rag", "cot"],  # 添加新策略
)
```

### 扩展 RAG 数据源

将 `.txt` 文件放入 `data/` 目录，文件名即为文档 ID：

```
data/
├── 迎新晚会案例.txt
├── 体育赛事策划.txt
└── 学术论坛指南.txt
```

### 运行测试

```bash
pytest test/ -v
```

---

## 技术重构规划

> 详细的重构计划请参阅 [REMAKE.md](REMAKE.md)

### 阶段一：基础设施加固

- [ ] API 客户端安全化（延迟初始化、密钥验证）
- [ ] 异常处理增强（分类异常处理）
- [ ] 路径安全加固

### 阶段二：架构清理

- [ ] 统一使用 SkillEngine 工作流
- [ ] 废弃 `prompts_choice.py` 重复逻辑
- [ ] 添加类型注解

### 阶段三：性能优化

- [ ] RAG 索引预加载机制
- [ ] LLM 响应缓存
- [ ] 并发控制

### 阶段四：功能扩展

- [ ] 新 Prompt 策略（CoT、Self-Consistency）
- [ ] 多格式输出（JSON、Word、PDF）
- [ ] 多租户支持

---

## 贡献指南

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8
- 使用类型注解
- 为公共函数编写 docstring
- 添加单元测试

### 问题反馈

如遇到问题，请通过以下方式反馈：

- [提交 Issue](https://github.com/your-repo/issues)
- 邮箱: your-email@example.com

---

## 📄 License

本项目基于 MIT License 开源，详见 [LICENSE](LICENSE) 文件。

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) - 数据应用框架
- [DeepSeek](https://deepseek.com/) - 大语言模型
- [FAISS](https://github.com/facebookresearch/faiss) - 向量检索库
- [Sentence-Transformers](https://www.sbert.net/) - 文本嵌入模型
