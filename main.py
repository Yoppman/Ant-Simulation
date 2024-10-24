# main.py
import pygame
import random
import math
from ant import Ant
from obstacle import Obstacle, generate_obstacles
from food import Food, Nest, Pheromone, FoodSpot
from utils import is_valid_nest_position, is_valid_food_spot, create_food_spots

# Screen dimensions
screen_width = 800
screen_height = 600

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ant Colony Simulation")

def main():
    # Create obstacle group
    obstacles = pygame.sprite.Group()
    generate_obstacles(obstacles, screen_width, screen_height)

    # Create a valid nest position
    while True:
        nest_x = random.randint(50, screen_width - 50)
        nest_y = random.randint(50, screen_height - 50)
        if is_valid_nest_position(nest_x, nest_y, obstacles):
            break
    nest = Nest(nest_x, nest_y)
    nest_group = pygame.sprite.GroupSingle(nest)


    # Create food spots and food sources
    food_spots = create_food_spots(2, obstacles, screen_width, screen_height)
    foods = pygame.sprite.Group()
    for spot in food_spots:
        for food_item in spot.food_items:
            foods.add(food_item)

    # Create ants
    ants = pygame.sprite.Group()
    for i in range(30):
        while True:
            x = nest.rect.centerx + random.randint(-20, 20)
            y = nest.rect.centery + random.randint(-20, 20)
            if not any(obstacle.rect.collidepoint(x, y) for obstacle in obstacles):
                ants.add(Ant(x, y, screen_width, screen_height, nest))
                break

    # Initialize pheromone list
    pheromones = []

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    replenish_timer = 0
    replenish_interval = 300  # Frames between food replenishment

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if is_valid_food_spot(mouse_x, mouse_y, obstacles, food_spots):
                        # Create new food spot
                        new_spot = FoodSpot(mouse_x, mouse_y)
                        new_spot.add_food(30)  # Add initial food items
                        food_spots.append(new_spot)
                        # Add food items to the foods group
                        for food_item in new_spot.food_items:
                            foods.add(food_item)

        # Update ants
        for ant in ants:
            ant.update(obstacles, foods, pheromones)

        # Update pheromones
        pheromones = [p for p in pheromones if not p.update()]

        # Replenish food periodically
        replenish_timer += 1
        if replenish_timer >= replenish_interval:
            replenish_timer = 0
            for spot in food_spots:
                if len(spot.food_items) < spot.max_food // 2:  # Replenish if below half capacity
                    spot.add_food(5)  # Add 5 new food items
                    for food_item in spot.food_items:
                        if food_item not in foods:
                            foods.add(food_item)

        # Draw everything
        screen.fill((255, 255, 255))  # White background
        
        # Draw food spots first
        for spot in food_spots:
            spot.draw(screen)
        
        # Draw pheromones
        for pheromone in pheromones:
            pheromone.draw(screen)
        
        # Draw other sprites
        obstacles.draw(screen)
        foods.draw(screen)
        nest_group.draw(screen)
        ants.draw(screen)

        # Draw food counter
        food_text = font.render(f"Food Stored: {nest.food_stored}", True, (0, 0, 0))
        screen.blit(food_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()