#!/usr/bin/env python3
"""
GitHub CLI Batch Searcher
使用 GitHub CLI 进行大规模项目搜索
"""

import json
import subprocess
import sqlite3
import time
from datetime import datetime
from typing import List, Dict

class GitHubCLISearcher:
    """使用 GitHub CLI 的批量搜索器"""

    def __init__(self, db_path: str = "../data/projects.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库（复用之前的表结构）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

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

        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化完成: {self.db_path}")

    def search_with_gh(self, query: str, limit: int = 30) -> List[Dict]:
        """使用 gh CLI 搜索仓库"""
        print(f"\n🔍 搜索: {query}")

        cmd = [
            "gh", "search", "repos",
            query,
            "--limit", str(limit),
            "--sort", "stars",
            "--json", "name,owner,stargazersCount,forksCount,description,url,updatedAt,createdAt,language,license,openIssuesCount"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            repos = json.loads(result.stdout)
            print(f"  ✅ 找到 {len(repos)} 个项目")
            return repos
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 搜索失败: {e.stderr}")
            return []
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON 解析失败: {e}")
            return []

    def calculate_activity_score(self, repo: Dict) -> float:
        """计算活跃度分数"""
        stars = repo.get("stargazersCount", 0)
        forks = repo.get("forksCount", 0)

        # 计算更新时间距今的天数
        try:
            last_updated = datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00"))
            days_since_update = (datetime.now(last_updated.tzinfo) - last_updated).days
        except:
            days_since_update = 365  # 默认一年

        # 活跃度公式（0-100 分）
        score = (
            min(stars / 100, 50) +
            min(forks / 20, 20) +
            max(30 - days_since_update / 10, 0)
        )

        return round(min(score, 100), 2)

    def convert_repo_data(self, repo: Dict, domain: str) -> Dict:
        """转换 gh CLI 输出格式到数据库格式"""
        owner_login = repo.get("owner", {}).get("login", "")
        repo_name = repo.get("name", "")
        full_name = f"{owner_login}/{repo_name}"

        # 提取语言
        language = repo.get("language", "")

        # 提取 license
        license_name = ""
        if repo.get("license"):
            if isinstance(repo["license"], dict):
                license_name = repo["license"].get("name", "")
            else:
                license_name = repo["license"]

        # GitHub CLI search repos 不返回 topics，暂时设为空
        topics = []

        return {
            "domain": domain,
            "name": repo_name,
            "full_name": full_name,
            "url": repo.get("url", f"https://github.com/{full_name}"),
            "stars": repo.get("stargazersCount", 0),
            "forks": repo.get("forksCount", 0),
            "watchers": repo.get("stargazersCount", 0),  # gh CLI 不返回 watchers
            "open_issues": repo.get("openIssuesCount", 0),
            "description": repo.get("description", ""),
            "main_language": language,
            "last_updated": repo.get("updatedAt", "")[:10],
            "created_at": repo.get("createdAt", "")[:10],
            "license": license_name,
            "topics": json.dumps(topics),
            "activity_score": self.calculate_activity_score(repo)
        }

    def save_to_database(self, projects: List[Dict]):
        """批量保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        saved_count = 0
        updated_count = 0

        for project in projects:
            try:
                cursor.execute("""
                INSERT INTO projects (
                    domain, name, full_name, url, stars, forks, watchers,
                    open_issues, description, main_language, last_updated,
                    created_at, activity_score, license, topics
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project["domain"], project["name"], project["full_name"],
                    project["url"], project["stars"], project["forks"],
                    project["watchers"], project["open_issues"],
                    project["description"], project["main_language"],
                    project["last_updated"], project["created_at"],
                    project["activity_score"], project["license"],
                    project["topics"]
                ))
                saved_count += 1
            except sqlite3.IntegrityError:
                # 已存在，更新
                cursor.execute("""
                UPDATE projects SET
                    stars = ?, forks = ?, watchers = ?,
                    open_issues = ?, description = ?,
                    last_updated = ?, activity_score = ?,
                    license = ?, topics = ?,
                    collected_at = CURRENT_TIMESTAMP
                WHERE full_name = ?
                """, (
                    project["stars"], project["forks"],
                    project["watchers"], project["open_issues"],
                    project["description"], project["last_updated"],
                    project["activity_score"], project["license"],
                    project["topics"], project["full_name"]
                ))
                updated_count += 1

        conn.commit()
        conn.close()

        print(f"\n💾 数据库保存: ✅ 新增 {saved_count} | 🔄 更新 {updated_count}")

    def search_latex_projects(self):
        """搜索 LaTeX 相关项目"""
        print("\n" + "="*70)
        print("🔬 开始 LaTeX AI Agent 项目大规模搜索")
        print("="*70)

        # LaTeX 搜索关键词（扩展版）
        search_queries = [
            # AI 辅助编写
            "latex ai stars:>50",
            "latex gpt stars:>50",
            "latex copilot stars:>20",
            "latex code completion stars:>20",
            "latex assistant stars:>20",

            # 公式生成
            "latex formula ai stars:>50",
            "math to latex stars:>100",
            "latex ocr stars:>50",
            "im2latex stars:>50",
            "pix2tex stars:>50",

            # TikZ 图形
            "tikz generation stars:>20",
            "tikz ai stars:>10",

            # 文档工具
            "markdown to latex stars:>100",
            "latex converter stars:>50",

            # VSCode 扩展
            "latex vscode stars:>50",

            # 通用搜索
            "latex machine learning stars:>30",
            "latex deep learning stars:>30"
        ]

        all_projects = []

        for query in search_queries:
            repos = self.search_with_gh(query, limit=30)

            for repo in repos:
                project = self.convert_repo_data(repo, "latex")
                all_projects.append(project)

            time.sleep(1)  # 避免过快请求

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
        """导出为 JSON"""
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
                try:
                    project["topics"] = json.loads(project["topics"])
                except:
                    project["topics"] = []
            projects.append(project)

        conn.close()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)

        print(f"\n📄 导出完成: {output_path}")
        print(f"   包含 {len(projects)} 个项目")

        return projects

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║      GitHub CLI Batch Searcher - LaTeX AI Projects         ║
║               使用 GitHub CLI 进行大规模调研                  ║
╚══════════════════════════════════════════════════════════════╝
    """)

    searcher = GitHubCLISearcher(db_path="../data/projects.db")

    # 执行搜索
    projects = searcher.search_latex_projects()

    # 导出 JSON
    searcher.export_to_json("latex", "../data/latex/projects.json")

    # 显示 Top 20
    print("\n🏆 Top 20 LaTeX AI 项目:")
    print("="*80)
    for i, project in enumerate(projects[:20], 1):
        desc = project['description'][:60] + "..." if project['description'] else "无描述"
        print(f"{i:2d}. ⭐ {project['stars']:6d} | {project['full_name']}")
        print(f"    {desc}")
        print(f"    语言: {project['main_language'] or 'N/A'} | 更新: {project['last_updated']} | 活跃度: {project['activity_score']}")
        print()

    print("✅ 搜索完成！")
    print(f"\n📁 数据已保存:")
    print(f"   - 数据库: ../data/projects.db")
    print(f"   - JSON: ../data/latex/projects.json")

if __name__ == "__main__":
    main()
