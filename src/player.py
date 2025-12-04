import pygame
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, is_echo=False):
        super().__init__()
        
        self.animations = {}
        self.size = (50, 80) 

        try:
            idle_img = pygame.image.load('assets/images/player_idle.png').convert_alpha()
            jump_img = pygame.image.load('assets/images/player_jump.png').convert_alpha()
            
            run_raw1 = pygame.image.load('assets/images/player_run.png').convert_alpha()
            run_raw3 = pygame.image.load('assets/images/player_run3.png').convert_alpha()
            
            idle_scaled = pygame.transform.scale(idle_img, self.size)
            self.animations['idle'] = idle_scaled
            self.animations['jump'] = pygame.transform.scale(jump_img, self.size)
            
            run_scaled1 = pygame.transform.scale(run_raw1, self.size)
            run_scaled3 = pygame.transform.scale(run_raw3, self.size)

            self.animations['run'] = [
                run_scaled1,
                idle_scaled,
                run_scaled3,
                idle_scaled
            ]
            
        except FileNotFoundError:
            surf = pygame.Surface(self.size)
            surf.fill(COLOR_PLAYER)
            self.animations['idle'] = surf
            self.animations['jump'] = surf
            self.animations['run'] = [surf]

        self.image = self.animations['idle']
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True
        self.is_echo = is_echo
        
        self.recording = [] 
        self.playback_index = 0
        self.finished_playback = False

        self.walk_timer = 0
        self.walk_frame = 0 

        if self.is_echo:
            self.tint_images()

    def tint_images(self):
        for key, value in self.animations.items():
            if isinstance(value, list):
                tinted_list = []
                for img in value:
                    tinted_list.append(self.apply_tint(img))
                self.animations[key] = tinted_list
            else:
                self.animations[key] = self.apply_tint(value)

    def apply_tint(self, surface):
        mask = pygame.mask.from_surface(surface)
        echo_surf = mask.to_surface(setcolor=COLOR_ECHO, unsetcolor=(0,0,0,0))
        echo_surf.set_alpha(150)
        return echo_surf

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
            img = self.animations['jump']
        elif self.velocity.x != 0:
            animation_speed = 120 
            
            if current_time - self.walk_timer > animation_speed:
                num_frames = len(self.animations['run'])
                self.walk_frame = (self.walk_frame + 1) % num_frames
                self.walk_timer = current_time
            
            img = self.animations['run'][self.walk_frame]
        else:
            img = self.animations['idle']
            if self.walk_frame != 0:
                 self.walk_frame = 0

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        self.image = img

    # --- CAMBIO AQUÍ: input_active ---
    def update(self, platforms, input_active=True):
        if not self.is_echo:
            # Si el input está activo, leemos teclas. Si no, frenamos al personaje.
            if input_active:
                self.handle_input()
            else:
                self.velocity.x = 0
            
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