#!/bin/bash

###############################################################################
# Claude Code Auto-Approval Manager
# 管理Claude Code自动批准功能的工具
###############################################################################

set -e

# 配置
PROJECT_DIR="/Users/xiaobotu/Documents/ai_agent"
CONFIG_FILE="$PROJECT_DIR/.claude/auto-approve-config.json"
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 显示当前状态
show_status() {
    echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Claude Code 自动批准状态                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
    echo ""

    if [ -f "$CONFIG_FILE" ]; then
        current_mode=$(jq -r '.mode // "disabled"' "$CONFIG_FILE")
        enabled=$(jq -r '.enabled // false' "$CONFIG_FILE")
    else
        current_mode="disabled"
        enabled="false"
    fi

    echo -e "📂 项目目录: $PROJECT_DIR"
    echo -e "🔧 配置文件: $([ -f "$CONFIG_FILE" ] && echo "✅" || echo "❌")"
    echo -e "🎯 当前状态: $([ "$enabled" = "true" ] && echo -e "${GREEN}已启用${NC}" || echo -e "${RED}已禁用${NC}")"
    echo -e "🛡️  安全模式: ${YELLOW}$current_mode${NC}"
    echo ""

    if [ "$enabled" = "true" ]; then
        case "$current_mode" in
            "yolo")
                echo -e "${RED}⚠️  YOLO模式：批准所有操作（极度危险！）${NC}"
                ;;
            "aggressive")
                echo -e "${YELLOW}⚠️  激进模式：批准大多数操作（中等风险）${NC}"
                ;;
            "moderate")
                echo -e "${YELLOW}ℹ️  适中模式：批准常见操作（低风险）${NC}"
                ;;
            "safe")
                echo -e "${GREEN}✅ 安全模式：仅批准读取操作（推荐）${NC}"
                ;;
        esac
    fi
    echo ""
}

# 设置模式
set_mode() {
    local mode="$1"

    # 验证模式
    case "$mode" in
        "disabled"|"safe"|"moderate"|"aggressive"|"yolo")
            ;;
        *)
            echo -e "${RED}❌ 无效的模式: $mode${NC}"
            echo "有效模式: disabled, safe, moderate, aggressive, yolo"
            exit 1
            ;;
    esac

    # 创建配置
    if [ "$mode" = "disabled" ]; then
        cat > "$CONFIG_FILE" <<EOF
{
  "enabled": false,
  "mode": "disabled",
  "updatedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
        echo -e "${GREEN}✅ 自动批准已禁用${NC}"
    else
        cat > "$CONFIG_FILE" <<EOF
{
  "enabled": true,
  "mode": "$mode",
  "updatedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
        echo -e "${GREEN}✅ 自动批准模式已设置为: $mode${NC}"
    fi

    # 显示模式说明
    echo ""
    case "$mode" in
        "disabled")
            echo "🔒 所有操作都需要手动确认"
            ;;
        "safe")
            echo "📖 自动批准："
            echo "   ✅ Read（读取文件）"
            echo "   ✅ Glob（文件搜索）"
            echo "   ✅ Grep（内容搜索）"
            echo "   ❌ 其他操作需要确认"
            ;;
        "moderate")
            echo "⚙️  自动批准："
            echo "   ✅ Read, Glob, Grep（读取操作）"
            echo "   ✅ Edit（编辑文件）"
            echo "   ✅ 安全的Bash命令（git, npm, python3等）"
            echo "   ❌ Write, 危险命令需要确认"
            ;;
        "aggressive")
            echo "🚀 自动批准："
            echo "   ✅ 几乎所有操作"
            echo "   ❌ 仅拒绝极度危险的命令（rm -rf, sudo等）"
            ;;
        "yolo")
            echo -e "${RED}💥 批准所有操作（包括危险操作！）${NC}"
            echo -e "${RED}⚠️  警告：此模式存在严重安全风险！${NC}"
            ;;
    esac
    echo ""
}

# 快速切换
toggle() {
    if [ -f "$CONFIG_FILE" ]; then
        enabled=$(jq -r '.enabled // false' "$CONFIG_FILE")
        current_mode=$(jq -r '.mode // "safe"' "$CONFIG_FILE")

        if [ "$enabled" = "true" ]; then
            # 当前启用，切换到禁用
            set_mode "disabled"
        else
            # 当前禁用，切换到上次的模式（或safe）
            if [ "$current_mode" = "disabled" ]; then
                current_mode="safe"
            fi
            set_mode "$current_mode"
        fi
    else
        # 没有配置，启用safe模式
        set_mode "safe"
    fi
}

# 显示帮助
show_help() {
    cat <<EOF
${BLUE}Claude Code 自动批准管理工具${NC}

用法: $0 [命令] [选项]

命令:
    status              显示当前状态（默认）
    enable [MODE]       启用自动批准并设置模式
    disable             禁用自动批准
    toggle              快速切换启用/禁用
    mode MODE           设置模式（不改变启用状态）

安全模式:
    disabled            禁用自动批准（需要手动确认所有操作）
    safe                安全模式：仅批准读取操作 ${GREEN}[推荐]${NC}
    moderate            适中模式：批准常见操作
    aggressive          激进模式：批准大多数操作 ${YELLOW}[有风险]${NC}
    yolo                YOLO模式：批准所有操作 ${RED}[极度危险]${NC}

示例:
    $0 status                  # 查看当前状态
    $0 enable safe            # 启用安全模式
    $0 enable moderate        # 启用适中模式
    $0 disable                # 禁用自动批准
    $0 toggle                 # 快速切换

快捷命令:
    claude-auto on            # 启用（默认safe模式）
    claude-auto off           # 禁用
    claude-auto yolo          # 启用YOLO模式
    claude-auto status        # 查看状态

EOF
}

# 主函数
main() {
    local command="${1:-status}"
    local arg="$2"

    case "$command" in
        status|"")
            show_status
            ;;
        enable)
            local mode="${arg:-safe}"
            set_mode "$mode"
            ;;
        disable)
            set_mode "disabled"
            ;;
        toggle)
            toggle
            ;;
        mode)
            if [ -z "$arg" ]; then
                echo -e "${RED}错误：请指定模式${NC}"
                echo "用法: $0 mode [safe|moderate|aggressive|yolo]"
                exit 1
            fi
            set_mode "$arg"
            ;;
        on)
            set_mode "${arg:-safe}"
            ;;
        off)
            set_mode "disabled"
            ;;
        safe|moderate|aggressive|yolo)
            set_mode "$command"
            ;;
        help|-h|--help)
            show_help
            ;;
        *)
            echo -e "${RED}未知命令: $command${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
