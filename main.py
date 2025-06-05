#!/usr/bin/env python3
"""
视频屏保程序 - 主入口
作者: AI Assistant
版本: 1.0.0
"""

import sys
import os

# 确保能够导入其他模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from screensaver import main

if __name__ == "__main__":
    # 启动主程序
    sys.exit(main()) 