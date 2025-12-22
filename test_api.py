#!/usr/bin/env python
"""
测试API功能
创建一个简单的测试图片并测试API功能
"""

import requests
import json
from PIL import Image, ImageDraw
import io
import uuid
import time

# 等待服务器启动
print("等待服务器启动...")
time.sleep(5)

# 创建一个简单的测试图片
def create_test_image():
    # 创建一个简单的彩色图片
    img = Image.new('RGB', (400, 400), color='red')
    draw = ImageDraw.Draw(img)
    # 绘制一些形状来模拟菜品
    draw.rectangle([100, 100, 300, 300], fill='yellow', outline='black', width=3)
    draw.ellipse([150, 150, 250, 250], fill='green', outline='black', width=2)
    
    # 保存到字节流
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

# 测试API
def test_api():
    # 创建测试图片
    test_img = create_test_image()
    
    # 测试菜品识别API
    print("测试菜品识别API...")
    try:
        response = requests.post(
            "http://localhost:8000/recognize/",
            files={"image": ("test_dish.jpg", test_img, "image/jpeg")}
        )
        print(f"识别API响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"识别结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"识别API错误: {response.text}")
    except Exception as e:
        print(f"识别API请求失败: {e}")
    
    # 测试健康检查
    print("\n测试健康检查API...")
    try:
        response = requests.get("http://localhost:8000/health/")
        print(f"健康检查响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"健康检查结果: {result}")
        else:
            print(f"健康检查API错误: {response.text}")
    except Exception as e:
        print(f"健康检查API请求失败: {e}")
    
    # 测试菜品列表
    print("\n测试菜品列表API...")
    try:
        response = requests.get("http://localhost:8000/dishes/")
        print(f"菜品列表响应状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"菜品数量: {result.get('count', 0)}")
        else:
            print(f"菜品列表API错误: {response.text}")
    except Exception as e:
        print(f"菜品列表API请求失败: {e}")

if __name__ == "__main__":
    print("开始测试API功能...")
    test_api()
    print("API测试完成！")