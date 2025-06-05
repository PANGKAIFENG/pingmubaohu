#!/usr/bin/env python3
"""
创建Windows安装包脚本
为视频屏保程序创建用户友好的安装包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def create_nsis_script():
    """创建NSIS安装脚本"""
    nsis_script = """
; 视频屏保程序安装脚本
; 使用 NSIS (Nullsoft Scriptable Install System) 创建

!define APP_NAME "视频屏保程序"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "您的名称"
!define APP_EXE "screensaver.exe"
!define APP_DIR "VideoScreensaver"

; 包含现代UI
!include "MUI2.nsh"

; 设置压缩
SetCompressor /SOLID lzma

; 安装包基本信息
Name "${APP_NAME}"
OutFile "VideoScreensaver_Setup.exe"
InstallDir "$PROGRAMFILES\\${APP_DIR}"
InstallDirRegKey HKLM "Software\\${APP_DIR}" "InstallPath"
RequestExecutionLevel admin

; 界面设置
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"  ; 如果有图标的话
!define MUI_UNICON "icon.ico"

; 安装页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; 卸载页面
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; 语言
!insertmacro MUI_LANGUAGE "SimpChinese"

; 安装段
Section "主程序" SecMain
    SetOutPath "$INSTDIR"
    
    ; 复制文件
    File "screensaver.exe"
    File "config.json"
    File "README.txt"
    
    ; 创建开始菜单快捷方式
    CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\卸载.lnk" "$INSTDIR\\uninstall.exe"
    
    ; 创建桌面快捷方式（可选）
    CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
    
    ; 写入注册表信息
    WriteRegStr HKLM "Software\\${APP_DIR}" "InstallPath" "$INSTDIR"
    WriteRegStr HKLM "Software\\${APP_DIR}" "Version" "${APP_VERSION}"
    
    ; 创建卸载程序
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    ; 添加到控制面板程序列表
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWord HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}" "NoModify" 1
    WriteRegDWord HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}" "NoRepair" 1
SectionEnd

; 开机启动选项（可选）
Section /o "开机启动" SecStartup
    CreateShortCut "$SMSTARTUP\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}" "--daemon"
SectionEnd

; 卸载段
Section "Uninstall"
    ; 删除程序文件
    Delete "$INSTDIR\\screensaver.exe"
    Delete "$INSTDIR\\config.json"
    Delete "$INSTDIR\\README.txt"
    Delete "$INSTDIR\\uninstall.exe"
    
    ; 删除快捷方式
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\卸载.lnk"
    RMDir "$SMPROGRAMS\\${APP_NAME}"
    Delete "$DESKTOP\\${APP_NAME}.lnk"
    Delete "$SMSTARTUP\\${APP_NAME}.lnk"
    
    ; 删除安装目录
    RMDir "$INSTDIR"
    
    ; 删除注册表项
    DeleteRegKey HKLM "Software\\${APP_DIR}"
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_DIR}"
SectionEnd

; 段描述
LangString DESC_SecMain ${LANG_SIMPCHINESE} "安装主程序文件"
LangString DESC_SecStartup ${LANG_SIMPCHINESE} "开机自动启动屏保服务"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
!insertmacro MUI_DESCRIPTION_TEXT ${SecStartup} $(DESC_SecStartup)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
"""
    
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    print("✅ NSIS安装脚本已创建: installer.nsi")


def create_license_file():
    """创建许可证文件"""
    license_text = """视频屏保程序 许可协议

版权所有 (c) 2024

特此免费授予任何获得本软件副本和相关文档文件（"软件"）的人不受限制地处理
软件的权利，包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或出售
软件副本的权利，以及允许接受软件的人员这样做，但须符合以下条件：

上述版权声明和本许可声明应包含在软件的所有副本或重要部分中。

软件按"原样"提供，不提供任何形式的明示或暗示保证，包括但不限于对适销性、
特定用途适用性和非侵权性的保证。在任何情况下，作者或版权持有人均不对任何
索赔、损害或其他责任负责，无论是在合同行为、侵权行为或其他方面，由软件或
软件的使用或其他交易引起或与之相关。
"""
    
    with open("LICENSE.txt", "w", encoding="utf-8") as f:
        f.write(license_text)
    
    print("✅ 许可证文件已创建: LICENSE.txt")


def create_readme_file():
    """创建用户说明文件"""
    readme_text = """🎬 视频屏保程序 - 使用说明

欢迎使用视频屏保程序！

🚀 快速开始
===========

1. 准备视频文件
   - 将您的MP4视频文件重命名为 "video.mp4"
   - 放在程序安装目录中

2. 运行程序
   - 双击桌面上的"视频屏保程序"图标
   - 选择"1. 启动屏保服务"

3. 配置设置（可选）
   - 编辑 config.json 文件修改设置
   - video_path: 视频文件路径
   - idle_minutes: 空闲触发时间（分钟）

⚙️ 主要功能
============

✅ 系统空闲时自动播放视频
✅ 全屏播放，循环播放
✅ 支持音频播放
✅ 任意操作立即退出
✅ 可配置空闲时间
✅ 支持开机启动

📞 技术支持
============

如果遇到问题：
1. 确认视频文件为MP4格式
2. 检查config.json配置是否正确
3. 以管理员权限运行程序

享受您的个性化屏保体验！
"""
    
    with open("README.txt", "w", encoding="utf-8") as f:
        f.write(readme_text)
    
    print("✅ 用户说明文件已创建: README.txt")


def create_batch_installer():
    """创建批处理安装脚本（简单版本）"""
    batch_script = """@echo off
chcp 65001 >nul
echo ========================================
echo     视频屏保程序 简易安装器
echo ========================================
echo.

set "INSTALL_DIR=%ProgramFiles%\\VideoScreensaver"
set "START_MENU=%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs"

echo 正在创建安装目录...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 正在复制程序文件...
copy "screensaver.exe" "%INSTALL_DIR%\\" >nul
copy "config.json" "%INSTALL_DIR%\\" >nul
copy "README.txt" "%INSTALL_DIR%\\" >nul

echo 正在创建开始菜单快捷方式...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\\视频屏保程序.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\screensaver.exe'; $Shortcut.Save()"

echo 正在创建桌面快捷方式...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\视频屏保程序.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\screensaver.exe'; $Shortcut.Save()"

echo.
echo ✅ 安装完成！
echo.
echo 您可以：
echo 1. 从桌面快捷方式启动程序
echo 2. 从开始菜单找到"视频屏保程序"
echo 3. 将您的MP4视频文件重命名为video.mp4并放入：
echo    %INSTALL_DIR%
echo.
pause
"""
    
    with open("install.bat", "w", encoding="gbk") as f:
        f.write(batch_script)
    
    print("✅ 批处理安装脚本已创建: install.bat")


def create_portable_package():
    """创建便携版打包"""
    portable_dir = Path("VideoScreensaver_Portable")
    
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir()
    
    # 复制必要文件
    files_to_copy = [
        "screensaver.exe",
        "config.json", 
        "README.txt"
    ]
    
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy(file_name, portable_dir)
    
    # 创建启动脚本
    start_script = """@echo off
chcp 65001 >nul
echo 🎬 视频屏保程序 - 便携版
echo.
echo 请确保video.mp4文件在当前目录中
echo 按任意键启动程序...
pause >nul
start screensaver.exe
"""
    
    with open(portable_dir / "启动程序.bat", "w", encoding="gbk") as f:
        f.write(start_script)
    
    print(f"✅ 便携版已创建: {portable_dir}")
    return portable_dir


def main():
    """主函数"""
    print("🎬 视频屏保程序 - 安装包制作工具")
    print("=" * 50)
    
    # 检查是否有编译好的exe文件
    if not Path("screensaver.exe").exists():
        print("❌ 未找到 screensaver.exe 文件")
        print("请先运行 python build.py 来构建可执行文件")
        return 1
    
    print("请选择要创建的安装包类型:")
    print("1. NSIS安装包（推荐，需要安装NSIS）")
    print("2. 批处理安装脚本（简单，无需额外软件）")
    print("3. 便携版压缩包（免安装）")
    print("4. 创建所有类型")
    
    try:
        choice = input("\n请输入选项 (1-4): ").strip()
        
        # 创建必要的文件
        create_license_file()
        create_readme_file()
        
        if choice == "1":
            create_nsis_script()
            print("\n📋 后续步骤:")
            print("1. 安装 NSIS (https://nsis.sourceforge.io/)")
            print("2. 右键点击 installer.nsi -> Compile NSIS Script")
            print("3. 生成 VideoScreensaver_Setup.exe 安装包")
            
        elif choice == "2":
            create_batch_installer()
            print("\n📋 使用方法:")
            print("1. 将 install.bat 和程序文件放在同一目录")
            print("2. 以管理员权限运行 install.bat")
            
        elif choice == "3":
            portable_dir = create_portable_package()
            print(f"\n📋 使用方法:")
            print(f"1. 将 {portable_dir} 文件夹压缩成ZIP")
            print("2. 用户解压后直接运行'启动程序.bat'")
            
        elif choice == "4":
            create_nsis_script()
            create_batch_installer() 
            portable_dir = create_portable_package()
            print("\n✅ 所有安装包类型已创建！")
            
        else:
            print("无效的选项")
            return 1
        
        print("\n🎉 安装包制作完成！")
        print("\n💡 提醒用户:")
        print("- 将video.mp4文件放在程序目录")
        print("- 可以修改config.json调整设置")
        print("- 程序需要在Windows系统上运行")
        
    except KeyboardInterrupt:
        print("\n用户取消操作")
        return 1
    except Exception as e:
        print(f"\n❌ 创建安装包时出错: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 