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
from video_player import VideoPlayerApp


class ScreensaverController:
    """屏保控制器"""
    
    def __init__(self, config_file: str = "config.json"):
        # 初始化组件
        self.config_manager = ConfigManager(config_file)
        self.system_monitor = SystemMonitor()
        self.video_player_app = VideoPlayerApp()
        
        # 状态标志
        self.is_running = False
        self.is_playing = False
        self.player_thread: Optional[threading.Thread] = None
        
        # 设置回调
        self.system_monitor.set_idle_callback(self.on_system_idle)
        
        self._setup_monitor()
        
        print("屏保控制器初始化完成")
    
    def _setup_monitor(self):
        """设置系统监听器"""
        # 从配置文件获取空闲阈值
        idle_seconds = self.config_manager.get_idle_seconds()
        self.system_monitor.set_idle_threshold(idle_seconds)
        
        print(f"空闲阈值设置为: {self.config_manager.get_idle_minutes()} 分钟")
        print(f"视频文件路径: {self.config_manager.get_video_path()}")
    
    def on_system_idle(self):
        """系统空闲回调 - 触发屏保"""
        if not self.is_playing:
            print("系统空闲，启动屏保视频...")
            self.start_screensaver()
    
    def start_screensaver(self):
        """启动屏保视频播放"""
        if self.is_playing:
            print("屏保已在播放中")
            return
        
        video_path = self.config_manager.get_video_path()
        
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            print(f"视频文件不存在: {video_path}")
            print("请检查config.json中的video_path设置")
            return
        
        # 设置播放状态
        self.is_playing = True
        
        # 在新线程中启动视频播放（避免阻塞主线程）
        self.player_thread = threading.Thread(
            target=self._play_video_thread,
            args=(video_path,),
            daemon=True
        )
        self.player_thread.start()
    
    def _play_video_thread(self, video_path: str):
        """视频播放线程"""
        try:
            print(f"在新线程中播放视频: {video_path}")
            
            # 播放视频（阻塞调用）
            self.video_player_app.play_video_fullscreen(
                video_path, 
                self.on_video_exit
            )
            
        except Exception as e:
            print(f"视频播放线程出错: {e}")
        finally:
            self.is_playing = False
    
    def on_video_exit(self):
        """视频播放退出回调"""
        print("用户操作，屏保视频退出")
        self.is_playing = False
        
        # 重置系统监听器的空闲时间记录
        self.system_monitor._last_idle_time = 0
    
    def stop_screensaver(self):
        """停止屏保播放"""
        if self.is_playing:
            print("停止屏保播放...")
            self.video_player_app.stop_playback()
            self.is_playing = False
    
    def reload_config(self):
        """重新加载配置"""
        print("重新加载配置文件...")
        self.config_manager.reload_config()
        self._setup_monitor()
        print("配置重新加载完成")
    
    def start(self):
        """启动屏保服务"""
        if self.is_running:
            print("屏保服务已在运行中")
            return
        
        print("启动屏保服务...")
        self.is_running = True
        
        # 启动系统监听
        self.system_monitor.start_monitoring()
        
        print("屏保服务已启动，等待系统空闲...")
        print(f"空闲阈值: {self.config_manager.get_idle_minutes()} 分钟")
        print("按 Ctrl+C 停止服务")
    
    def stop(self):
        """停止屏保服务"""
        if not self.is_running:
            print("屏保服务未在运行")
            return
        
        print("停止屏保服务...")
        self.is_running = False
        
        # 停止视频播放
        self.stop_screensaver()
        
        # 停止系统监听
        self.system_monitor.stop_monitoring()
        
        # 等待播放线程结束
        if self.player_thread and self.player_thread.is_alive():
            self.player_thread.join(timeout=5.0)
        
        print("屏保服务已停止")
    
    def get_status(self) -> dict:
        """获取服务状态"""
        return {
            "is_running": self.is_running,
            "is_playing": self.is_playing,
            "config": {
                "video_path": self.config_manager.get_video_path(),
                "idle_minutes": self.config_manager.get_idle_minutes()
            },
            "monitor_status": self.system_monitor.get_status()
        }
    
    def run_interactive(self):
        """交互式运行模式"""
        print("\n" + "="*50)
        print("🎬 视频屏保程序")
        print("="*50)
        
        while True:
            print("\n请选择操作:")
            print("1. 启动屏保服务")
            print("2. 停止屏保服务") 
            print("3. 查看状态")
            print("4. 重新加载配置")
            print("5. 立即播放测试")
            print("6. 退出程序")
            
            try:
                choice = input("\n请输入选项 (1-6): ").strip()
                
                if choice == "1":
                    self.start()
                    
                elif choice == "2":
                    self.stop()
                    
                elif choice == "3":
                    status = self.get_status()
                    print("\n当前状态:")
                    print(f"  服务运行: {'是' if status['is_running'] else '否'}")
                    print(f"  视频播放: {'是' if status['is_playing'] else '否'}")
                    print(f"  视频路径: {status['config']['video_path']}")
                    print(f"  空闲阈值: {status['config']['idle_minutes']} 分钟")
                    print(f"  当前空闲: {status['monitor_status']['current_idle_time']:.1f} 秒")
                    
                elif choice == "4":
                    self.reload_config()
                    
                elif choice == "5":
                    print("立即播放测试视频...")
                    self.start_screensaver()
                    
                elif choice == "6":
                    print("退出程序...")
                    self.stop()
                    break
                    
                else:
                    print("无效的选项，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n\n检测到 Ctrl+C，退出程序...")
                self.stop()
                break
            except Exception as e:
                print(f"操作出错: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="视频屏保程序")
    parser.add_argument("-c", "--config", default="config.json",
                       help="配置文件路径 (默认: config.json)")
    parser.add_argument("-d", "--daemon", action="store_true",
                       help="后台服务模式（自动启动）")
    parser.add_argument("--test", action="store_true",
                       help="测试模式（立即播放视频）")
    
    args = parser.parse_args()
    
    try:
        # 创建屏保控制器
        controller = ScreensaverController(args.config)
        
        if args.test:
            # 测试模式 - 立即播放
            print("测试模式：立即播放视频")
            controller.start_screensaver()
            
        elif args.daemon:
            # 后台服务模式
            print("后台服务模式启动...")
            controller.start()
            try:
                while controller.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n收到停止信号，正在停止服务...")
                controller.stop()
                
        else:
            # 交互式模式
            controller.run_interactive()
            
    except Exception as e:
        print(f"程序运行出错: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 