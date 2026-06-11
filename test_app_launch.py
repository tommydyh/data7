import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('Testing Application Launch...')
print('=' * 60)
print()

try:
    import streamlit as st
    print('[OK] streamlit imported')
except ImportError as e:
    print(f'[FAIL] streamlit: {e}')
    sys.exit(1)

try:
    import pandas as pd
    print('[OK] pandas imported')
except ImportError as e:
    print(f'[FAIL] pandas: {e}')
    sys.exit(1)

try:
    import plotly
    print('[OK] plotly imported')
except ImportError as e:
    print(f'[FAIL] plotly: {e}')
    sys.exit(1)

try:
    import sklearn
    print('[OK] sklearn imported')
except ImportError as e:
    print(f'[FAIL] sklearn: {e}')
    sys.exit(1)

try:
    from src.data_pipeline import SKILL_COLUMNS, run_pipeline
    print('[OK] src.data_pipeline imported')
    print(f'      SKILL_COLUMNS: {SKILL_COLUMNS}')
except Exception as e:
    print(f'[FAIL] src.data_pipeline: {e}')
    sys.exit(1)

try:
    from src.model_pipeline import FEATURE_COLUMNS, PlayerClusterEngine
    print('[OK] src.model_pipeline imported')
    print(f'      FEATURE_COLUMNS: {FEATURE_COLUMNS}')
except Exception as e:
    print(f'[FAIL] src.model_pipeline: {e}')
    sys.exit(1)

try:
    import app
    print('[OK] app module imported')
except Exception as e:
    print(f'[FAIL] app module: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print('=' * 60)
print('[SUCCESS] All imports successful!')
print('=' * 60)
print()
print('Next step:')
print('  Run: streamlit run app.py')
print('  Or: D:\\python\\python.exe -m streamlit run app.py')
print()