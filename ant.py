import pygame
import random
from steering import Steering

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 0, 0))  # Black color for ants
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.max_speed = 2
        self.steering = Steering(self)

    def update(self, obstacles):
        # Apply steering behaviors
        wander_force = self.steering.wander()
        avoid_force = self.steering.avoid_obstacles(obstacles)
        
        # Combine forces (you can adjust the weights)
        steering = wander_force + avoid_force * 2
        
        self.velocity += steering
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize() * self.max_speed
        else:
            # If velocity becomes zero, give it a small random direction
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * self.max_speed
        
        # Update position
        new_position = self.position + self.velocity
        
        # Check for collisions with obstacles
        collision = False
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(new_position):
                collision = True
                break
        
        if collision:
            # If collision detected, find a safe direction to move
            for angle in range(0, 360, 10):  # Check every 10 degrees
                test_velocity = pygame.math.Vector2(1, 0).rotate(angle) * self.max_speed
                test_position = self.position + test_velocity
                if not any(obstacle.rect.collidepoint(test_position) for obstacle in obstacles):
                    self.velocity = test_velocity
                    new_position = test_position
                    break
            else:
                # If no safe direction found, don't move
                return
        
        # Update position
        self.position = new_position
        self.rect.center = self.position

        # Wrap around screen edges
        self.position.x %= self.screen_width
        self.position.y %= self.screen_height
        self.rect.center = self.position