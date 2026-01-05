# 专业领域 AI Agent 调研平台

> 全面调研 CAD、Circuit、LaTeX、Framework 等专业领域的 AI Agent 项目和技术栈

## 项目概述

这是一个自动化的技术调研平台，旨在：
- 🔍 自动搜索和分析 GitHub 上的相关项目（已收集 **328+ 项目**）
- 📊 生成交互式可视化报告（多领域对比分析）
- 🚀 **并行搜索**：10个并行 agent，4秒完成全领域搜索
- 🤖 AI 智能推荐最佳技术栈
- 💰 混合 LLM 策略（Claude + OpenAI + 本地模型）降低成本

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd /Users/xiaobotu/Documents/ai_agent

# 安装依赖
pip install requests

# （可选但推荐）设置 GitHub Token
export GITHUB_TOKEN="your_github_token_here"
```

### 2. 获取 GitHub Token

访问 https://github.com/settings/tokens 创建 Personal Access Token：
- 无需任何特殊权限
- 作用：将 API 限额从 60 次/小时提升到 5000 次/小时

### 3. 运行搜索工具

#### 方式 1: 单领域搜索（LaTeX）
```bash
cd tools
python3 gh_batch_search.py
```

#### 方式 2: 多领域并行搜索（推荐）
```bash
cd tools
python3 parallel_search.py
```

这将：
- 🚀 使用 10 个并行线程同时搜索 4 个领域
- 🔍 搜索 328+ 个 AI Agent 相关项目
  - LaTeX: 138 项目（平均 1.5K stars）
  - Framework: 138 项目（平均 10K stars）
  - CAD: 32 项目（平均 697 stars）
  - Circuit: 20 项目（平均 194 stars）
- 💾 自动创建 SQLite 数据库
- 📄 导出各领域 JSON 数据文件
- ⚡ 仅需 **4 秒**完成全部搜索

## 项目结构

```
ai_agent/
├── README.md                    # 本文件
├── tools/                       # 调研工具
│   ├── github_searcher.py      # GitHub REST API 搜索
│   ├── gh_batch_search.py      # GitHub CLI 批量搜索
│   ├── parallel_search.py      # 并行多领域搜索
│   ├── recommendation_engine.py # AI 智能推荐引擎 ⭐ NEW
│   ├── project_analyzer.py     # 项目深度分析（开发中）
│   └── llm_router.py           # 智能 LLM 路由（计划中）
├── api/                         # API 服务 ⭐ NEW
│   ├── recommendation_api.py   # 推荐引擎 RESTful API
│   └── requirements.txt        # API 依赖
├── data/                        # 数据存储
│   ├── projects.db             # SQLite 数据库（328+ 项目）
│   ├── latex/                  # LaTeX 领域数据（138 项目）
│   │   └── projects.json
│   ├── cad/                    # CAD 领域数据（32 项目）
│   │   └── projects.json
│   ├── circuit/                # Circuit 领域数据（20 项目）
│   │   └── projects.json
│   └── framework/              # Framework 领域数据（138 项目）
│       └── projects.json
├── reports/                     # 调研报告 ⭐ NEW
│   ├── 2025_latest/            # 2025 最新调研
│   │   └── Executive_Summary.md # 执行摘要（WebSearch 数据）
│   └── WebSearch_Research_Report.md # 完整调研报告
├── web/                         # 交互式网页
│   ├── overview.html           # 多领域概览仪表板
│   ├── recommendation.html     # AI 智能推荐页面 ⭐ NEW
│   ├── index.html              # LaTeX 专题页
│   └── comparison.html         # 项目对比（计划中）
└── 专业领域AI Agent产品计划.md   # 产品规划

```

## 功能特性

### ✅ 已完成
- [x] 项目目录结构
- [x] GitHub 自动搜索工具（REST API + CLI）
- [x] **并行搜索引擎**（10个并发线程）⭐
- [x] SQLite 数据库设计（328+ 项目）
- [x] **多领域数据收集**：LaTeX、CAD、Circuit、Framework ⭐
- [x] **交互式网页界面**（多领域概览 + LaTeX 专题页）⭐
- [x] 实时数据可视化（Chart.js）
- [x] 领域分布分析和语言统计
- [x] **WebSearch 补充调研**（20个查询，2025最新数据）⭐
- [x] **AI 智能推荐引擎**（需求匹配 + 相关度评分）⭐ NEW
  - 基于用户需求自动推荐最佳工具
  - 整合 GitHub 328+ 项目 + 2025 商业工具数据
  - 支持多维度筛选（领域、经验、预算、功能）
  - 智能评分算法（活跃度、功能匹配、社区支持）
  - RESTful API 接口

### 🚧 进行中
- [ ] 项目深度分析工具
- [ ] 项目对比功能

### 📅 计划中
- [ ] 自动化更新脚本
- [ ] GitHub Pages 部署
- [ ] 增强推荐算法（机器学习模型）

## 使用示例

### 并行搜索多个领域（推荐）

```bash
cd tools
python3 parallel_search.py
```

输出示例：
```
🚀 启动并行搜索，使用 10 个工作线程
📊 总共 20 个搜索任务

✅ [framework] 找到 30 个项目
✅ [latex] 找到 13 个项目
✅ [cad] 找到 15 个项目
✅ [circuit] 找到 12 个项目

📊 搜索统计:
   总耗时: 4.02 秒
   总计找到: 216 个项目（含重复）
   去重后: 203 个唯一项目
```

### 查看数据库

```bash
cd data
sqlite3 projects.db

# 查询各领域统计
SELECT domain, COUNT(*) as count,
       ROUND(AVG(stars)) as avg_stars
FROM projects
GROUP BY domain
ORDER BY count DESC;

# 查询 Top 10 跨领域项目
SELECT domain, full_name, stars
FROM projects
ORDER BY stars DESC
LIMIT 10;
```

### 访问网页界面

```bash
# 打开多领域概览
open web/overview.html

# 打开 AI 智能推荐引擎
open web/recommendation.html

# 打开 LaTeX 专题页
open web/index.html
```

### 使用 AI 推荐引擎

#### 方式 1: 网页界面（推荐）

直接打开 [web/recommendation.html](web/recommendation.html) 使用可视化界面：
1. 选择领域（LaTeX/CAD/Circuit/Framework）
2. 设置经验水平（初学者/中级/高级）
3. 选择预算（免费/低/中/高）
4. 勾选需要的功能
5. 点击"获取智能推荐"

推荐引擎将基于您的需求，从 328+ GitHub 项目和 2025 最新商业工具中，智能匹配并推荐最适合的工具。

#### 方式 2: Python API

```python
from tools.recommendation_engine import (
    RecommendationEngine, UserRequirements,
    Domain, Experience, Budget
)

engine = RecommendationEngine()

# 示例：LaTeX 初学者需要免费 AI 协作工具
requirements = UserRequirements(
    domain=Domain.LATEX,
    experience=Experience.BEGINNER,
    budget=Budget.FREE,
    features=["ai", "collaboration", "templates"],
    priority="ease_of_use",
    language_preference=["Python"]
)

results = engine.get_recommendations(requirements, top_n=5)

for rec in results["recommendations"]:
    print(f"{rec['name']}: {rec['relevance_score']}/100")
    print(f"理由: {rec['reasoning']}")
```

#### 方式 3: RESTful API（可选）

启动 API 服务器：
```bash
cd api
pip install -r requirements.txt
python3 recommendation_api.py
```

调用 API：
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "latex",
    "experience": "beginner",
    "budget": "free",
    "features": ["ai", "collaboration"],
    "priority": "ease_of_use"
  }'
```

## API 成本对比

| 方案 | 月成本 | 说明 |
|------|--------|------|
| 纯 OpenAI | $408 | GPT-4 Turbo 全部任务 |
| 纯 Claude | $157.5 | Claude 3.5 Sonnet 全部任务 |
| **混合策略** | **$129** | 本地 + Claude + GPT-4V |

**节省 68%！** 🎉

## 技术栈

- **搜索工具**: Python + GitHub API
- **数据库**: SQLite
- **网页**: HTML5 + TailwindCSS + Alpine.js + Chart.js
- **AI**: Claude 3.5 Sonnet (主力) + GPT-4V (图像) + Ollama (本地)

## 贡献指南

这是一个个人调研项目，欢迎提出建议和改进！

## License

MIT License

---

## 🎉 项目里程碑

- ✅ **Day 1 完成**: 并行搜索引擎、多领域数据收集、交互式网页
- 📊 **数据规模**: 328+ 项目，覆盖 4 个专业领域
- ⚡ **性能**: 10个并行agent，4秒完成全域搜索
- 🌟 **顶级项目**: langchain (123K⭐), markitdown (85K⭐), MetaGPT (62K⭐)

**开发进度**: Day 1 已完成，Day 2 进行中
**预计完成**: 7-11 天
**最后更新**: 2025-12-31

**开发者**: [@corning-AI](https://github.com/corning-AI)
**工具**: Claude Code with 10 parallel agents
