"""
配置文件
定义系统参数和路径配置
"""
import os
from typing import Dict, Any

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 创建必要目录
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# YOLO模型配置
MODEL_CONFIG = {
    "model_name": "yolov10n",  # 使用YOLOv10 nano版本
    "model_path": os.path.join(MODELS_DIR, "yolov10n_dish.pt"),
    "input_size": 640,  # 输入图像尺寸
    "conf_threshold": 0.5,  # 置信度阈值
    "iou_threshold": 0.5,   # NMS IOU阈值
    "max_det": 10,          # 最大检测数量
}

# 数据库配置
DATABASE_CONFIG = {
    "db_path": os.path.join(DATA_DIR, "dish_database.json"),
    "training_data_path": os.path.join(DATA_DIR, "training"),
    "validation_split": 0.2,
}

# API配置
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 1,
    "reload": True,
    "log_level": "info",
}

# 文件上传配置
UPLOAD_CONFIG = {
    "allowed_extensions": {".jpg", ".jpeg", ".png", ".bmp", ".webp"},
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "upload_directory": UPLOADS_DIR,
}

# 菜品类别映射（示例）
DISH_CATEGORIES = [
    "热菜",
    "凉菜", 
    "汤类",
    "主食",
    "素菜",
    "荤菜",
    "家常菜",
    "特色菜"
]

# 默认菜品数据
DEFAULT_DISHES = {
    "dish_001": {"dish_code": "dish_001", "dish_desc": "宫保鸡丁", "category": "热菜"},
    "dish_002": {"dish_code": "dish_002", "dish_desc": "麻婆豆腐", "category": "热菜"},
    "dish_003": {"dish_code": "dish_003", "dish_desc": "红烧肉", "category": "热菜"},
    "dish_004": {"dish_code": "dish_004", "dish_desc": "青椒土豆丝", "category": "素菜"},
    "dish_005": {"dish_code": "dish_005", "dish_desc": "西红柿鸡蛋", "category": "家常菜"},
    "dish_006": {"dish_code": "dish_006", "dish_desc": "蒜蓉小白菜", "category": "素菜"},
    "dish_007": {"dish_code": "dish_007", "dish_desc": "糖醋里脊", "category": "热菜"},
    "dish_008": {"dish_code": "dish_008", "dish_desc": "鱼香肉丝", "category": "热菜"},
    "dish_009": {"dish_code": "dish_009", "dish_desc": "清蒸鲈鱼", "category": "荤菜"},
    "dish_010": {"dish_code": "dish_010", "dish_desc": "白米饭", "category": "主食"},
}

def get_config() -> Dict[str, Any]:
    """获取完整配置"""
    return {
        "model": MODEL_CONFIG,
        "database": DATABASE_CONFIG,
        "api": API_CONFIG,
        "upload": UPLOAD_CONFIG,
        "categories": DISH_CATEGORIES,
        "default_dishes": DEFAULT_DISHES
    }