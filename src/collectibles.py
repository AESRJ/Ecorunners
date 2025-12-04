import pygame
from src.settings import *

class Crystal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            img = pygame.image.load('assets/images/soul_fragment.png').convert_alpha()
            # --- CAMBIO: AUMENTO DE TAMAÑO (Antes 24x24) ---
            self.image = pygame.transform.scale(img, (40, 40))
        except FileNotFoundError:
            # Fallback más grande también
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            # Dibujamos un rombo más grande
            pygame.draw.polygon(self.image, COLOR_RESONANCE, [(20, 0), (40, 20), (20, 40), (0, 20)])
        
        self.rect = self.image.get_rect(center=(x, y))

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {}
        try:
            closed = pygame.image.load('assets/images/portal_closed.png').convert_alpha()
            opened = pygame.image.load('assets/images/portal_open.png').convert_alpha()
            
            # --- CAMBIO: AUMENTO DE TAMAÑO (Antes 64x96) ---
            # Ahora son mucho más altos y anchos
            new_size = (100, 150)
            
            self.images['closed'] = pygame.transform.scale(closed, new_size)
            self.images['open'] = pygame.transform.scale(opened, new_size)
            self.image = self.images['closed']
        except FileNotFoundError:
            # Fallback grande
            self.image = pygame.Surface((100, 150))
            self.image.fill((50, 50, 50))
            self.images = None

        # Usamos bottomleft para que crezca hacia arriba desde el suelo
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.active = False 

    def activate(self):
        self.active = True
        if self.images:
            self.image = self.images['open']
        else:
            self.image.fill(COLOR_ECHO)