"""
快速测试脚本 - 验证数据加载和网站运行
"""

import os
import sys
import io

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("测试 2026 World Cup Dashboard")
print("=" * 60)
print()

# 测试 1: 检查 data 文件夹
print("测试 1: 检查数据文件...")
print()

data_files = [
    "data/world_cup_players.csv",
    "data/world_cup_teams.csv",
    "data/world_cup_squads.csv"
]

all_exist = True
for file in data_files:
    exists = os.path.exists(file)
    status = "[OK]" if exists else "[MISS]"
    print(f"   {status} {file}")
    if not exists:
        all_exist = False

print()

if not all_exist:
    print("错误: 缺少数据文件！")
    print("请确保 data/ 文件夹中有以下文件：")
    for file in data_files:
        print(f"   • {file}")
    sys.exit(1)

# 测试 2: 检查 Python 模块
print("=" * 60)
print("测试 2: 检查 Python 依赖...")
print()

try:
    import pandas as pd
    print("   [OK] pandas")
except ImportError:
    print("   [FAIL] pandas - 请运行: pip install pandas")
    sys.exit(1)

try:
    import numpy as np
    print("   [OK] numpy")
except ImportError:
    print("   [FAIL] numpy - 请运行: pip install numpy")
    sys.exit(1)

try:
    import sklearn
    print("   [OK] scikit-learn")
except ImportError:
    print("   [FAIL] scikit-learn - 请运行: pip install scikit-learn")
    sys.exit(1)

try:
    import plotly
    print("   [OK] plotly")
except ImportError:
    print("   [FAIL] plotly - 请运行: pip install plotly")
    sys.exit(1)

try:
    import streamlit
    print("   [OK] streamlit")
except ImportError:
    print("   [FAIL] streamlit - 请运行: pip install streamlit")
    sys.exit(1)

print()

# 测试 3: 读取数据文件
print("=" * 60)
print("测试 3: 读取数据文件...")
print()

try:
    players_df = pd.read_csv("data/world_cup_players.csv", encoding='utf-8')
    print(f"   [OK] world_cup_players.csv: {len(players_df)} 行, {len(players_df.columns)} 列")
    print(f"       列: {list(players_df.columns)[:5]}...")
except Exception as e:
    print(f"   [FAIL] world_cup_players.csv: {e}")
    sys.exit(1)

try:
    teams_df = pd.read_csv("data/world_cup_teams.csv", encoding='utf-8')
    print(f"   [OK] world_cup_teams.csv: {len(teams_df)} 行, {len(teams_df.columns)} 列")
except Exception as e:
    print(f"   [FAIL] world_cup_teams.csv: {e}")
    sys.exit(1)

try:
    squads_df = pd.read_csv("data/world_cup_squads.csv", encoding='utf-8')
    print(f"   [OK] world_cup_squads.csv: {len(squads_df)} 行, {len(squads_df.columns)} 列")
except Exception as e:
    print(f"   [FAIL] world_cup_squads.csv: {e}")
    sys.exit(1)

print()

# 测试 4: 导入自定义模块
print("=" * 60)
print("测试 4: 导入自定义模块...")
print()

try:
    from src.data_pipeline import get_data_path, standardize_name
    print("   [OK] src.data_pipeline")
except Exception as e:
    print(f"   [FAIL] src.data_pipeline: {e}")
    sys.exit(1)

try:
    from src.model_pipeline import PlayerClusterEngine, calculate_kpis
    print("   [OK] src.model_pipeline")
except Exception as e:
    print(f"   [FAIL] src.model_pipeline: {e}")
    sys.exit(1)

print()

# 测试 5: 测试路径解析
print("=" * 60)
print("测试 5: 测试路径解析...")
print()

test_paths = [
    get_data_path("world_cup_players.csv"),
    get_data_path("world_cup_teams.csv"),
    get_data_path("world_cup_squads.csv")
]

for path in test_paths:
    exists = os.path.exists(path)
    status = "[OK]" if exists else "[MISS]"
    print(f"   {status} {path}")
    if not exists:
        print(f"      警告: 文件不存在")

print()

# 测试 6: 测试导入 app.py
print("=" * 60)
print("测试 6: 导入 app.py...")
print()

try:
    import app
    print("   [OK] app.py 导入成功")
except Exception as e:
    print(f"   [FAIL] app.py 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("所有测试通过！")
print("=" * 60)
print()
print("下一步:")
print("   运行: streamlit run app.py")
print("   或双击: 启动仪表盘.bat")
print()