# AI Agent 调研平台 - 文档索引

> 完整的项目文档导航

## 📚 核心文档

### 入门指南
- **[README.md](README.md)** - 项目主页和快速开始
  - 项目概述
  - 快速开始（环境准备、运行工具）
  - 功能特性
  - 使用示例（Web 服务器、CLI、搜索工具）
  - 项目里程碑

### 部署指南
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 部署和发布流程
  - GitHub Pages 部署
  - 域名配置
  - 自动化部署

## 📊 分析报告

### 综合调研报告
- **[Comprehensive_Deep_Research_Report.md](reports/Comprehensive_Deep_Research_Report.md)** ⭐ 主报告
  - **版本**: v1.1 (Expanded)
  - **数据规模**: 1,003 个 GitHub 项目
  - **内容**: 15,000+ 字深度分析
  - **包含**:
    - 执行摘要（核心发现）
    - 领域概览（数据分布、技术栈）
    - 深度质量分析（活跃度、许可证、规模）
    - 生态系统分析（成熟度、新兴项目）
    - 2025 趋势预测
    - 关键洞察与建议

### WebSearch 调研
- **[WebSearch_Research_Report.md](reports/WebSearch_Research_Report.md)**
  - 基于 20 个 WebSearch 查询
  - 2025 年最新商业工具和趋势
  - LaTeX、CAD、Circuit 领域深度分析

- **[Executive_Summary.md](reports/2025_latest/Executive_Summary.md)**
  - WebSearch 调研执行摘要
  - 2025 最新发现

### 分析数据
- **[project_analysis.json](reports/project_analysis.json)** - 项目质量分析数据
  - 技术栈分布
  - 活跃度趋势
  - 质量层级分类
  - 许可证统计
  - 规模分布

- **[ecosystem_analysis.json](reports/ecosystem_analysis.json)** - 生态系统分析数据
  - 技术栈组合
  - 时间趋势
  - 新兴项目（2024-2025）
  - 领域成熟度评分

## 🛠️ 工具文档

### 搜索工具
- **[tools/deep_search.py](tools/deep_search.py)** - 深度搜索引擎
  - 71 个关键词查询
  - 10 并发线程
  - 智能去重
  - 质量评分

- **[tools/parallel_search.py](tools/parallel_search.py)** - 并行搜索
  - 多领域同时搜索
  - GitHub CLI 集成

### 分析工具
- **[tools/project_analyzer.py](tools/project_analyzer.py)** - 项目分析
  - 技术栈分析
  - 活跃度分析
  - 质量层级分类
  - 许可证分析

- **[tools/ecosystem_analyzer.py](tools/ecosystem_analyzer.py)** - 生态分析
  - 领域成熟度评分
  - 新兴项目识别
  - 技术栈组合分析
  - 时间趋势分析

### 推荐引擎
- **[tools/recommendation_engine.py](tools/recommendation_engine.py)** - AI 智能推荐
  - 基于需求的项目推荐
  - 相关度评分算法
  - 多维度筛选

### 实用工具
- **[start_server.py](start_server.py)** - Web 服务器
  - 本地 HTTP 服务器
  - CORS 支持
  - 自动打开浏览器

- **[cli.py](cli.py)** - 命令行工具
  - `recommend` - 获取智能推荐
  - `stats` - 查看统计数据
  - `list` - 列出项目
  - `web` - 打开网页界面

## 🌐 Web 界面

- **[web/recommendation.html](web/recommendation.html)** - AI 智能推荐引擎
  - 交互式推荐界面
  - 多维度筛选
  - 实时推荐结果

- **[web/overview.html](web/overview.html)** - 多领域数据概览
  - 数据可视化
  - 领域对比
  - 统计图表

- **[web/index.html](web/index.html)** - LaTeX 专题页
  - LaTeX 工具专题分析
  - 项目详情

## 📦 数据文件

### 数据库
- **[data/projects.db](data/projects.db)** - SQLite 数据库
  - 1,003 个项目完整数据
  - 21 个字段
  - 质量评分

### JSON 导出
- **[data/cad/projects.json](data/cad/projects.json)** - CAD 领域（535 项目）
- **[data/circuit/projects.json](data/circuit/projects.json)** - Circuit 领域（192 项目）
- **[data/framework/projects.json](data/framework/projects.json)** - Framework 领域（138 项目）
- **[data/latex/projects.json](data/latex/projects.json)** - LaTeX 领域（138 项目）

## 🔧 配置文件

- **[.gitignore](.gitignore)** - Git 忽略规则
- **[api/requirements.txt](api/requirements.txt)** - API 依赖

## 📋 产品规划

- **[专业领域AI Agent产品计划.md](专业领域AI Agent产品计划.md)** - 产品战略规划
  - 市场分析
  - 产品定位
  - 开发路线图

## 🎯 快速导航

### 我想...
- **了解项目** → [README.md](README.md)
- **查看数据分析** → [Comprehensive_Deep_Research_Report.md](reports/Comprehensive_Deep_Research_Report.md)
- **使用推荐引擎** → 运行 `python3 start_server.py`
- **搜索更多项目** → [tools/deep_search.py](tools/deep_search.py)
- **查看统计** → 运行 `python3 cli.py stats`
- **部署到 GitHub Pages** → [DEPLOYMENT.md](DEPLOYMENT.md)

## 📊 数据概览

| 领域 | 项目数 | 平均 Stars | 成熟度 | 2024新项目 |
|------|--------|-----------|--------|-----------|
| CAD | 535 | 128 | 15.8/100 | 137 |
| Circuit | 192 | 98 | 16.3/100 | 27 |
| Framework | 138 | 10,021 | 72.0/100 | 70 |
| LaTeX | 138 | 1,515 | 46.9/100 | 34 |
| **总计** | **1,003** | **1,221** | **46.0/100** | **268** |

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/Corning-AI/ai-agent-research
- **在线演示**: https://corning-ai.github.io/ai-agent-research/ (待部署)
- **反馈建议**: [GitHub Issues](https://github.com/Corning-AI/ai-agent-research/issues)

---

**最后更新**: 2026-01-05
**文档版本**: 1.1
