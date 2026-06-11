import pandas as pd
from src.data_pipeline import SKILL_COLUMNS, get_data_path

print('Testing column configuration...')
print()
print('SKILL_COLUMNS:', SKILL_COLUMNS)
print()

# Test loading with actual columns
try:
    df = pd.read_csv('data/world_cup_players.csv', nrows=5, encoding='utf-8', quotechar='"', skipinitialspace=True, on_bad_lines='skip', engine='python')
    print('Actual columns in CSV:')
    print([col for col in df.columns if col in SKILL_COLUMNS])
    print()

    missing = [col for col in SKILL_COLUMNS if col not in df.columns]
    if missing:
        print('Missing columns:', missing)
    else:
        print('All skill columns exist!')
except Exception as e:
    print('Error:', e)