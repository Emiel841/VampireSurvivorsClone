import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Enemies/slime.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.dmg = 10
        self.hp = hp
        self.xp_worth = self.hp//4
        self.mask = pygame.mask.from_surface(self.image)
        self.last_hit = pygame.time.get_ticks()
        self.hit_by_sword = False
        self.last_sword_hit = pygame.time.get_ticks()
        self.is_tank = False
        tank_image = pygame.image.load("Assets/Enemies/tank.png").convert_alpha()
        tank_image = pygame.transform.scale(tank_image, (100, 100))
        tank_image = pygame.transform.rotate(tank_image, 90)
        if self.hp == 120:
            self.is_tank = True
            self.image = tank_image
            self.dmg = 30
        elif self.hp == 85:
            self.image = pygame.image.load("Assets/Enemies/red_slime.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (w, h))
            self.speed = 1.8
            self.dmg = 15
        elif self.hp > 120:
            self.dmg = 25

        self.original = self.image
        self.rotatel = pygame.transform.rotate(self.image, 90)
        self.rotater = pygame.transform.rotate(self.image, -90)
        self.rotated = pygame.transform.rotate(self.image, 180)

    def take_damage(self, damage, id):
        if id  == "spear":
            damage *= 4
        if id == "tornado":
            now = pygame.time.get_ticks()
            if now - self.last_hit > 250:
                self.last_hit = now
                damage *= 2
            else:
                damage = 0
        if id == "sword":
            now = pygame.time.get_ticks()
            if now - self.last_sword_hit > 250:
                self.last_sword_hit = now
            else:
                damage = 0
        elif id == "gun":
            damage *= 2


        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            return self.xp_worth
        return 0

    def update(self, player, enemies_group):
        player_x, player_y = player.center

        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery

        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance

        if self.is_tank:
            if dx >= dy:
                if dx > 0:
                    self.image = self.rotatel
                elif dx <= 0:
                    self.image = self.rotater
            elif dy > dx:
                if dy >= 0:
                    self.image = self.original
                elif dy < 0:
                    self.image = self.rotated




        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        for other_enemy in enemies_group:
            if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                overlap_vector = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(other_enemy.rect.center)
                if overlap_vector.length() != 0:
                    overlap_vector = overlap_vector.normalize()
                    self.rect.x += overlap_vector.x * self.speed
                    self.rect.y += overlap_vector.y * self.speed


