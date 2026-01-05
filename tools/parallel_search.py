#!/usr/bin/env python3
"""
Parallel GitHub Search Tool
使用多进程并行搜索 CAD、Circuit 和其他领域的 AI 项目
"""

import json
import subprocess
import sqlite3
import time
from datetime import datetime
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class ParallelGitHubSearcher:
    """并行 GitHub 搜索器"""

    def __init__(self, db_path: str = "../data/projects.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()

    def init_database(self):
        """初始化数据库"""
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

    def search_with_gh(self, query: str, domain: str, limit: int = 30) -> Tuple[str, List[Dict]]:
        """使用 gh CLI 搜索仓库"""
        print(f"🔍 [{domain}] 搜索: {query}")

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
            print(f"  ✅ [{domain}] 找到 {len(repos)} 个项目")
            return (domain, repos)
        except subprocess.CalledProcessError as e:
            print(f"  ❌ [{domain}] 搜索失败: {e.stderr}")
            return (domain, [])
        except json.JSONDecodeError as e:
            print(f"  ❌ [{domain}] JSON 解析失败: {e}")
            return (domain, [])

    def calculate_activity_score(self, repo: Dict) -> float:
        """计算活跃度分数"""
        stars = repo.get("stargazersCount", 0)
        forks = repo.get("forksCount", 0)

        try:
            last_updated = datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00"))
            days_since_update = (datetime.now(last_updated.tzinfo) - last_updated).days
        except:
            days_since_update = 365

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

        language = repo.get("language", "")

        license_name = ""
        if repo.get("license"):
            if isinstance(repo["license"], dict):
                license_name = repo["license"].get("name", "")
            else:
                license_name = repo["license"]

        topics = []

        return {
            "domain": domain,
            "name": repo_name,
            "full_name": full_name,
            "url": repo.get("url", f"https://github.com/{full_name}"),
            "stars": repo.get("stargazersCount", 0),
            "forks": repo.get("forksCount", 0),
            "watchers": repo.get("stargazersCount", 0),
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
        """批量保存到数据库（线程安全）"""
        with self.lock:
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

            return saved_count, updated_count

    def parallel_search(self, search_queries: List[Tuple[str, str]], max_workers: int = 10):
        """并行执行多个搜索查询"""
        print(f"\n🚀 启动并行搜索，使用 {max_workers} 个工作线程")
        print(f"📊 总共 {len(search_queries)} 个搜索任务\n")

        all_results = []
        domain_stats = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有搜索任务
            future_to_query = {
                executor.submit(self.search_with_gh, query, domain): (query, domain)
                for query, domain in search_queries
            }

            # 收集结果
            for future in as_completed(future_to_query):
                query, domain = future_to_query[future]
                try:
                    domain_result, repos = future.result()

                    # 转换数据并收集
                    for repo in repos:
                        project = self.convert_repo_data(repo, domain_result)
                        all_results.append(project)

                    # 统计
                    if domain_result not in domain_stats:
                        domain_stats[domain_result] = 0
                    domain_stats[domain_result] += len(repos)

                except Exception as exc:
                    print(f"  ❌ 查询 '{query}' 失败: {exc}")

        return all_results, domain_stats

    def export_to_json(self, domain: str, output_path: str):
        """导出指定领域的数据为 JSON"""
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
            if project["topics"]:
                try:
                    project["topics"] = json.loads(project["topics"])
                except:
                    project["topics"] = []
            projects.append(project)

        conn.close()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)

        print(f"📄 导出完成: {output_path} ({len(projects)} 个项目)")
        return projects


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        Parallel GitHub Searcher - Multi-Domain AI           ║
║           使用 10 个并行线程进行大规模调研                     ║
╚══════════════════════════════════════════════════════════════╝
    """)

    searcher = ParallelGitHubSearcher(db_path="../data/projects.db")

    # 定义搜索查询矩阵（查询关键词, 领域）
    search_queries = [
        # CAD 领域 (5个查询)
        ("cad ai stars:>50", "cad"),
        ("autocad automation stars:>50", "cad"),
        ("solidworks api stars:>20", "cad"),
        ("fusion360 automation stars:>20", "cad"),
        ("cad machine learning stars:>30", "cad"),

        # Circuit 领域 (5个查询)
        ("circuit simulator ai stars:>50", "circuit"),
        ("pcb design automation stars:>50", "circuit"),
        ("spice simulator stars:>50", "circuit"),
        ("electronic design automation stars:>30", "circuit"),
        ("circuit analysis ai stars:>20", "circuit"),

        # 补充 LaTeX 搜索 (5个查询)
        ("latex neural network stars:>20", "latex"),
        ("latex template generator stars:>50", "latex"),
        ("academic writing ai stars:>50", "latex"),
        ("bibliography management stars:>100", "latex"),
        ("latex syntax checker stars:>20", "latex"),

        # Framework/通用 AI Agent 框架 (5个查询)
        ("ai agent framework stars:>100", "framework"),
        ("langchain stars:>100", "framework"),
        ("autogen stars:>50", "framework"),
        ("crewai stars:>50", "framework"),
        ("openai assistant api stars:>50", "framework"),
    ]

    # 执行并行搜索
    start_time = time.time()
    all_projects, domain_stats = searcher.parallel_search(search_queries, max_workers=10)
    elapsed_time = time.time() - start_time

    # 去重
    unique_projects = {}
    for project in all_projects:
        unique_projects[project["full_name"]] = project

    final_projects = list(unique_projects.values())
    final_projects.sort(key=lambda x: x["stars"], reverse=True)

    print(f"\n{'='*70}")
    print(f"📊 搜索统计:")
    print(f"   总耗时: {elapsed_time:.2f} 秒")
    print(f"   总计找到: {len(all_projects)} 个项目（含重复）")
    print(f"   去重后: {len(final_projects)} 个唯一项目")
    print(f"\n   各领域分布:")
    for domain, count in sorted(domain_stats.items()):
        print(f"      {domain}: {count} 个项目")

    # 保存到数据库
    saved, updated = searcher.save_to_database(final_projects)
    print(f"\n💾 数据库保存: ✅ 新增 {saved} | 🔄 更新 {updated}")

    # 按领域导出 JSON
    import os
    for domain in set(p["domain"] for p in final_projects):
        os.makedirs(f"../data/{domain}", exist_ok=True)
        searcher.export_to_json(domain, f"../data/{domain}/projects.json")

    # 显示 Top 10
    print(f"\n🏆 Top 10 跨领域 AI 项目:")
    print("="*80)
    for i, project in enumerate(final_projects[:10], 1):
        desc = project['description'][:60] + "..." if project['description'] else "无描述"
        print(f"{i:2d}. [{project['domain']:8s}] ⭐ {project['stars']:6d} | {project['full_name']}")
        print(f"    {desc}")
        print(f"    语言: {project['main_language'] or 'N/A':12s} | 更新: {project['last_updated']} | 活跃度: {project['activity_score']}")
        print()

    print("✅ 并行搜索完成！")
    print(f"\n📁 数据已保存:")
    print(f"   - 数据库: ../data/projects.db")
    for domain in set(p["domain"] for p in final_projects):
        print(f"   - JSON ({domain}): ../data/{domain}/projects.json")


if __name__ == "__main__":
    main()
