import pygame
import random

class Steering:
    def __init__(self, ant):
        self.ant = ant
        self.max_force = 0.1
        self.perception_radius = 50

    def calculate_steering(self, obstacles):
        wander_force = self.wander()
        avoid_force = self.avoid_obstacles(obstacles)

        # Dynamic weighting based on the proximity to obstacles
        if avoid_force.length_squared() > 0:
            # If there's an obstacle, prioritize avoidance more heavily
            return wander_force * 0.5 + avoid_force * 2
        else:
            # Normal wandering behavior
            return wander_force * 1.5 + avoid_force

    def avoid_obstacles(self, obstacles):
        steering = pygame.math.Vector2(0, 0)
        for obstacle in obstacles:
            to_obstacle = pygame.math.Vector2(obstacle.rect.center) - self.ant.position
            distance = to_obstacle.length()
            
            closest_point = pygame.math.Vector2(
                max(obstacle.rect.left, min(self.ant.position.x, obstacle.rect.right)),
                max(obstacle.rect.top, min(self.ant.position.y, obstacle.rect.bottom))
            )
            
            to_closest = closest_point - self.ant.position
            distance_to_edge = to_closest.length()
            
            if distance_to_edge < self.ant.rect.width / 2 + 1:  # Adding 1 pixel buffer
                if distance_to_edge > 0:
                    avoidance = -to_closest.normalize() * self.max_force * 3
                else:
                    avoidance = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * self.max_force * 2
            elif distance < self.perception_radius + obstacle.rect.width / 2:
                avoidance = -to_obstacle.normalize() * (self.perception_radius - distance) / self.perception_radius
            else:
                avoidance = pygame.math.Vector2(0, 0)
            
            steering += avoidance
        
        if steering.length_squared() > 0:
            return steering.clamp_magnitude(self.max_force)
        else:
            return steering
    
    def wander(self):
        # Wandering behavior logic 
        wander_radius = 30
        wander_distance = 50
        wander_jitter = 0.5

        wander_point = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * wander_radius
        target = self.ant.position + self.ant.velocity.normalize() * wander_distance + wander_point

        desired = (target - self.ant.position).normalize() * self.ant.max_speed
        steering = desired - self.ant.velocity
        return steering.clamp_magnitude(self.max_force)

