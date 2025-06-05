#!/usr/bin/env python3
"""
PyInstaller 打包脚本
将Python项目打包为Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{description}...")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        print("✅ 成功")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失败: {e}")
        if e.stdout:
            print(f"标准输出: {e.stdout}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False


def check_requirements():
    """检查依赖"""
    print("检查项目依赖...")
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 检查PyQt5
    try:
        import PyQt5
        print(f"✅ PyQt5 已安装")
    except ImportError:
        print("❌ PyQt5 未安装")
        print("请运行: pip install PyQt5")
        return False
    
    # 检查主要文件
    required_files = ['main.py', 'screensaver.py', 'config.json']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 不存在")
            return False
    
    return True


def build_single_file():
    """构建单文件版本"""
    print("🔨 构建单文件版本...")
    
    cmd = [
        "pyinstaller",
        "main.py",
        "--name=screensaver",
        "--onefile", 
        "--windowed",  # 重要：不显示控制台窗口
        "--add-data=config.json;.",
        "--hidden-import=PyQt5.QtMultimedia",
        "--hidden-import=PyQt5.QtMultimediaWidgets",
        "--hidden-import=win32api",
        "--hidden-import=win32gui",
        "--clean"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("✅ 成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def build_directory():
    """构建目录版本"""
    print("🔨 构建目录版本...")
    
    cmd = [
        "pyinstaller", 
        "main.py",
        "--name=screensaver",
        "--onedir",
        "--windowed",  # 重要：不显示控制台窗口
        "--add-data=config.json;.",
        "--hidden-import=PyQt5.QtMultimedia",
        "--hidden-import=PyQt5.QtMultimediaWidgets", 
        "--hidden-import=win32api",
        "--hidden-import=win32gui",
        "--clean"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("✅ 成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def create_release_package():
    """创建发布包"""
    print("\n" + "="*50)
    print("📦 创建发布包")
    print("="*50)
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # 复制文件到发布目录
    dist_dir = Path("dist")
    
    # 复制可执行文件
    exe_file = dist_dir / "screensaver.exe"
    if exe_file.exists():
        shutil.copy(exe_file, release_dir)
        print(f"✅ 复制可执行文件: screensaver.exe")
    
    # 复制配置文件
    shutil.copy("config.json", release_dir)
    print(f"✅ 复制配置文件: config.json")
    
    # 创建示例视频文件说明
    video_readme = release_dir / "视频文件说明.txt"
    with open(video_readme, 'w', encoding='utf-8') as f:
        f.write("视频文件说明\n")
        f.write("=" * 20 + "\n\n")
        f.write("请将您的视频文件重命名为 'video.mp4' 并放在此目录中。\n")
        f.write("或者修改 config.json 文件中的 'video_path' 设置。\n\n")
        f.write("支持的视频格式: MP4, AVI, MKV 等\n")
        f.write("建议使用 MP4 格式以获得最佳兼容性。\n")
    
    print(f"✅ 创建说明文件: {video_readme}")
    
    print(f"\n📁 发布包已创建: {release_dir}")
    return True


def main():
    """主函数"""
    print("🎬 视频屏保程序打包工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_requirements():
        print("\n❌ 依赖检查失败，请先安装必要的依赖")
        return 1
    
    print("\n请选择打包方式:")
    print("1. 单文件版本 (screensaver.exe)")
    print("2. 目录版本 (screensaver 文件夹)")
    print("3. 同时构建两个版本")
    
    try:
        choice = input("\n请输入选项 (1-3): ").strip()
        
        success = False
        
        if choice == "1":
            success = build_single_file()
        elif choice == "2":
            success = build_directory()
        elif choice == "3":
            success = build_single_file()
            if success:
                # 重新构建目录版本前先备份单文件版本
                single_file = Path("dist/screensaver.exe")
                if single_file.exists():
                    backup_file = Path("screensaver_single.exe")
                    shutil.copy(single_file, backup_file)
                    print(f"✅ 单文件版本已备份为: {backup_file}")
                
                success = build_directory()
                
                # 恢复单文件到dist目录
                if backup_file.exists():
                    shutil.copy(backup_file, single_file)
                    backup_file.unlink()
        else:
            print("无效的选项")
            return 1
        
        if success:
            create_release_package()
            print("\n🎉 构建完成！")
            print("\n使用说明:")
            print("1. 将您的视频文件重命名为 'video.mp4'")
            print("2. 运行 screensaver.exe")
            print("3. 按照程序提示操作")
        else:
            print("\n❌ 构建失败")
            return 1
            
    except KeyboardInterrupt:
        print("\n用户取消操作")
        return 1
    except Exception as e:
        print(f"\n❌ 构建出错: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 