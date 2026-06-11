"""
Test CSV loading with hardened configurations
"""

import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("CSV Loading Test - Hardened Configurations")
print("=" * 60)
print()

data_files = [
    "data/world_cup_players.csv",
    "data/world_cup_teams.csv",
    "data/world_cup_squads.csv"
]

all_success = True

for file in data_files:
    print(f"Testing: {file}")
    print("-" * 60)

    try:
        df = pd.read_csv(
            file,
            encoding='utf-8',
            quotechar='"',
            skipinitialspace=True,
            on_bad_lines='skip',
            engine='python'
        )

        print(f"   ✅ Success!")
        print(f"   📊 Rows: {len(df)}")
        print(f"   📋 Columns: {len(df.columns)}")
        print(f"   🔤 Columns: {list(df.columns)[:5]}...")

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        all_success = False

    print()

print("=" * 60)
if all_success:
    print("All CSV files loaded successfully!")
else:
    print("Some files failed to load!")
print("=" * 60)
print()

if all_success:
    print("Next step:")
    print("   Run: streamlit run app.py")
    print("   Or: D:\\python\\python.exe -m streamlit run app.py")
    print()
else:
    print("Please check the errors above.")
    print()