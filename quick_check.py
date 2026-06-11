"""
快速验证脚本 - 检查文件和路径配置
"""

import os

print("=" * 60)
print("2026 World Cup Dashboard - 快速验证")
print("=" * 60)
print()

# 检查 data 文件夹
print("1. 检查数据文件:")
print()

data_files = [
    "data/world_cup_players.csv",
    "data/world_cup_teams.csv",
    "data/world_cup_squads.csv"
]

for file in data_files:
    exists = os.path.exists(file)
    size = os.path.getsize(file) / 1024 / 1024 if exists else 0
    status = "OK" if exists else "MISS"
    print(f"   [{status}] {file} - {size:.2f} MB")

print()

# 检查代码文件
print("2. 检查代码文件:")
print()

code_files = [
    "app.py",
    "src/data_pipeline.py",
    "src/model_pipeline.py",
    ".streamlit/config.toml",
    ".streamlit/secrets.toml"
]

for file in code_files:
    exists = os.path.exists(file)
    status = "OK" if exists else "MISS"
    print(f"   [{status}] {file}")

print()

# 测试路径解析
print("3. 测试路径解析:")
print()

try:
    from src.data_pipeline import get_data_path

    test_paths = [
        ("world_cup_players.csv", get_data_path("world_cup_players.csv")),
        ("world_cup_teams.csv", get_data_path("world_cup_teams.csv")),
        ("world_cup_squads.csv", get_data_path("world_cup_squads.csv"))
    ]

    for name, path in test_paths:
        exists = os.path.exists(path)
        status = "OK" if exists else "MISS"
        print(f"   [{status}] {name}")
        if exists:
            print(f"        路径: {path}")
        else:
            print(f"        警告: {path} 不存在")

except Exception as e:
    print(f"   [FAIL] 无法导入 src.data_pipeline: {e}")

print()

print("=" * 60)
print("验证完成！")
print("=" * 60)
print()
print("下一步:")
print("   1. 确保已安装: pip install -r requirements.txt")
print("   2. 运行: streamlit run app.py")
print("   3. 访问: http://localhost:8501")
print()