#!/usr/bin/env python3
"""
GitHub Profile Dashboard Generator
Uses GitHub API to collect repository data and generate charts
"""

import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import json

# Settings
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Create directories
os.makedirs('charts', exist_ok=True)
os.makedirs('docs', exist_ok=True)

def get_github_data():
    """Get repository data from GitHub API"""
    repos_data = []

    # Popular repositories to track
    repos_to_track = [
        'facebook/react',
        'microsoft/vscode',
        'google/tensorflow',
        'apple/swift',
        'netflix/zuul',
        'amazon/aws-sdk-js',
        'stripe/stripe-js',
        'twilio/twilio-python'
    ]

    for repo_name in repos_to_track:
        try:
            url = f'https://api.github.com/repos/{repo_name}'
            response = requests.get(url, headers=HEADERS)

            if response.status_code == 200:
                repo_data = response.json()
                repos_data.append({
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'owner': repo_data['owner']['login'],
                    'stars': repo_data['stargazers_count'],
                    'language': repo_data['language'] or 'Unknown',
                    'created_at': repo_data['created_at'],
                    'updated_at': repo_data['updated_at']
                })
            else:
                print(f"Failed to get data for {repo_name}: {response.status_code}")

        except Exception as e:
            print(f"Error processing {repo_name}: {e}")

    return repos_data

def generate_overview_chart(repos_data):
    """Generate market overview chart"""
    if not repos_data:
        return

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('GitHub Repositories Market Overview', fontsize=16)

    # Stars distribution
    stars = [repo['stars'] for repo in repos_data]
    ax1.hist(stars, bins=20, color='#1f77b4', alpha=0.7)
    ax1.set_title('Stars Distribution')
    ax1.set_xlabel('Stars Count')
    ax1.set_ylabel('Number of Repositories')

    # Popular languages
    languages = defaultdict(int)
    for repo in repos_data:
        languages[repo['language']] += 1

    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
    if top_langs:
        langs, counts = zip(*top_langs)
        ax2.bar(langs, counts, color='#ff7f0e')
        ax2.set_title('Popular Languages')
        ax2.tick_params(axis='x', rotation=45)

    # Top repositories by stars
    top_repos = sorted(repos_data, key=lambda x: x['stars'], reverse=True)[:10]
    names = [repo['name'][:15] + '...' if len(repo['name']) > 15 else repo['name'] for repo in top_repos]
    stars_count = [repo['stars'] for repo in top_repos]

    ax3.barh(names[::-1], stars_count[::-1], color='#2ca02c')
    ax3.set_title('Top Repositories by Stars')

    # Repository owners
    owners = defaultdict(int)
    for repo in repos_data:
        owners[repo['owner']] += 1

    top_owners = sorted(owners.items(), key=lambda x: x[1], reverse=True)[:8]
    if top_owners:
        owner_names, owner_counts = zip(*top_owners)
        ax4.bar(owner_names, owner_counts, color='#9467bd')
        ax4.set_title('Repository Owners')
        ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('charts/overview.png', dpi=150, bbox_inches='tight')
    plt.close()

def generate_language_chart(repos_data):
    """Generate language popularity chart"""
    languages = defaultdict(int)
    for repo in repos_data:
        languages[repo['language']] += 1

    if languages:
        plt.figure(figsize=(10, 6))
        langs = list(languages.keys())
        counts = list(languages.values())

        sorted_data = sorted(zip(langs, counts), key=lambda x: x[1], reverse=True)
        langs, counts = zip(*sorted_data)

        plt.bar(langs, counts, color='#e74c3c')
        plt.title('Programming Languages in Tracked Repositories')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Number of Repositories')
        plt.tight_layout()
        plt.savefig('charts/languages.png', dpi=150, bbox_inches='tight')
        plt.close()

def update_readme(repos_data):
    """Update README.md with current data"""
    total_repos = len(repos_data)
    total_stars = sum(repo['stars'] for repo in repos_data)
    avg_stars = total_stars // total_repos if total_repos > 0 else 0

    top_repos = sorted(repos_data, key=lambda x: x['stars'], reverse=True)[:5]

    readme_content = f"""# NickScherbakov-dashboard

## 📊 GitHub Repositories Market Dashboard

Monitoring GitHub repository market - tracking popular projects and technologies.

### 📈 Current Statistics
- **Tracked Repositories**: {total_repos}
- **Total Stars**: {total_stars:,}
- **Average Stars**: {avg_stars:,}

### 📊 Market Overview
![Market Overview](charts/overview.png)

### 🏷️ Popular Languages
![Languages](charts/languages.png)

### 🔝 Top 5 Repositories
| Repository | Owner | Stars | Language |
|------------|-------|-------|----------|
"""

    for repo in top_repos:
        readme_content += f"| [{repo['name']}](https://github.com/{repo['full_name']}) | {repo['owner']} | ⭐ {repo['stars']:,} | {repo['language']} |\n"

    readme_content += f"\n*Dashboard updates automatically every 6 hours. Last update: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_index_html(repos_data):
    """Create index.html for GitHub Pages"""
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NickScherbakov - GitHub Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        .chart-container {{
            margin: 30px 0;
            text-align: center;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .repos-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
        }}
        .repos-table th, .repos-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .repos-table th {{
            background: #f8f9fa;
            font-weight: 600;
        }}
        .update-time {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 NickScherbakov</h1>
            <p>GitHub Repositories Market Dashboard</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3>{len(repos_data)}</h3>
                <p>Tracked Repositories</p>
            </div>
            <div class="stat-card">
                <h3>{sum(repo['stars'] for repo in repos_data):,}</h3>
                <p>Total Stars</p>
            </div>
            <div class="stat-card">
                <h3>{sum(repo['stars'] for repo in repos_data) // len(repos_data) if repos_data else 0:,}</h3>
                <p>Average Stars</p>
            </div>
        </div>

        <div class="chart-container">
            <h2>📊 Market Overview</h2>
            <img src="charts/overview.png" alt="Market Overview Chart">
        </div>

        <div class="chart-container">
            <h2>🏷️ Popular Languages</h2>
            <img src="charts/languages.png" alt="Languages Chart">
        </div>

        <h2>🔝 Top Repositories</h2>
        <table class="repos-table">
            <thead>
                <tr>
                    <th>Repository</th>
                    <th>Owner</th>
                    <th>Stars</th>
                    <th>Language</th>
                </tr>
            </thead>
            <tbody>"""

    top_repos = sorted(repos_data, key=lambda x: x['stars'], reverse=True)[:10]
    for repo in top_repos:
        html_content += f"""
                <tr>
                    <td><a href="https://github.com/{repo['full_name']}" target="_blank">{repo['name']}</a></td>
                    <td>{repo['owner']}</td>
                    <td>⭐ {repo['stars']:,}</td>
                    <td>{repo['language']}</td>
                </tr>"""

    html_content += f"""
            </tbody>
        </table>

        <div class="update-time">
            📅 Last update: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
        </div>
    </div>
</body>
</html>"""

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    """Main function"""
    print("🚀 Starting dashboard generation...")

    # Get data
    print("📊 Getting data from GitHub API...")
    repos_data = get_github_data()

    if not repos_data:
        print("❌ Failed to get data")
        return

    print(f"✅ Got data for {len(repos_data)} repositories")

    # Generate charts
    print("📈 Generating charts...")
    generate_overview_chart(repos_data)
    generate_language_chart(repos_data)

    # Update README
    print("📝 Updating README...")
    update_readme(repos_data)

    # Create HTML page
    print("🌐 Creating HTML page...")
    create_index_html(repos_data)

    print("🎉 Dashboard updated successfully!")

if __name__ == '__main__':
    main()