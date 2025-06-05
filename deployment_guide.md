# 🚀 视频屏保程序部署指南

本指南将帮助您将exe文件提供给用户下载的多种方法。

## 📋 准备工作

### 1. 生成exe文件
首先，您需要在Windows电脑上生成可执行文件：

```bash
# 在Windows电脑上执行
git clone <您的项目>
cd video-screensaver
pip install -r requirements.txt
python build.py
```

这将生成：
- `dist/screensaver.exe` - 单文件可执行程序
- `视频屏保程序_安装包.zip` - 完整安装包

---

## 🎯 部署方案

### 方案一：GitHub Releases（免费 + 专业）

**优点**: 
- ✅ 完全免费
- ✅ 无限下载量
- ✅ 版本管理
- ✅ 下载统计
- ✅ 专业可信

**步骤**:

1. **创建GitHub仓库**
   ```bash
   # 在GitHub上创建新仓库：video-screensaver
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/video-screensaver.git
   git push -u origin main
   ```

2. **创建Release**
   - 访问: `https://github.com/YOUR_USERNAME/video-screensaver/releases`
   - 点击 "Create a new release"
   - Tag: `v1.0.0`
   - Title: `视频屏保程序 v1.0.0`
   - 上传文件: `screensaver.exe`, `安装包.zip`

3. **分享下载链接**
   ```
   直接下载链接：
   https://github.com/YOUR_USERNAME/video-screensaver/releases/latest/download/screensaver.exe
   
   Release页面：
   https://github.com/YOUR_USERNAME/video-screensaver/releases/latest
   ```

### 方案二：云存储分享（简单快速）

**百度网盘**:
```
1. 上传exe文件到百度网盘
2. 创建分享链接
3. 给用户分享链接 + 提取码
```

**阿里云盘**:
```
1. 上传文件到阿里云盘
2. 生成分享链接
3. 分享给用户
```

**Google Drive / OneDrive**:
```
1. 上传文件
2. 设置为"任何人都可以查看"
3. 获取直接下载链接
```

### 方案三：自建网站托管

**使用免费静态托管**:

1. **Netlify (推荐)**
   ```bash
   # 1. 创建一个包含HTML和exe文件的文件夹
   mkdir website
   cp download.html website/index.html
   cp screensaver.exe website/files/
   
   # 2. 拖拽到 netlify.com 部署
   # 3. 获得免费域名: https://random-name.netlify.app
   ```

2. **GitHub Pages**
   ```bash
   # 1. 创建gh-pages分支
   git checkout -b gh-pages
   git add download.html
   git commit -m "Add download page"
   git push origin gh-pages
   
   # 2. 访问: https://YOUR_USERNAME.github.io/video-screensaver
   ```

3. **Vercel**
   ```bash
   # 连接GitHub仓库到Vercel
   # 自动部署，获得免费域名
   ```

---

## 🔗 下载链接格式

### GitHub Releases
```html
<!-- 最新版本 -->
<a href="https://github.com/用户名/仓库名/releases/latest/download/screensaver.exe">
    下载视频屏保程序
</a>

<!-- 指定版本 -->
<a href="https://github.com/用户名/仓库名/releases/download/v1.0.0/screensaver.exe">
    下载 v1.0.0
</a>
```

### 直接文件链接
```html
<!-- 静态文件托管 -->
<a href="https://your-domain.com/files/screensaver.exe" download>
    下载程序
</a>
```

---

## 📱 推广方式

### 1. 二维码分享
```bash
# 使用在线工具生成下载页面的二维码
# 推荐: qr-code-generator.com
```

### 2. 短链接
```bash
# 使用短链接服务
# GitHub Release: https://git.io/
# 通用短链接: https://tinyurl.com/
```

### 3. 社交媒体分享
```markdown
🎬 我做了一个超酷的视频屏保程序！

✨ 特点：
- 系统空闲时自动播放你的视频
- 全屏播放，支持音效
- 任意操作立即退出
- 完全免费，无广告

📥 下载链接：[下载地址]

#屏保 #个性化 #免费软件
```

---

## 🛡️ 安全考虑

### 1. 文件签名
```bash
# 为exe文件添加数字签名（可选）
# 需要代码签名证书
signtool sign /f certificate.pfx /p password screensaver.exe
```

### 2. 病毒扫描报告
```bash
# 上传到VirusTotal获取扫描报告
# https://www.virustotal.com/gui/home/upload
# 分享扫描结果给用户增加信任
```

### 3. 文件完整性
```bash
# 提供文件哈希值
sha256sum screensaver.exe > screensaver.exe.sha256
```

---

## 📊 下载统计

### GitHub Analytics
- 在GitHub Release页面查看下载次数
- 使用GitHub API获取详细统计

### Google Analytics
```html
<!-- 在下载页面添加 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
  
  // 下载事件跟踪
  function trackDownload(filename) {
    gtag('event', 'download', {
      'file_name': filename,
      'custom_parameter': 'value'
    });
  }
</script>
```

---

## 🎯 推荐方案组合

### 适合个人/小项目
1. **GitHub Releases** (主要)
2. **简单HTML下载页** (美观)
3. **社交媒体分享** (推广)

### 适合商业/正式项目
1. **自建网站** (专业域名)
2. **CDN加速** (下载速度)
3. **数字签名** (安全可信)
4. **用户统计** (数据分析)

---

## 📝 用户使用说明模板

```markdown
# 🎬 视频屏保程序下载使用指南

## 📥 下载
点击这里下载：[下载链接]

## 🚀 使用方法
1. 下载文件到Windows电脑
2. 准备一个MP4视频文件
3. 将视频重命名为 video.mp4
4. 将video.mp4放在程序同一目录
5. 双击运行程序
6. 选择"启动屏保服务"

## 💡 提示
- 默认5分钟无操作后开始播放
- 任意鼠标或键盘操作退出屏保
- 可修改config.json调整设置

## 🔧 系统要求
- Windows 7/8/10/11 (64位)
- 支持MP4格式视频文件

有问题请联系：[您的联系方式]
```

现在您有了完整的部署方案！推荐从GitHub Releases开始，这是最专业且免费的方式。 