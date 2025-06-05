#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
屏保主控制器
整合配置管理、系统监听和视频播放功能
"""

import os
import sys
import threading
import time
from typing import Optional

from config_manager import ConfigManager
from system_monitor import SystemMonitor
from video_player import VideoPlayer


class VideoScreensaver:
    """视频屏保主控制器"""
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager or ConfigManager()
        self.system_monitor = SystemMonitor()
        self.video_player = None
        self.monitoring = False
        self.monitor_thread = None
        
        print("📱 视频屏保程序初始化完成")
        
    def start_monitoring(self):
        """开始监控系统空闲状态"""
        if self.monitoring:
            return
            
        self.monitoring = True
        print("🔍 开始监控系统空闲状态...")
        
        config = self.config_manager.get_config()
        idle_time_minutes = config.get('idle_time_minutes', 5)
        idle_time_seconds = config.get('idle_time_seconds', 0)
        total_idle_seconds = idle_time_minutes * 60 + idle_time_seconds
        
        print(f"⏱️ 空闲触发时间: {idle_time_minutes}分{idle_time_seconds}秒 (总计{total_idle_seconds}秒)")
        
        while self.monitoring:
            try:
                idle_time = self.system_monitor.get_idle_time()
                
                if idle_time >= total_idle_seconds:
                    if not self.video_player or not self.video_player.isVisible():
                        print(f"💤 系统空闲 {idle_time} 秒，启动屏保...")
                        self.show_screensaver()
                        
                # 根据设置的时间调整检查频率
                if total_idle_seconds <= 30:
                    check_interval = 1  # 短时间设置时每秒检查
                elif total_idle_seconds <= 120:
                    check_interval = 2  # 2分钟内每2秒检查
                else:
                    check_interval = 5  # 长时间每5秒检查
                    
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"❌ 监控过程中出现错误: {e}")
                time.sleep(10)  # 出错时等待更长时间
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.video_player:
            self.video_player.close()
        print("⏹️ 停止监控系统空闲状态")
    
    def show_screensaver(self):
        """显示屏保"""
        try:
            config = self.config_manager.get_config()
            video_path = config.get('video_path', 'video.mp4')
            
            if not os.path.exists(video_path):
                print(f"❌ 视频文件不存在: {video_path}")
                return
            
            # 关闭之前的播放器
            if self.video_player:
                self.video_player.close()
            
            # 创建新的播放器
            self.video_player = VideoPlayer(config)
            self.video_player.play_video(video_path)
            
        except Exception as e:
            print(f"❌ 播放视频失败: {e}")
    
    def hide_screensaver(self):
        """隐藏屏保"""
        if self.video_player:
            self.video_player.close()


def main():
    """命令行模式的主函数（保持向后兼容）"""
    try:
        print("🎬 视频屏保程序启动中...")
        
        # 创建配置管理器
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        # 检查视频文件
        video_path = config.get('video_path', 'video.mp4')
        if not os.path.exists(video_path):
            print(f"❌ 错误: 找不到视频文件 '{video_path}'")
            print("💡 请确保视频文件存在并重命名为 'video.mp4'")
            input("按回车键退出...")
            return
        
        print(f"📁 视频文件: {video_path}")
        print(f"⏱️ 空闲检测时间: {config.get('idle_time_minutes', 5)} 分钟")
        print(f"🔊 播放音量: {config.get('volume', 50)}%")
        print()
        
        # 创建屏保对象
        screensaver = VideoScreensaver(config_manager)
        
        print("✅ 程序已启动！系统空闲时将自动播放视频屏保")
        print("💡 提示: 按 Ctrl+C 退出程序")
        print("=" * 50)
        
        try:
            screensaver.start_monitoring()
        except KeyboardInterrupt:
            print("\n🛑 用户中断程序")
        finally:
            screensaver.stop_monitoring()
            print("👋 程序已退出")
            
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        input("按回车键退出...")


if __name__ == "__main__":
    main() 