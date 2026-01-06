#!/bin/bash

###############################################################################
# Cursor Activity Monitor
# 监控Cursor窗口活动，当检测到需要确认时发送通知
###############################################################################

# 配置
CHECK_INTERVAL=2  # 检查间隔（秒）
CURSOR_APP="Cursor"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# 检查Cursor是否在运行
is_cursor_running() {
    pgrep -x "$CURSOR_APP" > /dev/null
    return $?
}

# 检查Cursor是否是前台应用
is_cursor_frontmost() {
    local frontmost=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)
    [[ "$frontmost" == "$CURSOR_APP" ]]
    return $?
}

# 发送通知
send_notification() {
    local message="${1:-Claude Code需要您的确认}"
    osascript -e "display notification \"$message\" with title \"⚠️ Cursor提醒\" sound name \"Glass\""
}

# 发送对话框
send_alert() {
    local message="${1:-Claude Code需要您的确认，请返回Cursor查看}"
    osascript <<EOF
tell application "System Events"
    activate
    set userChoice to button returned of (display dialog "$message" buttons {"稍后", "立即查看"} default button "立即查看" with icon caution with title "Cursor需要确认")
    if userChoice is "立即查看" then
        tell application "$CURSOR_APP" to activate
    end if
end tell
EOF
}

# 监控Cursor窗口标题（高级功能）
monitor_cursor_window() {
    local window_title=$(osascript -e "tell application \"System Events\" to get title of window 1 of process \"$CURSOR_APP\"" 2>/dev/null)
    echo "$window_title"
}

# 主监控循环
monitor_loop() {
    log_info "开始监控Cursor活动..."
    log_info "检查间隔: ${CHECK_INTERVAL}秒"
    log_info "按 Ctrl+C 停止监控"
    echo ""

    local last_status=""
    local notification_sent=false

    while true; do
        if is_cursor_running; then
            if ! is_cursor_frontmost; then
                # Cursor在运行但不在前台
                if [[ "$last_status" != "background" ]]; then
                    log_info "Cursor在后台运行"
                    last_status="background"
                    notification_sent=false
                fi

                # 这里可以添加更多检测逻辑
                # 例如检查窗口标题、检查特定进程等

            else
                # Cursor在前台
                if [[ "$last_status" != "foreground" ]]; then
                    log_info "Cursor在前台"
                    last_status="foreground"
                    notification_sent=false
                fi
            fi
        else
            if [[ "$last_status" != "not_running" ]]; then
                log_warn "Cursor未运行"
                last_status="not_running"
            fi
        fi

        sleep $CHECK_INTERVAL
    done
}

# 测试模式
test_notifications() {
    echo "测试通知功能..."
    echo ""

    echo "1. 发送通知横幅..."
    send_notification "这是一个测试通知"
    sleep 2

    echo "2. 发送对话框..."
    send_alert "这是一个测试对话框"

    echo ""
    echo "测试完成！"
}

# 显示帮助
show_help() {
    cat <<EOF
Cursor Activity Monitor - Cursor活动监控工具

用法: $0 [选项]

选项:
    -m, --monitor       启动监控模式（默认）
    -t, --test          测试通知功能
    -n, --notify        发送单次通知
    -a, --alert         发送单次对话框
    -i, --interval N    设置检查间隔（秒，默认2）
    -h, --help          显示此帮助信息

示例:
    $0                      # 启动监控
    $0 --test              # 测试通知
    $0 --notify            # 发送一次通知
    $0 --interval 5        # 每5秒检查一次

EOF
}

# 主函数
main() {
    local mode="monitor"

    while [[ $# -gt 0 ]]; do
        case $1 in
            -m|--monitor)
                mode="monitor"
                shift
                ;;
            -t|--test)
                mode="test"
                shift
                ;;
            -n|--notify)
                mode="notify"
                shift
                ;;
            -a|--alert)
                mode="alert"
                shift
                ;;
            -i|--interval)
                CHECK_INTERVAL="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done

    case $mode in
        monitor)
            monitor_loop
            ;;
        test)
            test_notifications
            ;;
        notify)
            send_notification "Claude Code需要您的确认"
            ;;
        alert)
            send_alert
            ;;
    esac
}

# 捕获中断信号
trap 'echo -e "\n${YELLOW}监控已停止${NC}"; exit 0' INT TERM

main "$@"
