#!/usr/bin/env python3
"""
Recommendation API Server
提供 RESTful API 接口供网页调用
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# 添加 tools 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

from recommendation_engine import (
    RecommendationEngine,
    UserRequirements,
    Domain,
    Experience,
    Budget
)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化推荐引擎
engine = RecommendationEngine(db_path="../data/projects.db")


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({"status": "healthy", "version": "1.0.0"})


@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    获取推荐

    Request JSON:
    {
        "domain": "latex|cad|circuit|framework",
        "experience": "beginner|intermediate|advanced",
        "budget": "free|low|medium|high",
        "features": ["feature1", "feature2"],
        "priority": "performance|ease_of_use|features|community",
        "language_preference": ["Python", "JavaScript"],  // optional
        "top_n": 10  // optional, default 10
    }
    """
    try:
        data = request.get_json()

        # 验证必需字段
        required_fields = ['domain', 'experience', 'budget', 'features', 'priority']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # 构造用户需求
        requirements = UserRequirements(
            domain=Domain(data['domain']),
            experience=Experience(data['experience']),
            budget=Budget(data['budget']),
            features=data['features'],
            priority=data['priority'],
            language_preference=data.get('language_preference', None)
        )

        # 获取推荐数量
        top_n = data.get('top_n', 10)

        # 获取推荐结果
        results = engine.get_recommendations(requirements, top_n=top_n)

        return jsonify(results)

    except ValueError as e:
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/api/domains', methods=['GET'])
def get_domains():
    """获取所有支持的领域"""
    return jsonify({
        "domains": [d.value for d in Domain],
        "experiences": [e.value for e in Experience],
        "budgets": [b.value for b in Budget],
        "priorities": ["performance", "ease_of_use", "features", "community"]
    })


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """获取数据库统计信息"""
    try:
        import sqlite3
        conn = sqlite3.connect('../data/projects.db')
        cursor = conn.cursor()

        # 总项目数
        cursor.execute("SELECT COUNT(*) FROM projects")
        total = cursor.fetchone()[0]

        # 各领域分布
        cursor.execute("""
        SELECT domain, COUNT(*) as count, AVG(stars) as avg_stars
        FROM projects
        GROUP BY domain
        """)

        domains = []
        for row in cursor.fetchall():
            domains.append({
                "domain": row[0],
                "count": row[1],
                "avg_stars": round(row[2], 0)
            })

        # 热门项目
        cursor.execute("""
        SELECT name, full_name, domain, stars
        FROM projects
        ORDER BY stars DESC
        LIMIT 5
        """)

        top_projects = []
        for row in cursor.fetchall():
            top_projects.append({
                "name": row[0],
                "full_name": row[1],
                "domain": row[2],
                "stars": row[3]
            })

        conn.close()

        return jsonify({
            "total_projects": total,
            "domains": domains,
            "top_projects": top_projects
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/commercial-tools/<domain>', methods=['GET'])
def get_commercial_tools(domain):
    """获取商业工具列表"""
    try:
        if domain not in [d.value for d in Domain]:
            return jsonify({"error": "Invalid domain"}), 400

        tools = engine.commercial_tools.get(domain, [])
        return jsonify({"domain": domain, "tools": tools})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║          AI Agent Recommendation API Server                  ║
║                   v1.0.0 - 2025 Edition                      ║
╚══════════════════════════════════════════════════════════════╝

API Endpoints:
  GET  /api/health              - Health check
  POST /api/recommend           - Get recommendations
  GET  /api/domains             - Get available options
  GET  /api/stats               - Get database statistics
  GET  /api/commercial-tools/<domain> - Get commercial tools

Starting server on http://localhost:5000
    """)

    app.run(debug=True, host='0.0.0.0', port=5000)
