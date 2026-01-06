# ⚡ Claude Code 自动批准 - 快速开始

## 🎯 一分钟上手

### 最常用命令

```bash
# 启用安全模式（推荐）
claude-auto safe

# 启用适中模式（常用）
claude-auto moderate

# 禁用自动批准
claude-auto off

# 查看当前状态
claude-auto status
```

---

## 📊 模式速查

| 模式 | 命令 | 说明 | 推荐场景 |
|-----|------|------|---------|
| 🔒 Disabled | `claude-auto off` | 所有操作需确认 | 敏感操作、生产环境 |
| ✅ Safe | `claude-auto safe` | 仅批准读取 | **日常开发（推荐）** |
| ⚙️ Moderate | `claude-auto moderate` | 批准读取+编辑+安全命令 | 活跃开发、重构 |
| 🚀 Aggressive | `claude-auto aggressive` | 批准几乎所有操作 | 原型开发、实验 |
| 💥 YOLO | `claude-auto yolo` | 批准所有操作 | ⚠️ 仅测试环境 |

---

## 🚀 首次使用

### 1. 激活Shell别名
```bash
source ~/.zshrc
```

### 2. 启用自动批准
```bash
claude-auto safe
```

### 3. 重启Cursor
重启Cursor以加载新的配置。

### 4. 测试
在Cursor中让Claude Code读取一个文件，应该会自动批准而不需要您确认。

---

## ⚠️ 重要提示

### 配置生效
修改自动批准设置后，可能需要：
1. **重启Cursor** 以加载新配置
2. 或等待几秒钟让Cursor重新读取配置

### 当前项目有效
自动批准配置仅对当前项目有效：
- 项目路径：`/Users/xiaobotu/Documents/ai_agent`
- 配置文件：`.claude/settings.json`

### 安全建议
- 🟢 日常使用：`safe` 或 `moderate`
- 🟡 快速开发：`moderate` 或 `aggressive`
- 🔴 绝不使用：`yolo`（除非完全隔离的测试环境）

---

## 📖 详细文档

查看完整使用指南：
```bash
cat /Users/xiaobotu/Documents/ai_agent/.claude/AUTO_APPROVE_GUIDE.md
```

或在VSCode/Cursor中打开：
```
/Users/xiaobotu/Documents/ai_agent/.claude/AUTO_APPROVE_GUIDE.md
```

---

## 🔧 常见操作

### 临时切换模式
```bash
# 开发时
claude-auto moderate

# 提交前检查
claude-auto safe

# 代码审查
claude-auto off
```

### 快速切换
```bash
# 切换启用/禁用
claude-auto toggle
```

### 查看帮助
```bash
claude-auto help
```

---

## ✅ 验证安装

```bash
# 1. 检查别名
which claude-auto

# 2. 查看状态
claude-auto status

# 3. 测试hook
echo '{"tool_name":"Read"}' | CLAUDE_PROJECT_DIR=$PWD .claude/hooks/auto-approve.sh
```

---

**安装位置**: `/Users/xiaobotu/Documents/ai_agent/.claude/`
**Shell别名**: `claude-auto`
**配置文件**: `.claude/auto-approve-config.json`
