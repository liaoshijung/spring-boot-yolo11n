package com.example.dishrecognition.repository;

import com.example.dishrecognition.entity.Dish;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DishRepository extends JpaRepository<Dish, Long> {
    Optional<Dish> findByDishCode(String dishCode);
    Optional<Dish> findByDishDescriptionContainingIgnoreCase(String description);
}