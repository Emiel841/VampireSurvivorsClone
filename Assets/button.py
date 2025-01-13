import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("Assets/Gui/Upgrades/upgradeholder.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            return True
        return False