"""
系统空闲监听模块
使用Windows API监测用户最后输入时间，判断系统空闲状态
"""

import time
import threading
from ctypes import windll, Structure, c_uint, sizeof, byref
from typing import Callable, Optional


class LASTINPUTINFO(Structure):
    """Windows API LASTINPUTINFO结构体"""
    _fields_ = [("cbSize", c_uint), ("dwTime", c_uint)]


class SystemMonitor:
    """系统空闲监听器"""
    
    def __init__(self, idle_callback: Callable = None):
        self.idle_callback = idle_callback
        self.idle_threshold = 300  # 默认5分钟 (300秒)
        self.check_interval = 1.0  # 检查间隔1秒
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._last_idle_time = 0
    
    def get_idle_time(self) -> float:
        """
        获取系统空闲时间（秒）
        
        Returns:
            float: 空闲时间（秒）
        """
        try:
            last_input_info = LASTINPUTINFO()
            last_input_info.cbSize = sizeof(last_input_info)
            
            # 调用Windows API获取最后输入信息
            windll.user32.GetLastInputInfo(byref(last_input_info))
            
            # 获取系统启动时间
            millis = windll.kernel32.GetTickCount()
            
            # 计算空闲时间（毫秒转秒）
            idle_time = (millis - last_input_info.dwTime) / 1000.0
            
            return max(0, idle_time)
            
        except Exception as e:
            print(f"获取系统空闲时间失败: {e}")
            return 0
    
    def set_idle_threshold(self, seconds: int):
        """
        设置空闲触发阈值
        
        Args:
            seconds (int): 空闲时间阈值（秒）
        """
        if seconds > 0:
            self.idle_threshold = seconds
            print(f"空闲阈值设置为: {seconds} 秒")
    
    def set_check_interval(self, interval: float):
        """
        设置检查间隔
        
        Args:
            interval (float): 检查间隔（秒）
        """
        if interval > 0:
            self.check_interval = interval
    
    def set_idle_callback(self, callback: Callable):
        """
        设置空闲回调函数
        
        Args:
            callback (Callable): 当系统空闲达到阈值时调用的函数
        """
        self.idle_callback = callback
    
    def _monitor_loop(self):
        """监听循环"""
        print("开始监听系统空闲状态...")
        
        while self.monitoring:
            try:
                current_idle = self.get_idle_time()
                
                # 检查是否达到空闲阈值
                if current_idle >= self.idle_threshold:
                    # 避免重复触发
                    if self._last_idle_time < self.idle_threshold:
                        print(f"系统空闲 {current_idle:.1f} 秒，触发屏保")
                        if self.idle_callback:
                            try:
                                self.idle_callback()
                            except Exception as e:
                                print(f"执行空闲回调失败: {e}")
                
                self._last_idle_time = current_idle
                
                # 等待下次检查
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"监听循环出错: {e}")
                time.sleep(self.check_interval)
    
    def start_monitoring(self):
        """开始监听"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print(f"系统监听已启动，空闲阈值: {self.idle_threshold} 秒")
        else:
            print("系统监听已在运行中")
    
    def stop_monitoring(self):
        """停止监听"""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=2.0)
            print("系统监听已停止")
        else:
            print("系统监听未在运行")
    
    def is_monitoring(self) -> bool:
        """检查是否正在监听"""
        return self.monitoring
    
    def get_status(self) -> dict:
        """获取监听器状态"""
        return {
            "monitoring": self.monitoring,
            "idle_threshold": self.idle_threshold,
            "check_interval": self.check_interval,
            "current_idle_time": self.get_idle_time()
        }


def idle_callback_example():
    """示例空闲回调函数"""
    print("系统空闲，触发屏保！")


if __name__ == "__main__":
    # 测试系统监听器
    monitor = SystemMonitor(idle_callback_example)
    
    # 设置较短的测试阈值（10秒）
    monitor.set_idle_threshold(10)
    
    try:
        monitor.start_monitoring()
        
        # 持续显示当前空闲时间
        while True:
            status = monitor.get_status()
            print(f"当前空闲时间: {status['current_idle_time']:.1f} 秒", end="\r")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n停止监听...")
        monitor.stop_monitoring() 