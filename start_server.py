#!/usr/bin/env python3
"""
简易 Web 服务器
用于本地预览 AI Agent 研究平台的网页界面
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# 切换到项目根目录
PROJECT_ROOT = Path(__file__).parent
os.chdir(PROJECT_ROOT)

PORT = 8888

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加 CORS 头，允许本地跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # 简化日志输出
        print(f"[{self.address_string()}] {format % args}")


def start_server():
    """启动本地服务器"""
    print("\n" + "="*80)
    print("🚀 AI Agent 研究平台 - Web 服务器")
    print("="*80 + "\n")

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✅ 服务器已启动: http://localhost:{PORT}\n")
        print("📄 可访问页面:")
        print(f"   • 推荐引擎:   http://localhost:{PORT}/web/recommendation.html")
        print(f"   • 数据概览:   http://localhost:{PORT}/web/overview.html")
        print(f"   • LaTeX专题:  http://localhost:{PORT}/web/index.html")
        print(f"\n💡 提示: 按 Ctrl+C 停止服务器\n")
        print("="*80 + "\n")

        # 自动打开推荐引擎页面
        webbrowser.open(f"http://localhost:{PORT}/web/recommendation.html")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 服务器已停止\n")


if __name__ == "__main__":
    start_server()
