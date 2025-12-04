import pygame
from .settings import *

class Lever(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.activated = False
        try:
            self.image_off = pygame.image.load('assets/images/palanca.png').convert_alpha()
            self.image_on = pygame.image.load('assets/images/palanca_activada.png').convert_alpha()
            self.image_off = pygame.transform.scale(self.image_off, (40, 40))
            self.image_on = pygame.transform.scale(self.image_on, (40, 40))
        except FileNotFoundError:
            self.image_off = pygame.Surface((30, 40))
            self.image_off.fill((200, 50, 50)) 
            self.image_on = pygame.Surface((30, 40))
            self.image_on.fill((50, 200, 50)) 
        self.image = self.image_off
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def update(self, active_entities):
        collision = False
        for entity in active_entities:
            if self.rect.colliderect(entity.rect):
                collision = True
                break
        self.activated = collision
        self.image = self.image_on if self.activated else self.image_off

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20, move_y=150, color=(100, 100, 120), loop=False):
        super().__init__()
        
        # --- CAMBIO: USAR IMAGEN 'platform.png' ---
        try:
            # Cargamos la textura de la plataforma
            plat_img = pygame.image.load('assets/images/platform.png').convert_alpha()
            # La escalamos al tamaño exacto que pide el objeto (width, height)
            self.image = pygame.transform.scale(plat_img, (width, height))
            
            # Opcional: Si quieres mantener el tinte de color (ej. azul para indicar que es móvil),
            # descomenta las siguientes 3 líneas. Si prefieres la textura original, déjalas comentadas.
            # colored_surface = pygame.Surface(self.image.get_size()).convert_alpha()
            # colored_surface.fill(color)
            # self.image.blit(colored_surface, (0,0), special_flags=pygame.BLEND_MULT)
            
        except FileNotFoundError:
            # Fallback si no encuentra la imagen
            self.image = pygame.Surface((width, height))
            self.image.fill(color) 
            pygame.draw.rect(self.image, (255, 255, 255), (0,0,width,height), 2) 
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_y = y
        self.target_y = y + move_y 
        self.speed = 2
        self.type = "gate"
        self.active = True
        
        # Lógica de Bucle
        self.loop = loop
        self.moving_to_target = True 

    def update_position(self, should_open):
        dy = 0
        if self.loop and should_open:
            target = self.target_y if self.moving_to_target else self.initial_y
            if self.rect.y < target:
                dy = self.speed
                if self.rect.y + dy > target: dy = target - self.rect.y
            elif self.rect.y > target:
                dy = -self.speed
                if self.rect.y + dy < target: dy = target - self.rect.y
            self.rect.y += dy
            if self.rect.y == target:
                self.moving_to_target = not self.moving_to_target
        else:
            target = self.target_y if should_open else self.initial_y
            if self.rect.y < target:
                dy = self.speed
                if self.rect.y + dy > target: dy = target - self.rect.y
                self.rect.y += dy
            elif self.rect.y > target:
                dy = -self.speed
                if self.rect.y + dy < target: dy = target - self.rect.y
                self.rect.y += dy
        return dy

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width=40):
        super().__init__()
        try:
            # --- CAMBIO: Nombre del archivo a 'pinchos.png' ---
            spike_img = pygame.image.load('assets/images/pinchos.png').convert_alpha()
            # Escalamos el tile base (ej. 30x30)
            spike_tile = pygame.transform.scale(spike_img, (30, 30))
            
            self.image = pygame.Surface((width, 30), pygame.SRCALPHA)
            # Repetimos la imagen para cubrir el ancho
            for i in range(0, width, 30):
                self.image.blit(spike_tile, (i, 0))
                
        except FileNotFoundError:
            self.image = pygame.Surface((width, 30), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (255, 0, 0), [(0, 30), (width//2, 0), (width, 30)])
        
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        try:
            barrier_img = pygame.image.load('assets/images/barrera.png').convert_alpha()
            self.image = pygame.transform.scale(barrier_img, (width, height))
            tinted_image = self.image.copy()
            tinted_image.fill(color, special_flags=pygame.BLEND_MULT)
            self.image = tinted_image
            self.image.set_alpha(200)
        except FileNotFoundError:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
            self.image.set_alpha(180)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = True
        self.original_pos = (x, y)

    def update_state(self, is_active):
        self.active = is_active
        if self.active:
            self.rect.topleft = self.original_pos
        else:
            self.rect.x = -2000