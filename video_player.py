"""
全屏视频播放器模块
实现全屏视频播放、循环播放和用户输入检测退出功能
"""

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTimer
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QCursor
from typing import Callable, Optional


class FullScreenVideoPlayer(QMainWindow):
    """全屏视频播放器"""
    
    # 信号定义
    user_input_detected = pyqtSignal()  # 用户输入检测信号
    playback_error = pyqtSignal(str)    # 播放错误信号
    
    def __init__(self, video_path: str = None, exit_callback: Callable = None):
        super().__init__()
        
        self.video_path = video_path
        self.exit_callback = exit_callback
        self.media_player = None
        self.video_widget = None
        
        self.init_ui()
        self.init_media_player()
        self.setup_signals()
        
        # 隐藏鼠标光标
        self.setCursor(QCursor(Qt.BlankCursor))
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle("屏保视频播放器")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        # 创建视频显示控件
        self.video_widget = QVideoWidget()
        self.video_widget.setAspectRatioMode(Qt.KeepAspectRatioByExpanding)
        
        # 设置中央控件
        self.setCentralWidget(self.video_widget)
        
        # 设置为全屏
        self.showFullScreen()
        
        # 确保窗口获得焦点以接收键盘事件
        self.setFocus()
        self.activateWindow()
    
    def init_media_player(self):
        """初始化媒体播放器"""
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        
        # 设置音量（100%）
        self.media_player.setVolume(100)
    
    def setup_signals(self):
        """设置信号连接"""
        # 连接播放器信号
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.media_player.error.connect(self.on_media_error)
        self.media_player.positionChanged.connect(self.on_position_changed)
        
        # 连接自定义信号
        self.user_input_detected.connect(self.exit_player)
        self.playback_error.connect(self.on_playback_error)
    
    def load_video(self, video_path: str) -> bool:
        """
        加载视频文件
        
        Args:
            video_path (str): 视频文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            if not os.path.exists(video_path):
                print(f"视频文件不存在: {video_path}")
                return False
            
            # 设置媒体内容
            media_content = QMediaContent(QUrl.fromLocalFile(os.path.abspath(video_path)))
            self.media_player.setMedia(media_content)
            self.video_path = video_path
            
            print(f"视频文件已加载: {video_path}")
            return True
            
        except Exception as e:
            print(f"加载视频文件失败: {e}")
            self.playback_error.emit(f"加载视频失败: {e}")
            return False
    
    def play_video(self, video_path: str = None):
        """
        播放视频
        
        Args:
            video_path (str, optional): 视频文件路径
        """
        try:
            # 如果提供了新的视频路径，先加载
            if video_path:
                if not self.load_video(video_path):
                    return
            elif self.video_path:
                if not self.load_video(self.video_path):
                    return
            else:
                print("没有指定视频文件")
                self.playback_error.emit("没有指定视频文件")
                return
            
            # 开始播放
            self.media_player.play()
            print("开始播放视频")
            
        except Exception as e:
            print(f"播放视频失败: {e}")
            self.playback_error.emit(f"播放失败: {e}")
    
    def stop_video(self):
        """停止播放"""
        try:
            if self.media_player:
                self.media_player.stop()
                print("视频播放已停止")
        except Exception as e:
            print(f"停止播放失败: {e}")
    
    def on_media_status_changed(self, status):
        """媒体状态变化处理"""
        if status == QMediaPlayer.EndOfMedia:
            # 视频播放结束，重新开始（循环播放）
            print("视频播放结束，重新开始循环播放")
            self.media_player.setPosition(0)
            self.media_player.play()
        elif status == QMediaPlayer.LoadedMedia:
            print("媒体文件加载完成")
        elif status == QMediaPlayer.BufferedMedia:
            print("媒体文件缓冲完成")
    
    def on_media_error(self, error):
        """媒体播放错误处理"""
        error_string = self.media_player.errorString()
        print(f"媒体播放错误: {error_string}")
        self.playback_error.emit(f"播放错误: {error_string}")
    
    def on_position_changed(self, position):
        """播放位置变化处理（可用于调试）"""
        # 可以在这里添加播放进度相关逻辑
        pass
    
    def on_playback_error(self, error_message: str):
        """播放错误处理"""
        print(f"播放错误: {error_message}")
        # 可以在这里添加错误处理逻辑，比如尝试播放备用视频
        QTimer.singleShot(3000, self.exit_player)  # 3秒后退出
    
    # 事件处理方法 - 检测用户输入
    def keyPressEvent(self, event: QKeyEvent):
        """键盘按键事件"""
        print(f"检测到键盘输入: {event.key()}")
        self.user_input_detected.emit()
        super().keyPressEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标点击事件"""
        print("检测到鼠标点击")
        self.user_input_detected.emit()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        print("检测到鼠标移动")
        self.user_input_detected.emit()
        super().mouseMoveEvent(event)
    
    def wheelEvent(self, event):
        """鼠标滚轮事件"""
        print("检测到鼠标滚轮")
        self.user_input_detected.emit()
        super().wheelEvent(event)
    
    def exit_player(self):
        """退出播放器"""
        print("退出视频播放器")
        
        try:
            # 停止播放
            self.stop_video()
            
            # 恢复鼠标光标
            self.setCursor(QCursor(Qt.ArrowCursor))
            
            # 调用退出回调
            if self.exit_callback:
                self.exit_callback()
            
            # 关闭窗口
            self.close()
            
        except Exception as e:
            print(f"退出播放器时出错: {e}")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.stop_video()
        super().closeEvent(event)


class VideoPlayerApp:
    """视频播放器应用程序封装"""
    
    def __init__(self):
        self.app = None
        self.player = None
    
    def create_app(self):
        """创建Qt应用程序"""
        if not self.app:
            self.app = QApplication.instance()
            if not self.app:
                self.app = QApplication(sys.argv)
    
    def play_video_fullscreen(self, video_path: str, exit_callback: Callable = None):
        """
        全屏播放视频
        
        Args:
            video_path (str): 视频文件路径
            exit_callback (Callable): 退出回调函数
        """
        try:
            self.create_app()
            
            # 创建播放器
            self.player = FullScreenVideoPlayer(video_path, exit_callback)
            
            # 播放视频
            self.player.play_video()
            
            # 运行应用程序（阻塞）
            return self.app.exec_()
            
        except Exception as e:
            print(f"播放视频时出错: {e}")
            return 1
    
    def stop_playback(self):
        """停止播放"""
        if self.player:
            self.player.exit_player()
    
    def quit_app(self):
        """退出应用程序"""
        if self.app:
            self.app.quit()


def exit_callback_example():
    """示例退出回调函数"""
    print("视频播放器已退出")


if __name__ == "__main__":
    # 测试视频播放器
    import argparse
    
    parser = argparse.ArgumentParser(description="全屏视频播放器测试")
    parser.add_argument("video_path", nargs="?", default="video.mp4", 
                       help="视频文件路径（默认: video.mp4）")
    
    args = parser.parse_args()
    
    # 创建播放器应用
    player_app = VideoPlayerApp()
    
    # 播放视频
    exit_code = player_app.play_video_fullscreen(args.video_path, exit_callback_example)
    
    print(f"播放器退出，退出码: {exit_code}")
    sys.exit(exit_code) 