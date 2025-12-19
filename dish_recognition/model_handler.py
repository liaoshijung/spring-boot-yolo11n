"""
模型处理器
负责YOLOv10n模型的加载、预测和管理
"""
import os
import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from PIL import Image
import torch
from ultralytics import YOLO
from config import MODEL_CONFIG, BASE_DIR

class DishRecognitionModel:
    def __init__(self):
        self.model = None
        self.model_path = MODEL_CONFIG["model_path"]
        self.input_size = MODEL_CONFIG["input_size"]
        self.conf_threshold = MODEL_CONFIG["conf_threshold"]
        self.iou_threshold = MODEL_CONFIG["iou_threshold"]
        self.max_det = MODEL_CONFIG["max_det"]
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 初始化模型
        self.load_model()
    
    def load_model(self):
        """加载YOLOv10n模型"""
        try:
            # 如果模型文件不存在，尝试下载预训练的YOLOv10n模型
            if not os.path.exists(self.model_path):
                print(f"模型文件不存在: {self.model_path}")
                print("正在初始化YOLOv10n模型...")
                # 这里使用ultralytics的预训练模型作为基础，后续可以替换为自定义训练的模型
                self.model = YOLO('yolo10n.pt')  # 使用yolo10n预训练模型
                print("模型加载成功!")
            else:
                self.model = YOLO(self.model_path)
                print(f"从 {self.model_path} 加载模型成功!")
                
            # 将模型移动到指定设备
            self.model.to(self.device)
            
        except Exception as e:
            print(f"模型加载失败: {str(e)}")
            # 创建一个模拟模型用于演示
            self.model = None
    
    def predict(self, image_path: str) -> List[Dict[str, Any]]:
        """
        对单张图片进行预测
        返回检测结果列表
        """
        if self.model is None:
            # 模拟预测结果
            return self.simulate_prediction(image_path)
        
        try:
            # 使用YOLO模型进行预测
            results = self.model(
                source=image_path,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                max_det=self.max_det,
                imgsz=self.input_size,
                device=self.device,
                verbose=False
            )
            
            detections = []
            img = cv2.imread(image_path)
            height, width = img.shape[:2]
            
            # 处理检测结果
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # 获取边界框坐标
                        xyxy = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
                        
                        # 获取置信度
                        conf = float(box.conf[0])
                        
                        # 获取类别名称（这里需要映射到实际菜品名称）
                        cls_id = int(box.cls[0])
                        class_name = result.names[cls_id] if hasattr(result, 'names') else f"class_{cls_id}"
                        
                        # 将类别名映射到菜品码（模拟）
                        dish_code = self.map_class_to_dish(class_name)
                        dish_desc = self.get_dish_description(dish_code)
                        
                        detection = {
                            "dish_code": dish_code,
                            "dish_desc": dish_desc,
                            "confidence": round(conf, 2),
                            "bbox": [float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])],
                            "bbox_normalized": [
                                round(xyxy[0]/width, 3), 
                                round(xyxy[1]/height, 3), 
                                round(xyxy[2]/width, 3), 
                                round(xyxy[3]/height, 3)
                            ]
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"预测过程中出现错误: {str(e)}")
            # 返回空结果
            return []
    
    def simulate_prediction(self, image_path: str) -> List[Dict[str, Any]]:
        """
        模拟预测结果（当真实模型不可用时）
        """
        print("使用模拟预测功能")
        
        # 加载图片获取尺寸
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        
        # 模拟检测到的菜品（随机选择）
        from config import DEFAULT_DISHES
        dish_codes = list(DEFAULT_DISHES.keys())
        
        detected_codes = []
        num_detections = np.random.randint(1, 4)  # 随机检测1-3个菜品
        
        results = []
        for _ in range(num_detections):
            # 随机选择一个菜品
            dish_code = np.random.choice(dish_codes)
            if dish_code not in detected_codes:  # 确保不重复
                detected_codes.append(dish_code)
                
                # 随机生成边界框坐标
                x_center = np.random.uniform(0.2, 0.8) * width
                y_center = np.random.uniform(0.2, 0.8) * height
                w = np.random.uniform(0.1, 0.4) * width
                h = np.random.uniform(0.1, 0.4) * height
                
                x1 = max(0, x_center - w/2)
                y1 = max(0, y_center - h/2)
                x2 = min(width, x_center + w/2)
                y2 = min(height, y_center + h/2)
                
                # 随机置信度
                confidence = round(np.random.uniform(0.7, 0.99), 2)
                
                results.append({
                    "dish_code": dish_code,
                    "dish_desc": DEFAULT_DISHES[dish_code]["dish_desc"],
                    "confidence": confidence,
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "bbox_normalized": [
                        round(x1/width, 3), 
                        round(y1/height, 3), 
                        round(x2/width, 3), 
                        round(y2/height, 3)
                    ]
                })
        
        return results
    
    def map_class_to_dish(self, class_name: str) -> str:
        """
        将模型输出的类别映射到菜品码
        在实际应用中，这应该是训练时定义的映射关系
        """
        # 模拟映射逻辑
        from config import DEFAULT_DISHES
        dish_codes = list(DEFAULT_DISHES.keys())
        
        # 简单的哈希映射，确保一致性
        hash_val = hash(class_name) % len(dish_codes)
        return dish_codes[hash_val]
    
    def get_dish_description(self, dish_code: str) -> str:
        """
        根据菜品码获取菜品描述
        """
        from config import DEFAULT_DISHES
        return DEFAULT_DISHES.get(dish_code, {}).get("dish_desc", dish_code)
    
    def train_model(self, data_path: str, epochs: int = 100):
        """
        训练模型
        data_path: 训练数据路径，应包含images和labels子目录
        """
        if self.model is None:
            print("无法训练：模型未加载")
            return False
        
        try:
            print(f"开始训练模型，数据路径: {data_path}, 周期数: {epochs}")
            
            # 开始训练
            results = self.model.train(
                data=data_path,
                epochs=epochs,
                imgsz=self.input_size,
                device=self.device,
                batch=-1,  # 自动批次大小
                save_period=10,  # 每10轮保存一次
                project=os.path.join(BASE_DIR, "runs/train"),
                name="dish_recognition",
                exist_ok=True,
                verbose=True
            )
            
            print("模型训练完成!")
            return True
            
        except Exception as e:
            print(f"训练过程中出现错误: {str(e)}")
            return False

# 全局模型实例
dish_model = DishRecognitionModel()

def get_model():
    """获取模型实例"""
    return dish_model