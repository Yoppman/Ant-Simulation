# food.py
import pygame
import random
import math

class FoodSpot:
    def __init__(self, x, y, radius=50):
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius
        self.food_items = []
        self.max_food = 50  # Maximum food items in one spot

    def add_food(self, amount=10):
        for _ in range(amount):
            if len(self.food_items) >= self.max_food:
                break
            # Generate food within the radius
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(0, self.radius)
            x = self.position.x + distance * math.cos(angle)
            y = self.position.y + distance * math.sin(angle)
            self.food_items.append(Food(x, y))

    def draw(self, surface):
        # Draw the food spot area (semi-transparent)
        spot_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(spot_surface, (0, 255, 0, 30), (self.radius, self.radius), self.radius)
        surface.blit(spot_surface, (self.position.x - self.radius, self.position.y - self.radius))

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, amount=10):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill((0, 255, 0))  # Green color for food
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.amount = amount

    def reduce_amount(self, amount=1):
        self.amount -= amount
        return self.amount <= 0

class Nest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((139, 69, 19))  # Brown color for nest
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.food_stored = 0

    def store_food(self, amount):
        self.food_stored += amount

class Pheromone:
    def __init__(self, x, y, strength=100, type='food'):
        self.position = pygame.math.Vector2(x, y)
        self.strength = strength
        self.type = type  # 'food' or 'home'
        self.decay_rate = 0.2  # Reduced decay rate for longer-lasting trails

    def update(self):
        self.strength -= self.decay_rate
        return self.strength <= 0

    def draw(self, surface):
        if self.type == 'food':
            color = (0, min(255, int(self.strength)), 0, min(255, int(self.strength)))
        else:  # home
            color = (min(255, int(self.strength)), 0, 0, min(255, int(self.strength)))
        
        # Create a surface with alpha for transparency
        pheromone_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(pheromone_surface, color, (2, 2), 2)
        surface.blit(pheromone_surface, (self.position.x - 2, self.position.y - 2))