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
        self.image = pygame.Surface((width, height))
        self.image.fill(color) 
        pygame.draw.rect(self.image, (255, 255, 255), (0,0,width,height), 2) 
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_y = y
        self.target_y = y + move_y 
        self.speed = 2
        self.type = "gate"
        self.active = True
        
        # --- NUEVO: Lógica de Bucle ---
        self.loop = loop
        self.moving_to_target = True # Dirección actual del bucle

    def update_position(self, should_open):
        dy = 0
        
        # Si está en modo bucle y activada
        if self.loop and should_open:
            target = self.target_y if self.moving_to_target else self.initial_y
            
            # Moverse hacia el objetivo actual
            if self.rect.y < target:
                dy = self.speed
                if self.rect.y + dy > target: dy = target - self.rect.y
            elif self.rect.y > target:
                dy = -self.speed
                if self.rect.y + dy < target: dy = target - self.rect.y
            
            self.rect.y += dy
            
            # Si llegamos, cambiamos dirección
            if self.rect.y == target:
                self.moving_to_target = not self.moving_to_target
                
        # Comportamiento normal (ir y quedarse)
        else:
            # Si no hay señal de abrir, siempre intentar volver al inicio
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
            spike_img = pygame.image.load('assets/images/pincho.png').convert_alpha()
            spike_tile = pygame.transform.scale(spike_img, (30, 30))
            self.image = pygame.Surface((width, 30), pygame.SRCALPHA)
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