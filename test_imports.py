#!/usr/bin/env python
"""
测试导入修复
验证所有模块都可以正确导入
"""

print("开始测试模块导入...")

try:
    import sys
    import os
    sys.path.append('/workspace/dish_recognition')
    
    print("1. 测试导入config模块...")
    from dish_recognition.config import DEFAULT_DISHES, DATABASE_CONFIG
    print("   ✓ config模块导入成功")
    
    print("2. 测试导入model_handler模块...")
    from dish_recognition.model_handler import get_model
    print("   ✓ model_handler模块导入成功")
    
    print("3. 测试导入data_manager模块...")
    from dish_recognition.data_manager import get_data_manager
    print("   ✓ data_manager模块导入成功")
    
    print("4. 测试导入main模块...")
    from dish_recognition.main import app
    print("   ✓ main模块导入成功")
    
    print("\n所有模块导入测试通过！")
    print(f"默认菜品数量: {len(DEFAULT_DISHES)}")
    
    # 测试数据管理器
    dm = get_data_manager()
    dishes = dm.get_all_dishes()
    print(f"数据管理器加载菜品数量: {len(dishes)}")
    
    # 测试模型获取（可能失败但不应该抛出导入错误）
    try:
        model = get_model()
        print("模型获取成功（即使模拟模式）")
    except Exception as e:
        print(f"模型获取遇到预期外的问题: {e}")
        
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)
except Exception as e:
    print(f"其他错误: {e}")
    sys.exit(1)

print("\n模块导入测试完成！")