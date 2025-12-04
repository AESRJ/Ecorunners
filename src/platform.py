import pygame
from src.settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, type="normal", width=None, is_resonance=False):
        super().__init__()
        self.is_resonance = is_resonance
        self.type = type
        
        self.images = {}
        try:
            # Cargamos imágenes
            floor_img = pygame.image.load('assets/images/piso.png').convert_alpha()
            medium_img = pygame.image.load('assets/images/platform.png').convert_alpha()
            small_img = pygame.image.load('assets/images/plataforma_chica.png').convert_alpha()
            
            self.images['piso'] = floor_img
            # Normal: 200x40
            self.images['normal'] = pygame.transform.scale(medium_img, (200, 40))
            # Chica: 100x40
            self.images['chica'] = pygame.transform.scale(small_img, (100, 40))
            
        except FileNotFoundError:
            self.images = None

        # Selección de imagen
        if self.is_resonance:
            self.image = pygame.Surface((100, 20))
            self.image.fill(COLOR_RESONANCE)
            self.image.set_alpha(50) 
        
        elif self.images:
            if type == "piso":
                target_w = width if width else SCREEN_WIDTH
                # El piso tiene 60px de alto según tu imagen
                self.image = pygame.transform.scale(self.images['piso'], (target_w, 60))
            elif type == "normal":
                self.image = self.images['normal']
            elif type == "chica":
                self.image = self.images['chica']
            else:
                self.image = pygame.Surface((200, 40))
                self.image.fill(COLOR_PLATFORM)
        else:
            w = width if width else 200
            self.image = pygame.Surface((w, 40))
            self.image.fill(COLOR_PLATFORM)
            
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # --- CAMBIO CRÍTICO: HITBOX FIEL ---
        # Eliminamos los ajustes manuales de altura (-10).
        # Ahora confiamos en que tu imagen es sólida desde el píxel 0.
        # Esto soluciona que el personaje se hunda o flote.
        
        self.active = not is_resonance 

    def update_resonance(self, active):
        if self.is_resonance:
            self.active = active
            self.image.set_alpha(255 if active else 50)