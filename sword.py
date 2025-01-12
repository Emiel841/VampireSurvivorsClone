import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        image1 = pygame.image.load("Assets/Weapons/sword_slash1.png").convert_alpha()
        image1 = pygame.transform.scale(image1, (512, 512))
        image2 = pygame.image.load("Assets/Weapons/sword_slash2.png").convert_alpha()
        image2 = pygame.transform.scale(image2, (512, 512))
        image3 = pygame.image.load("Assets/Weapons/sword_slash3.png").convert_alpha()
        image3 = pygame.transform.scale(image3, (512, 512))
        self.image = pygame.transform.scale(image1, (0, 0))

        image1_flipped = pygame.transform.flip(image1, True, False)
        image2_flipped = pygame.transform.flip(image2, True, False)
        image3_flipped = pygame.transform.flip(image3, True, False)


        self.images = [self.image, image1, image2, image3, image3]
        self.images_flipped = [self.image, image1_flipped, image2_flipped, image3_flipped, image3_flipped]
        self.current_image = 0

        self.id = "sword"


        collision_img = pygame.image.load("Assets/Weapons/sword_col_shape.png").convert_alpha()
        collision_img = pygame.transform.scale(collision_img, (512, 512))
        self.mask = pygame.mask.from_surface(collision_img)

        self.rect = collision_img.get_rect()
        self.rect.center = (x, y)

    def update(self, flipped, x, y):
        if flipped:
            self.rect.center = (x+100, y)
        else:
            self.rect.center = (x-100, y)


        if not flipped:
            self.image = self.images[int(self.current_image)]
        else:
            self.image = self.images_flipped[int(self.current_image)]
        self.current_image += 0.2
        if self.current_image >= len(self.images_flipped):
            self.kill()