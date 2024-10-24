import pygame
import random
from food import FoodSpot

def is_valid_food_spot(x, y, obstacles, food_spots, min_distance=200):
    # Check if spot is too close to obstacles
    for obstacle in obstacles:
        if pygame.math.Vector2(x - obstacle.rect.centerx, 
                             y - obstacle.rect.centery).length() < 100:
            return False
            
    # Check if spot is too close to other food spots
    for spot in food_spots:
        if pygame.math.Vector2(x - spot.position.x, 
                             y - spot.position.y).length() < min_distance:
            return False
    
    return True

def create_food_spots(num_spots, obstacles, screen_width, screen_height):
    food_spots = []
    min_distance = 200  # Minimum distance between food spots
    
    while len(food_spots) < num_spots:
        x = random.randint(100, screen_width - 100)
        y = random.randint(100, screen_height - 100)
        
        if is_valid_food_spot(x, y, obstacles, food_spots, min_distance):
            spot = FoodSpot(x, y)
            spot.add_food(30)  # Add initial food items
            food_spots.append(spot)
    
    return food_spots

def is_valid_nest_position(x, y, obstacles, min_distance=100):
    # Check if the nest's position is too close to any obstacle
    for obstacle in obstacles:
        if pygame.math.Vector2(x - obstacle.rect.centerx, y - obstacle.rect.centery).length() < min_distance:
            return False
    return True