"""
数据管理模块
负责菜品数据库的读取、写入和管理
"""
import os
import json
from typing import Dict, Any, List
from config import DATABASE_CONFIG, DEFAULT_DISHES

class DishDataManager:
    def __init__(self):
        self.db_path = DATABASE_CONFIG["db_path"]
        self.dish_database = self.load_dish_database()
    
    def load_dish_database(self) -> Dict[str, Any]:
        """从文件加载菜品数据库"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"从 {self.db_path} 加载菜品数据库成功，共 {len(data)} 个菜品")
                return data
            except Exception as e:
                print(f"加载菜品数据库失败: {str(e)}，使用默认数据")
                return DEFAULT_DISHES.copy()
        else:
            print("菜品数据库文件不存在，使用默认数据")
            return DEFAULT_DISHES.copy()
    
    def save_dish_database(self):
        """保存菜品数据库到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.dish_database, f, ensure_ascii=False, indent=2)
            print(f"菜品数据库已保存到 {self.db_path}")
        except Exception as e:
            print(f"保存菜品数据库失败: {str(e)}")
    
    def get_all_dishes(self) -> Dict[str, Any]:
        """获取所有菜品信息"""
        return self.dish_database
    
    def get_dish_by_code(self, dish_code: str) -> Dict[str, Any]:
        """根据菜品码获取菜品信息"""
        return self.dish_database.get(dish_code, {})
    
    def add_dish(self, dish_code: str, dish_desc: str, category: str) -> bool:
        """添加新菜品"""
        if dish_code in self.dish_database:
            print(f"菜品码 {dish_code} 已存在")
            return False
        
        self.dish_database[dish_code] = {
            "dish_code": dish_code,
            "dish_desc": dish_desc,
            "category": category
        }
        
        # 保存到文件
        self.save_dish_database()
        return True
    
    def update_dish(self, dish_code: str, dish_desc: str = None, category: str = None) -> bool:
        """更新菜品信息"""
        if dish_code not in self.dish_database:
            return False
        
        if dish_desc is not None:
            self.dish_database[dish_code]["dish_desc"] = dish_desc
        if category is not None:
            self.dish_database[dish_code]["category"] = category
        
        # 保存到文件
        self.save_dish_database()
        return True
    
    def delete_dish(self, dish_code: str) -> bool:
        """删除菜品"""
        if dish_code in self.dish_database:
            del self.dish_database[dish_code]
            # 保存到文件
            self.save_dish_database()
            return True
        return False

# 全局数据管理实例
data_manager = DishDataManager()

def get_data_manager():
    """获取数据管理实例"""
    return data_manager