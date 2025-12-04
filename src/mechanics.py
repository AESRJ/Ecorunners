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
        if self.activated:
            self.image = self.image_on
        else:
            self.image = self.image_off

class Gate(pygame.sprite.Sprite):
    """Usada para plataformas móviles (ascensores)"""
    def __init__(self, x, y, width=100, height=20, move_y=150, color=(100, 200, 255)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color) 
        pygame.draw.rect(self.image, (255, 255, 255), (0,0,width,height), 2)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_y = y
        self.target_y = y + move_y
        self.speed = 2
        self.active = True 

    def update_position(self, should_open):
        dy = 0 
        if should_open:
            if self.rect.y > self.target_y if self.target_y < self.initial_y else self.rect.y < self.target_y:
                # Determinar dirección
                direction = 1 if self.target_y > self.initial_y else -1
                dy = self.speed * direction
                
                # Ajuste para no pasarse
                if direction == 1 and self.rect.y + dy > self.target_y: dy = self.target_y - self.rect.y
                if direction == -1 and self.rect.y + dy < self.target_y: dy = self.target_y - self.rect.y
                
                self.rect.y += dy
        else:
            if self.rect.y != self.initial_y:
                direction = -1 if self.target_y > self.initial_y else 1
                dy = self.speed * direction
                
                if direction == 1 and self.rect.y + dy > self.initial_y: dy = self.initial_y - self.rect.y
                if direction == -1 and self.rect.y + dy < self.initial_y: dy = self.initial_y - self.rect.y
                
                self.rect.y += dy
        return dy

# --- NUEVAS CLASES ---

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width=40):
        super().__init__()
        # Dibujamos triángulos rojos
        self.image = pygame.Surface((width, 30), pygame.SRCALPHA)
        # Dibujar 3 picos
        p1 = (0, 30); p2 = (width//6, 0); p3 = (width//3, 30)
        p4 = (width//3, 30); p5 = (width//2, 0); p6 = (2*width//3, 30)
        p7 = (2*width//3, 30); p8 = (5*width//6, 0); p9 = (width, 30)
        
        pygame.draw.polygon(self.image, (255, 0, 0), [p1, p2, p3])
        pygame.draw.polygon(self.image, (255, 0, 0), [p4, p5, p6])
        pygame.draw.polygon(self.image, (255, 0, 0), [p7, p8, p9])
        
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.image.set_alpha(180) # Semi transparente
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = True
        self.original_pos = (x, y)

    def update_state(self, is_active):
        self.active = is_active
        if self.active:
            # Si está activa, la movemos a su lugar original
            self.rect.topleft = self.original_pos
        else:
            # Si se desactiva, la mandamos fuera de pantalla para que no colisione
            self.rect.x = -1000