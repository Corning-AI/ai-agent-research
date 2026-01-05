#!/usr/bin/env python3
"""
AI Agent Research Platform CLI
命令行工具，支持自动补全
"""

import click
import json
import sys
import os
from pathlib import Path

# 添加 tools 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'tools'))

from recommendation_engine import (
    RecommendationEngine,
    UserRequirements,
    Domain,
    Experience,
    Budget
)


@click.group()
@click.version_option(version='1.0.0', prog_name='AI Agent Research CLI')
def cli():
    """
    🤖 AI Agent 调研平台 - 命令行工具

    支持搜索、推荐、统计等功能
    """
    pass


@cli.command()
@click.option('--domain', '-d',
              type=click.Choice(['latex', 'cad', 'circuit', 'framework'], case_sensitive=False),
              required=True,
              help='专业领域')
@click.option('--experience', '-e',
              type=click.Choice(['beginner', 'intermediate', 'advanced'], case_sensitive=False),
              default='intermediate',
              help='经验水平')
@click.option('--budget', '-b',
              type=click.Choice(['free', 'low', 'medium', 'high'], case_sensitive=False),
              default='free',
              help='预算范围')
@click.option('--features', '-f',
              multiple=True,
              help='需要的功能（可多次指定）')
@click.option('--priority', '-p',
              type=click.Choice(['performance', 'ease_of_use', 'features', 'community'], case_sensitive=False),
              default='ease_of_use',
              help='优先考虑')
@click.option('--language', '-l',
              multiple=True,
              help='编程语言偏好（可多次指定）')
@click.option('--top', '-n',
              type=int,
              default=10,
              help='返回推荐数量')
@click.option('--output', '-o',
              type=click.Choice(['text', 'json'], case_sensitive=False),
              default='text',
              help='输出格式')
def recommend(domain, experience, budget, features, priority, language, top, output):
    """
    🎯 获取 AI 智能推荐

    示例：
    \b
    cli.py recommend -d latex -e beginner -f ai -f collaboration
    cli.py recommend --domain cad --budget medium --priority performance
    """
    click.echo(click.style(f'\n🔍 正在分析您的需求...', fg='cyan', bold=True))

    try:
        engine = RecommendationEngine()

        requirements = UserRequirements(
            domain=Domain(domain.lower()),
            experience=Experience(experience.lower()),
            budget=Budget(budget.lower()),
            features=list(features) if features else [],
            priority=priority.lower(),
            language_preference=list(language) if language else None
        )

        results = engine.get_recommendations(requirements, top_n=top)

        if output == 'json':
            click.echo(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            _print_recommendations(results)

    except Exception as e:
        click.echo(click.style(f'\n❌ 错误: {str(e)}', fg='red', bold=True))
        sys.exit(1)


def _print_recommendations(results):
    """格式化打印推荐结果"""
    click.echo(click.style(f'\n✅ 找到 {len(results["recommendations"])} 个推荐\n', fg='green', bold=True))

    req = results['requirements']
    click.echo(f"  领域: {click.style(req['domain'], fg='blue', bold=True)}")
    click.echo(f"  经验: {click.style(req['experience'], fg='blue')}")
    click.echo(f"  预算: {click.style(req['budget'], fg='blue')}")
    click.echo(f"  优先级: {click.style(req['priority'], fg='blue')}\n")

    click.echo(click.style('=' * 80, fg='white'))

    for i, rec in enumerate(results['recommendations'], 1):
        # 标题
        name = rec.get('name') or rec.get('full_name', 'Unknown')
        type_label = '商业工具' if rec['type'] == 'commercial' else '开源项目'
        type_color = 'magenta' if rec['type'] == 'commercial' else 'cyan'

        click.echo(f"\n{click.style(f'#{i}', fg='yellow', bold=True)} "
                   f"{click.style(name, fg='white', bold=True)} "
                   f"{click.style(f'[{type_label}]', fg=type_color)}")

        # 评分
        score = rec['relevance_score']
        score_color = 'green' if score >= 80 else 'yellow' if score >= 60 else 'red'
        click.echo(f"   相关度: {click.style(f'{score}/100', fg=score_color, bold=True)}")

        # 星标/价格
        if rec['type'] == 'open_source':
            stars = rec.get('stars', 0)
            click.echo(f"   ⭐ Stars: {click.style(f'{stars:,}', fg='yellow')}")
            if rec.get('main_language'):
                click.echo(f"   💻 语言: {rec['main_language']}")
            if rec.get('license'):
                click.echo(f"   📜 许可证: {rec['license']}")
        else:
            price = rec.get('price', 'N/A')
            click.echo(f"   💰 价格: {click.style(price, fg='green')}")

        # 描述
        desc = rec.get('description', 'N/A')
        if len(desc) > 100:
            desc = desc[:100] + '...'
        click.echo(f"   📝 {desc}")

        # 推荐理由
        reasoning = rec.get('reasoning', '')
        click.echo(f"   {click.style('💡 推荐理由:', fg='yellow')} {reasoning}")

        # URL
        url = rec.get('url', '')
        if url:
            click.echo(f"   🔗 {click.style(url, fg='blue', underline=True)}")

        click.echo(click.style('-' * 80, fg='white', dim=True))


@cli.command()
@click.option('--domain', '-d',
              type=click.Choice(['latex', 'cad', 'circuit', 'framework', 'all'], case_sensitive=False),
              default='all',
              help='领域筛选')
def stats(domain):
    """
    📊 查看数据统计

    示例：
    \b
    cli.py stats
    cli.py stats --domain latex
    """
    import sqlite3

    click.echo(click.style('\n📊 数据统计\n', fg='cyan', bold=True))

    try:
        conn = sqlite3.connect('data/projects.db')
        cursor = conn.cursor()

        if domain == 'all':
            # 总体统计
            cursor.execute("SELECT COUNT(*) FROM projects")
            total = cursor.fetchone()[0]
            click.echo(f"总项目数: {click.style(str(total), fg='green', bold=True)}")

            # 各领域统计
            cursor.execute("""
            SELECT domain, COUNT(*) as count,
                   ROUND(AVG(stars)) as avg_stars,
                   MAX(stars) as max_stars
            FROM projects
            GROUP BY domain
            ORDER BY count DESC
            """)

            click.echo(f"\n{click.style('领域分布:', fg='yellow', bold=True)}\n")
            click.echo(f"  {'领域':<12} {'项目数':<10} {'平均Stars':<12} {'最高Stars':<12}")
            click.echo(f"  {'-' * 50}")

            for row in cursor.fetchall():
                domain_name, count, avg_stars, max_stars = row
                click.echo(f"  {domain_name:<12} {count:<10} {int(avg_stars):<12,} {int(max_stars):<12,}")
        else:
            # 单个领域统计
            cursor.execute("""
            SELECT COUNT(*),
                   ROUND(AVG(stars)),
                   MAX(stars),
                   MIN(stars)
            FROM projects
            WHERE domain = ?
            """, (domain,))

            count, avg_stars, max_stars, min_stars = cursor.fetchone()

            click.echo(f"领域: {click.style(domain.upper(), fg='blue', bold=True)}\n")
            click.echo(f"  项目总数: {click.style(str(count), fg='green')}")
            click.echo(f"  平均 Stars: {click.style(f'{int(avg_stars):,}', fg='yellow')}")
            click.echo(f"  最高 Stars: {click.style(f'{int(max_stars):,}', fg='green')}")
            click.echo(f"  最低 Stars: {click.style(f'{int(min_stars):,}', fg='red')}")

            # Top 5 项目
            cursor.execute("""
            SELECT name, stars, description
            FROM projects
            WHERE domain = ?
            ORDER BY stars DESC
            LIMIT 5
            """, (domain,))

            click.echo(f"\n{click.style('Top 5 项目:', fg='yellow', bold=True)}\n")
            for i, (name, stars, desc) in enumerate(cursor.fetchall(), 1):
                desc_short = desc[:60] + '...' if desc and len(desc) > 60 else desc or ''
                click.echo(f"  {i}. {click.style(name, fg='cyan')} ({stars:,} ⭐)")
                click.echo(f"     {desc_short}\n")

        conn.close()

    except Exception as e:
        click.echo(click.style(f'\n❌ 错误: {str(e)}', fg='red', bold=True))
        sys.exit(1)


@cli.command()
@click.option('--domain', '-d',
              type=click.Choice(['latex', 'cad', 'circuit', 'framework'], case_sensitive=False),
              required=True,
              help='领域')
@click.option('--limit', '-n',
              type=int,
              default=10,
              help='显示数量')
@click.option('--sort',
              type=click.Choice(['stars', 'activity', 'forks'], case_sensitive=False),
              default='stars',
              help='排序方式')
def list(domain, limit, sort):
    """
    📋 列出项目

    示例：
    \b
    cli.py list -d latex
    cli.py list --domain cad --limit 20 --sort activity
    """
    import sqlite3

    click.echo(click.style(f'\n📋 {domain.upper()} 领域项目\n', fg='cyan', bold=True))

    try:
        conn = sqlite3.connect('data/projects.db')
        cursor = conn.cursor()

        sort_column = {
            'stars': 'stars',
            'activity': 'activity_score',
            'forks': 'forks'
        }[sort]

        cursor.execute(f"""
        SELECT name, full_name, stars, forks, activity_score, description, url
        FROM projects
        WHERE domain = ?
        ORDER BY {sort_column} DESC
        LIMIT ?
        """, (domain, limit))

        for i, (name, full_name, stars, forks, activity, desc, url) in enumerate(cursor.fetchall(), 1):
            click.echo(f"{click.style(f'#{i}', fg='yellow')} {click.style(name, fg='white', bold=True)}")
            click.echo(f"   {full_name}")
            click.echo(f"   ⭐ {stars:,} | 🍴 {forks:,} | 📈 {activity}")
            if desc:
                desc_short = desc[:80] + '...' if len(desc) > 80 else desc
                click.echo(f"   {desc_short}")
            click.echo(f"   🔗 {click.style(url, fg='blue', underline=True)}")
            click.echo()

        conn.close()

    except Exception as e:
        click.echo(click.style(f'\n❌ 错误: {str(e)}', fg='red', bold=True))
        sys.exit(1)


@cli.command()
def web():
    """
    🌐 打开网页界面
    """
    import webbrowser

    click.echo(click.style('\n🌐 正在打开网页界面...', fg='cyan', bold=True))

    pages = [
        ('主页', 'index.html'),
        ('AI 推荐', 'web/recommendation.html'),
        ('数据概览', 'web/overview.html'),
        ('LaTeX 专题', 'web/index.html'),
    ]

    click.echo('\n请选择要打开的页面：\n')
    for i, (name, _) in enumerate(pages, 1):
        click.echo(f"  {i}. {name}")

    choice = click.prompt('\n输入选项', type=int, default=1)

    if 1 <= choice <= len(pages):
        name, path = pages[choice - 1]
        file_path = os.path.abspath(path)
        webbrowser.open(f'file://{file_path}')
        click.echo(click.style(f'\n✅ 已打开 {name}', fg='green'))
    else:
        click.echo(click.style('\n❌ 无效选项', fg='red'))


@cli.command()
def setup_completion():
    """
    ⚙️  设置 Shell 自动补全

    支持 Bash, Zsh, Fish
    """
    click.echo(click.style('\n⚙️  Shell 自动补全设置\n', fg='cyan', bold=True))

    shells = ['bash', 'zsh', 'fish']

    click.echo('请选择您的 Shell：\n')
    for i, shell in enumerate(shells, 1):
        click.echo(f"  {i}. {shell}")

    choice = click.prompt('\n输入选项', type=int, default=1)

    if 1 <= choice <= len(shells):
        shell = shells[choice - 1]

        click.echo(f"\n{click.style('安装步骤:', fg='yellow', bold=True)}\n")

        if shell == 'bash':
            click.echo("1. 运行以下命令生成补全脚本：")
            click.echo(click.style("   eval \"$(_CLI_COMPLETE=bash_source ./cli.py)\" >> ~/.bashrc", fg='green'))
            click.echo("\n2. 重新加载配置：")
            click.echo(click.style("   source ~/.bashrc", fg='green'))

        elif shell == 'zsh':
            click.echo("1. 运行以下命令生成补全脚本：")
            click.echo(click.style("   eval \"$(_CLI_COMPLETE=zsh_source ./cli.py)\" >> ~/.zshrc", fg='green'))
            click.echo("\n2. 重新加载配置：")
            click.echo(click.style("   source ~/.zshrc", fg='green'))

        elif shell == 'fish':
            click.echo("1. 运行以下命令生成补全脚本：")
            click.echo(click.style("   eval (env _CLI_COMPLETE=fish_source ./cli.py) > ~/.config/fish/completions/cli.fish", fg='green'))
            click.echo("\n2. 重新加载配置：")
            click.echo(click.style("   source ~/.config/fish/config.fish", fg='green'))

        click.echo(f"\n{click.style('完成后，您可以使用 Tab 键自动补全命令和选项！', fg='cyan')}")

    else:
        click.echo(click.style('\n❌ 无效选项', fg='red'))


if __name__ == '__main__':
    cli()
