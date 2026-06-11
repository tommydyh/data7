# Git Commands for Streamlit Cloud Fix

## 🚀 Quick Commands

```bash
# 1. Check status
git status

# 2. Add modified file
git add src/data_pipeline.py

# 3. Commit
git commit -m "fix: 修正 Streamlit Cloud 部署路径问题"

# 4. Push
git push origin main
```

---

## 📋 Detailed Steps

### Step 1: Navigate to Project
```bash
cd "d:\cursor data 2"
```

### Step 2: Check What Changed
```bash
git status
```

Expected output:
```
modified: src/data_pipeline.py
```

### Step 3: Review Changes (Optional)
```bash
git diff src/data_pipeline.py
```

### Step 4: Stage the File
```bash
git add src/data_pipeline.py
```

### Step 5: Create Commit
```bash
git commit -m "fix: 修正 Streamlit Cloud 部署路径问题

- 更新 get_data_path() 以正确处理 data/ 子目录
- 修复云端环境下文件路径解析错误

Error: FileNotFoundError on world_cup_squads.csv
Fix: 现在正确返回 data/world_cup_squads.csv"
```

### Step 6: Push to GitHub
```bash
git push origin main
```

---

## 🔄 After Push

Streamlit Cloud will:
- ✅ Detect new commit
- ✅ Auto-redeploy
- ✅ Fix the file not found error

**Deployment time:** ~1-2 minutes

---

## 🔗 Quick Links

- **Your App:** https://course-data-4-xkgwklnkppxuyfm8kkkqrw.streamlit.app/
- **GitHub Repo:** https://github.com/tommydyh/course-data-4
- **Streamlit Cloud:** https://share.streamlit.io

---

## 📝 One-Liner Command

```bash
git add src/data_pipeline.py && git commit -m "fix: 修正 Streamlit Cloud 部署路径问题" && git push origin main
```

---

## ⚡ Or Just Run the Script

**Double-click:** `修复并推送部署.bat`

---

**Push now to fix the deployment!** 🚀