# GitHub Pages 部署指南

## 快速部署步骤

### 1. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库（假设名称为：ai-agent-research）
# 不要初始化 README、.gitignore 或 license
```

### 2. 提交代码到 Git

```bash
cd /Users/xiaobotu/Documents/ai_agent

# 添加所有文件
git add .

# 创建首次提交
git commit -m "Initial commit: AI Agent Research Platform

- 328+ GitHub projects across 4 domains
- AI intelligent recommendation engine
- Interactive web dashboards
- 2025 latest research data"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-research.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 访问仓库的 **Settings** 页面
2. 在左侧菜单找到 **Pages**
3. 在 **Source** 下拉菜单中选择：
   - Branch: `main`
   - Folder: `/ (root)`
4. 点击 **Save**
5. 等待 1-2 分钟，页面会显示：
   ```
   Your site is live at https://YOUR_USERNAME.github.io/ai-agent-research/
   ```

### 4. 访问网站

部署完成后，可以通过以下 URL 访问：

- **主页**: `https://YOUR_USERNAME.github.io/ai-agent-research/`
- **AI 推荐**: `https://YOUR_USERNAME.github.io/ai-agent-research/web/recommendation.html`
- **数据概览**: `https://YOUR_USERNAME.github.io/ai-agent-research/web/overview.html`
- **LaTeX 专题**: `https://YOUR_USERNAME.github.io/ai-agent-research/web/index.html`

## 后续更新

每次更新代码后，重新推送到 GitHub：

```bash
# 添加修改的文件
git add .

# 提交更改
git commit -m "Update: description of changes"

# 推送到 GitHub
git push

# GitHub Pages 会自动重新部署（约 1-2 分钟）
```

## 自定义域名（可选）

如果您有自己的域名：

1. 在仓库根目录创建 `CNAME` 文件：
   ```bash
   echo "yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. 在域名 DNS 设置中添加：
   - Type: `CNAME`
   - Name: `www` (或 `@` 用于根域名)
   - Value: `YOUR_USERNAME.github.io`

3. 在 GitHub Pages 设置中输入自定义域名

## 部署检查清单

- [ ] 所有 HTML 文件中的相对路径正确
- [ ] JSON 数据文件已包含在仓库中
- [ ] 图片和静态资源路径正确
- [ ] 外部 CDN 资源可访问（TailwindCSS、Chart.js、Alpine.js）
- [ ] 数据库文件 (.db) 已在 .gitignore 中排除（太大，使用 JSON 替代）
- [ ] 测试所有页面链接是否正常

## 已包含的文件

✅ 主页: `index.html`
✅ Web 界面: `web/` 目录
  - `overview.html` - 多领域概览
  - `recommendation.html` - AI 推荐引擎
  - `index.html` - LaTeX 专题页
✅ 数据文件: `data/*/projects.json`
✅ 调研报告: `reports/` 目录
✅ 文档: `README.md`

## 注意事项

1. **数据库文件**: SQLite 数据库 (`projects.db`) 不会部署到 GitHub Pages，因为：
   - 文件较大
   - GitHub Pages 是静态托管，无法运行数据库查询
   - 已导出为 JSON 格式供网页使用

2. **API 服务**: `api/recommendation_api.py` 需要单独部署到服务器（如 Heroku、Railway、Vercel）如果需要动态推荐功能。当前网页版使用客户端 JavaScript 实现推荐逻辑。

3. **Python 工具**: `tools/` 目录中的 Python 脚本用于数据收集和分析，不会在 GitHub Pages 上运行。

## 性能优化建议

1. **启用压缩**: GitHub Pages 自动启用 gzip 压缩
2. **CDN 缓存**: 外部资源（TailwindCSS、Chart.js）使用 CDN
3. **图片优化**: 如果添加图片，使用 WebP 格式并压缩
4. **懒加载**: 大型数据可考虑按需加载

## 故障排查

### 页面显示空白
- 检查浏览器控制台是否有 404 错误
- 确认所有路径使用相对路径（如 `web/overview.html` 而非 `/web/overview.html`）

### JSON 数据加载失败
- 确认 `data/` 目录中的 JSON 文件已推送到 GitHub
- 检查 CORS 设置（GitHub Pages 默认支持）

### 样式错误
- 确认 CDN 资源可访问
- 检查网络连接

## 联系方式

如有问题，请访问：
- GitHub Issues: https://github.com/YOUR_USERNAME/ai-agent-research/issues
- 开发者: [@corning-AI](https://github.com/corning-AI)
