#!/usr/bin/env python3
"""
GitHub Project Searcher
自动化搜索 GitHub 上与 AI Agent 相关的项目
"""

import os
import json
import time
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import requests
from urllib.parse import urlencode

class GitHubSearcher:
    """GitHub 项目搜索和分析工具"""

    def __init__(self, token: Optional[str] = None, db_path: str = "../data/projects.db"):
        """
        初始化 GitHub 搜索器

        Args:
            token: GitHub Personal Access Token (可选，但强烈推荐)
            db_path: SQLite 数据库路径
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.db_path = db_path
        self.base_url = "https://api.github.com"

        # 请求头
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

        # 速率限制跟踪
        self.remaining_requests = None
        self.reset_time = None

        # 初始化数据库
        self.init_database()

    def init_database(self):
        """初始化 SQLite 数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建项目表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            name TEXT NOT NULL,
            full_name TEXT UNIQUE NOT NULL,
            url TEXT NOT NULL,
            stars INTEGER DEFAULT 0,
            forks INTEGER DEFAULT 0,
            watchers INTEGER DEFAULT 0,
            open_issues INTEGER DEFAULT 0,
            description TEXT,
            main_language TEXT,
            tech_stack TEXT,
            last_updated DATE,
            created_at DATE,
            activity_score REAL DEFAULT 0,
            relevance_score REAL DEFAULT 0,
            readme_summary TEXT,
            license TEXT,
            topics TEXT,
            contributors_count INTEGER DEFAULT 0,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(full_name)
        )
        """)

        # 创建功能特性表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            feature_type TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        """)

        # 创建索引
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_domain ON projects(domain)
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_stars ON projects(stars DESC)
        """)

        conn.commit()
        conn.close()

        print(f"✅ 数据库初始化完成: {self.db_path}")

    def check_rate_limit(self):
        """检查 GitHub API 速率限制"""
        response = requests.get(
            f"{self.base_url}/rate_limit",
            headers=self.headers
        )

        if response.status_code == 200:
            data = response.json()
            core = data["resources"]["core"]
            self.remaining_requests = core["remaining"]
            self.reset_time = datetime.fromtimestamp(core["reset"])

            print(f"📊 API 速率限制: {self.remaining_requests} 次剩余")
            print(f"🕐 重置时间: {self.reset_time}")

            if self.remaining_requests < 10:
                wait_seconds = (self.reset_time - datetime.now()).seconds
                print(f"⚠️  接近速率限制，等待 {wait_seconds} 秒...")
                time.sleep(wait_seconds + 1)
        else:
            print(f"❌ 无法获取速率限制: {response.status_code}")

    def search_repositories(
        self,
        query: str,
        domain: str,
        sort: str = "stars",
        order: str = "desc",
        max_results: int = 100,
        min_stars: int = 10
    ) -> List[Dict]:
        """
        搜索 GitHub 仓库

        Args:
            query: 搜索关键词
            domain: 领域分类 ('latex', 'cad', 'circuit', 'framework')
            sort: 排序方式 ('stars', 'forks', 'updated')
            order: 排序顺序 ('desc', 'asc')
            max_results: 最大结果数
            min_stars: 最小 stars 数量

        Returns:
            项目列表
        """
        all_repos = []
        page = 1
        per_page = 100  # GitHub API 最大值

        # 构建查询字符串，添加 stars 过滤
        search_query = f"{query} stars:>{min_stars}"

        print(f"\n🔍 搜索: {search_query} (领域: {domain})")

        while len(all_repos) < max_results:
            # 检查速率限制
            if self.remaining_requests and self.remaining_requests < 10:
                self.check_rate_limit()

            # 构建请求 URL
            params = {
                "q": search_query,
                "sort": sort,
                "order": order,
                "per_page": per_page,
                "page": page
            }

            url = f"{self.base_url}/search/repositories?{urlencode(params)}"

            response = requests.get(url, headers=self.headers)

            # 更新速率限制信息
            self.remaining_requests = int(response.headers.get("X-RateLimit-Remaining", 0))

            if response.status_code != 200:
                print(f"❌ 搜索失败: {response.status_code}")
                print(f"   错误: {response.json().get('message', 'Unknown error')}")
                break

            data = response.json()
            items = data.get("items", [])

            if not items:
                print(f"✅ 搜索完成，共找到 {len(all_repos)} 个项目")
                break

            # 处理每个仓库
            for repo in items:
                if len(all_repos) >= max_results:
                    break

                project_data = self.extract_repo_data(repo, domain)
                all_repos.append(project_data)

                print(f"  ⭐ {repo['full_name']}: {repo['stargazers_count']} stars")

            page += 1
            time.sleep(1)  # 避免触发速率限制

        return all_repos

    def extract_repo_data(self, repo: Dict, domain: str) -> Dict:
        """从 GitHub API 响应中提取项目数据"""
        return {
            "domain": domain,
            "name": repo["name"],
            "full_name": repo["full_name"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "watchers": repo["watchers_count"],
            "open_issues": repo["open_issues_count"],
            "description": repo.get("description", ""),
            "main_language": repo.get("language", ""),
            "last_updated": repo["updated_at"][:10],
            "created_at": repo["created_at"][:10],
            "license": repo.get("license").get("name", "") if repo.get("license") else "",
            "topics": json.dumps(repo.get("topics", [])),
            "activity_score": self.calculate_activity_score(repo),
            "relevance_score": 0.0  # 后续计算
        }

    def calculate_activity_score(self, repo: Dict) -> float:
        """
        计算项目活跃度分数

        综合考虑：
        - Stars 数量
        - Forks 数量
        - 最近更新时间
        - Open issues 数量
        """
        stars = repo["stargazers_count"]
        forks = repo["forks_count"]

        # 计算更新时间距今的天数
        last_updated = datetime.strptime(repo["updated_at"][:10], "%Y-%m-%d")
        days_since_update = (datetime.now() - last_updated).days

        # 活跃度公式（0-100 分）
        # stars 和 forks 越多越好，最近更新越好
        score = (
            min(stars / 100, 50) +  # stars 最高 50 分
            min(forks / 20, 20) +    # forks 最高 20 分
            max(30 - days_since_update / 10, 0)  # 最近更新最高 30 分
        )

        return round(min(score, 100), 2)

    def save_to_database(self, projects: List[Dict]):
        """将项目保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        saved_count = 0
        updated_count = 0

        for project in projects:
            try:
                # 尝试插入
                cursor.execute("""
                INSERT INTO projects (
                    domain, name, full_name, url, stars, forks, watchers,
                    open_issues, description, main_language, last_updated,
                    created_at, activity_score, license, topics
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project["domain"],
                    project["name"],
                    project["full_name"],
                    project["url"],
                    project["stars"],
                    project["forks"],
                    project["watchers"],
                    project["open_issues"],
                    project["description"],
                    project["main_language"],
                    project["last_updated"],
                    project["created_at"],
                    project["activity_score"],
                    project["license"],
                    project["topics"]
                ))
                saved_count += 1
            except sqlite3.IntegrityError:
                # 已存在，更新
                cursor.execute("""
                UPDATE projects SET
                    stars = ?,
                    forks = ?,
                    watchers = ?,
                    open_issues = ?,
                    description = ?,
                    last_updated = ?,
                    activity_score = ?,
                    license = ?,
                    topics = ?,
                    collected_at = CURRENT_TIMESTAMP
                WHERE full_name = ?
                """, (
                    project["stars"],
                    project["forks"],
                    project["watchers"],
                    project["open_issues"],
                    project["description"],
                    project["last_updated"],
                    project["activity_score"],
                    project["license"],
                    project["topics"],
                    project["full_name"]
                ))
                updated_count += 1

        conn.commit()
        conn.close()

        print(f"\n💾 数据库保存完成:")
        print(f"   ✅ 新增: {saved_count} 个项目")
        print(f"   🔄 更新: {updated_count} 个项目")

    def search_latex_projects(self, max_results: int = 100):
        """搜索 LaTeX 相关项目"""
        print("\n" + "="*60)
        print("🔬 开始搜索 LaTeX AI Agent 相关项目")
        print("="*60)

        # LaTeX 搜索关键词矩阵
        latex_keywords = [
            "latex ai",
            "latex gpt",
            "latex code completion",
            "latex formula ai",
            "math to latex",
            "latex ocr",
            "im2latex",
            "tikz generation",
            "tikz ai",
            "markdown to latex",
            "latex assistant",
            "latex autocomplete"
        ]

        all_projects = []

        for keyword in latex_keywords:
            projects = self.search_repositories(
                query=keyword,
                domain="latex",
                max_results=max_results // len(latex_keywords),
                min_stars=50  # LaTeX 项目相对小众，降低门槛
            )
            all_projects.extend(projects)
            time.sleep(2)  # 避免触发速率限制

        # 去重（基于 full_name）
        unique_projects = {}
        for project in all_projects:
            unique_projects[project["full_name"]] = project

        final_projects = list(unique_projects.values())

        # 按 stars 排序
        final_projects.sort(key=lambda x: x["stars"], reverse=True)

        print(f"\n📊 搜索统计:")
        print(f"   总计找到: {len(all_projects)} 个项目（含重复）")
        print(f"   去重后: {len(final_projects)} 个唯一项目")

        # 保存到数据库
        self.save_to_database(final_projects)

        return final_projects

    def export_to_json(self, domain: str, output_path: str):
        """导出数据为 JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM projects WHERE domain = ? ORDER BY stars DESC
        """, (domain,))

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        projects = []
        for row in rows:
            project = dict(zip(columns, row))
            # 解析 JSON 字段
            if project["topics"]:
                project["topics"] = json.loads(project["topics"])
            projects.append(project)

        conn.close()

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)

        print(f"\n📄 导出完成: {output_path}")
        print(f"   包含 {len(projects)} 个项目")

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         GitHub Project Searcher - LaTeX AI Agent            ║
║                   专业领域 AI Agent 调研工具                  ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # 初始化搜索器
    searcher = GitHubSearcher(db_path="../data/projects.db")

    # 检查 API 速率限制
    searcher.check_rate_limit()

    # 搜索 LaTeX 项目
    projects = searcher.search_latex_projects(max_results=100)

    # 导出 JSON
    searcher.export_to_json("latex", "../data/latex/projects.json")

    # 显示 Top 10
    print("\n🏆 Top 10 LaTeX AI 项目:")
    print("-" * 80)
    for i, project in enumerate(projects[:10], 1):
        print(f"{i:2d}. ⭐ {project['stars']:5d} | {project['full_name']}")
        if project['description']:
            print(f"     {project['description'][:70]}...")

    print("\n✅ 搜索完成！数据已保存到数据库。")
    print(f"\n💡 提示：请设置 GITHUB_TOKEN 环境变量以提高 API 限额")
    print(f"   未认证: 60 次/小时")
    print(f"   已认证: 5000 次/小时")

if __name__ == "__main__":
    main()
