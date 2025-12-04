import pygame
from src.settings import *

class Crystal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            img = pygame.image.load('assets/images/soul_fragment.png').convert_alpha()
            # Reducimos tamaño para que sea un ítem flotante delicado
            self.image = pygame.transform.scale(img, (24, 24))
        except FileNotFoundError:
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, COLOR_RESONANCE, [(10, 0), (20, 10), (10, 20), (0, 10)])
        
        self.rect = self.image.get_rect(center=(x, y))

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {}
        try:
            closed = pygame.image.load('assets/images/portal_closed.png').convert_alpha()
            opened = pygame.image.load('assets/images/portal_open.png').convert_alpha()
            
            # Hacemos el portal un poco más alto que el jugador (que mide 48)
            # 64x90 es un buen tamaño para una puerta mística
            self.images['closed'] = pygame.transform.scale(closed, (64, 96))
            self.images['open'] = pygame.transform.scale(opened, (64, 96))
            self.image = self.images['closed']
        except FileNotFoundError:
            self.image = pygame.Surface((50, 90))
            self.image.fill((50, 50, 50))
            self.images = None

        # Usamos bottomleft para colocarlo pegado al suelo fácilmente
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.active = False 

    def activate(self):
        self.active = True
        if self.images:
            self.image = self.images['open']
        else:
            self.image.fill(COLOR_ECHO)