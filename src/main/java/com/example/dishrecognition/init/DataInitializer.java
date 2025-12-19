package com.example.dishrecognition.init;

import com.example.dishrecognition.entity.Dish;
import com.example.dishrecognition.repository.DishRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private DishRepository dishRepository;

    @Override
    public void run(String... args) throws Exception {
        // Initialize with some sample dishes
        if (dishRepository.count() == 0) {  // Only initialize if no dishes exist
            dishRepository.save(new Dish("DISH_001", "Red Apple", "images/apples.jpg"));
            dishRepository.save(new Dish("DISH_002", "Banana", "images/bananas.jpg"));
            dishRepository.save(new Dish("DISH_003", "Orange", "images/oranges.jpg"));
            dishRepository.save(new Dish("DISH_004", "Grilled Chicken", "images/chicken.jpg"));
            dishRepository.save(new Dish("DISH_005", "Beef Steak", "images/steak.jpg"));
            dishRepository.save(new Dish("DISH_006", "Vegetable Salad", "images/salad.jpg"));
            dishRepository.save(new Dish("DISH_007", "Spaghetti Bolognese", "images/spaghetti.jpg"));
            dishRepository.save(new Dish("DISH_008", "Pizza Margherita", "images/pizza.jpg"));
            dishRepository.save(new Dish("DISH_009", "Rice Bowl", "images/rice.jpg"));
            dishRepository.save(new Dish("DISH_010", "Sushi Platter", "images/sushi.jpg"));
            
            System.out.println("Sample dishes initialized successfully!");
        }
    }
}