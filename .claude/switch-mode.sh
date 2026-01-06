#!/bin/bash

###############################################################################
# Claude Code 模式快速切换
# 通过替换settings.json来切换模式
###############################################################################

PROJECT_DIR="/Users/xiaobotu/Documents/ai_agent"
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"
PRESETS_DIR="$PROJECT_DIR/.claude/presets"
BACKUP_FILE="$PROJECT_DIR/.claude/settings.backup.json"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 备份当前配置
backup_settings() {
    if [ -f "$SETTINGS_FILE" ]; then
        cp "$SETTINGS_FILE" "$BACKUP_FILE"
        echo -e "${GREEN}✅ 已备份当前配置${NC}"
    fi
}

# 切换到YOLO模式（完全自动批准）
yolo_mode() {
    backup_settings
    cat > "$SETTINGS_FILE" <<'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
EOF
    echo -e "${RED}💥 YOLO模式已启用 - 所有操作自动批准！${NC}"
    echo -e "${YELLOW}⚠️  警告：此模式会自动批准所有操作，包括危险操作！${NC}"
}

# 安全模式
safe_mode() {
    backup_settings
    if [ -f "$PRESETS_DIR/safe-mode.json" ]; then
        cp "$PRESETS_DIR/safe-mode.json" "$SETTINGS_FILE"
    else
        cat > "$SETTINGS_FILE" <<'EOF'
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Glob(**)",
      "Grep(**)"
    ],
    "defaultMode": "dontAsk"
  }
}
EOF
    fi
    echo -e "${GREEN}✅ 安全模式已启用 - 仅自动批准读取操作${NC}"
}

# 适中模式
moderate_mode() {
    backup_settings
    cat > "$SETTINGS_FILE" <<'EOF'
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Glob(**)",
      "Grep(**)",
      "Edit(/Users/xiaobotu/Documents/ai_agent/**)",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(python3:*)",
      "Bash(ls:*)",
      "Bash(pwd:*)",
      "Bash(cat:*)",
      "Bash(mkdir:*)"
    ],
    "deny": [
      "Read(**/.env)",
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ],
    "defaultMode": "dontAsk"
  }
}
EOF
    echo -e "${GREEN}✅ 适中模式已启用 - 自动批准常见操作${NC}"
}

# 禁用自动批准
disable_mode() {
    backup_settings
    cat > "$SETTINGS_FILE" <<'EOF'
{
  "permissions": {
    "defaultMode": "default"
  }
}
EOF
    echo -e "${YELLOW}🔒 自动批准已禁用 - 所有操作需要确认${NC}"
}

# 显示当前模式
show_status() {
    if [ ! -f "$SETTINGS_FILE" ]; then
        echo -e "${RED}❌ 配置文件不存在${NC}"
        return
    fi

    local default_mode=$(jq -r '.permissions.defaultMode // "unknown"' "$SETTINGS_FILE" 2>/dev/null)

    echo -e "${GREEN}当前配置:${NC}"
    case "$default_mode" in
        "bypassPermissions")
            echo -e "  模式: ${RED}YOLO (完全自动批准)${NC}"
            ;;
        "dontAsk")
            echo -e "  模式: ${YELLOW}DontAsk (根据白名单自动批准)${NC}"
            ;;
        "default")
            echo -e "  模式: ${GREEN}Default (需要确认)${NC}"
            ;;
        *)
            echo -e "  模式: ${YELLOW}$default_mode${NC}"
            ;;
    esac

    echo ""
    echo "配置文件: $SETTINGS_FILE"
}

# 主函数
main() {
    case "${1:-status}" in
        "yolo")
            yolo_mode
            ;;
        "safe")
            safe_mode
            ;;
        "moderate"|"mod")
            moderate_mode
            ;;
        "off"|"disable")
            disable_mode
            ;;
        "status"|"")
            show_status
            ;;
        "help"|"-h"|"--help")
            cat <<EOF
用法: $0 [模式]

模式:
    yolo        完全自动批准（危险！）
    moderate    适中模式（推荐）
    safe        安全模式（仅读取）
    off         禁用自动批准
    status      显示当前模式

示例:
    $0 yolo      # 启用YOLO模式
    $0 moderate  # 启用适中模式
    $0 off       # 禁用
    $0 status    # 查看状态

EOF
            ;;
        *)
            echo -e "${RED}未知模式: $1${NC}"
            echo "使用 '$0 help' 查看帮助"
            exit 1
            ;;
    esac

    echo ""
    echo -e "${YELLOW}💡 提示: 重启Cursor以应用新配置${NC}"
}

main "$@"
