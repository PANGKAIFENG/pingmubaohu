"""
配置文件管理模块
负责读取、验证和管理config.json配置文件
"""

import json
import os
from typing import Dict, Any


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "video_path": "video.mp4",
            "idle_minutes": 5
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 验证并合并默认配置
                    return self._validate_config(config)
            else:
                # 配置文件不存在，创建默认配置
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """保存配置文件"""
        try:
            config_to_save = config if config is not None else self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证配置参数"""
        validated_config = self.default_config.copy()
        
        # 验证视频路径
        if "video_path" in config and isinstance(config["video_path"], str):
            validated_config["video_path"] = config["video_path"]
        
        # 验证空闲时间（必须是正整数）
        if "idle_minutes" in config:
            try:
                idle_minutes = int(config["idle_minutes"])
                if idle_minutes > 0:
                    validated_config["idle_minutes"] = idle_minutes
            except (ValueError, TypeError):
                pass
        
        return validated_config
    
    def get_video_path(self) -> str:
        """获取视频文件路径"""
        return self.config.get("video_path", self.default_config["video_path"])
    
    def get_idle_minutes(self) -> int:
        """获取空闲触发时间（分钟）"""
        return self.config.get("idle_minutes", self.default_config["idle_minutes"])
    
    def get_idle_seconds(self) -> int:
        """获取空闲触发时间（秒）"""
        return self.get_idle_minutes() * 60
    
    def set_video_path(self, path: str) -> bool:
        """设置视频文件路径"""
        if isinstance(path, str):
            self.config["video_path"] = path
            return self.save_config()
        return False
    
    def set_idle_minutes(self, minutes: int) -> bool:
        """设置空闲触发时间"""
        if isinstance(minutes, int) and minutes > 0:
            self.config["idle_minutes"] = minutes
            return self.save_config()
        return False
    
    def reload_config(self) -> Dict[str, Any]:
        """重新加载配置文件"""
        self.config = self.load_config()
        return self.config


if __name__ == "__main__":
    # 测试配置管理器
    config_manager = ConfigManager()
    print("当前配置:")
    print(f"视频路径: {config_manager.get_video_path()}")
    print(f"空闲时间: {config_manager.get_idle_minutes()} 分钟")
    print(f"空闲时间: {config_manager.get_idle_seconds()} 秒") 