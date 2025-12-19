"""
测试脚本
用于验证食堂菜品识别系统的基本功能
"""
import os
import sys
import requests
import json

# 添加项目路径
sys.path.append('/workspace/dish_recognition')

from config import API_CONFIG
from data_manager import get_data_manager

def test_system():
    print("开始测试食堂菜品识别系统...")
    
    # 测试数据管理器
    print("\n1. 测试数据管理器...")
    dm = get_data_manager()
    dishes = dm.get_all_dishes()
    print(f"   加载菜品数量: {len(dishes)}")
    print(f"   菜品示例: {list(dishes.values())[:3]}")
    
    # 测试API服务
    print("\n2. 测试API服务...")
    base_url = f"http://{API_CONFIG['host']}:{API_CONFIG['port']}"
    
    try:
        # 测试健康检查
        health_url = f"{base_url}/health"
        response = requests.get(health_url)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   健康检查: {health_data}")
        else:
            print(f"   健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"   API测试失败: {str(e)}")
        print("   (如果服务未启动，这是正常的)")
    
    # 测试配置
    print("\n3. 测试配置加载...")
    from config import get_config
    config = get_config()
    print(f"   模型配置: {config['model']['model_name']}")
    print(f"   API端口: {config['api']['port']}")
    print(f"   菜品类别数: {len(config['categories'])}")
    
    # 测试目录创建
    print("\n4. 测试目录结构...")
    required_dirs = ['data', 'models', 'uploads', 'static']
    base_path = '/workspace/dish_recognition'
    for dir_name in required_dirs:
        dir_path = os.path.join(base_path, dir_name)
        if os.path.exists(dir_path):
            print(f"   ✓ {dir_name}/ 目录存在")
        else:
            print(f"   ✗ {dir_name}/ 目录不存在")
    
    print("\n系统测试完成!")

if __name__ == "__main__":
    test_system()