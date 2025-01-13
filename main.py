import pygame
from player import Player
from enemy import Enemy
from Shield import Shield
from Medkit import Medkit
import random

pygame.init()

screen = pygame.display.set_mode((1280, 720))

velocity = pygame.math.Vector2(0, 0)
speed = 2

player = Player(640, 360)


running = True

enemies = pygame.sprite.Group()

basic_enemy_hp = 40
last_spawn = 0
spawn_time = 2400

background_tile = pygame.image.load("Assets/Bg/background.png").convert_alpha()
background_tile = pygame.transform.scale(background_tile, (128, 128))
background_surface = pygame.Surface((1280, 720))
wh = 128

chungus_chance = 8
tank_chance = 25
red_slime_chance = 25

previous_chance_increase = pygame.time.get_ticks()

for i in range(720//wh+1):
    y = i * wh
    for j in range(1280//wh):
        x = j * wh
        background_surface.blit(background_tile, (x, y))

projectiles = pygame.sprite.Group()
pickups = pygame.sprite.Group()

last_pickup_spawn = pygame.time.get_ticks()
pickup_spawn_time = 18000

def pickup_spawn_manager(last_pickup_spawn):
    if len(pickups) <= 2:
        now = pygame.time.get_ticks()

        if now - last_pickup_spawn > pickup_spawn_time:
            last_pickup_spawn = now
            if random.randint(0, 1) == 0:
                pickups.add(Shield(random.randint(32, 1248), random.randint(32, 688)))
            else:
                pickups.add(Medkit(random.randint(32, 1248), random.randint(32, 688)))

    return last_pickup_spawn


def enemy_spawn_manager(last_spawn):

    now = pygame.time.get_ticks()

    xoffsetter = random.randint(0, 4)
    yoffsetter = random.randint(0, 4)
    x, y = 0, 0
    if xoffsetter == 1: x = 1480
    elif xoffsetter == 2: x = -1480
    elif xoffsetter == 3: x = -80

    if yoffsetter == 1: y = 920
    elif yoffsetter == 2: y = -920
    elif yoffsetter == 3: y = -80

    if random.randint(0, 1) == 0:
        x = random.randint(0, 1480)
    else:
        y = random.randint(0, 920)

    if now - last_spawn >= spawn_time:
        chungus = random.randint(0, 100)
        if chungus > 0 and chungus < tank_chance:
            tank = Enemy(x, y, 128, 128, 120)
            enemies.add(tank)
        elif chungus > tank_chance and chungus < chungus_chance+tank_chance and player.lvl > 0:
            enemies.add(Enemy(x, y, 256, 256, 250))
        elif chungus > chungus_chance+tank_chance and chungus < chungus_chance+tank_chance+red_slime_chance and player.lvl > 1:
            enemies.add(Enemy(x, y, 80, 80, 85))
        else:
            enemies.add(Enemy(x, y, 80, 80, 65))
        last_spawn = pygame.time.get_ticks()
    return last_spawn

def mask_collision(sprite1, sprite2):
    offset = (sprite2.rect.x - sprite1.rect.x, sprite2.rect.y - sprite1.rect.y)
    return sprite1.mask.overlap(sprite2.mask, offset) is not None



def draw():
    screen.blit(background_surface, (0, 0))
    screen.blit(player.image, player.rect)
    if pickups:
        pickups.draw(screen)
    if enemies:
        enemies.draw(screen)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    velocity.x = 0
    velocity.y = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        direction = 2
        velocity.y = -speed
    elif keys[pygame.K_s]:
        direction = 1
        velocity.y = speed
    if keys[pygame.K_a]:
        direction = 4
        velocity.x = -speed
    elif keys[pygame.K_d]:
        direction = 3
        velocity.x = speed
    if velocity:
        velocity = velocity.normalize()
        velocity *= speed
    draw()
    if pickups:
        pickups.update()
    enemies.update(player.rect, enemies)
    player.update(velocity, screen, enemies)

    projectiles.add(player.projectiles)
    projectiles.add(player.swords)

    hit_pickups = pygame.sprite.spritecollide(player, pickups, False)
    for hit_pickup in hit_pickups:
        if hit_pickup.id == "shield":
            player.set_shielded_true()
        elif hit_pickup.id == "medkit":
            player.heal()
        hit_pickup.kill()

    for projectile in projectiles:
        hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False, collided=mask_collision)
        for enemy in hit_enemies:
            player.get_xp(enemy.take_damage(player.dmg, projectile.id))
            if projectile.id != "tornado" and projectile.id != "sword":
                projectile.kill()

    for enemy in enemies:
        if pygame.sprite.collide_mask(player, enemy):
            if player.shielded:
                enemy.kill()
                player.lose_hp(enemy.dmg)
            elif player.lose_hp(enemy.dmg): running = False
            break

    pygame.display.update()

    last_pickup_spawn = pickup_spawn_manager(last_pickup_spawn)

    last_spawn = enemy_spawn_manager(last_spawn)
    spawn_time *= 0.99998
    spawn_time -= 0.001

    now = pygame.time.get_ticks()
    if now - previous_chance_increase >= 12000:
        chungus_chance += 1
        tank_chance += 1
        previous_chance_increase = now

pygame.quit()
