#!/usr/bin/env python3
"""
项目深度分析工具
分析项目质量、活跃度、技术栈、成熟度
"""

import sqlite3
import subprocess
import json
import re
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
from datetime import datetime


class ProjectAnalyzer:
    """项目分析器"""

    def __init__(self, db_path: str = "../data/projects.db"):
        self.db_path = db_path

    def get_projects(self, domain: str = None, limit: int = None) -> List[Dict]:
        """获取项目列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if domain:
            query = "SELECT * FROM projects WHERE domain = ? ORDER BY stars DESC"
            params = (domain,)
        else:
            query = "SELECT * FROM projects ORDER BY stars DESC"
            params = ()

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        projects = [dict(zip(columns, row)) for row in rows]
        conn.close()

        return projects

    def analyze_tech_stack(self, projects: List[Dict]) -> Dict:
        """分析技术栈分布"""
        language_stats = Counter()
        language_by_domain = defaultdict(Counter)

        for project in projects:
            lang = project.get('main_language', 'Unknown')
            domain = project.get('domain', 'Unknown')

            if lang and lang != 'Unknown':
                language_stats[lang] += 1
                language_by_domain[domain][lang] += 1

        return {
            "overall": dict(language_stats.most_common(15)),
            "by_domain": {d: dict(langs.most_common(10))
                         for d, langs in language_by_domain.items()}
        }

    def analyze_activity_trends(self, projects: List[Dict]) -> Dict:
        """分析活跃度趋势"""
        now = datetime.now()

        activity_levels = {
            "highly_active": 0,  # 30天内更新
            "active": 0,         # 90天内更新
            "moderate": 0,       # 180天内更新
            "low": 0,            # 1年内更新
            "inactive": 0        # 1年以上未更新
        }

        by_domain = defaultdict(lambda: dict(activity_levels))

        for project in projects:
            updated = project.get('last_updated', '')
            domain = project.get('domain', 'Unknown')

            if not updated:
                activity_levels["inactive"] += 1
                by_domain[domain]["inactive"] += 1
                continue

            try:
                update_date = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                days_ago = (now.replace(tzinfo=update_date.tzinfo) - update_date).days

                if days_ago < 30:
                    level = "highly_active"
                elif days_ago < 90:
                    level = "active"
                elif days_ago < 180:
                    level = "moderate"
                elif days_ago < 365:
                    level = "low"
                else:
                    level = "inactive"

                activity_levels[level] += 1
                by_domain[domain][level] += 1

            except:
                activity_levels["inactive"] += 1
                by_domain[domain]["inactive"] += 1

        return {
            "overall": activity_levels,
            "by_domain": dict(by_domain)
        }

    def analyze_quality_tiers(self, projects: List[Dict]) -> Dict:
        """分析项目质量层级"""
        tiers = {
            "top_tier": [],       # Score >= 80
            "high_quality": [],   # 60 <= Score < 80
            "good": [],           # 40 <= Score < 60
            "developing": []      # Score < 40
        }

        by_domain = defaultdict(lambda: {
            "top_tier": 0,
            "high_quality": 0,
            "good": 0,
            "developing": 0
        })

        for project in projects:
            score = project.get('activity_score', 0)
            domain = project.get('domain', 'Unknown')
            name = project.get('full_name', 'Unknown')

            if score >= 80:
                tier = "top_tier"
            elif score >= 60:
                tier = "high_quality"
            elif score >= 40:
                tier = "good"
            else:
                tier = "developing"

            tiers[tier].append({
                "name": name,
                "domain": domain,
                "score": score,
                "stars": project.get('stars', 0)
            })
            by_domain[domain][tier] += 1

        # 只保留每层前10个
        for tier in tiers:
            tiers[tier] = sorted(tiers[tier],
                                key=lambda x: x['score'],
                                reverse=True)[:10]

        return {
            "tiers": tiers,
            "by_domain": dict(by_domain)
        }

    def analyze_license_distribution(self, projects: List[Dict]) -> Dict:
        """分析许可证分布"""
        license_stats = Counter()
        by_domain = defaultdict(Counter)

        for project in projects:
            license_name = project.get('license', 'No License')
            domain = project.get('domain', 'Unknown')

            if not license_name or license_name == '':
                license_name = 'No License'

            license_stats[license_name] += 1
            by_domain[domain][license_name] += 1

        return {
            "overall": dict(license_stats.most_common(10)),
            "by_domain": {d: dict(licenses.most_common(5))
                         for d, licenses in by_domain.items()}
        }

    def analyze_size_distribution(self, projects: List[Dict]) -> Dict:
        """分析项目规模分布（基于 stars）"""
        size_categories = {
            "mega": 0,      # > 10k stars
            "large": 0,     # 1k - 10k stars
            "medium": 0,    # 100 - 1k stars
            "small": 0,     # 10 - 100 stars
            "micro": 0      # < 10 stars
        }

        by_domain = defaultdict(lambda: dict(size_categories))

        for project in projects:
            stars = project.get('stars', 0)
            domain = project.get('domain', 'Unknown')

            if stars > 10000:
                category = "mega"
            elif stars > 1000:
                category = "large"
            elif stars > 100:
                category = "medium"
            elif stars > 10:
                category = "small"
            else:
                category = "micro"

            size_categories[category] += 1
            by_domain[domain][category] += 1

        return {
            "overall": size_categories,
            "by_domain": dict(by_domain)
        }

    def generate_analysis_report(self, output_path: str = None) -> Dict:
        """生成完整分析报告"""
        print("\n" + "="*80)
        print("📊 项目深度分析")
        print("="*80 + "\n")

        projects = self.get_projects()
        total_projects = len(projects)

        print(f"总项目数: {total_projects}\n")

        # 1. 技术栈分析
        print("1️⃣  技术栈分析...")
        tech_stack = self.analyze_tech_stack(projects)

        # 2. 活跃度分析
        print("2️⃣  活跃度分析...")
        activity = self.analyze_activity_trends(projects)

        # 3. 质量层级分析
        print("3️⃣  质量层级分析...")
        quality = self.analyze_quality_tiers(projects)

        # 4. 许可证分析
        print("4️⃣  许可证分析...")
        licenses = self.analyze_license_distribution(projects)

        # 5. 规模分析
        print("5️⃣  规模分析...")
        sizes = self.analyze_size_distribution(projects)

        # 6. 领域统计
        print("6️⃣  领域统计...")
        domain_stats = self._get_domain_stats()

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_projects": total_projects,
            "domain_stats": domain_stats,
            "tech_stack": tech_stack,
            "activity": activity,
            "quality": quality,
            "licenses": licenses,
            "sizes": sizes
        }

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ 报告已保存到: {output_path}")

        self._print_summary(report)

        return report

    def _get_domain_stats(self) -> Dict:
        """获取领域统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT domain,
               COUNT(*) as count,
               ROUND(AVG(stars)) as avg_stars,
               MAX(stars) as max_stars,
               ROUND(AVG(activity_score)) as avg_quality
        FROM projects
        GROUP BY domain
        ORDER BY count DESC
        """)

        stats = {}
        for row in cursor.fetchall():
            domain, count, avg_stars, max_stars, avg_quality = row
            stats[domain] = {
                "count": count,
                "avg_stars": int(avg_stars) if avg_stars else 0,
                "max_stars": int(max_stars) if max_stars else 0,
                "avg_quality": int(avg_quality) if avg_quality else 0
            }

        conn.close()
        return stats

    def _print_summary(self, report: Dict):
        """打印摘要"""
        print("\n" + "="*80)
        print("📈 分析摘要")
        print("="*80 + "\n")

        # 领域统计
        print("📊 领域分布:")
        for domain, stats in sorted(report['domain_stats'].items(),
                                    key=lambda x: x[1]['count'],
                                    reverse=True):
            print(f"  {domain:12} - {stats['count']:3d} 项目 | "
                  f"平均 {stats['avg_stars']:6,} ⭐ | "
                  f"质量 {stats['avg_quality']}/100")

        # 技术栈
        print("\n💻 主流技术栈:")
        for lang, count in list(report['tech_stack']['overall'].items())[:10]:
            print(f"  {lang:20} - {count:3d} 项目")

        # 活跃度
        print("\n📈 活跃度分布:")
        activity = report['activity']['overall']
        total = sum(activity.values())
        for level, count in activity.items():
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {level:20} - {count:3d} ({pct:5.1f}%)")

        # 质量层级
        print("\n🏆 质量层级:")
        quality_counts = {k: len(v) if isinstance(v, list) else v
                         for k, v in report['quality']['tiers'].items()}
        for tier, projects in quality_counts.items():
            count = len(projects) if isinstance(projects, list) else 0
            print(f"  {tier:20} - {count:3d} 项目")


def main():
    """主函数"""
    analyzer = ProjectAnalyzer()

    output_path = "../reports/project_analysis.json"
    analyzer.generate_analysis_report(output_path)

    print(f"\n✅ 分析完成！")


if __name__ == "__main__":
    main()
