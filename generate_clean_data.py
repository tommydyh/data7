"""Generate clean processed data files using backup data."""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("Loading source data...")

# Load squad data
squad_df = pd.read_csv(
    'data/world_cup_squads.csv',
    encoding='utf-8'
)

# Load FIFA players from backup (cleaner data)
players_df = pd.read_csv(
    'archive_backup/male_players.csv',
    encoding='utf-8'
)

# Extract position from player_positions column (first position)
if 'player_positions' in players_df.columns:
    players_df['club_position'] = players_df['player_positions'].apply(
        lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Unknown'
    )

print(f"Squad data: {len(squad_df)} records")
print(f"FIFA players: {len(players_df)} records")

# Simple name matching
def normalize_name(name):
    if pd.isna(name):
        return ""
    return str(name).lower().strip()

squad_df['name_std'] = squad_df['name'].apply(normalize_name)
players_df['name_std'] = players_df['short_name'].apply(normalize_name)

# Select only key FIFA columns
fifa_cols = ['short_name', 'long_name', 'overall', 'potential', 'pace', 'shooting',
             'passing', 'dribbling', 'defending', 'physic', 'club_name', 'nationality_name', 'club_position']
available_fifa_cols = [c for c in fifa_cols if c in players_df.columns]
players_df = players_df[available_fifa_cols + ['name_std']]

print(f"Selected FIFA columns: {available_fifa_cols}")

# Merge data
merged = squad_df.merge(
    players_df,
    on='name_std',
    how='left',
    suffixes=('_squad', '_fifa')
)

print(f"Merged: {len(merged)} records")

# Select key columns
skill_cols = ['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
output_cols = ['name', 'team_name', 'group', 'appearances', 'goals', 'assists', 'minutes', 'club_position']

# Add nationality from FIFA data if available
if 'nationality_name' in merged.columns:
    # Rename nationality_name to nationality for consistency with app
    processed_df = merged[output_cols + skill_cols + ['nationality_name']].copy()
    processed_df = processed_df.rename(columns={'nationality_name': 'nationality'})
else:
    processed_df = merged[output_cols + skill_cols].copy()
    processed_df['nationality'] = 'Unknown'  # Fallback

available_skill_cols = [c for c in skill_cols if c in processed_df.columns]
final_cols = output_cols + available_skill_cols + ['nationality']

# Fill missing skill values with column means
for col in available_skill_cols:
    # Convert to numeric, coercing errors to NaN
    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
    if processed_df[col].isna().any():
        mean_val = processed_df[col].mean()
        if pd.notna(mean_val):
            processed_df[col] = processed_df[col].fillna(mean_val)

print(f"Skill columns processed: {available_skill_cols}")

# Save processed data
processed_df.to_csv('final_squad_with_skills.csv', index=False, encoding='utf-8')
print(f"Saved final_squad_with_skills.csv: {len(processed_df)} records")

# Simple clustering
feature_cols = ['shooting', 'passing', 'dribbling', 'defending', 'physic']
available_features = [c for c in feature_cols if c in processed_df.columns]

features = processed_df[available_features].copy()

# Remove rows with all NaN features
valid_rows = ~features.isna().all(axis=1)
features = features[valid_rows]
valid_indices = features.index

print(f"Valid players for clustering: {len(valid_indices)}")

if len(valid_indices) > 10:  # Need at least 10 players for clustering
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled_features)

    # Add cluster labels
    processed_df['cluster_label'] = np.nan
    processed_df.loc[valid_indices, 'cluster_label'] = labels

    # Simple role mapping based on cluster characteristics
    processed_df['role'] = "Unknown"
    for cluster_id in range(4):
        cluster_players = processed_df[processed_df['cluster_label'] == cluster_id]
        if len(cluster_players) > 0:
            # Calculate cluster averages
            avg_shooting = cluster_players['shooting'].mean()
            avg_passing = cluster_players['passing'].mean()
            avg_defending = cluster_players['defending'].mean()
            avg_physic = cluster_players['physic'].mean()

            # Assign role based on characteristics
            if avg_shooting > avg_passing and avg_shooting > avg_defending:
                role = "Clinical Finisher"
            elif avg_passing > avg_shooting and avg_passing > avg_defending:
                role = "Midfield Maestro"
            elif avg_defending > avg_shooting and avg_defending > avg_passing:
                role = "Defensive Anchor"
            else:
                role = "Physical Engine"

            processed_df.loc[processed_df['cluster_label'] == cluster_id, 'role'] = role

            print(f"Cluster {cluster_id} ({role}): {len(cluster_players)} players - "
                  f"S:{avg_shooting:.1f}, P:{avg_passing:.1f}, D:{avg_defending:.1f}, Ph:{avg_physic:.1f}")

else:
    processed_df['cluster_label'] = 0
    processed_df['role'] = "Unknown"
    print("Not enough players for clustering")

# Save labeled data
processed_df.to_csv('final_squad_labeled.csv', index=False, encoding='utf-8')
print(f"Saved final_squad_labeled.csv: {len(processed_df)} records")

# Verify data quality
print("\nData quality check:")
print(f"Skill ranges (should be 0-100):")
for col in ['shooting', 'passing', 'dribbling', 'defending', 'physic']:
    if col in processed_df.columns:
        print(f"  {col}: {processed_df[col].min():.1f} - {processed_df[col].max():.1f}")

print("\nRole distribution:")
print(processed_df['role'].value_counts())

print("\nSample data:")
print(processed_df[['name', 'team_name', 'overall', 'shooting', 'passing', 'defending', 'role']].head(10))

print("\nData generation complete!")