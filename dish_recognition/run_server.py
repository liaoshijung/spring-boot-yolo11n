"""
启动脚本
用于启动食堂菜品识别API服务
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import uvicorn
from config import API_CONFIG

def main():
    print("正在启动食堂菜品AI识别系统...")
    print(f"API服务将运行在 {API_CONFIG['host']}:{API_CONFIG['port']}")
    
    uvicorn.run(
        "main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"],
        log_level=API_CONFIG["log_level"]
    )

if __name__ == "__main__":
    main()