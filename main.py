# Slightly modified example for Ant Simulation
# created by Generative AI (Google)

"""
Instructions for installing Pygame: https://www.pygame.org/wiki/GettingStarted

Overview:
- Imports: Import necessary libraries (Pygame for graphics and random for ant movement).
- Initialization: Initialize Pygame, set up the game window, and define colors.
- Ant class: Create an Ant class that inherits from pygame.sprite.Sprite.
             This class defines the ant's appearance, movement, and behavior.
- Create ants: Create a group of ants and initialize their positions randomly.
- Game loop: The main game loop handles events, updates the ants' positions, and
             draws them on the screen.

Ideas for Enhancement:
- Food: Add food sources that ants can collect and bring back to a nest.
- Pheromones: Implement pheromone trails that ants follow to find food and the nest.
- Different ant types: Create different types of ants with specialized roles (e.g., workers, soldiers).
- Obstacles: Add obstacles that ants must navigate around.
- Improved movement: Make the ant movement more realistic using steering behaviors or other algorithms.
"""

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ant Simulation with Obstacles")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128, 128, 128)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(grey)
        self.rect = self.image.get_rect(topleft=(x, y))

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(black)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.max_speed = 2
        self.max_force = 0.1
        self.perception_radius = 30

    def update(self, obstacles):
        # Apply steering behaviors
        wander_force = self.wander()
        avoid_force = self.avoid_obstacles(obstacles)
        
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
        self.position.x %= screen_width
        self.position.y %= screen_height
        self.rect.center = self.position

    def avoid_obstacles(self, obstacles):
        steering = pygame.math.Vector2(0, 0)
        for obstacle in obstacles:
            to_obstacle = pygame.math.Vector2(obstacle.rect.center) - self.position
            distance = to_obstacle.length()
            
            # Calculate the closest point on the obstacle's edge to the ant
            closest_point = pygame.math.Vector2(
                max(obstacle.rect.left, min(self.position.x, obstacle.rect.right)),
                max(obstacle.rect.top, min(self.position.y, obstacle.rect.bottom))
            )
            
            # Vector from the ant to the closest point on the obstacle
            to_closest = closest_point - self.position
            distance_to_edge = to_closest.length()
            
            # If the ant is very close to or inside the obstacle, apply a strong avoidance force
            if distance_to_edge < self.rect.width / 2 + 1:  # Adding 1 pixel buffer
                if distance_to_edge > 0:
                    avoidance = -to_closest.normalize() * self.max_force * 2  # Stronger force
                else:
                    # If distance is zero, choose a random direction to move away
                    avoidance = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * self.max_force * 2
            elif distance < self.perception_radius + obstacle.rect.width / 2:
                # Normal avoidance behavior
                avoidance = -to_obstacle.normalize() * (self.perception_radius - distance) / self.perception_radius
            else:
                avoidance = pygame.math.Vector2(0, 0)
            
            steering += avoidance
        
        # Check if steering vector is non-zero before clamping
        if steering.length_squared() > 0:
            return steering.clamp_magnitude(self.max_force)
        else:
            return steering  # Return zero vector if no steering is applied

    def wander(self):
        # Simple wandering behavior
        wander_radius = 3
        wander_distance = 5
        wander_jitter = 0.5

        wander_point = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * wander_radius
        target = self.position + self.velocity.normalize() * wander_distance + wander_point

        desired = (target - self.position).normalize() * self.max_speed
        steering = desired - self.velocity
        return steering.clamp_magnitude(self.max_force)

def main():
    # Create obstacles
    obstacles = pygame.sprite.Group()
    for i in range(15):  # Create 5 random obstacles
        x = random.randint(0, screen_width - 50)
        y = random.randint(0, screen_height - 50)
        width = random.randint(20, 60)
        height = random.randint(20, 60)
        obstacles.add(Obstacle(x, y, width, height))
    # Create ants
    ants = pygame.sprite.Group()
    for i in range(20):
        while True:
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            if not any(obstacle.rect.collidepoint(x, y) for obstacle in obstacles):
                ants.add(Ant(x, y))
                break



    # Game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update ants
        for ant in ants:
            ant.update(obstacles)

        # Draw everything
        screen.fill(white)
        obstacles.draw(screen)
        ants.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()