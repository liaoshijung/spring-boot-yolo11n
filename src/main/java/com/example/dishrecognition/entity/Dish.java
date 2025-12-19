package com.example.dishrecognition.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "dishes")
public class Dish {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "dish_code", unique = true, nullable = false)
    private String dishCode;
    
    @Column(name = "dish_description", nullable = false)
    private String dishDescription;
    
    @Column(name = "image_path")
    private String imagePath;
    
    // Constructors
    public Dish() {}
    
    public Dish(String dishCode, String dishDescription, String imagePath) {
        this.dishCode = dishCode;
        this.dishDescription = dishDescription;
        this.imagePath = imagePath;
    }
    
    // Getters and setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
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
    
    public String getImagePath() {
        return imagePath;
    }
    
    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }
}