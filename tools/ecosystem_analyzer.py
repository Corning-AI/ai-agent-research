#!/usr/bin/env python3
"""
生态系统分析工具
分析项目间关系、技术栈组合、开发者网络、趋势
"""

import sqlite3
import json
from typing import Dict, List
from collections import defaultdict, Counter
from datetime import datetime


class EcosystemAnalyzer:
    """生态系统分析器"""

    def __init__(self, db_path: str = "../data/projects.db"):
        self.db_path = db_path

    def analyze_tech_stack_combinations(self) -> Dict:
        """分析技术栈组合"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT domain, main_language, COUNT(*) as count
        FROM projects
        WHERE main_language IS NOT NULL AND main_language != ''
        GROUP BY domain, main_language
        ORDER BY domain, count DESC
        """)

        combos = defaultdict(list)
        for domain, lang, count in cursor.fetchall():
            combos[domain].append({"language": lang, "count": count})

        conn.close()
        return dict(combos)

    def analyze_temporal_trends(self) -> Dict:
        """分析时间趋势"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 按年份分组
        cursor.execute("""
        SELECT
            domain,
            strftime('%Y', created_at) as year,
            COUNT(*) as count
        FROM projects
        WHERE created_at IS NOT NULL AND created_at != ''
        GROUP BY domain, year
        ORDER BY year, domain
        """)

        trends = defaultdict(lambda: defaultdict(int))
        for domain, year, count in cursor.fetchall():
            if year and year != '':
                trends[domain][year] = count

        # 最近更新趋势
        cursor.execute("""
        SELECT
            domain,
            CASE
                WHEN julianday('now') - julianday(last_updated) < 30 THEN 'last_month'
                WHEN julianday('now') - julianday(last_updated) < 90 THEN 'last_quarter'
                WHEN julianday('now') - julianday(last_updated) < 365 THEN 'last_year'
                ELSE 'older'
            END as period,
            COUNT(*) as count
        FROM projects
        WHERE last_updated IS NOT NULL AND last_updated != ''
        GROUP BY domain, period
        ORDER BY domain
        """)

        update_trends = defaultdict(dict)
        for domain, period, count in cursor.fetchall():
            update_trends[domain][period] = count

        conn.close()

        return {
            "creation_trends": dict(trends),
            "update_trends": dict(update_trends)
        }

    def identify_emerging_projects(self) -> List[Dict]:
        """识别新兴项目（高增长、新创建）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 2024-2025 创建且高活跃度的项目
        cursor.execute("""
        SELECT domain, full_name, stars, forks, created_at, last_updated, activity_score
        FROM projects
        WHERE created_at >= '2024-01-01'
          AND activity_score > 60
        ORDER BY activity_score DESC, stars DESC
        LIMIT 30
        """)

        emerging = []
        for row in cursor.fetchall():
            domain, name, stars, forks, created, updated, score = row
            emerging.append({
                "domain": domain,
                "name": name,
                "stars": stars,
                "forks": forks,
                "created_at": created,
                "last_updated": updated,
                "activity_score": score
            })

        conn.close()
        return emerging

    def analyze_domain_maturity(self) -> Dict:
        """分析领域成熟度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        maturity = {}

        for domain in ['latex', 'cad', 'circuit', 'framework']:
            cursor.execute("""
            SELECT
                COUNT(*) as total_projects,
                AVG(stars) as avg_stars,
                MAX(stars) as max_stars,
                AVG(forks) as avg_forks,
                AVG(activity_score) as avg_activity,
                AVG(julianday('now') - julianday(created_at)) as avg_age_days,
                COUNT(CASE WHEN stars > 1000 THEN 1 END) as mature_projects,
                COUNT(CASE WHEN created_at >= '2024-01-01' THEN 1 END) as new_projects
            FROM projects
            WHERE domain = ?
            """, (domain,))

            row = cursor.fetchone()
            if row:
                total, avg_stars, max_stars, avg_forks, avg_activity, avg_age, mature, new = row

                # 计算成熟度指数 (0-100)
                maturity_score = 0
                if mature:
                    maturity_score += min((mature / total) * 40, 40)  # 成熟项目占比
                if avg_stars:
                    maturity_score += min((avg_stars / 1000) * 30, 30)  # 平均星标
                if avg_activity:
                    maturity_score += min((avg_activity / 100) * 30, 30)  # 平均活跃度

                maturity[domain] = {
                    "total_projects": total,
                    "avg_stars": round(avg_stars, 0) if avg_stars else 0,
                    "max_stars": max_stars,
                    "avg_forks": round(avg_forks, 0) if avg_forks else 0,
                    "avg_activity_score": round(avg_activity, 1) if avg_activity else 0,
                    "avg_age_days": round(avg_age, 0) if avg_age else 0,
                    "mature_projects": mature,
                    "new_projects_2024": new,
                    "maturity_score": round(maturity_score, 1)
                }

        conn.close()
        return maturity

    def generate_ecosystem_report(self, output_path: str = None) -> Dict:
        """生成生态系统报告"""
        print("\n" + "="*80)
        print("🌐 生态系统分析")
        print("="*80 + "\n")

        # 1. 技术栈组合
        print("1️⃣  分析技术栈组合...")
        tech_combos = self.analyze_tech_stack_combinations()

        # 2. 时间趋势
        print("2️⃣  分析时间趋势...")
        trends = self.analyze_temporal_trends()

        # 3. 新兴项目
        print("3️⃣  识别新兴项目...")
        emerging = self.identify_emerging_projects()

        # 4. 领域成熟度
        print("4️⃣  分析领域成熟度...")
        maturity = self.analyze_domain_maturity()

        report = {
            "generated_at": datetime.now().isoformat(),
            "tech_stack_combinations": tech_combos,
            "temporal_trends": trends,
            "emerging_projects": emerging,
            "domain_maturity": maturity
        }

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ 报告已保存到: {output_path}")

        self._print_summary(report)

        return report

    def _print_summary(self, report: Dict):
        """打印摘要"""
        print("\n" + "="*80)
        print("📊 生态系统摘要")
        print("="*80 + "\n")

        # 技术栈组合
        print("💻 技术栈分布:")
        for domain, langs in sorted(report['tech_stack_combinations'].items()):
            print(f"\n  {domain.upper()}:")
            for lang_data in langs[:5]:
                lang = lang_data['language']
                count = lang_data['count']
                print(f"    {lang:20} - {count:3d} 项目")

        # 领域成熟度
        print("\n🎯 领域成熟度:")
        for domain, stats in sorted(report['domain_maturity'].items(),
                                    key=lambda x: x[1]['maturity_score'],
                                    reverse=True):
            print(f"\n  {domain.upper()} (成熟度: {stats['maturity_score']}/100)")
            print(f"    总项目: {stats['total_projects']}")
            print(f"    平均 Stars: {stats['avg_stars']:,.0f}")
            print(f"    成熟项目 (>1K stars): {stats['mature_projects']}")
            print(f"    2024新项目: {stats['new_projects_2024']}")
            print(f"    平均年龄: {stats['avg_age_days']/365:.1f} 年")

        # 新兴项目
        print("\n🌟 新兴项目 (2024-2025):")
        for i, proj in enumerate(report['emerging_projects'][:10], 1):
            print(f"  {i:2d}. {proj['name']:40} | "
                  f"{proj['domain']:10} | "
                  f"{proj['stars']:6,} ⭐ | "
                  f"活跃度 {proj['activity_score']}")


def main():
    """主函数"""
    analyzer = EcosystemAnalyzer()

    output_path = "../reports/ecosystem_analysis.json"
    analyzer.generate_ecosystem_report(output_path)

    print(f"\n✅ 生态系统分析完成！")


if __name__ == "__main__":
    main()
