#!/bin/bash

###############################################################################
# Claude Code Notification Helper
# 当Claude Code需要确认时发送macOS通知
###############################################################################

# 配置
NOTIFICATION_TITLE="⚠️ Claude Code需要确认"
NOTIFICATION_MESSAGE="请返回Cursor查看并确认操作"
SOUND="Glass"  # 可选: Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink

# 函数：发送通知
send_notification() {
    local title="${1:-$NOTIFICATION_TITLE}"
    local message="${2:-$NOTIFICATION_MESSAGE}"
    local sound="${3:-$SOUND}"

    osascript -e "display notification \"$message\" with title \"$title\" sound name \"$sound\""
}

# 函数：发送对话框（更强提醒）
send_alert_dialog() {
    local message="${1:-Claude Code需要您的确认，请返回Cursor查看}"

    osascript <<EOF
tell application "System Events"
    activate
    display dialog "$message" buttons {"确定"} default button "确定" with icon caution with title "Claude Code"
end tell
EOF
}

# 主函数
main() {
    case "${1:-notification}" in
        "notification")
            send_notification
            ;;
        "alert")
            send_alert_dialog
            ;;
        "both")
            send_notification
            sleep 0.5
            send_alert_dialog
            ;;
        *)
            echo "用法: $0 [notification|alert|both]"
            echo "  notification - 发送通知横幅（默认）"
            echo "  alert       - 弹出对话框"
            echo "  both        - 先通知再弹窗"
            exit 1
            ;;
    esac
}

main "$@"
