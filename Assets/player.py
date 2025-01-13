from asyncio import shield

import pygame
import random
from button import Button
from bullet import Bullet
from spear import Spear
from tornado import Tornado
from Bar import Bar
from sword import Sword
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        PATH = "Assets/Player/sorcerer.png"
        WIDHT = 80
        HEIGHT = 80

        self.width = WIDHT
        self.height = HEIGHT

        self.STARTERITEM = "gun"

        #buttons
        self.button_w = 18 * 4
        self.button_h = 18 * 4

        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button(384, 640, self.button_w, self.button_h))
        self.buttons.add(Button(640, 640, self.button_w, self.button_h))
        self.buttons.add(Button(896, 640, self.button_w, self.button_h))


        self.all_weapons = ["sword", "tornado", "spear", "gun"]
        self.weapons_unlocked = [self.STARTERITEM]
        self.upgrade_list = ["sword", "tornado", "spear", "gun", "hp", "dmg", "attack speed"]

        self.upgrade_list.remove(self.STARTERITEM)
        self.sword_image = pygame.image.load("Assets/Weapons/Sword.png").convert_alpha()
        self.sword_image = pygame.transform.scale(self.sword_image, (64, 64))

        self.gun_image = pygame.image.load("Assets/Weapons/gun.png").convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, (64, 64))

        self.spear_image = pygame.image.load("Assets/Weapons/spear.png").convert_alpha()
        self.spear_image = pygame.transform.scale(self.spear_image, (64, 64))

        self.tornado_image = pygame.image.load("Assets/Weapons/tornado.png").convert_alpha()
        self.tornado_image = pygame.transform.scale(self.tornado_image, (64, 64))

        self.hp_image = pygame.image.load("Assets/Weapons/hp.png").convert_alpha()
        self.hp_image = pygame.transform.scale(self.hp_image, (64, 64))

        self.dmg_image = pygame.image.load("Assets/Weapons/damage.png").convert_alpha()
        self.dmg_image = pygame.transform.scale(self.dmg_image, (64, 64))

        self.attack_speed_image = pygame.image.load("Assets/Weapons/attack.png").convert_alpha()
        self.attack_speed_image = pygame.transform.scale(self.attack_speed_image, (64, 64))


        self.max_hp = 100
        self.hp = 100
        self.dmg = 10
        self.immune_time = 200
        self.last_hit = pygame.time.get_ticks()
        self.xp = 0
        self.max_xp = 100
        self.lvl = 0
        self.image = pygame.image.load(PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDHT, HEIGHT))
        self.no_flip = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.flipped = pygame.transform.flip(self.image, True, False)


        shield = pygame.image.load("Assets/Player/shield_in_action.png").convert_alpha()
        shield = pygame.transform.scale(shield, (120, 120))

        shield.blit(shield, (0, 0))
        shield.blit(self.no_flip, (20, 20))
        self.no_flip_shield = shield
        self.flipped_shield = pygame.transform.flip(self.no_flip_shield, True, False)

        self.shielded = False
        self.is_flipped = True
        self.upgrading = False
        self.choices = []

        self.projectiles = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.last_spear_shot = pygame.time.get_ticks()
        self.last_tornado_shot = pygame.time.get_ticks()
        self.last_sword_swing = pygame.time.get_ticks()
        self.fire_rate = 500

        #bars
        self.hp_bar = Bar(20, 20, 200, 20, self.max_hp, self.max_hp, "red", "black")
        self.xp_bar = Bar(20, 50, 150, 15, self.max_xp, 0, "green", "purple")

        self.swords = pygame.sprite.Group()
    def set_shielded_true(self):
        self.shielded = True
        self.image = self.no_flip_shield

    def heal(self):
        self.hp += 30
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.hp_bar.value = self.hp
    def lose_hp(self, amount):
        if not self.shielded:
            now = pygame.time.get_ticks()
            if now - self.last_hit > self.immune_time:
                self.hp -= amount
                self.last_hit = now
                self.hp_bar.value = self.hp
            if self.hp <= 0:
                return True
            return False
        elif self.shielded:
            self.image = self.no_flip
            self.shielded = False
            self.last_hit = pygame.time.get_ticks()

    def get_xp(self, amount):
            self.xp += amount
            if self.xp >= self.max_xp:
                while self.xp >= self.max_xp:
                    self.xp -= self.max_xp
                    self.lvl += 1
                    self.max_xp *= 1.3
                    self.xp_bar.max = self.max_xp
                    if not self.upgrading:
                        self.upgrade()
            self.xp_bar.value = self.xp

    def reasignbutton(self):
        i = -1
        for button in self.buttons:
            new_button = pygame.Surface((self.button_w, self.button_h))
            new_button.fill("white")
            new_button.blit(button.default_image, (0, 0))
            i += 1
            if self.choices[i] == "sword":
                new_button.blit(self.sword_image, (8, 8))
            elif self.choices[i] == "gun":
                new_button.blit(self.gun_image, (8, 8))
            elif self.choices[i] == "spear":
                new_button.blit(self.spear_image, (8, 8))
            elif self.choices[i] == "dmg":
                new_button.blit(self.dmg_image, (8, 8))
            elif self.choices[i] == "tornado":
                new_button.blit(self.tornado_image, (8, 8))
            elif self.choices[i] == "attack speed":
                new_button.blit(self.attack_speed_image, (8, 8))
            elif self.choices[i] == "hp":
                new_button.blit(self.hp_image, (8, 8))


            button.image = new_button


    def pick(self):
        result = []
        i = 0
        picklist = self.upgrade_list[:]
        while i < 3:
            i += 1
            p = random.randint(0, len(picklist) -1)
            result.append(picklist.pop(p))
        return result

    def upgrade(self):
        self.choices = self.pick()
        self.reasignbutton()
        self.upgrading = True

    def perform_upgrade(self, item):
        #"sword", "tornado", "spear", "gun", "hp", "dmg", "attack speed"
        if item == "sword":
            if not "sword" in self.weapons_unlocked:
                self.weapons_unlocked.append("sword")
                self.upgrade_list.remove("sword")
        elif item == "tornado":
            if not "tornado" in self.weapons_unlocked:
                self.weapons_unlocked.append("tornado")
                self.upgrade_list.remove("tornado")
        elif item == "gun":
            if not "gun" in self.weapons_unlocked:
                self.weapons_unlocked.append("gun")
                self.upgrade_list.remove("gun")
        elif item == "spear":
            if not "spear" in self.weapons_unlocked:
                self.weapons_unlocked.append("spear")
                self.upgrade_list.remove("spear")
        elif item == "dmg":
            self.dmg += 1
        elif item == "hp":
            self.hp += 30
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.hp_bar.value = self.hp
            self.hp_bar.max = self.max_hp
        elif item == "attack speed":
            self.fire_rate *= 0.93


    def update(self, velocity, screen, enemies_group):
        if not self.shielded:
            if self.is_flipped and velocity.x > 0:
                self.image = self.no_flip
                self.is_flipped = False
            if not self.is_flipped and velocity.x < 0:
                self.image = self.flipped
                self.is_flipped = True
            self.rect.move_ip(velocity)
        else:
            if self.is_flipped and velocity.x > 0:
                self.image = self.no_flip_shield
                self.is_flipped = False
            if not self.is_flipped and velocity.x < 0:
                self.image = self.flipped_shield
                self.is_flipped = True
            self.rect.move_ip(velocity)


        if self.upgrading:
            self.buttons.update()
            self.buttons.draw(screen)
            i = -1
            for button in self.buttons:
                #pygame.draw.rect(screen, "red", button.rect)
                i += 1
                if button.click():
                    self.upgrading = False
                    self.perform_upgrade(self.choices[i])
                    break
            keys = pygame.key.get_pressed()

            if keys[pygame.K_1]: i = 0
            elif keys[pygame.K_2]: i = 1
            elif keys[pygame.K_3]: i = 2

        if "gun" in self.weapons_unlocked:
            self.gun_attack(enemies_group)

        if "spear" in self.weapons_unlocked:
            self.spear_attack(enemies_group)

        if "tornado" in self.weapons_unlocked:
            self.tornado_attack(enemies_group)

        if "sword" in self.weapons_unlocked:
            self.sword_attack()

        self.swords.update(not self.is_flipped, self.rect.centerx, self.rect.centery)
        self.swords.draw(screen)
        self.projectiles.update()
        self.projectiles.draw(screen)
        self.hp_bar.draw(screen)
        self.xp_bar.draw(screen)


    def gun_attack(self, targets):

        now = pygame.time.get_ticks()
        if now - self.last_shot < self.fire_rate:
            return
        self.last_shot = now

        if targets:
            closest_enemy = min(targets, key=lambda enemy: math.hypot(self.rect.x-enemy.rect.x, self.rect.y-enemy.rect.y))
            bullet = Bullet(self.rect.centerx, self.rect.centery, closest_enemy.rect.centerx,
                            closest_enemy.rect.centery)
            self.projectiles.add(bullet)

    def spear_attack(self, targets):
        now = pygame.time.get_ticks()
        if now - self.last_spear_shot < self.fire_rate * 3:
            return
        self.last_spear_shot = now

        if targets:
            closest_enemy = min(targets,
                                key=lambda enemy: math.hypot(self.rect.x - enemy.rect.x, self.rect.y - enemy.rect.y))
            spear = Spear(self.rect.centerx, self.rect.centery, closest_enemy.rect.centerx,
                            closest_enemy.rect.centery)
            self.projectiles.add(spear)

    def tornado_attack(self, targets):
        now = pygame.time.get_ticks()
        if now - self.last_tornado_shot < self.fire_rate * 4:
            return
        self.last_tornado_shot = now

        if targets:
            closest_enemy = min(targets,
                                key=lambda enemy: math.hypot(self.rect.x - enemy.rect.x, self.rect.y - enemy.rect.y))
            tornado = Tornado(self.rect.centerx, self.rect.centery, closest_enemy.rect.centerx,
                          closest_enemy.rect.centery)
            self.projectiles.add(tornado)
    def sword_attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_sword_swing < self.fire_rate:
            return
        self.last_sword_swing = now

        self.swords.add(Sword(self.rect.centerx, self.rect.centery))



