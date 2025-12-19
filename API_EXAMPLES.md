# Cafeteria Dish Recognition API Examples

This document provides examples of how to use the API endpoints for the cafeteria dish recognition system.

## API Endpoints

### 1. Dish Recognition
**POST** `/api/dish/recognize`

Upload an image to recognize the dish.

Example using curl:
```bash
curl -X POST http://localhost:8080/api/dish/recognize \
  -F "image=@path/to/your/dish/image.jpg"
```

Expected response:
```json
[
  {
    "dishCode": "DISH_001",
    "dishDescription": "Red Apple"
  }
]
```

### 2. Add New Dish
**POST** `/api/dish/dish`

Add a new dish to the system.

Example using curl:
```bash
curl -X POST http://localhost:8080/api/dish/dish \
  -H "Content-Type: application/json" \
  -d '{
    "dishCode": "DISH_011",
    "dishDescription": "Caesar Salad",
    "imagePath": "images/caesar_salad.jpg"
  }'
```

Expected response:
```json
{
  "id": 11,
  "dishCode": "DISH_011",
  "dishDescription": "Caesar Salad",
  "imagePath": "images/caesar_salad.jpg"
}
```

### 3. Get All Dishes
**GET** `/api/dish/dishes`

Retrieve all dishes in the system.

Example using curl:
```bash
curl -X GET http://localhost:8080/api/dish/dishes
```

Expected response:
```json
[
  {
    "id": 1,
    "dishCode": "DISH_001",
    "dishDescription": "Red Apple",
    "imagePath": "images/apples.jpg"
  },
  {
    "id": 2,
    "dishCode": "DISH_002",
    "dishDescription": "Banana",
    "imagePath": "images/bananas.jpg"
  }
]
```

### 4. Get Dish by Code
**GET** `/api/dish/dish/{dishCode}`

Retrieve a specific dish by its code.

Example using curl:
```bash
curl -X GET http://localhost:8080/api/dish/dish/DISH_001
```

Expected response:
```json
{
  "id": 1,
  "dishCode": "DISH_001",
  "dishDescription": "Red Apple",
  "imagePath": "images/apples.jpg"
}
```

### 5. Update Dish
**PUT** `/api/dish/dish/{dishCode}`

Update an existing dish.

Example using curl:
```bash
curl -X PUT http://localhost:8080/api/dish/dish/DISH_001 \
  -H "Content-Type: application/json" \
  -d '{
    "dishCode": "DISH_001",
    "dishDescription": "Green Apple",
    "imagePath": "images/green_apples.jpg"
  }'
```

Expected response:
```json
{
  "id": 1,
  "dishCode": "DISH_001",
  "dishDescription": "Green Apple",
  "imagePath": "images/green_apples.jpg"
}
```

### 6. Delete Dish
**DELETE** `/api/dish/dish/{dishCode}`

Delete a dish by its code.

Example using curl:
```bash
curl -X DELETE http://localhost:8080/api/dish/dish/DISH_001
```

Expected response:
```
Dish deleted successfully
```

## Running the Application

1. Start the application:
   ```bash
   ./run.sh
   ```

2. The application will be available at: `http://localhost:8080`

3. The H2 console will be available at: `http://localhost:8080/h2-console`

## Notes

- The application uses an in-memory H2 database for demonstration purposes
- Images are temporarily stored in the `uploads/` directory
- The YOLOv11n model is simulated in this demo - for production, you would need to integrate the actual model
- All responses return only dish code and description as requested