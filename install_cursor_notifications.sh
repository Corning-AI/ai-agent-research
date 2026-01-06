#!/bin/bash

###############################################################################
# Cursor通知系统安装脚本
# 自动配置macOS通知和Cursor集成
###############################################################################

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Cursor通知系统安装向导${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 步骤1：检查Cursor是否已安装
echo -e "${GREEN}[1/5]${NC} 检查Cursor应用..."
if [ -d "/Applications/Cursor.app" ]; then
    echo "✅ 找到Cursor应用"
else
    echo "❌ 未找到Cursor应用，请先安装Cursor"
    exit 1
fi
echo ""

# 步骤2：打开系统通知设置
echo -e "${GREEN}[2/5]${NC} 配置macOS系统通知..."
echo "请在打开的系统设置中进行以下配置："
echo "  1. 在左侧找到'Cursor'"
echo "  2. 启用'允许通知'"
echo "  3. 横幅样式选择'提醒'（不会自动消失）"
echo "  4. 启用'播放提示音'"
echo ""
read -p "按回车键打开系统通知设置..."
open "x-apple.systempreferences:com.apple.preference.notifications"
echo "请完成配置后返回终端..."
read -p "配置完成后按回车继续..."
echo ""

# 步骤3：创建通知脚本目录
echo -e "${GREEN}[3/5]${NC} 设置通知脚本..."
SCRIPT_DIR="$HOME/.cursor-notifications"
mkdir -p "$SCRIPT_DIR"

# 复制脚本
cp /Users/xiaobotu/Documents/ai_agent/claude_code_notifier.sh "$SCRIPT_DIR/"
cp /Users/xiaobotu/Documents/ai_agent/cursor_activity_monitor.sh "$SCRIPT_DIR/"
chmod +x "$SCRIPT_DIR"/*.sh

echo "✅ 脚本已安装到: $SCRIPT_DIR"
echo ""

# 步骤4：添加到shell配置
echo -e "${GREEN}[4/5]${NC} 配置shell别名..."
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    echo "" >> "$SHELL_RC"
    echo "# Cursor通知系统别名" >> "$SHELL_RC"
    echo "alias cursor-notify='$SCRIPT_DIR/claude_code_notifier.sh'" >> "$SHELL_RC"
    echo "alias cursor-monitor='$SCRIPT_DIR/cursor_activity_monitor.sh'" >> "$SHELL_RC"
    echo "✅ 别名已添加到: $SHELL_RC"
else
    echo "⚠️  未找到shell配置文件，请手动添加别名"
fi
echo ""

# 步骤5：测试通知
echo -e "${GREEN}[5/5]${NC} 测试通知功能..."
read -p "是否要测试通知？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$SCRIPT_DIR/cursor_activity_monitor.sh" --test
fi
echo ""

# 完成
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}安装完成！${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "📝 使用说明:"
echo ""
echo "1. 发送通知："
echo "   cursor-notify notification"
echo ""
echo "2. 发送对话框："
echo "   cursor-notify alert"
echo ""
echo "3. 监控Cursor活动："
echo "   cursor-monitor"
echo ""
echo "4. 查看完整文档："
echo "   cat /Users/xiaobotu/Documents/ai_agent/cursor_notification_setup.md"
echo ""
echo "💡 提示：重新打开终端或运行 'source $SHELL_RC' 来使别名生效"
echo ""
