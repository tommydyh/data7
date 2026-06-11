# 🔧 Git 连接 GitHub 失败 - 解决方案

## ❌ 问题原因

从日志看，Git 配置了代理但无法连接：

```
Failed to connect to github.com port 443 via 127.0.0.1
Could not resolve proxy: socks5
```

这意味着：
1. Git 试图通过本地代理（127.0.0.1）连接
2. 但代理服务没有运行或配置错误
3. 即使 VPN 开启，代理设置也不匹配

---

## ✅ 解决方案

### 方法 1：取消代理设置（推荐）⭐

**双击运行：`修复Git连接.bat`**

或手动执行：

```bash
# 取消全局代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 测试连接
git ls-remote https://github.com/tommydyh/dongyaohua-sport-task.git HEAD
```

---

### 方法 2：检查并配置正确的代理

如果您确实需要代理，请查看 VPN 设置：

```bash
# 查看当前代理配置
git config --global --get http.proxy
git config --global --get https.proxy

# 设置正确的代理（示例）
git config --global http.proxy socks5://127.0.0.1:7890
git config --global https.proxy socks5://127.0.0.1:7890
```

**注意：** 端口号需要根据您的 VPN 设置修改。

---

### 方法 3：检查 VPN 设置

1. 打开 VPN 客户端
2. 查找"代理设置"或"局域网设置"
3. 检查代理地址和端口
4. 在 Git 中使用相同的配置

---

## 📋 修复步骤

```
1. 运行修复脚本
   ↓
2. 取消代理设置
   ↓
3. 测试连接
   ↓
4. 推送代码到 GitHub
```

---

## 🆘 如果仍然失败

### 检查网络连接

```bash
# 测试 GitHub 连接
ping github.com

# 测试 HTTPS 连接
curl https://github.com
```

### 检查 Git 配置

```bash
# 查看所有配置
git config --global --list

# 查看远程仓库
git remote -v
```

---

## 💡 为什么会出现这个问题？

当您使用 VPN 时，某些 VPN 客户端会自动设置系统代理。Git 会读取这些代理设置，但：

1. 代理服务可能没有运行
2. 代理地址配置错误
3. VPN 的代理模式与 Git 不兼容

**解决方案就是取消 Git 的代理设置**，让 Git 直接通过 VPN 连接。

---

**现在双击 `修复Git连接.bat` 试试！** 🔧