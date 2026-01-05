#!/usr/bin/env python3
"""
深度 GitHub 搜索工具
增强版搜索，支持智能关键词扩展、多维度过滤、去重合并
"""

import subprocess
import json
import sqlite3
import time
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict


class DeepSearchEngine:
    """深度搜索引擎"""

    def __init__(self, db_path: str = "../data/projects.db"):
        self.db_path = db_path
        self.existing_repos: Set[str] = self._load_existing_repos()

        # 扩展搜索关键词库
        self.search_queries = {
            "cad": [
                # 基础 CAD
                ("CAD python", "cad"),
                ("computer aided design", "cad"),
                ("3D modeling automation", "cad"),
                ("parametric design", "cad"),
                ("generative design", "cad"),
                ("topology optimization", "cad"),

                # 技术栈
                ("OpenCASCADE python", "cad"),
                ("FreeCAD scripting", "cad"),
                ("Blender python API", "cad"),
                ("pythonOCC", "cad"),
                ("cadquery", "cad"),

                # AI 相关
                ("AI CAD", "cad"),
                ("machine learning 3D modeling", "cad"),
                ("neural CAD", "cad"),
                ("AI 3D generation", "cad"),
                ("text to 3D model", "cad"),
                ("LLM CAD assistant", "cad"),
                ("GPT CAD automation", "cad"),

                # 应用领域
                ("mechanical design automation", "cad"),
                ("architectural design tool", "cad"),
                ("product design software", "cad"),
                ("CAM programming", "cad"),
                ("CNC automation", "cad"),

                # 新兴方向
                ("procedural modeling", "cad"),
                ("computational design", "cad"),
                ("algorithm design", "cad"),
                ("design optimization", "cad"),
            ],

            "circuit": [
                # 基础电路
                ("circuit design", "circuit"),
                ("PCB design", "circuit"),
                ("electronic design automation", "circuit"),
                ("EDA tools", "circuit"),
                ("IC design", "circuit"),

                # 仿真
                ("circuit simulation", "circuit"),
                ("SPICE simulator", "circuit"),
                ("analog simulation", "circuit"),
                ("digital logic simulation", "circuit"),
                ("ngspice python", "circuit"),

                # 硬件描述
                ("Verilog HDL", "circuit"),
                ("VHDL design", "circuit"),
                ("hardware description language", "circuit"),
                ("RTL design", "circuit"),

                # PCB 工具
                ("KiCad automation", "circuit"),
                ("KiCad python", "circuit"),
                ("PCB router", "circuit"),
                ("PCB autorouter", "circuit"),
                ("gerber generation", "circuit"),

                # AI 相关
                ("AI PCB routing", "circuit"),
                ("machine learning circuit", "circuit"),
                ("neural network hardware", "circuit"),
                ("AI chip design", "circuit"),
                ("ML accelerator", "circuit"),

                # 测试验证
                ("circuit testing", "circuit"),
                ("hardware verification", "circuit"),
                ("formal verification", "circuit"),

                # 新兴方向
                ("quantum circuit", "circuit"),
                ("neuromorphic hardware", "circuit"),
                ("FPGA design", "circuit"),
            ],

            "cross_domain": [
                # LaTeX + AI
                ("GPT LaTeX", "latex"),
                ("AI paper writing", "latex"),
                ("LLM academic writing", "latex"),
                ("automated LaTeX generation", "latex"),

                # CAD + LLM
                ("text to 3D", "cad"),
                ("conversational CAD", "cad"),
                ("LLM 3D modeling", "cad"),
                ("GPT CAD", "cad"),

                # Circuit + ML
                ("neural hardware design", "circuit"),
                ("AI chip", "circuit"),
                ("ML hardware accelerator", "circuit"),

                # Framework + Domain
                ("multi-agent CAD", "framework"),
                ("LLM framework design", "framework"),
                ("agent-based modeling", "framework"),
            ]
        }

    def _load_existing_repos(self) -> Set[str]:
        """加载已存在的仓库，避免重复"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT full_name FROM projects")
            repos = {row[0] for row in cursor.fetchall()}
            conn.close()
            return repos
        except:
            return set()

    def search_with_gh(self, query: str, domain: str, limit: int = 30) -> Tuple[Dict, List[Dict]]:
        """使用 GitHub CLI 搜索"""
        print(f"  🔍 搜索: {query[:50]}...")

        try:
            cmd = [
                "gh", "search", "repos",
                query,
                "--limit", str(limit),
                "--sort", "stars",
                "--json", "name,owner,stargazersCount,forksCount,description,url,updatedAt,createdAt,language,license,openIssuesCount"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                print(f"    ❌ 搜索失败: {result.stderr[:100]}")
                return {"query": query, "domain": domain, "count": 0}, []

            repos = json.loads(result.stdout)

            # 过滤已存在的仓库
            new_repos = []
            for repo in repos:
                full_name = f"{repo['owner']['login']}/{repo['name']}"
                if full_name not in self.existing_repos:
                    new_repos.append(repo)
                    self.existing_repos.add(full_name)  # 添加到集合防止重复

            print(f"    ✅ 找到 {len(repos)} 个项目，{len(new_repos)} 个新项目")

            return {
                "query": query,
                "domain": domain,
                "count": len(new_repos),
                "total": len(repos)
            }, new_repos

        except subprocess.TimeoutExpired:
            print(f"    ⏱️  搜索超时")
            return {"query": query, "domain": domain, "count": 0, "error": "timeout"}, []
        except Exception as e:
            print(f"    ❌ 错误: {str(e)[:100]}")
            return {"query": query, "domain": domain, "count": 0, "error": str(e)}, []

    def calculate_quality_score(self, repo: Dict) -> float:
        """计算项目质量分数（0-100）"""
        score = 0.0

        # 1. Stars (30分)
        stars = repo.get("stargazersCount", 0)
        if stars > 10000:
            score += 30
        elif stars > 1000:
            score += 20
        elif stars > 100:
            score += 10
        elif stars > 10:
            score += 5

        # 2. 更新时间 (20分)
        updated = repo.get("updatedAt", "")
        if updated:
            try:
                update_date = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                days_ago = (datetime.now(update_date.tzinfo) - update_date).days
                if days_ago < 30:
                    score += 20
                elif days_ago < 90:
                    score += 15
                elif days_ago < 180:
                    score += 10
                elif days_ago < 365:
                    score += 5
            except:
                pass

        # 3. Forks (15分)
        forks = repo.get("forksCount", 0)
        if forks > 1000:
            score += 15
        elif forks > 100:
            score += 10
        elif forks > 10:
            score += 5

        # 4. Issues (15分) - 有适量的 open issues 说明活跃
        issues = repo.get("openIssuesCount", 0)
        if 10 <= issues <= 100:
            score += 15
        elif 1 <= issues < 10:
            score += 10
        elif issues > 100:
            score += 5

        # 5. 描述 (10分)
        if repo.get("description"):
            score += 10

        # 6. License (10分)
        license_info = repo.get("license")
        if license_info:
            license_name = license_info.get("name", "").lower() if isinstance(license_info, dict) else str(license_info).lower()
            if "mit" in license_name or "apache" in license_name or "bsd" in license_name:
                score += 10
            else:
                score += 5

        return round(score, 2)

    def save_to_database(self, repos: List[Dict], domain: str):
        """保存到数据库"""
        if not repos:
            return 0

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        saved_count = 0
        for repo in repos:
            try:
                owner_login = repo["owner"]["login"]
                name = repo["name"]
                full_name = f"{owner_login}/{name}"

                # 检查是否已存在
                cursor.execute("SELECT COUNT(*) FROM projects WHERE full_name = ?", (full_name,))
                if cursor.fetchone()[0] > 0:
                    continue

                stars = repo.get("stargazersCount", 0)
                forks = repo.get("forksCount", 0)
                description = repo.get("description", "")
                url = repo.get("url", "")
                updated_at = repo.get("updatedAt", "")
                created_at = repo.get("createdAt", "")
                language = repo.get("language", "")

                license_name = ""
                if repo.get("license"):
                    if isinstance(repo["license"], dict):
                        license_name = repo["license"].get("name", "")
                    else:
                        license_name = repo["license"]

                # 计算质量分数
                quality_score = self.calculate_quality_score(repo)

                cursor.execute("""
                INSERT INTO projects (
                    domain, name, full_name, owner, url, description,
                    stars, forks, main_language, license, topics,
                    created_at, last_updated, activity_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    domain, name, full_name, owner_login, url, description,
                    stars, forks, language, license_name, "[]",
                    created_at, updated_at, quality_score
                ))

                saved_count += 1

            except Exception as e:
                print(f"    ⚠️  保存失败 {full_name}: {str(e)[:50]}")

        conn.commit()
        conn.close()

        return saved_count

    def parallel_deep_search(self, domains: List[str], max_workers: int = 10):
        """并行深度搜索"""
        print(f"\n{'='*80}")
        print(f"🚀 启动深度搜索引擎 - {max_workers} 个并发线程")
        print(f"{'='*80}\n")

        # 准备搜索任务
        search_tasks = []
        for domain_key in domains:
            if domain_key in self.search_queries:
                for query, domain in self.search_queries[domain_key]:
                    search_tasks.append((query, domain))

        print(f"📊 总共 {len(search_tasks)} 个搜索任务\n")

        all_results = []
        domain_stats = defaultdict(lambda: {"total": 0, "new": 0, "repos": []})

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(self.search_with_gh, query, domain): (query, domain)
                for query, domain in search_tasks
            }

            for future in as_completed(future_to_task):
                query, domain = future_to_task[future]
                try:
                    result, repos = future.result()
                    all_results.append(result)

                    if repos:
                        domain_stats[domain]["total"] += result.get("total", 0)
                        domain_stats[domain]["new"] += len(repos)
                        domain_stats[domain]["repos"].extend(repos)

                except Exception as e:
                    print(f"  ❌ 任务失败: {query[:30]} - {str(e)[:50]}")

        elapsed = time.time() - start_time

        # 保存到数据库
        print(f"\n{'='*80}")
        print(f"💾 保存到数据库...")
        print(f"{'='*80}\n")

        total_saved = 0
        for domain, stats in domain_stats.items():
            saved = self.save_to_database(stats["repos"], domain)
            total_saved += saved
            print(f"  {domain:12} - 保存 {saved}/{stats['new']} 个新项目")

        # 统计报告
        print(f"\n{'='*80}")
        print(f"📈 深度搜索完成")
        print(f"{'='*80}\n")
        print(f"  总耗时: {elapsed:.2f} 秒")
        print(f"  搜索任务: {len(search_tasks)} 个")
        print(f"  新增项目: {total_saved} 个")
        print(f"\n各领域统计:")

        for domain in sorted(domain_stats.keys()):
            stats = domain_stats[domain]
            print(f"  {domain:12} - 搜索到 {stats['total']:3d} 个，新增 {stats['new']:3d} 个")

        return domain_stats, total_saved


def main():
    """主函数"""
    engine = DeepSearchEngine()

    print("\n" + "="*80)
    print("🎯 深度 GitHub 搜索计划")
    print("="*80)
    print("\n选择搜索范围：")
    print("  1. CAD 领域深度搜索")
    print("  2. Circuit 领域深度搜索")
    print("  3. 跨领域项目搜索")
    print("  4. 全部执行（推荐）")

    choice = input("\n请选择 (1-4, 默认 4): ").strip() or "4"

    domains_map = {
        "1": ["cad"],
        "2": ["circuit"],
        "3": ["cross_domain"],
        "4": ["cad", "circuit", "cross_domain"]
    }

    domains = domains_map.get(choice, ["cad", "circuit", "cross_domain"])

    print(f"\n将执行: {', '.join(domains)}")
    input("\n按 Enter 开始搜索...")

    stats, total = engine.parallel_deep_search(domains, max_workers=10)

    print(f"\n✅ 深度搜索完成！新增 {total} 个项目")


if __name__ == "__main__":
    main()
