#!/bin/bash

###############################################################################
# Claude Code Auto-Approval Hook
# 根据安全级别自动批准工具调用
###############################################################################

# 读取配置文件
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/auto-approve-config.json"
DEFAULT_MODE="${CLAUDE_AUTO_APPROVE_MODE:-safe}"

# 读取stdin（hook输入）
input=$(cat)

# 解析工具名称和输入
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
tool_input=$(echo "$input" | jq -r '.tool_input // {}')

# 读取当前模式（从配置文件或环境变量）
if [ -f "$CONFIG_FILE" ]; then
    current_mode=$(jq -r '.mode // "safe"' "$CONFIG_FILE")
else
    current_mode="$DEFAULT_MODE"
fi

# 如果模式是disabled，不做任何处理
if [ "$current_mode" = "disabled" ]; then
    exit 0
fi

# 日志函数（可选）
log_approval() {
    if [ "${CLAUDE_AUTO_APPROVE_LOG:-false}" = "true" ]; then
        echo "[$(date)] AUTO-APPROVED: $tool_name" >> "$CLAUDE_PROJECT_DIR/.claude/auto-approve.log"
    fi
}

# 根据不同模式决定是否自动批准
case "$current_mode" in
    "yolo")
        # YOLO模式：批准所有操作（除了明确拒绝的）
        log_approval
        echo '{
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Auto-approved (YOLO mode)"
            }
        }'
        exit 0
        ;;

    "aggressive")
        # 激进模式：批准大多数操作，只拒绝危险命令
        case "$tool_name" in
            "Bash")
                command=$(echo "$tool_input" | jq -r '.command // empty')
                # 检查危险命令
                if [[ "$command" =~ ^(rm -rf|sudo|chmod 777|dd if=) ]]; then
                    exit 0  # 让默认权限流程处理
                fi
                ;;
        esac
        log_approval
        echo '{
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Auto-approved (Aggressive mode)"
            }
        }'
        exit 0
        ;;

    "moderate")
        # 适中模式：批准读取、编辑和常见命令
        case "$tool_name" in
            "Read"|"Glob"|"Grep")
                log_approval
                echo '{
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "permissionDecisionReason": "Auto-approved (Moderate mode - read operation)"
                    }
                }'
                exit 0
                ;;
            "Edit")
                log_approval
                echo '{
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "permissionDecisionReason": "Auto-approved (Moderate mode - edit operation)"
                    }
                }'
                exit 0
                ;;
            "Bash")
                command=$(echo "$tool_input" | jq -r '.command // empty')
                # 只批准安全的bash命令
                if [[ "$command" =~ ^(git |npm |python3 |ls |pwd |cat |echo |mkdir ) ]]; then
                    log_approval
                    echo '{
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "allow",
                            "permissionDecisionReason": "Auto-approved (Moderate mode - safe command)"
                        }
                    }'
                    exit 0
                fi
                ;;
        esac
        # 其他情况使用默认流程
        exit 0
        ;;

    "safe")
        # 安全模式：只批准读取操作
        case "$tool_name" in
            "Read"|"Glob"|"Grep")
                log_approval
                echo '{
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "permissionDecisionReason": "Auto-approved (Safe mode - read-only)"
                    }
                }'
                exit 0
                ;;
        esac
        # 其他操作需要用户确认
        exit 0
        ;;

    *)
        # 未知模式，使用默认流程
        exit 0
        ;;
esac
