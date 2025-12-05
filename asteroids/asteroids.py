"""
🌟 Asteroids
Destroy asteroids and survive in space!

Controls:
- Left/Right arrows to rotate
- UP arrow to thrust
- SPACE to shoot
- ESC to quit, R to restart
"""

import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

class Ship:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle = -90
        self.velocity = [0, 0]
        self.size = 20
    
    def rotate(self, direction):
        self.angle += direction * 5
    
    def thrust(self):
        rad = math.radians(self.angle)
        self.velocity[0] += math.cos(rad) * 0.3
        self.velocity[1] += math.sin(rad) * 0.3
    
    def update(self):
        self.x = (self.x + self.velocity[0]) % WIDTH
        self.y = (self.y + self.velocity[1]) % HEIGHT
        self.velocity[0] *= 0.99
        self.velocity[1] *= 0.99
    
    def draw(self, screen):
        rad = math.radians(self.angle)
        points = [
            (self.x + math.cos(rad) * self.size, self.y + math.sin(rad) * self.size),
            (self.x + math.cos(rad + 2.5) * self.size * 0.6, self.y + math.sin(rad + 2.5) * self.size * 0.6),
            (self.x + math.cos(rad - 2.5) * self.size * 0.6, self.y + math.sin(rad - 2.5) * self.size * 0.6)
        ]
        pygame.draw.polygon(screen, WHITE, points, 2)
    
    def shoot(self):
        rad = math.radians(self.angle)
        return Bullet(self.x, self.y, math.cos(rad) * 8, math.sin(rad) * 8)

class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = 60
    
    def update(self):
        self.x = (self.x + self.vx) % WIDTH
        self.y = (self.y + self.vy) % HEIGHT
        self.life -= 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 3)

class Asteroid:
    def __init__(self, x=None, y=None, size=3):
        self.x = x or random.randint(0, WIDTH)
        self.y = y or random.randint(0, HEIGHT)
        self.size = size
        self.radius = size * 15
        speed = (4 - size) * 0.5 + 1
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.points = [(random.uniform(0.7, 1.3) * self.radius * math.cos(i * 0.7),
                       random.uniform(0.7, 1.3) * self.radius * math.sin(i * 0.7)) for i in range(9)]
    
    def update(self):
        self.x = (self.x + self.vx) % WIDTH
        self.y = (self.y + self.vy) % HEIGHT
    
    def draw(self, screen):
        pts = [(self.x + p[0], self.y + p[1]) for p in self.points]
        pygame.draw.polygon(screen, WHITE, pts, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🌟 Asteroids")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        self.ship = Ship()
        self.bullets = []
        self.asteroids = [Asteroid() for _ in range(5)]
        self.score = 0
        self.lives = 3
        self.game_over = False
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.bullets.append(self.ship.shoot())
            
            keys = pygame.key.get_pressed()
            if not self.game_over:
                if keys[pygame.K_LEFT]: self.ship.rotate(-1)
                if keys[pygame.K_RIGHT]: self.ship.rotate(1)
                if keys[pygame.K_UP]: self.ship.thrust()
                
                self.ship.update()
                for b in self.bullets[:]:
                    b.update()
                    if b.life <= 0: self.bullets.remove(b)
                for a in self.asteroids: a.update()
                
                # Collision detection
                for b in self.bullets[:]:
                    for a in self.asteroids[:]:
                        if math.hypot(b.x - a.x, b.y - a.y) < a.radius:
                            self.bullets.remove(b) if b in self.bullets else None
                            self.asteroids.remove(a)
                            self.score += (4 - a.size) * 20
                            if a.size > 1:
                                self.asteroids.extend([Asteroid(a.x, a.y, a.size - 1) for _ in range(2)])
                            break
                
                for a in self.asteroids:
                    if math.hypot(self.ship.x - a.x, self.ship.y - a.y) < a.radius + 10:
                        self.lives -= 1
                        self.ship = Ship()
                        if self.lives <= 0: self.game_over = True
                        break
                
                if not self.asteroids:
                    self.asteroids = [Asteroid() for _ in range(5)]
            
            self.screen.fill(BLACK)
            if not self.game_over: self.ship.draw(self.screen)
            for b in self.bullets: b.draw(self.screen)
            for a in self.asteroids: a.draw(self.screen)
            self.screen.blit(self.font.render(f"Score: {self.score}  Lives: {self.lives}", True, WHITE), (10, 10))
            if self.game_over:
                self.screen.blit(self.font.render("GAME OVER - Press R", True, WHITE), (WIDTH//2 - 130, HEIGHT//2))
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
