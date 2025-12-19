# 食堂菜品AI识别系统

基于FastAPI + YOLOv10n构建的菜品图像识别服务，支持菜品识别、训练数据动态更新功能，是一个典型的轻量级边缘AI识别应用。

## 功能特性

- 🍽️ **菜品识别**: 上传菜品图片，返回菜品编码和描述
- 📊 **动态训练**: 支持在线添加新的训练数据
- 📈 **检测历史**: 记录和查询历史检测结果
- 🔄 **模型管理**: 支持模型训练和更新
- 📁 **文件管理**: 安全的图片上传和存储

## 技术架构

- **后端框架**: FastAPI
- **AI模型**: YOLOv10n (nano版本)
- **依赖管理**: pip
- **容器化**: Docker
- **API文档**: 自动生成的Swagger UI

## 安装部署

### 方法一：本地运行

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 启动服务
```bash
cd dish_recognition
python run_server.py
```

3. 访问服务
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 方法二：Docker运行

1. 构建镜像
```bash
docker build -t dish-recognition .
```

2. 运行容器
```bash
docker run -d -p 8000:8000 --name dish-recognition-app dish-recognition
```

## API接口

### 1. 菜品识别
- **接口**: `POST /recognize/`
- **功能**: 上传菜品图片进行识别
- **参数**: 
  - `image`: 图片文件
- **返回**: 菜品编码、描述、置信度、边界框信息

### 2. 添加训练数据
- **接口**: `POST /add_training_data/`
- **功能**: 动态添加新的训练数据
- **参数**:
  - `image`: 训练图片
  - `dish_code`: 菜品编码
  - `dish_desc`: 菜品描述
  - `category`: 菜品类别
- **返回**: 添加结果信息

### 3. 列出所有菜品
- **接口**: `GET /dishes/`
- **功能**: 获取所有已知菜品列表

### 4. 检测历史记录
- **接口**: `GET /detection_history/`
- **功能**: 获取历史检测记录

### 5. 健康检查
- **接口**: `GET /health/`
- **功能**: 检查服务状态

## 项目结构

```
/workspace/
├── dish_recognition/          # 主应用目录
│   ├── main.py               # 主应用文件
│   ├── config.py             # 配置文件
│   ├── model_handler.py      # 模型处理器
│   ├── data_manager.py       # 数据管理器
│   ├── run_server.py         # 启动脚本
│   ├── data/                 # 数据存储目录
│   ├── models/               # 模型存储目录
│   ├── uploads/              # 上传文件目录
│   └── static/               # 静态文件目录
├── requirements.txt          # 依赖文件
├── Dockerfile               # Docker配置
└── README.md                # 项目说明
```

## 使用示例

### 菜品识别示例

使用curl进行菜品识别:
```bash
curl -X POST "http://localhost:8000/recognize/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@path/to/dish_image.jpg"
```

### 添加训练数据示例

```bash
curl -X POST "http://localhost:8000/add_training_data/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@path/to/new_dish.jpg" \
  -F "dish_code=dish_011" \
  -F "dish_desc=新菜品名称" \
  -F "category=热菜"
```

## 模型训练

系统支持动态训练模型，当添加新的菜品数据后，可以重新训练模型以提升识别准确性。

训练API接口:
```bash
# 该功能在model_handler.py中实现
# 可通过扩展API支持在线训练
```

## 配置说明

- **模型配置**: `config.py` 中的 `MODEL_CONFIG`
- **API配置**: `config.py` 中的 `API_CONFIG`
- **上传配置**: `config.py` 中的 `UPLOAD_CONFIG`

## 扩展功能

- [ ] 实时模型训练
- [ ] 模型性能监控
- [ ] 批量处理API
- [ ] 图像预处理优化
- [ ] 模型压缩和加速

## 注意事项

1. 首次运行时会自动下载YOLOv10n预训练模型
2. 上传图片大小限制为10MB
3. 支持的图片格式：JPG, JPEG, PNG, BMP, WEBP
4. 模型会根据添加的训练数据自动更新菜品数据库

## 许可证

本项目为演示用途，如需商业使用请遵守相关开源协议。