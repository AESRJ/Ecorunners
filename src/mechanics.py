import pygame
from .settings import *

class Lever(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.activated = False
        
        # --- CARGA DE IMÁGENES DE PALANCA ---
        try:
            # Imagen cuando NO la tocas (Desactivada)
            self.image_off = pygame.image.load('assets/images/palanca.png').convert_alpha()
            # Imagen cuando LA tocas (Activada)
            self.image_on = pygame.image.load('assets/images/palanca_activada.png').convert_alpha()
            
            # Escalar si es necesario (ajustamos a 40x40 para que se vea bien en el mapa)
            # Si tus imágenes ya tienen el tamaño perfecto, puedes quitar estas líneas.
            self.image_off = pygame.transform.scale(self.image_off, (40, 40))
            self.image_on = pygame.transform.scale(self.image_on, (40, 40))
            
        except FileNotFoundError:
            # Fallback por si olvidas poner las imágenes en la carpeta
            print("ERROR: No se encontraron palanca.png o palanca_activada.png")
            self.image_off = pygame.Surface((30, 40))
            self.image_off.fill((200, 50, 50)) # Rojo
            self.image_on = pygame.Surface((30, 40))
            self.image_on.fill((50, 200, 50)) # Verde
            
        self.image = self.image_off
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def update(self, active_entities):
        # Detectar colisión con jugador o ecos
        collision = False
        for entity in active_entities:
            if self.rect.colliderect(entity.rect):
                collision = True
                break
        
        self.activated = collision
        
        # Cambiar imagen visualmente según el estado
        if self.activated:
            self.image = self.image_on
        else:
            self.image = self.image_off

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20, move_y=150):
        super().__init__()
        # La Gate es una plataforma que se mueve
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 120)) # Color metálico
        pygame.draw.rect(self.image, (255, 255, 255), (0,0,width,height), 2) # Borde
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_y = y
        self.target_y = y + move_y # Cuánto baja
        self.speed = 2
        self.type = "gate" # Para identificarla en colisiones
        self.active = True # Siempre colisionable

    def update_position(self, should_open):
        dy = 0 # Inicializamos el desplazamiento
        
        if should_open:
            # Bajar hacia target_y
            if self.rect.y < self.target_y:
                dy = self.speed
                if self.rect.y + dy > self.target_y:
                    dy = self.target_y - self.rect.y
                self.rect.y += dy
        else:
            # Subir hacia initial_y
            if self.rect.y > self.initial_y:
                dy = -self.speed
                if self.rect.y + dy < self.initial_y:
                    dy = self.initial_y - self.rect.y
                self.rect.y += dy
        
        return dy # Importante devolver dy para la física del jugador