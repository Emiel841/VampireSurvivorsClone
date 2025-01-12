import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Weapons/bullet.png")
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.id = "gun"
        self.mask = pygame.mask.from_surface(self.image)

        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.speed_x = dx / distance * speed
            self.speed_y = dy / distance * speed
        else:
            self.speed_x = speed
            self.speed_y = 0
    def update(self):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        if self.rect.right < 0 or self.rect.left > 1280 or self.rect.bottom < 0 or self.rect.top > 720:
            self.kill()
