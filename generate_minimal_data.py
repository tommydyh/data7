"""Generate minimal processed data files for deployment."""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("Loading source data...")

# Load squad data
squad_df = pd.read_csv(
    'data/world_cup_squads.csv',
    encoding='utf-8',
    quotechar='"',
    skipinitialspace=True,
    on_bad_lines='skip',
    engine='python'
)

# Load players data
players_df = pd.read_csv(
    'data/world_cup_players.csv',
    encoding='utf-8',
    quotechar='"',
    skipinitialspace=True,
    on_bad_lines='skip',
    engine='python'
)

print(f"Squad data: {len(squad_df)} records")
print(f"Players data: {len(players_df)} records")

# Simple name matching (case-insensitive)
def normalize_name(name):
    if pd.isna(name):
        return ""
    return str(name).lower().strip()

squad_df['name_std'] = squad_df['name'].apply(normalize_name)
players_df['name_std'] = players_df['short_name'].apply(normalize_name)

# Merge data
merged = squad_df.merge(
    players_df,
    on='name_std',
    how='left',
    suffixes=('_squad', '_fifa')
)

print(f"Merged: {len(merged)} records")
print(f"Merged columns: {list(merged.columns)[:20]}...")

# Select key columns
skill_cols = ['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
output_cols = ['name', 'team_name', 'group', 'appearances', 'goals', 'assists', 'minutes']

# Add nationality if available (it might have different name after merge)
if 'nationality' in merged.columns:
    output_cols.append('nationality')
elif 'nationality_squad' in merged.columns:
    output_cols.append('nationality_squad')
elif 'nation' in merged.columns:
    output_cols.append('nation')

available_skill_cols = [c for c in skill_cols if c in merged.columns]
available_output_cols = [c for c in output_cols if c in merged.columns]
final_cols = available_output_cols + available_skill_cols

# Create processed dataframe
processed_df = merged[final_cols].copy()

# Fill missing skill values with column means
for col in available_skill_cols:
    # Convert to numeric, coercing errors to NaN
    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
    if processed_df[col].isna().any():
        mean_val = processed_df[col].mean()
        if pd.notna(mean_val):
            processed_df[col] = processed_df[col].fillna(mean_val)

# Save processed data
processed_df.to_csv('final_squad_with_skills.csv', index=False, encoding='utf-8')
print(f"Saved final_squad_with_skills.csv: {len(processed_df)} records")

# Simple clustering
feature_cols = ['shooting', 'passing', 'dribbling', 'defending', 'physic']
available_features = [c for c in feature_cols if c in processed_df.columns]

features = processed_df[available_features].copy()

# Remove rows with all NaN features
features = features.dropna(how='all')
valid_indices = features.index

if len(valid_indices) > 0:
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features.loc[valid_indices])

    # K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled_features)

    # Add cluster labels
    processed_df['cluster_label'] = np.nan
    processed_df.loc[valid_indices, 'cluster_label'] = labels

    # Role mapping
    role_mapping = {
        0: "Clinical Finisher",
        1: "Midfield Maestro",
        2: "Defensive Anchor",
        3: "Physical Engine"
    }

    processed_df['role'] = "Unknown"
    for idx in valid_indices:
        cluster = processed_df.at[idx, 'cluster_label']
        if pd.notna(cluster):
            processed_df.at[idx, 'role'] = role_mapping.get(int(cluster), "Unknown")

    print(f"Clustering completed: {len(valid_indices)} players clustered")
else:
    processed_df['cluster_label'] = 0
    processed_df['role'] = "Unknown"
    print("No valid features for clustering")

# Save labeled data
processed_df.to_csv('final_squad_labeled.csv', index=False, encoding='utf-8')
print(f"Saved final_squad_labeled.csv: {len(processed_df)} records")
print("Data generation complete!")