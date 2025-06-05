# 🖥️ Windows电脑上的构建指令

当您在Windows电脑上时，请按以下步骤生成exe文件：

## 📋 准备工作

1. **下载项目代码**：
   - 从GitHub仓库下载ZIP文件
   - 或使用GitHub Desktop克隆到本地

2. **安装Python**（如果还没有）：
   - 访问 https://python.org
   - 下载Python 3.9或更新版本
   - 安装时勾选"Add Python to PATH"

## 🔨 构建步骤

```bash
# 1. 打开命令提示符(CMD)或PowerShell
# 2. 切换到项目目录
cd C:\path\to\video-screensaver

# 3. 安装依赖
pip install -r requirements.txt

# 4. 构建可执行文件
python build.py

# 5. 创建安装包
python create_installer.py
```

## 📦 生成的文件

构建完成后会得到：
- `dist/screensaver.exe` - 单文件可执行程序
- `视频屏保程序_安装包.zip` - 完整安装包

## 📤 上传到GitHub Release

1. 打开您的GitHub仓库
2. 进入Releases页面
3. 编辑v1.0.0 Release
4. 上传生成的exe和zip文件
5. 发布Release

## 🎉 完成！

用户现在可以直接下载您的exe文件了！

下载链接格式：
```
https://github.com/您的用户名/video-screensaver/releases/latest/download/screensaver.exe
``` 