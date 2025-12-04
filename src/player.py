import pygame
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, is_echo=False):
        super().__init__()
        
        self.animations = {}
        self.size = (50, 80) 

        try:
            idle_img = pygame.image.load('assets/images/player_idle.png').convert_alpha()
            run_img = pygame.image.load('assets/images/player_run.png').convert_alpha()
            jump_img = pygame.image.load('assets/images/player_jump.png').convert_alpha()
            
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
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True
        self.is_echo = is_echo
        
        self.recording = [] 
        self.playback_index = 0
        self.finished_playback = False

        # --- NUEVO: Variables para animación fluida ---
        self.walk_timer = 0
        self.walk_frame = 0 # 0 = Idle, 1 = Run

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
        current_time = pygame.time.get_ticks()
        img = self.animations['idle']

        if not self.on_ground:
            # Si salta, usamos la imagen de salto fija
            img = self.animations['jump']
        elif self.velocity.x != 0:
            # --- NUEVO: LÓGICA DE CAMINATA (WALK CYCLE) ---
            # Si se mueve en el suelo, alternamos entre IDLE y RUN cada 150ms
            # Esto crea la ilusión de que está moviendo las piernas.
            if current_time - self.walk_timer > 150: # Velocidad de animación
                self.walk_frame = (self.walk_frame + 1) % 2
                self.walk_timer = current_time
            
            if self.walk_frame == 0:
                img = self.animations['run'] # Paso abierto
            else:
                img = self.animations['idle'] # Paso cerrado (pies juntos)
        else:
            # Si está quieto
            img = self.animations['idle']

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        self.image = img

    def update(self, platforms):
        if not self.is_echo:
            self.handle_input()
            self.velocity.y += GRAVITY
            
            self.rect.x += self.velocity.x
            self.check_collisions(platforms, 'horizontal')
            
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
                if self.velocity.x > 0: self.rect.right = platform.rect.left
                if self.velocity.x < 0: self.rect.left = platform.rect.right
            elif direction == 'vertical':
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                if self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0