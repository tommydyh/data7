"""
ETL & Data Pipeline for 2026 World Cup Scouter
================================================
Handles loading, cleaning, merging, and feature engineering of FIFA datasets.
"""

import pandas as pd
import numpy as np
import unicodedata
import os
from typing import Tuple

# ============================================================
# CONFIGURATION
# ============================================================

def get_data_path(filename: str) -> str:
    """
    Get data file path, handling both local and cloud environments.
    Files are located in the 'data/' subdirectory.
    """
    # Check if running in Streamlit Cloud
    if os.getenv('STREAMLIT_SHARING_MODE'):
        # Cloud environment - files are in the data/ subdirectory
        return os.path.join("data", filename)

    # Local environment - try multiple possible locations
    base_paths = [
        os.getcwd(),
        os.path.dirname(__file__),
        os.path.join(os.path.dirname(__file__), "..")
    ]

    for base_path in base_paths:
        # Try with data/ prefix
        full_path = os.path.join(base_path, "data", filename)
        if os.path.exists(full_path):
            return full_path

        # Try without data/ prefix (backward compatibility)
        full_path = os.path.join(base_path, filename)
        if os.path.exists(full_path):
            return full_path

    # Default to data/filename.csv
    return os.path.join("data", filename)


# Data file paths
SQUADS_PATH = get_data_path("world_cup_squads.csv")
PLAYERS_PATH = get_data_path("world_cup_players.csv")
TEAMS_PATH = get_data_path("world_cup_teams.csv")
OUTPUT_PATH = "final_squad_with_skills.csv"

# Core feature columns for analysis (lowercase to match actual CSV columns)
SKILL_COLUMNS = ["overall", "pace", "shooting", "passing", "dribbling", "defending", "physic"]


def standardize_name(name: str) -> str:
    """
    Normalize player names for improved matching:
    - Convert to lowercase
    - Strip whitespace
    - Remove diacritics/accents (e.g., Müller -> Muller)

    Args:
        name: Raw player name string

    Returns:
        Standardized name string
    """
    if pd.isna(name):
        return ""
    # Convert to ASCII, removing diacritics
    normalized = unicodedata.normalize('NFKD', str(name))
    ascii_name = normalized.encode('ASCII', 'ignore').decode('ASCII')
    return ascii_name.lower().strip()


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and inspect the source datasets.

    Returns:
        Tuple of (squad_df, players_df) DataFrames
    """
    print("📂 Loading source datasets...")

    # Load 2026 World Cup Squad Dataset
    squad_df = pd.read_csv(
        SQUADS_PATH,
        encoding='utf-8',
        quotechar='"',
        skipinitialspace=True,
        on_bad_lines='skip',
        engine='python'
    )
    print(f"   ✅ Squads loaded: {len(squad_df)} records")
    print(f"   📋 Columns: {list(squad_df.columns)}")

    # Load FIFA 24 Player Stats Dataset
    players_df = pd.read_csv(
        PLAYERS_PATH,
        encoding='utf-8',
        quotechar='"',
        skipinitialspace=True,
        on_bad_lines='skip',
        engine='python'
    )
    print(f"   ✅ Players loaded: {len(players_df)} records")
    print(f"   📋 Key columns: {[c for c in players_df.columns if c in SKILL_COLUMNS + ['short_name', 'club_name']]}")

    return squad_df, players_df


def standardize_and_join(
    squad_df: pd.DataFrame,
    players_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Apply name standardization and perform relational left join.
    Preserves complete World Cup roster while appending FIFA 24 attributes.

    Args:
        squad_df: World Cup squad DataFrame
        players_df: FIFA 24 player stats DataFrame

    Returns:
        Merged DataFrame with standardized names
    """
    print("🔄 Standardizing names and joining datasets...")

    # Create standardized name columns
    squad_df["name_std"] = squad_df["name"].apply(standardize_name)
    players_df["name_std"] = players_df["short_name"].apply(standardize_name)

    # Count original matches
    original_matches = squad_df["name_std"].isin(players_df["name_std"]).sum()
    print(f"   🔍 Direct name matches: {original_matches}/{len(squad_df)}")

    # Perform left join on standardized names
    merged_df = squad_df.merge(
        players_df,
        on="name_std",
        how="left",
        suffixes=("_squad", "_fifa")
    )

    # Keep squad priority columns, add FIFA skill columns
    print(f"   ✅ Merged dataset: {len(merged_df)} records")

    return merged_df


def positional_mean_imputation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply Positional Mean Imputation for missing skill metrics.
    Fills missing values with the average of that position in FIFA 24.

    Args:
        df: Merged DataFrame with potential missing values

    Returns:
        DataFrame with imputed values
    """
    print("🧮 Applying positional mean imputation...")

    # Determine position column (try various possible names)
    position_col = None
    for col in ["position_squad", "Position", "position", "club_position", "Best Position"]:
        if col in df.columns:
            position_col = col
            break

    if position_col is None:
        print("   ⚠️  No position column found, using global mean...")
        for col in SKILL_COLUMNS:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mean())
        return df

    # Count missing values before imputation
    missing_before = df[SKILL_COLUMNS].isna().sum().sum()
    print(f"   📊 Missing values before: {missing_before}")

    # Apply positional mean imputation
    for col in SKILL_COLUMNS:
        if col in df.columns:
            # Calculate position-specific means
            position_means = df.groupby(position_col)[col].transform('mean')
            # Fill missing with position mean, then global mean if still missing
            df[col] = df[col].fillna(position_means).fillna(df[col].mean())

    # Count missing values after imputation
    missing_after = df[SKILL_COLUMNS].isna().sum().sum()
    print(f"   ✅ Missing values after: {missing_after}")
    print(f"   📈 Imputed: {missing_before - missing_after} values")

    return df


def export_enriched_dataset(df: pd.DataFrame) -> str:
    """
    Serialize the fully enriched dataframe to CSV.

    Args:
        df: Enriched DataFrame with all features

    Returns:
        Path to exported CSV file
    """
    print("💾 Exporting enriched dataset...")

    # Select relevant columns for final output
    output_columns = []

    # Priority: squad columns first, then FIFA skills
    for col in df.columns:
        if not col.endswith("_fifa") or col.replace("_fifa", "") in SKILL_COLUMNS:
            output_columns.append(col)

    # Ensure core columns are present
    final_df = df[output_columns]

    # Export to CSV
    final_df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    print(f"   ✅ Exported to: {OUTPUT_PATH}")
    print(f"   📊 Final shape: {final_df.shape}")

    return OUTPUT_PATH


def run_pipeline() -> pd.DataFrame:
    """
    Execute the complete ETL pipeline.

    Returns:
        Fully enriched DataFrame ready for analysis
    """
    print("=" * 60)
    print("🚀 STARTING ETL PIPELINE")
    print("=" * 60)

    # Load datasets
    squad_df, players_df = load_datasets()

    # Standardize and join
    merged_df = standardize_and_join(squad_df, players_df)

    # Impute missing values
    enriched_df = positional_mean_imputation(merged_df)

    # Export
    export_path = export_enriched_dataset(enriched_df)

    print("=" * 60)
    print("✅ ETL PIPELINE COMPLETED")
    print("=" * 60)

    return enriched_df


if __name__ == "__main__":
    # Run pipeline on execution
    final_df = run_pipeline()

    # Display sample
    print("\n📋 Sample records:")
    sample_cols = ["name", "nationality", "position"] + [c for c in SKILL_COLUMNS if c in final_df.columns]
    available_cols = [c for c in sample_cols if c in final_df.columns]
    print(final_df[available_cols].head(10))