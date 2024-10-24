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
from ant import Ant
from obstacle import Obstacle

# Screen dimensions
screen_width = 800
screen_height = 600


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

def main():
    # Create obstacles
    obstacles = pygame.sprite.Group()
    for i in range(15):
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
                ants.add(Ant(x, y, screen_width, screen_height))
                break

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update ants
        ants.update(obstacles)

        # Draw everything
        screen.fill((255, 255, 255))  # White background
        obstacles.draw(screen)
        ants.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()