import pygame
import math

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=2):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Weapons/spear_projectile.png").convert_alpha()
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (64, 64))



        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.speed_x = dx / distance * speed
            self.speed_y = dy / distance * speed
        else:
            self.speed_x = speed
            self.speed_y = 0


        self.image = pygame.transform.rotate(self.image, math.degrees(math.atan2(dx, dy)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.mask = pygame.mask.from_surface(self.image)

        self.id = "spear"


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right < 0 or self.rect.left > 1280 or self.rect.bottom < 0 or self.rect.top > 720:
            self.kill()
