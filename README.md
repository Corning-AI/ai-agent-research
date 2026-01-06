# 专业领域 AI Agent 调研平台

> 全面调研 CAD、Circuit、LaTeX、Framework 等专业领域的 AI Agent 项目和技术栈

## 项目概述

这是一个自动化的技术调研平台，旨在：
- 🔍 自动搜索和分析 GitHub 上的相关项目（已收集 **1,003 项目**）
- 📊 生成交互式可视化报告（多领域对比分析）
- 🚀 **深度搜索**：71个关键词查询，10个并发线程
- 🤖 AI 智能推荐引擎（整合 1,003 项目数据）
- 📈 完整分析报告（质量评分、生态分析、趋势预测）
- 🌐 交互式 Web 界面（推荐引擎、数据可视化）

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
- 🚀 使用 10 个并发线程深度搜索
- 🔍 搜索 1,003 个 AI Agent 相关项目
  - **CAD**: 535 项目（平均 128 stars）⭐ 16.7x 增长
  - **Circuit**: 192 项目（平均 98 stars）⭐ 9.6x 增长
  - **Framework**: 138 项目（平均 10K stars）
  - **LaTeX**: 138 项目（平均 1.5K stars）
- 💾 自动创建 SQLite 数据库
- 📄 导出各领域 JSON 数据文件
- 📊 生成质量评分和生态分析

## 项目结构

```
ai_agent/
├── README.md                    # 项目说明
├── start_server.py             # Web 服务器（推荐使用）⭐
├── cli.py                       # 命令行工具 ⭐
├── tools/                       # 调研工具
│   ├── deep_search.py          # 深度搜索引擎（71个查询）⭐
│   ├── parallel_search.py      # 并行多领域搜索
│   ├── project_analyzer.py     # 项目质量分析 ⭐
│   ├── ecosystem_analyzer.py   # 生态系统分析 ⭐
│   ├── recommendation_engine.py # AI 智能推荐引擎
│   └── gh_batch_search.py      # GitHub CLI 批量搜索
├── data/                        # 数据存储
│   ├── projects.db             # SQLite 数据库（1,003 项目）⭐
│   ├── cad/                    # CAD 领域（535 项目）⭐
│   ├── circuit/                # Circuit 领域（192 项目）⭐
│   ├── framework/              # Framework 领域（138 项目）
│   └── latex/                  # LaTeX 领域（138 项目）
├── reports/                     # 分析报告
│   ├── Comprehensive_Deep_Research_Report.md  # 综合报告 v1.1 ⭐
│   ├── project_analysis.json   # 项目分析数据 ⭐
│   ├── ecosystem_analysis.json # 生态分析数据 ⭐
│   └── WebSearch_Research_Report.md  # 2025调研报告
├── web/                         # 交互式网页
│   ├── recommendation.html     # AI 智能推荐引擎 ⭐
│   ├── overview.html           # 多领域数据概览
│   └── index.html              # LaTeX 专题页
└── api/                         # API 服务（可选）
    └── recommendation_api.py   # RESTful API

```

## 功能特性

### ✅ 已完成
- [x] **深度搜索引擎**（71个关键词查询，10并发线程）⭐
- [x] **数据大幅扩展**（328 → 1,003 项目，3.1x 增长）⭐
  - CAD: 32 → 535 项目（16.7x）
  - Circuit: 20 → 192 项目（9.6x）
- [x] **项目质量分析**（活跃度、许可证、规模分布）⭐
- [x] **生态系统分析**（成熟度评分、新兴项目识别）⭐
- [x] **综合调研报告** v1.1（15,000+ 字深度分析）⭐
- [x] **AI 智能推荐引擎**（整合 1,003 项目数据）⭐
  - 基于用户需求自动推荐最佳工具
  - 支持多维度筛选（领域、经验、预算、功能）
  - 智能评分算法（活跃度、功能匹配、社区支持）
  - 交互式 Web 界面
- [x] **本地 Web 服务器**（解决 CORS 问题）⭐
- [x] **CLI 命令行工具**（推荐、统计、列表）⭐
- [x] 交互式网页界面（推荐引擎、数据概览、LaTeX 专题）
- [x] 实时数据可视化（Chart.js）
- [x] WebSearch 补充调研（2025最新数据）

### 📅 未来计划
- [ ] 自动化定期更新脚本
- [ ] GitHub Pages 部署
- [ ] 增强推荐算法（机器学习模型）
- [ ] 项目对比功能

## 使用示例

### 启动 Web 服务器（推荐）⭐

使用本地 Web 服务器访问所有交互式功能：

```bash
# 启动服务器
python3 start_server.py
```

服务器将自动：
- 🚀 启动在 http://localhost:8888
- 🌐 自动打开推荐引擎页面
- ✅ 解决 CORS 跨域问题
- 📊 提供所有 Web 界面访问

访问地址：
- **推荐引擎**: http://localhost:8888/web/recommendation.html
- **数据概览**: http://localhost:8888/web/overview.html
- **LaTeX 专题**: http://localhost:8888/web/index.html

### 使用 CLI 工具 ⭐

```bash
# 获取智能推荐
python3 cli.py recommend -d cad -e beginner -b free

# 查看统计数据
python3 cli.py stats --domain cad

# 列出项目
python3 cli.py list -d circuit --limit 20 --sort stars

# 查看帮助
python3 cli.py --help
```

### 深度搜索（扩展数据）

```bash
cd tools
python3 deep_search.py
```

执行 71 个关键词查询，大幅扩展数据集。

### 并行搜索多个领域

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

推荐引擎将基于您的需求，从 **1,003 个 GitHub 项目**和 2025 最新商业工具中，智能匹配并推荐最适合的工具。

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

### v1.1 - 数据大扩展 (2026-01-05)
- 🚀 **深度搜索**: 71个关键词查询，10并发线程
- 📊 **数据规模**: 1,003 项目（3.1x 增长）
  - CAD: 535 项目（16.7x）
  - Circuit: 192 项目（9.6x）
- 📈 **分析报告**: 15,000+ 字综合报告 v1.1
- 🌐 **Web 服务器**: 解决 CORS 问题
- 🔧 **CLI 工具**: 完整命令行界面

### v1.0 - 初版发布 (2025-12-31)
- ✅ 并行搜索引擎、多领域数据收集
- 📊 328 项目，覆盖 4 个专业领域
- 🤖 AI 智能推荐引擎
- 🌟 顶级项目: langchain (123K⭐), markitdown (85K⭐), MetaGPT (62K⭐)

---

**仓库**: https://github.com/Corning-AI/ai-agent-research
**开发者**: [@Corning-AI](https://github.com/Corning-AI)
**工具**: Claude Code + Claude Sonnet 4.5
