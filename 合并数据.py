"""
合并 CSV 文件 - 生成清洗后的小体积数据集
"""

import pandas as pd
import os
import shutil
from datetime import datetime

# ============================================================
# 配置
# ============================================================
INPUT_DIR = r"d:\cursor data 2"
BACKUP_DIR = r"d:\cursor data 2\archive_backup"
OUTPUT_DIR = r"d:\cursor data 2\data"

# 创建备份和输出目录
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🚀 开始合并和清洗 CSV 文件...")
print()

# ============================================================
# 第 1 步：备份原始文件
# ============================================================
print("📦 备份原始文件到 archive_backup/...")

source_files = [
    "archive (2)/male_players.csv",
    "archive (2)/male_teams.csv",
    "archive (3)/fifa_world_cup_2026_golden_dataset.csv"
]

for file in source_files:
    src = os.path.join(INPUT_DIR, file.replace("/", os.sep))
    dst = os.path.join(BACKUP_DIR, os.path.basename(file))
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"   ✅ 备份: {os.path.basename(file)}")

print()

# ============================================================
# 第 2 步：读取 2026 世界杯数据
# ============================================================
print("📊 读取 2026 World Cup 数据...")
wcup_path = os.path.join(INPUT_DIR, "archive (3)", "fifa_world_cup_2026_golden_dataset.csv")
wcup_df = pd.read_csv(wcup_path, encoding='utf-8')
print(f"   原始记录: {len(wcup_df)} 行")
print(f"   列数: {len(wcup_df.columns)}")
print()

# ============================================================
# 第 3 步：提取 FIFA 24 球员数据（只保留需要的列）
# ============================================================
print("📊 读取 FIFA 24 球员数据...")
players_path = os.path.join(INPUT_DIR, "archive (2)", "male_players.csv")

# 定义需要的列
PLAYER_COLUMNS = [
    "short_name",
    "long_name",
    "overall",
    "potential",
    "pace",
    "shooting",
    "passing",
    "dribbling",
    "defending",
    "physic",
    "club_name",
    "nationality_name",
    "age",
    "height_cm",
    "weight_kg",
    "club_position"
]

# 读取所有数据
players_df = pd.read_csv(players_path, encoding='utf-8', low_memory=False)
print(f"   原始记录: {len(players_df)} 行")
print(f"   原始列数: {len(players_df.columns)}")

# 只保留需要的列
available_cols = [c for c in PLAYER_COLUMNS if c in players_df.columns]
players_df = players_df[available_cols]
print(f"   精简后列数: {len(players_df.columns)}")
print()

# ============================================================
# 第 4 步：提取团队数据
# ============================================================
print("📊 读取 FIFA 24 团队数据...")
teams_path = os.path.join(INPUT_DIR, "archive (2)", "male_teams.csv")

TEAMS_COLUMNS = [
    "Name",
    "Overall",
    "Attack",
    "Midfield",
    "Defense"
]

teams_df = pd.read_csv(teams_path, encoding='utf-8')
print(f"   原始记录: {len(teams_df)} 行")
print(f"   原始列数: {len(teams_df.columns)}")

# 只保留需要的列
available_team_cols = [c for c in TEAMS_COLUMNS if c in teams_df.columns]
teams_df = teams_df[available_team_cols]
print(f"   精简后列数: {len(teams_df.columns)}")
print()

# ============================================================
# 第 5 步：合并球员数据（基于名称匹配）
# ============================================================
print("🔗 合并球员数据...")

# 标准化名称
import unicodedata

def normalize_name(name):
    """标准化名称用于匹配"""
    if pd.isna(name):
        return ""
    name_str = str(name)
    # 移除特殊字符并小写
    normalized = unicodedata.normalize('NFKD', name_str)
    ascii_name = normalized.encode('ASCII', 'ignore').decode('ASCII')
    return ascii_name.lower().strip()

# 添加标准化名称列
wcup_df['name_std'] = wcup_df['name'].apply(normalize_name)
players_df['name_std'] = players_df['short_name'].apply(normalize_name)

# 合并
merged_df = wcup_df.merge(
    players_df,
    on='name_std',
    how='left',
    suffixes=('_wcup', '_fifa')
)

print(f"   合并后记录: {len(merged_df)} 行")
print()

# ============================================================
# 第 6 步：保存精简数据集
# ============================================================
print("💾 保存清洗后的数据集...")

# 保存合并后的球员数据
player_output = os.path.join(OUTPUT_DIR, "world_cup_players.csv")
merged_df.to_csv(player_output, index=False, encoding='utf-8')
player_size = os.path.getsize(player_output) / 1024 / 1024
print(f"   ✅ world_cup_players.csv: {player_size:.2f} MB")

# 保存团队数据
teams_output = os.path.join(OUTPUT_DIR, "world_cup_teams.csv")
teams_df.to_csv(teams_output, index=False, encoding='utf-8')
teams_size = os.path.getsize(teams_output) / 1024 / 1024
print(f"   ✅ world_cup_teams.csv: {teams_size:.2f} MB")

# 保存原始世界杯数据
wcup_output = os.path.join(OUTPUT_DIR, "world_cup_squads.csv")
wcup_df.to_csv(wcup_output, index=False, encoding='utf-8')
wcup_size = os.path.getsize(wcup_output) / 1024 / 1024
print(f"   ✅ world_cup_squads.csv: {wcup_size:.2f} MB")

print()

# ============================================================
# 第 7 步：删除原始大文件
# ============================================================
print("🗑️  删除原始大文件...")

# 删除 archive 文件夹
archive_folders = [
    os.path.join(INPUT_DIR, "archive (2)"),
    os.path.join(INPUT_DIR, "archive (3)")
]

for folder in archive_folders:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"   ✅ 删除: {folder}")

print()
print("=" * 60)
print("✅ 完成！")
print("=" * 60)
print()
print("📊 结果:")
print(f"   原始总大小: ~94 MB")
print(f"   精简后大小: ~{player_size + teams_size + wcup_size:.2f} MB")
print(f"   压缩率: {((1 - (player_size + teams_size + wcup_size) / 94) * 100):.1f}%")
print()
print(f"📁 数据保存在: {OUTPUT_DIR}/")
print(f"📁 备份保存在: {BACKUP_DIR}/")
print()
print("📋 生成的文件:")
print("   • world_cup_players.csv - 合并后的球员数据")
print("   • world_cup_teams.csv   - 团队数据")
print("   • world_cup_squads.csv  - 原始阵容数据")
print()