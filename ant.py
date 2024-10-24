# ant.py
import pygame
import random
import math
from steering import Steering
from food import Pheromone

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height, nest):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.max_speed = 2
        self.steering = Steering(self)
        
        # Modified attributes for anti-circling
        self.carrying_food = False
        self.nest = nest
        self.pheromone_drop_interval = 20
        self.pheromone_timer = 0
        self.perception_radius = 100
        self.exploration_bias = random.uniform(0.8, 1.5)
        self.last_direction_change = 0
        self.direction_change_interval = random.randint(50, 150)
        self.has_found_food = False
        self.last_food_position = None
        self.returning_to_food = False
        self.successful_trip = False
        
        # Anti-circling attributes
        self.movement_memory = []
        self.memory_length = 50 # Increase memory length to have more data points to evaluate if stuck
        self.stuck_threshold = 60 # Increase the threshold for detecting if the ant is stuck
        self.last_stuck_check = 0
        self.stuck_check_interval = 20
        self.current_direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.direction_persistence = random.randint(30, 60)
        self.direction_timer = 0

    def find_nearby_pheromones(self, pheromones, type_to_follow):
        nearby = []
        for p in pheromones:
            distance = (self.position - p.position).length()
            if distance < self.perception_radius:
                nearby.append((p, distance))
        return nearby

    def handle_food_collection(self, foods):
        if not self.carrying_food:
            for food in foods:
                if self.rect.colliderect(food.rect):
                    self.carrying_food = True
                    self.has_found_food = True
                    self.last_food_position = pygame.math.Vector2(food.position)
                    self.returning_to_food = False
                    if food.reduce_amount():
                        foods.remove(food)
                    self.image.fill((255, 0, 0))  # Red color when carrying food
                    return

    def handle_food_delivery(self):
        if self.carrying_food:
            distance_to_nest = (self.position - self.nest.position).length()
            if distance_to_nest < 20:  # Nest radius
                self.carrying_food = False
                self.nest.store_food(1)
                self.image.fill((0, 0, 0))  # Back to black when not carrying food
                self.successful_trip = True
                self.returning_to_food = True
                self.exploration_bias = 0.3

    def drop_pheromone(self, pheromones):
        if self.pheromone_timer <= 0:
            strength = 20  # Base pheromone strength
            pheromone_type = 'food'

            if self.carrying_food:
                strength = 300  # Strong pheromone when carrying food
            elif self.successful_trip and self.returning_to_food:
                strength = 200  # Strong pheromone when returning to known food
            elif self.has_found_food:
                strength = 100  # Medium strength for experienced ants

            pheromones.append(Pheromone(self.position.x, self.position.y, strength, pheromone_type))
            self.pheromone_timer = self.pheromone_drop_interval
        else:
            self.pheromone_timer -= 1

    def is_stuck(self):
        if len(self.movement_memory) < self.memory_length:
            return False
            
        center = pygame.math.Vector2(0, 0)
        for pos in self.movement_memory:
            center += pos
        center /= len(self.movement_memory)
        
        avg_distance = sum((pos - center).length() for pos in self.movement_memory) / len(self.movement_memory)
        return avg_distance < self.stuck_threshold

    def update_movement_memory(self):
        self.movement_memory.append(pygame.math.Vector2(self.position))
        if len(self.movement_memory) > self.memory_length:
            self.movement_memory.pop(0)

    def calculate_pheromone_influence(self, pheromones):
        nearby = self.find_nearby_pheromones(pheromones, 'food')
        if not nearby:
            return pygame.math.Vector2(0, 0)

        weighted_pos = pygame.math.Vector2(0, 0)
        total_weight = 0

        for pheromone, distance in nearby:
            if distance < 10:  # Ignore very close pheromones
                continue
                
            weight = (pheromone.strength / max(distance, 1)) * random.uniform(1, 1.5)
            # Increase weighting for pheromones if the ant has found food
            if self.carrying_food:
                weight *= 15  # Ants carrying food should follow pheromones more strongly
            weighted_pos += pheromone.position * weight
            total_weight += weight

        if total_weight > 0:
            weighted_pos /= total_weight
            direction = (weighted_pos - self.position).normalize()
            random_offset = pygame.math.Vector2(random.uniform(-0.3, 0.3), 
                                              random.uniform(-0.3, 0.3))
            direction += random_offset
            return direction.normalize()
            
        return pygame.math.Vector2(0, 0)

    def update(self, obstacles, foods, pheromones):
        self.handle_food_collection(foods)
        self.handle_food_delivery()
        self.drop_pheromone(pheromones)
        
        # Update movement memory and check for circling
        self.update_movement_memory()
        
        # Update direction persistence
        self.direction_timer += 1
        if self.direction_timer >= self.direction_persistence:
            self.direction_timer = 0
            self.direction_persistence = random.randint(30, 60)
            self.current_direction = pygame.math.Vector2(random.uniform(-1, 1), 
                                                       random.uniform(-1, 1)).normalize()

        # Calculate base forces
        wander_force = self.steering.wander()
        avoid_force = self.steering.avoid_obstacles(obstacles) * 2
        
        # Calculate movement force
        movement_force = pygame.math.Vector2(0, 0)
        
        if self.carrying_food:
            # Head straight back to nest with some randomness
            to_nest = self.nest.position - self.position
            if to_nest.length_squared() > 0:
                movement_force = to_nest.normalize() * 2.0
                movement_force += pygame.math.Vector2(random.uniform(-0.1, 0.1), 
                                                    random.uniform(-0.1, 0.1))
        elif self.returning_to_food and self.last_food_position:
            to_food = self.last_food_position - self.position
            if to_food.length_squared() > 0:
                movement_force = to_food.normalize() * 1.5
                movement_force += pygame.math.Vector2(random.uniform(-0.2, 0.2), 
                                                    random.uniform(-0.2, 0.2))
                
                if to_food.length() < 20 and not any(food.rect.collidepoint(self.position) for food in foods):
                    self.returning_to_food = False
                    self.exploration_bias = random.uniform(0.6, 0.9)
        else:
            pheromone_force = self.calculate_pheromone_influence(pheromones)
            movement_force = pheromone_force * (1.2 if self.has_found_food else 0.4)

        # Check if stuck in circles
        if self.is_stuck() and not self.carrying_food:
            self.current_direction = pygame.math.Vector2(random.uniform(-1, 1), 
                                                       random.uniform(-1, 1)).normalize()
            self.exploration_bias = min(self.exploration_bias * 1.5, 0.9)
            wander_force = self.current_direction * 2.0
            movement_force *= 0.2

        if not self.carrying_food and not self.returning_to_food:
            self.exploration_bias = random.uniform(1.0, 1.5)  # Strong exploration when idle
        elif self.successful_trip:
            self.exploration_bias = 0.3  # Reduce exploration after successful trip

        # Combine forces
        if self.carrying_food:
            steering = (avoid_force + 
                       movement_force * 2.0 + 
                       self.current_direction * 0.3)
        elif self.returning_to_food:
            steering = (avoid_force + 
                       movement_force * 1.5 + 
                       self.current_direction * 0.5)
        else:
            steering = (wander_force * self.exploration_bias + 
                       avoid_force + 
                       movement_force * (0.8 if self.has_found_food else 0.3) +
                       self.current_direction * 0.4)

        # Update velocity
        self.velocity += steering
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize() * self.max_speed
            self.velocity += pygame.math.Vector2(random.uniform(-0.1, 0.1), 
                                              random.uniform(-0.1, 0.1))

        # Update position with collision checking
        new_position = self.position + self.velocity
        
        collision = False
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(new_position):
                collision = True
                break
        
        if collision:
            for angle in range(0, 360, 10):
                test_velocity = pygame.math.Vector2(1, 0).rotate(angle) * self.max_speed
                test_position = self.position + test_velocity
                if not any(obstacle.rect.collidepoint(test_position) for obstacle in obstacles):
                    self.velocity = test_velocity
                    new_position = test_position
                    break
            else:
                return
        
        self.position = new_position
        self.rect.center = self.position
        self.position.x %= self.screen_width
        self.position.y %= self.screen_height
        self.rect.center = self.position