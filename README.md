# Cafeteria Dish Recognition System

This is a Spring Boot application that uses YOLOv11n for fast AI dish recognition in cafeteria scenarios. The system allows you to upload dish images for recognition and manage dish data.

## Features

- Dish image recognition using YOLOv11n (simulated in this demo)
- RESTful API for dish management
- Add, update, delete, and retrieve dish information
- Returns dish code and description only

## Prerequisites

- Java 17+
- Maven 3.6+
- OpenCV library installed (for actual YOLO integration)

## Setup Instructions

1. Clone the repository
2. Build the project:
   ```bash
   mvn clean install
   ```
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```

## API Endpoints

### Dish Recognition
- **POST** `/api/dish/recognize` - Upload an image to recognize the dish
  - Parameters: `image` (multipart file)
  - Response: Array of detected dishes with code and description

### Dish Management
- **GET** `/api/dish/dishes` - Get all dishes
- **GET** `/api/dish/dish/{dishCode}` - Get dish by code
- **POST** `/api/dish/dish` - Add a new dish
- **PUT** `/api/dish/dish/{dishCode}` - Update an existing dish
- **DELETE** `/api/dish/dish/{dishCode}` - Delete a dish

## Sample Request

To recognize a dish:
```bash
curl -X POST http://localhost:8080/api/dish/recognize \
  -F "image=@path/to/your/dish/image.jpg"
```

To add a dish:
```bash
curl -X POST http://localhost:8080/api/dish/dish \
  -H "Content-Type: application/json" \
  -d '{
    "dishCode": "DISH_NEW",
    "dishDescription": "New Dish Description",
    "imagePath": "images/new_dish.jpg"
  }'
```

## Implementation Notes

In this demo:
- The YOLOv11n model is simulated with a color-based classification algorithm
- Actual implementation would require the real YOLOv11n model files (weights and config)
- The application uses an in-memory H2 database for demonstration
- Image uploads are stored in the `uploads/` directory

For production use, you would need to:
1. Integrate the actual YOLOv11n model
2. Connect to a persistent database
3. Implement proper image preprocessing
4. Add authentication and security measures