package com.example.dishrecognition.service;

import com.example.dishrecognition.entity.Dish;
import com.example.dishrecognition.repository.DishRepository;
import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.dnn.Dnn;
import org.opencv.dnn.Net;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class DishRecognitionService {

    @Autowired
    private DishRepository dishRepository;

    private Net net;
    private List<String> classNames;

    // Directory for storing uploaded images
    private final String UPLOAD_DIR = "uploads/";

    public DishRecognitionService() {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME); // Load OpenCV native library
        initializeModel();
        initializeClassNames();
        
        // Create upload directory if it doesn't exist
        File uploadDir = new File(UPLOAD_DIR);
        if (!uploadDir.exists()) {
            uploadDir.mkdirs();
        }
    }

    /**
     * Initialize YOLO model (placeholder - in real implementation, you'd load the actual model)
     */
    private void initializeModel() {
        // In a real implementation, this would load the YOLOv11n model
        // For now, we'll simulate the model loading
        try {
            // Placeholder for YOLO model initialization
            // net = Dnn.readNetFromDarknet("yolov11n.cfg", "yolov11n.weights");
            
            // For demo purposes, we'll create a mock net object
            System.out.println("YOLOv11n model initialized (mock implementation)");
        } catch (Exception e) {
            System.err.println("Error initializing YOLO model: " + e.getMessage());
        }
    }

    /**
     * Initialize class names for the model (common cafeteria dishes)
     */
    private void initializeClassNames() {
        classNames = new ArrayList<>();
        classNames.add("apple"); // Example classes
        classNames.add("banana");
        classNames.add("orange");
        classNames.add("carrot");
        classNames.add("broccoli");
        classNames.add("pizza");
        classNames.add("hamburger");
        classNames.add("french_fries");
        classNames.add("hot_dog");
        classNames.add("spaghetti_bolognese");
        classNames.add("steak");
        classNames.add("chicken_curry");
        classNames.add("rice");
        classNames.add("salad");
        classNames.add("sandwich");
        classNames.add("soup");
        classNames.add("omelette");
        classNames.add("pancakes");
        classNames.add("sushi");
        classNames.add("taco");
        // Add more dishes as needed
    }

    /**
     * Process uploaded image and perform dish recognition
     */
    public RecognitionResult recognizeDish(MultipartFile imageFile) throws IOException {
        // Save uploaded image temporarily
        String fileName = saveImage(imageFile);
        String filePath = UPLOAD_DIR + fileName;
        
        // Simulate YOLO recognition
        // In real implementation, this would run inference on the model
        RecognitionResult result = simulateRecognition(filePath);
        
        // Clean up temporary file
        try {
            Files.deleteIfExists(Paths.get(filePath));
        } catch (IOException e) {
            System.err.println("Could not delete temp file: " + e.getMessage());
        }
        
        return result;
    }

    /**
     * Simulate dish recognition (in real implementation, this would run the actual model)
     */
    private RecognitionResult simulateRecognition(String imagePath) {
        Mat image = Imgcodecs.imread(imagePath);
        
        // In a real implementation, this would run detection
        // For demo purposes, we'll return a mock result based on image characteristics
        List<Detection> detections = new ArrayList<>();
        
        // Simple color-based detection simulation
        Scalar avgColor = calculateAverageColor(image);
        String detectedDish = classifyByColor(avgColor);
        
        // Check if detected dish exists in our database
        Optional<Dish> foundDish = dishRepository.findByDishDescriptionContainingIgnoreCase(detectedDish);
        
        if (foundDish.isPresent()) {
            Detection detection = new Detection(
                foundDish.get().getDishCode(),
                foundDish.get().getDishDescription()
            );
            detections.add(detection);
        } else {
            // If not found in DB, create a placeholder detection
            Detection detection = new Detection(
                "UNKNOWN_" + detectedDish.toUpperCase().replace(' ', '_'),
                detectedDish
            );
            detections.add(detection);
        }
        
        return new RecognitionResult(detections);
    }

    /**
     * Calculate average color of image (for simulation purposes)
     */
    private Scalar calculateAverageColor(Mat image) {
        Mat hsv = new Mat();
        Imgproc.cvtColor(image, hsv, Imgproc.COLOR_BGR2HSV);
        
        double[] avgHue = Core.mean(hsv).val;
        return new Scalar(avgHue);
    }

    /**
     * Classify dish based on average color (simulation)
     */
    private String classifyByColor(Scalar avgColor) {
        double hue = avgColor.val[0];
        
        if (hue >= 0 && hue < 10) return "Red Apple";
        else if (hue >= 10 && hue < 30) return "Orange";
        else if (hue >= 30 && hue < 70) return "Banana";
        else if (hue >= 70 && hue < 150) return "Green Salad";
        else if (hue >= 150 && hue <= 180) return "Purple Eggplant";
        else return "Mixed Dish";
    }

    /**
     * Save uploaded image to local storage
     */
    private String saveImage(MultipartFile file) throws IOException {
        String fileName = System.currentTimeMillis() + "_" + file.getOriginalFilename();
        Path filePath = Paths.get(UPLOAD_DIR, fileName);
        Files.write(filePath, file.getBytes());
        return fileName;
    }

    /**
     * Add or update a dish in the system
     */
    public Dish saveDish(Dish dish) {
        return dishRepository.save(dish);
    }

    /**
     * Get all dishes
     */
    public List<Dish> getAllDishes() {
        return dishRepository.findAll();
    }

    /**
     * Get dish by code
     */
    public Optional<Dish> getDishByCode(String dishCode) {
        return dishRepository.findByDishCode(dishCode);
    }

    /**
     * Delete dish by code
     */
    public boolean deleteDishByCode(String dishCode) {
        Optional<Dish> dishOpt = dishRepository.findByDishCode(dishCode);
        if (dishOpt.isPresent()) {
            dishRepository.delete(dishOpt.get());
            return true;
        }
        return false;
    }

    // Inner classes for recognition results
    public static class RecognitionResult {
        private List<Detection> detections;

        public RecognitionResult(List<Detection> detections) {
            this.detections = detections;
        }

        public List<Detection> getDetections() {
            return detections;
        }

        public void setDetections(List<Detection> detections) {
            this.detections = detections;
        }
    }

    public static class Detection {
        private String dishCode;
        private String dishDescription;

        public Detection(String dishCode, String dishDescription) {
            this.dishCode = dishCode;
            this.dishDescription = dishDescription;
        }

        public String getDishCode() {
            return dishCode;
        }

        public void setDishCode(String dishCode) {
            this.dishCode = dishCode;
        }

        public String getDishDescription() {
            return dishDescription;
        }

        public void setDishDescription(String dishDescription) {
            this.dishDescription = dishDescription;
        }
    }
}