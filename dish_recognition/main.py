"""
食堂菜品AI识别系统
基于FastAPI + YOLOv10n构建的菜品图像识别服务
支持菜品识别、训练数据动态更新功能
"""
import os
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import cv2
import numpy as np
from PIL import Image
import json
import shutil

# 导入配置、模型处理器和数据管理器
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DEFAULT_DISHES, DATABASE_CONFIG
from model_handler import get_model
from data_manager import get_data_manager

app = FastAPI(title="食堂菜品AI识别系统", description="基于YOLOv10n的菜品图像识别API")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 初始化数据管理器
data_manager = get_data_manager()
DISH_DATABASE = data_manager.get_all_dishes()

# 临时存储检测结果
DETECTION_RESULTS = []

class DetectionResult(BaseModel):
    """检测结果模型"""
    dish_code: str
    dish_desc: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]

class RecognitionResponse(BaseModel):
    """识别响应模型"""
    success: bool
    message: str
    results: List[DetectionResult]
    image_id: str

class AddTrainingDataRequest(BaseModel):
    """添加训练数据请求模型"""
    dish_code: str
    dish_desc: str
    category: str

@app.get("/")
async def root():
    return {"message": "欢迎使用食堂菜品AI识别系统!", "version": "1.0.0"}

@app.post("/recognize/", response_model=RecognitionResponse)
async def recognize_dish(image: UploadFile = File(...)):
    """
    上传菜品图片进行识别
    返回菜品编码和描述
    """
    try:
        # 验证文件类型
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="只支持图片文件上传")
        
        # 生成唯一ID
        image_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{image_id}.jpg"
        filepath = f"uploads/{filename}"
        
        # 保存上传的图片
        contents = await image.read()
        with open(filepath, "wb") as f:
            f.write(contents)
        
        # 使用YOLOv10n模型进行识别
        model = get_model()
        detection_results = model.predict(filepath)
        
        # 转换为API响应格式
        api_results = []
        for det in detection_results:
            api_results.append(DetectionResult(
                dish_code=det["dish_code"],
                dish_desc=det["dish_desc"],
                confidence=det["confidence"],
                bbox=det["bbox"]
            ))
        
        # 记录检测结果
        DETECTION_RESULTS.append({
            "image_id": image_id,
            "filepath": filepath,
            "results": detection_results,
            "timestamp": datetime.now().isoformat()
        })
        
        return RecognitionResponse(
            success=True,
            message="菜品识别成功",
            results=api_results,
            image_id=image_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"识别失败: {str(e)}")

@app.post("/add_training_data/")
async def add_training_data(
    image: UploadFile = File(...),
    dish_code: str = Form(...),
    dish_desc: str = Form(...),
    category: str = Form(...)
):
    """
    动态添加训练数据
    支持在线更新菜品数据集
    """
    try:
        # 验证菜品码格式
        if not dish_code or len(dish_code) < 5:
            raise HTTPException(status_code=400, detail="菜品码格式不正确")
        
        # 保存训练图片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"train_{timestamp}_{dish_code}.jpg"
        filepath = f"data/training/{filename}"
        
        # 确保目录存在
        os.makedirs("data/training", exist_ok=True)
        
        contents = await image.read()
        with open(filepath, "wb") as f:
            f.write(contents)
        
        # 使用数据管理器添加菜品
        success = data_manager.add_dish(dish_code, dish_desc, category)
        
        if not success:
            raise HTTPException(status_code=400, detail="菜品码已存在")
        
        # 更新全局菜品数据库
        global DISH_DATABASE
        DISH_DATABASE = data_manager.get_all_dishes()
        
        return {
            "success": True,
            "message": "训练数据添加成功",
            "dish_info": {
                "dish_code": dish_code,
                "dish_desc": dish_desc,
                "category": category,
                "image_path": filepath
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加训练数据失败: {str(e)}")

@app.get("/dishes/")
async def list_dishes():
    """列出所有已知菜品"""
    dishes = data_manager.get_all_dishes()
    return {
        "success": True,
        "count": len(dishes),
        "dishes": list(dishes.values())
    }

@app.get("/detection_history/")
async def detection_history():
    """获取检测历史记录"""
    return {
        "success": True,
        "count": len(DETECTION_RESULTS),
        "history": DETECTION_RESULTS[-20:]  # 只返回最近20条记录
    }

@app.get("/health/")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "dish_recognition_api",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)