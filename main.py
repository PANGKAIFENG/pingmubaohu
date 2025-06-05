#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QSpinBox, QGroupBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from screensaver import VideoScreensaver
from config_manager import ConfigManager
import json

class ScreensaverThread(QThread):
    """在单独线程中运行屏保监控"""
    status_changed = pyqtSignal(str)
    
    def __init__(self, screensaver):
        super().__init__()
        self.screensaver = screensaver
        self.running = True
    
    def run(self):
        try:
            self.screensaver.start_monitoring()
        except Exception as e:
            self.status_changed.emit(f"错误: {str(e)}")
    
    def stop(self):
        self.running = False
        if self.screensaver:
            self.screensaver.stop_monitoring()

class StatusWindow(QWidget):
    """状态显示窗口"""
    def __init__(self, screensaver_app):
        super().__init__()
        self.screensaver_app = screensaver_app
        self.config_manager = ConfigManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("视频屏保程序 - 控制面板")
        self.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel("🎬 视频屏保程序 v2.0")
        title.setFont(QFont("微软雅黑", 14, QFont.Bold))
        title.setStyleSheet("color: #2E86AB; margin: 10px;")
        layout.addWidget(title)
        
        # 状态信息
        self.status_label = QLabel("✅ 程序正在运行，监控系统空闲状态...")
        self.status_label.setStyleSheet("color: #28A745; margin: 5px; padding: 10px; background-color: #F8F9FA; border-radius: 5px;")
        layout.addWidget(self.status_label)
        
        # 时间设置组
        time_group = QGroupBox("⏱️ 空闲时间设置")
        time_group.setStyleSheet("QGroupBox { font-weight: bold; margin: 5px; }")
        time_layout = QVBoxLayout()
        
        # 快速预设
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("快速设置:"))
        
        self.preset_combo = QComboBox()
        presets = self.config_manager.get_config().get('quick_presets', {})
        self.preset_combo.addItem("自定义", None)
        for name, setting in presets.items():
            self.preset_combo.addItem(name, setting)
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        
        time_layout.addLayout(preset_layout)
        
        # 自定义时间设置
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("自定义:"))
        
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 60)
        self.minutes_spin.setSuffix(" 分钟")
        self.minutes_spin.valueChanged.connect(self.update_time_display)
        custom_layout.addWidget(self.minutes_spin)
        
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        self.seconds_spin.setSuffix(" 秒")
        self.seconds_spin.valueChanged.connect(self.update_time_display)
        custom_layout.addWidget(self.seconds_spin)
        
        time_layout.addLayout(custom_layout)
        
        # 当前设置显示
        self.time_display = QLabel()
        self.time_display.setStyleSheet("color: #666; font-size: 12px; margin: 5px;")
        time_layout.addWidget(self.time_display)
        
        # 应用按钮
        apply_btn = QPushButton("✅ 应用设置")
        apply_btn.clicked.connect(self.apply_time_settings)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        time_layout.addWidget(apply_btn)
        
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # 配置信息
        config = self.config_manager.get_config()
        info_text = f"""📁 视频文件: {config.get('video_path', 'video.mp4')}
🔊 音量: {config.get('volume', 50)}%"""
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: #666; margin: 5px; padding: 8px; background-color: #F1F3F4; border-radius: 5px; font-size: 12px;")
        layout.addWidget(info_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.toggle_btn = QPushButton("⏸️ 暂停监控")
        self.toggle_btn.clicked.connect(self.toggle_monitoring)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0A800;
            }
        """)
        
        test_btn = QPushButton("🎬 测试播放")
        test_btn.clicked.connect(self.test_screensaver)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #17A2B8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        button_layout.addWidget(self.toggle_btn)
        button_layout.addWidget(test_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        # 初始化当前设置
        self.load_current_settings()
    
    def load_current_settings(self):
        """加载当前设置"""
        config = self.config_manager.get_config()
        minutes = config.get('idle_time_minutes', 5)
        seconds = config.get('idle_time_seconds', 0)
        
        self.minutes_spin.setValue(minutes)
        self.seconds_spin.setValue(seconds)
        self.update_time_display()
    
    def on_preset_changed(self, preset_name):
        """预设改变时的处理"""
        if preset_name == "自定义":
            return
            
        config = self.config_manager.get_config()
        presets = config.get('quick_presets', {})
        
        if preset_name in presets:
            setting = presets[preset_name]
            self.minutes_spin.setValue(setting.get('minutes', 0))
            self.seconds_spin.setValue(setting.get('seconds', 0))
            self.update_time_display()
    
    def update_time_display(self):
        """更新时间显示"""
        minutes = self.minutes_spin.value()
        seconds = self.seconds_spin.value()
        total_seconds = minutes * 60 + seconds
        
        if total_seconds < 10:
            warning = " ⚠️ 时间过短，建议至少10秒"
            color = "#DC3545"
        elif total_seconds < 60:
            warning = " 💡 适合测试使用"
            color = "#FFC107"
        else:
            warning = " ✅ 正常使用范围"
            color = "#28A745"
        
        self.time_display.setText(f"总计: {total_seconds} 秒{warning}")
        self.time_display.setStyleSheet(f"color: {color}; font-size: 12px; margin: 5px;")
    
    def apply_time_settings(self):
        """应用时间设置"""
        minutes = self.minutes_spin.value()
        seconds = self.seconds_spin.value()
        total_seconds = minutes * 60 + seconds
        
        if total_seconds < 5:
            QMessageBox.warning(self, "时间设置", "空闲时间不能少于5秒！")
            return
        
        # 更新配置
        config = self.config_manager.get_config()
        config['idle_time_minutes'] = minutes
        config['idle_time_seconds'] = seconds
        self.config_manager.save_config(config)
        
        # 重新启动监控
        if self.screensaver_app.monitoring_active:
            self.screensaver_app.stop_monitoring()
            self.screensaver_app.start_monitoring()
        
        QMessageBox.information(self, "设置应用", f"空闲时间已设置为 {minutes}分{seconds}秒")
    
    def toggle_monitoring(self):
        if self.screensaver_app.monitoring_active:
            self.screensaver_app.stop_monitoring()
            self.toggle_btn.setText("▶️ 开始监控")
            self.toggle_btn.setStyleSheet(self.toggle_btn.styleSheet().replace("#FFC107", "#28A745").replace("#E0A800", "#218838"))
            self.status_label.setText("⏸️ 监控已暂停")
            self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#28A745", "#FFC107"))
        else:
            self.screensaver_app.start_monitoring()
            self.toggle_btn.setText("⏸️ 暂停监控")
            self.toggle_btn.setStyleSheet(self.toggle_btn.styleSheet().replace("#28A745", "#FFC107").replace("#218838", "#E0A800"))
            self.status_label.setText("✅ 程序正在运行，监控系统空闲状态...")
            self.status_label.setStyleSheet(self.status_label.styleSheet().replace("#FFC107", "#28A745"))
    
    def test_screensaver(self):
        """测试播放屏保"""
        try:
            if self.screensaver_app.screensaver:
                self.screensaver_app.screensaver.show_screensaver()
        except Exception as e:
            QMessageBox.warning(self, "测试失败", f"无法播放视频: {str(e)}")

class ScreensaverApp:
    """带托盘图标的屏保应用"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screensaver = None
        self.screensaver_thread = None
        self.monitoring_active = False
        self.status_window = None
        
        # 检查系统托盘支持
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "系统托盘", "系统不支持托盘图标")
            sys.exit(1)
        
        self.create_tray_icon()
        self.init_screensaver()
        
    def create_icon(self):
        """创建程序图标"""
        pixmap = QPixmap(32, 32)
        pixmap.fill()
        painter = QPainter(pixmap)
        painter.setFont(QFont("Arial", 20))
        painter.drawText(pixmap.rect(), 0x4 | 0x80, "🎬")  # Qt.AlignCenter
        painter.end()
        return QIcon(pixmap)
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.create_icon())
        self.tray_icon.setToolTip("视频屏保程序 - 点击查看状态")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 显示状态窗口
        show_action = QAction("📊 显示控制面板", None)
        show_action.triggered.connect(self.show_status_window)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        # 快速时间设置子菜单
        time_menu = QMenu("⏱️ 快速设置时间", None)
        
        quick_times = [
            ("测试模式 (10秒)", 0, 10),
            ("演示模式 (30秒)", 0, 30), 
            ("办公模式 (3分钟)", 3, 0),
            ("默认模式 (5分钟)", 5, 0),
            ("长时模式 (10分钟)", 10, 0)
        ]
        
        for name, minutes, seconds in quick_times:
            action = QAction(name, None)
            action.triggered.connect(lambda checked, m=minutes, s=seconds: self.quick_set_time(m, s))
            time_menu.addAction(action)
        
        tray_menu.addMenu(time_menu)
        
        # 开始/停止监控
        self.toggle_action = QAction("⏸️ 暂停监控", None)
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        tray_menu.addAction(self.toggle_action)
        
        # 测试播放
        test_action = QAction("🎬 测试播放", None)
        test_action.triggered.connect(self.test_screensaver)
        tray_menu.addAction(test_action)
        
        tray_menu.addSeparator()
        
        # 退出程序
        quit_action = QAction("❌ 退出程序", None)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        
        # 显示启动消息
        self.tray_icon.showMessage(
            "视频屏保程序 v2.0",
            "程序已启动！双击托盘图标查看控制面板\n可快速调整触发时间（最短10秒）",
            QSystemTrayIcon.Information,
            3000
        )
    
    def quick_set_time(self, minutes, seconds):
        """快速设置时间"""
        config_manager = ConfigManager()
        config = config_manager.get_config()
        config['idle_time_minutes'] = minutes
        config['idle_time_seconds'] = seconds
        config_manager.save_config(config)
        
        # 重新启动监控
        if self.monitoring_active:
            self.stop_monitoring()
            self.start_monitoring()
        
        total_seconds = minutes * 60 + seconds
        self.tray_icon.showMessage(
            "时间设置更新",
            f"空闲触发时间已设置为 {total_seconds} 秒",
            QSystemTrayIcon.Information,
            2000
        )
    
    def tray_icon_activated(self, reason):
        """托盘图标点击事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_status_window()
    
    def show_status_window(self):
        """显示状态窗口"""
        if not self.status_window:
            self.status_window = StatusWindow(self)
        
        self.status_window.show()
        self.status_window.raise_()
        self.status_window.activateWindow()
    
    def init_screensaver(self):
        """初始化屏保"""
        try:
            config_manager = ConfigManager()
            
            # 检查视频文件
            video_path = config_manager.get_config().get('video_path', 'video.mp4')
            if not os.path.exists(video_path):
                self.tray_icon.showMessage(
                    "提醒",
                    f"未找到视频文件: {video_path}\n请将视频文件重命名为 video.mp4",
                    QSystemTrayIcon.Warning,
                    5000
                )
            
            self.screensaver = VideoScreensaver(config_manager)
            self.start_monitoring()
            
        except Exception as e:
            QMessageBox.critical(None, "初始化失败", f"程序初始化失败: {str(e)}")
            sys.exit(1)
    
    def start_monitoring(self):
        """开始监控"""
        if not self.monitoring_active and self.screensaver:
            self.screensaver_thread = ScreensaverThread(self.screensaver)
            self.screensaver_thread.start()
            self.monitoring_active = True
            self.toggle_action.setText("⏸️ 暂停监控")
            
            config = ConfigManager().get_config()
            total_seconds = config.get('idle_time_minutes', 5) * 60 + config.get('idle_time_seconds', 0)
            
            self.tray_icon.showMessage(
                "监控开始",
                f"系统空闲监控已启动 (触发时间: {total_seconds}秒)",
                QSystemTrayIcon.Information,
                2000
            )
    
    def stop_monitoring(self):
        """停止监控"""
        if self.monitoring_active and self.screensaver_thread:
            self.screensaver_thread.stop()
            self.screensaver_thread.wait()
            self.monitoring_active = False
            self.toggle_action.setText("▶️ 开始监控")
            
            self.tray_icon.showMessage(
                "监控暂停",
                "系统空闲监控已暂停",
                QSystemTrayIcon.Information,
                2000
            )
    
    def toggle_monitoring(self):
        """切换监控状态"""
        if self.monitoring_active:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def test_screensaver(self):
        """测试播放屏保"""
        if self.screensaver:
            try:
                self.screensaver.show_screensaver()
            except Exception as e:
                self.tray_icon.showMessage(
                    "测试失败",
                    f"无法播放视频: {str(e)}",
                    QSystemTrayIcon.Critical,
                    3000
                )
    
    def quit_application(self):
        """退出应用程序"""
        self.stop_monitoring()
        if self.status_window:
            self.status_window.close()
        self.tray_icon.hide()
        self.app.quit()
    
    def run(self):
        """运行应用程序"""
        return self.app.exec_()

def main():
    try:
        app = ScreensaverApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main() 