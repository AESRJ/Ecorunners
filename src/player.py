import pygame
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, is_echo=False):
        super().__init__()
        
        self.animations = {}
        # --- CAMBIO: AUMENTO DE TAMAÑO ---
        # Antes era (32, 48), ahora lo hacemos más grande y heroico
        self.size = (50, 80) 

        try:
            # Cargar imágenes
            idle_img = pygame.image.load('assets/images/player_idle.png').convert_alpha()
            run_img = pygame.image.load('assets/images/player_run.png').convert_alpha()
            jump_img = pygame.image.load('assets/images/player_jump.png').convert_alpha()
            
            # Escalar al nuevo tamaño grande
            self.animations['idle'] = pygame.transform.scale(idle_img, self.size)
            self.animations['run'] = pygame.transform.scale(run_img, self.size)
            self.animations['jump'] = pygame.transform.scale(jump_img, self.size)
            
        except FileNotFoundError:
            surf = pygame.Surface(self.size)
            surf.fill(COLOR_PLAYER)
            self.animations['idle'] = surf
            self.animations['run'] = surf
            self.animations['jump'] = surf

        self.image = self.animations['idle']
        # Ajustamos el rect para que no atraviese el suelo al nacer
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True
        self.is_echo = is_echo
        
        self.recording = [] 
        self.playback_index = 0
        self.finished_playback = False

        if self.is_echo:
            self.tint_images()

    def tint_images(self):
        for key, img in self.animations.items():
            mask = pygame.mask.from_surface(img)
            echo_surf = mask.to_surface(setcolor=COLOR_ECHO, unsetcolor=(0,0,0,0))
            echo_surf.set_alpha(150)
            self.animations[key] = echo_surf

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[pygame.K_a]:
            self.velocity.x = -SPEED
            self.facing_right = False
        
        if keys[pygame.K_d]:
            self.velocity.x = SPEED
            self.facing_right = True
            
        if keys[pygame.K_w] and self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False

    def animate(self):
        state = 'idle'
        if not self.on_ground:
            state = 'jump'
        elif self.velocity.x != 0:
            state = 'run'
        
        img = self.animations[state]
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        self.image = img

    def update(self, platforms):
        if not self.is_echo:
            self.handle_input()
            
            # Gravedad
            self.velocity.y += GRAVITY
            
            # --- COLISIÓN X (Horizontal) ---
            self.rect.x += self.velocity.x
            self.check_collisions(platforms, 'horizontal')
            
            # --- COLISIÓN Y (Vertical) ---
            self.rect.y += self.velocity.y
            self.check_collisions(platforms, 'vertical')
            
            self.animate()
            
            frame_data = {
                'x': self.rect.x, 
                'y': self.rect.y,
                'facing_right': self.facing_right,
                'velocity_x': self.velocity.x,
                'on_ground': self.on_ground
            }
            self.recording.append(frame_data)
            
        else:
            if self.playback_index < len(self.recording):
                data = self.recording[self.playback_index]
                self.rect.x = data['x']
                self.rect.y = data['y']
                self.facing_right = data['facing_right']
                self.velocity.x = data.get('velocity_x', 0)
                self.on_ground = data.get('on_ground', True)
                self.animate()
                self.playback_index += 1
            else:
                self.finished_playback = True

    def check_collisions(self, platforms, direction):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if direction == 'horizontal':
                if self.velocity.x > 0: # Yendo a la derecha
                    self.rect.right = platform.rect.left
                if self.velocity.x < 0: # Yendo a la izquierda
                    self.rect.left = platform.rect.right
            
            elif direction == 'vertical':
                if self.velocity.y > 0: # Cayendo
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                if self.velocity.y < 0: # Saltando hacia arriba (cabezazo)
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0