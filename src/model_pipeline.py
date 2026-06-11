"""
Analytical Core: K-Means Clustering & Player Role Mapping
===========================================================
Unsupervised machine learning backend for the Player Performance Dashboard.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Dict, Tuple
import os

# ============================================================
# CONFIGURATION
# ============================================================
OUTPUT_PATH = "final_squad_with_skills.csv"

# Core feature columns for clustering (lowercase to match actual CSV columns)
FEATURE_COLUMNS = ["shooting", "passing", "dribbling", "defending", "physic"]

# Cluster semantic mapping - role definitions based on centroid patterns
ROLE_MAPPING = {
    0: "Clinical Finisher",      # High Shooting, lower Defending
    1: "Midfield Maestro",       # Balanced high Passing/Dribbling
    2: "Defensive Anchor",       # High Defending/Physicality
    3: "Physical Engine"         # High Physicality/Defending
}


class PlayerClusterEngine:
    """
    K-Means clustering engine for player performance segmentation.
    """

    def __init__(self, n_clusters: int = 4, random_state: int = 42, n_init: int = 10):
        """
        Initialize clustering engine.

        Args:
            n_clusters: Number of clusters (default: 4)
            random_state: Random seed for reproducibility
            n_init: Number of K-Means initializations
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.n_init = n_init
        self.scaler = StandardScaler()
        self.kmeans = None
        self.feature_columns = FEATURE_COLUMNS
        self.centroids = None
        self.role_mapping = ROLE_MAPPING

    def load_data(self, filepath: str = None) -> pd.DataFrame:
        """
        Load enriched dataset from ETL pipeline.

        Args:
            filepath: Path to CSV file (uses default if None)

        Returns:
            DataFrame with player data
        """
        if filepath is None:
            filepath = OUTPUT_PATH

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found at: {filepath}")

        df = pd.read_csv(
            filepath,
            encoding='utf-8',
            quotechar='"',
            skipinitialspace=True,
            on_bad_lines='skip',
            engine='python'
        )
        print(f"📂 Loaded dataset: {len(df)} players")

        return df

    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, list]:
        """
        Extract and scale features for clustering.

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (scaled_features_array, player_indices)
        """
        # Extract feature columns
        features = df[self.feature_columns].copy()

        # Remove any rows with missing features
        valid_indices = features.dropna().index
        features_clean = features.loc[valid_indices]

        print(f"🔢 Features extracted: {len(features_clean)} valid players")

        # Scale features to ensure parity for distance-based algorithms
        scaled_features = self.scaler.fit_transform(features_clean)

        print(f"📏 Feature scaling complete: {scaled_features.shape}")

        return scaled_features, valid_indices

    def fit_clusters(self, features: np.ndarray) -> np.ndarray:
        """
        Execute K-Means clustering.

        Args:
            features: Scaled feature array

        Returns:
            Array of cluster labels
        """
        print("🧠 Training K-Means model...")

        # Initialize and fit K-Means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=self.n_init
        )
        labels = self.kmeans.fit_predict(features)

        # Store centroids (unscaled for interpretability)
        self.centroids = self.scaler.inverse_transform(self.kmeans.cluster_centers_)

        # Calculate silhouette score for clustering quality
        silhouette = silhouette_score(features, labels)
        print(f"   ✅ Clustering complete")
        print(f"   📊 Silhouette Score: {silhouette:.3f} (higher is better)")

        return labels

    def analyze_centroids(self) -> Dict[int, str]:
        """
        Analyze cluster centroids to map numeric labels to football roles.

        Returns:
            Dictionary mapping cluster IDs to role names
        """
        print("🎯 Analyzing cluster centroids for role mapping...")

        centroid_df = pd.DataFrame(
            self.centroids,
            columns=self.feature_columns
        )

        # Calculate dominant attribute for each cluster
        dominant_attrs = centroid_df.idxmax(axis=1)

        # Automatic role mapping based on centroid patterns
        role_mapping = {}

        for cluster_id in range(self.n_clusters):
            centroid_row = self.centroids[cluster_id]
            shooting, passing, dribbling, defending, physical = centroid_row

            # Determine role based on attribute distribution
            if shooting > 75 and passing < 65:
                role = "Clinical Finisher"
            elif passing > 75 and dribbling > 70:
                role = "Midfield Maestro"
            elif defending > 75 and physical > 70:
                role = "Defensive Anchor"
            elif physical > 75:
                role = "Physical Engine"
            else:
                # Fallback to pre-defined mapping
                role = self.role_mapping.get(cluster_id, f"Player Type {cluster_id}")

            role_mapping[cluster_id] = role

            print(f"   📍 Cluster {cluster_id} → {role}")
            print(f"      Centroid: Shooting={shooting:.1f}, Passing={passing:.1f}, "
                  f"Dribbling={dribbling:.1f}, Defending={defending:.1f}, Physical={physical:.1f}")

        self.role_mapping = role_mapping

        return role_mapping

    def assign_labels(self, df: pd.DataFrame, valid_indices: list, labels: np.ndarray) -> pd.DataFrame:
        """
        Append cluster labels and role names to the DataFrame.

        Args:
            df: Original DataFrame
            valid_indices: Indices of valid players
            labels: Cluster label array

        Returns:
            DataFrame with added cluster_label and role columns
        """
        print("🏷️  Assigning cluster labels to players...")

        # Initialize columns
        df["cluster_label"] = np.nan
        df["role"] = "Unknown"

        # Assign labels to valid players
        for idx, label in zip(valid_indices, labels):
            df.at[idx, "cluster_label"] = int(label)
            df.at[idx, "role"] = self.role_mapping[label]

        # Count players per role
        role_counts = df["role"].value_counts()
        print(f"   ✅ Labels assigned to {len(valid_indices)} players")
        print(f"   📊 Role distribution:")
        for role, count in role_counts.items():
            print(f"      - {role}: {count} players")

        return df

    def get_similar_players(
        self,
        df: pd.DataFrame,
        player_name: str,
        top_n: int = 3
    ) -> pd.DataFrame:
        """
        Find players with similar playstyle within the same cluster using Euclidean distance.

        Args:
            df: DataFrame with player data
            player_name: Name of reference player
            top_n: Number of similar players to return

        Returns:
            DataFrame of similar players
        """
        # Find the reference player
        player_idx = df[df["name"].str.lower() == player_name.lower()].index

        if len(player_idx) == 0:
            print(f"⚠️  Player '{player_name}' not found")
            return pd.DataFrame()

        player_idx = player_idx[0]
        player_cluster = df.at[player_idx, "cluster_label"]

        if pd.isna(player_cluster):
            print(f"⚠️  Player '{player_name}' has no cluster assignment")
            return pd.DataFrame()

        # Get players in same cluster
        cluster_players = df[df["cluster_label"] == player_cluster].copy()

        # Extract features for all players in cluster
        cluster_features = cluster_players[self.feature_columns].values

        # Get reference player features
        ref_features = df.loc[player_idx, self.feature_columns].values

        # Calculate Euclidean distances
        distances = np.linalg.norm(cluster_features - ref_features, axis=1)

        # Add distances and sort
        cluster_players["distance"] = distances
        cluster_players = cluster_players.sort_values("distance")

        # Remove the reference player and get top_n
        similar = cluster_players[cluster_players["name"] != df.at[player_idx, "name"]].head(top_n)

        return similar[["name", "nationality", "role", "distance"] + self.feature_columns]

    def run_pipeline(self, input_path: str = None, output_path: str = None) -> pd.DataFrame:
        """
        Execute the complete clustering pipeline.

        Args:
            input_path: Path to input CSV (uses default if None)
            output_path: Path to save labeled CSV (optional)

        Returns:
            DataFrame with cluster labels and roles
        """
        print("=" * 60)
        print("🚀 STARTING K-MEANS CLUSTERING PIPELINE")
        print("=" * 60)

        # Load data
        df = self.load_data(input_path)

        # Prepare features
        features, valid_indices = self.prepare_features(df)

        # Fit clusters
        labels = self.fit_clusters(features)

        # Analyze centroids for role mapping
        self.analyze_centroids()

        # Assign labels to DataFrame
        labeled_df = self.assign_labels(df, valid_indices, labels)

        # Export if path provided
        if output_path:
            labeled_df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"💾 Labeled dataset exported to: {output_path}")

        print("=" * 60)
        print("✅ CLUSTERING PIPELINE COMPLETED")
        print("=" * 60)

        return labeled_df


def calculate_kpis(df: pd.DataFrame) -> Dict:
    """
    Calculate key performance indicators for the dashboard.

    Args:
        df: Labeled DataFrame with player data

    Returns:
        Dictionary of KPI values
    """
    kpis = {
        "total_players": len(df),
        "avg_age": df.get("age", pd.Series([0])).mean(),
        "max_value": df.get("value", pd.Series([0])).max(),
        "top_team": df.get("nationality", pd.Series(["Unknown"])).mode()[0]
    }

    return kpis


if __name__ == "__main__":
    # Run clustering pipeline
    engine = PlayerClusterEngine()
    labeled_df = engine.run_pipeline()

    # Calculate KPIs
    kpis = calculate_kpis(labeled_df)
    print("\n📊 Dashboard KPIs:")
    for key, value in kpis.items():
        print(f"   {key}: {value}")

    # Display sample
    print("\n📋 Sample labeled players:")
    cols = ["name", "nationality", "position", "role", "cluster_label"]
    available_cols = [c for c in cols if c in labeled_df.columns]
    print(labeled_df[available_cols].head(10))