# obstacle.py
import pygame
import math
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 128))  # Grey color for obstacles
        self.rect = self.image.get_rect(topleft=(x, y))

def heart_shape_coordinates(center_x, center_y, scale, num_points=100):
    points = []
    for i in range(num_points):
        t = i * (2 * math.pi) / num_points  # Vary t from 0 to 2*pi
        x = 16 * math.sin(t)**3  # Parametric equation for x
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)  # Parametric equation for y
        x = center_x + int(scale * x)
        y = center_y - int(scale * y)  # Invert y-axis
        points.append((x, y))
    return points

def circle_coordinates(center_x, center_y, radius, num_points=50):
    points = []
    for i in range(num_points):
        angle = i * (2 * math.pi) / num_points
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        points.append((x, y))
    return points

def square_coordinates(center_x, center_y, side_length, num_points=30):
    points = []
    half_side = side_length // 2
    for i in range(num_points):
        if i < num_points // 4:
            x = center_x - half_side + i * (side_length // (num_points // 4))
            y = center_y - half_side
        elif i < num_points // 2:
            x = center_x + half_side
            y = center_y - half_side + (i - num_points // 4) * (side_length // (num_points // 4))
        elif i < 3 * num_points // 4:
            x = center_x + half_side - (i - num_points // 2) * (side_length // (num_points // 4))
            y = center_y + half_side
        else:
            x = center_x - half_side
            y = center_y + half_side - (i - 3 * num_points // 4) * (side_length // (num_points // 4))
        points.append((x, y))
    return points

def random_coordinates(screen_width, screen_height, num_points=50):
    points = []
    for _ in range(num_points):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        points.append((x, y))
    return points

def generate_obstacles(obstacles, screen_width, screen_height):
    # Choose a shape type at random
    shape_choice = random.choice(['heart', 'circle', 'square', 'random'])
    print(f"Chosen shape: {shape_choice}")

    size = 10; # Default size of obstacles
    
    
    if shape_choice == 'heart':
        points = heart_shape_coordinates(screen_width // 2, screen_height // 2, scale=15, num_points=50)
        size = 10;
    elif shape_choice == 'circle':
        points = circle_coordinates(screen_width // 2, screen_height // 2, radius=250, num_points=50)
        size = 10;
    elif shape_choice == 'square':
        points = square_coordinates(screen_width // 2, screen_height // 2, side_length=450, num_points=50)
        size = 12;
    else:
        points = random_coordinates(screen_width, screen_height, num_points=30)
        size = 20;

    for (x, y) in points:
        width = height = size;
        obstacles.add(Obstacle(x, y, width, height))