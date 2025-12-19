package com.example.dishrecognition.controller;

import com.example.dishrecognition.entity.Dish;
import com.example.dishrecognition.service.DishRecognitionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/dish")
@CrossOrigin(origins = "*") // Allow cross-origin requests for testing
public class DishRecognitionController {

    @Autowired
    private DishRecognitionService dishRecognitionService;

    /**
     * Endpoint to recognize dish from uploaded image
     */
    @PostMapping("/recognize")
    public ResponseEntity<?> recognizeDish(@RequestParam("image") MultipartFile imageFile) {
        try {
            if (imageFile.isEmpty()) {
                return ResponseEntity.badRequest().body("Please select an image file");
            }

            // Validate file type
            String contentType = imageFile.getContentType();
            if (contentType == null || !contentType.startsWith("image/")) {
                return ResponseEntity.badRequest().body("Invalid file type. Please upload an image.");
            }

            // Perform dish recognition
            DishRecognitionService.RecognitionResult result = dishRecognitionService.recognizeDish(imageFile);

            // Return only dish code and description as requested
            return ResponseEntity.ok(result.getDetections());
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error processing image: " + e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Unexpected error: " + e.getMessage());
        }
    }

    /**
     * Endpoint to add or update a dish
     */
    @PostMapping("/dish")
    public ResponseEntity<?> addDish(@RequestBody Dish dish) {
        try {
            Dish savedDish = dishRecognitionService.saveDish(dish);
            return ResponseEntity.ok(savedDish);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error saving dish: " + e.getMessage());
        }
    }

    /**
     * Endpoint to get all dishes
     */
    @GetMapping("/dishes")
    public ResponseEntity<List<Dish>> getAllDishes() {
        List<Dish> dishes = dishRecognitionService.getAllDishes();
        return ResponseEntity.ok(dishes);
    }

    /**
     * Endpoint to get dish by code
     */
    @GetMapping("/dish/{dishCode}")
    public ResponseEntity<?> getDishByCode(@PathVariable String dishCode) {
        Optional<Dish> dish = dishRecognitionService.getDishByCode(dishCode);
        if (dish.isPresent()) {
            return ResponseEntity.ok(dish.get());
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * Endpoint to delete dish by code
     */
    @DeleteMapping("/dish/{dishCode}")
    public ResponseEntity<?> deleteDish(@PathVariable String dishCode) {
        boolean deleted = dishRecognitionService.deleteDishByCode(dishCode);
        if (deleted) {
            return ResponseEntity.ok().body("Dish deleted successfully");
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * Endpoint to update an existing dish
     */
    @PutMapping("/dish/{dishCode}")
    public ResponseEntity<?> updateDish(@PathVariable String dishCode, @RequestBody Dish updatedDish) {
        // First find the existing dish
        Optional<Dish> existingDishOpt = dishRecognitionService.getDishByCode(dishCode);
        if (!existingDishOpt.isPresent()) {
            return ResponseEntity.notFound().build();
        }

        Dish existingDish = existingDishOpt.get();
        // Update fields
        existingDish.setDishDescription(updatedDish.getDishDescription());
        existingDish.setImagePath(updatedDish.getImagePath());

        try {
            Dish savedDish = dishRecognitionService.saveDish(existingDish);
            return ResponseEntity.ok(savedDish);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error updating dish: " + e.getMessage());
        }
    }
}