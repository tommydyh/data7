import pandas as pd
from src.data_pipeline import SKILL_COLUMNS
from src.model_pipeline import FEATURE_COLUMNS

print('Column Configuration Check:')
print('=' * 60)
print()
print('SKILL_COLUMNS (data_pipeline.py):')
print(SKILL_COLUMNS)
print()
print('FEATURE_COLUMNS (model_pipeline.py):')
print(FEATURE_COLUMNS)
print()

# Verify all columns exist in CSV
df = pd.read_csv('data/world_cup_players.csv', nrows=1, encoding='utf-8', quotechar='"', skipinitialspace=True, on_bad_lines='skip', engine='python')
print('All CSV columns:')
for i, col in enumerate(df.columns):
    print(f'  {i}: {col}')
print()

missing_skills = [col for col in SKILL_COLUMNS if col not in df.columns]
missing_features = [col for col in FEATURE_COLUMNS if col not in df.columns]

if missing_skills:
    print('[FAIL] Missing SKILL_COLUMNS:', missing_skills)
else:
    print('[OK] All SKILL_COLUMNS exist in CSV')

if missing_features:
    print('[FAIL] Missing FEATURE_COLUMNS:', missing_features)
else:
    print('[OK] All FEATURE_COLUMNS exist in CSV')

print()
print('Test complete!')