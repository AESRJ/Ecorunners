import pygame
import asyncio # Necesario para la web (Pygbag)
import math

# ==========================================
# 1. CONFIGURACIÓN (Mover a src/settings.py)
# ==========================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Paleta Cyberpunk
COLOR_BG = (13, 12, 34)       # Azul casi negro
COLOR_PLAYER = (255, 0, 255)  # Magenta
COLOR_ECHO = (0, 255, 255)    # Cian
COLOR_RESONANCE = (255, 255, 0) # Amarillo
COLOR_PLATFORM = (50, 50, 70)

# Físicas
GRAVITY = 0.8
JUMP_FORCE = -16
SPEED = 5
MAX_ECHOES = 5
RESONANCE_DIST = 100 # Distancia en píxeles para activar resonancia

# ==========================================
# 2. CLASES (Mover a sus propios archivos en src/)
# ==========================================

class AssetManager:
    """Maneja la carga de recursos y crea placeholders si faltan archivos."""
    def __init__(self):
        self.sounds = {}
        self.images = {}

    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(0.5)
        except Exception:
            print(f"Advertencia: No se encontró sonido '{path}'.")
            # Crear sonido dummy (vacío) para evitar crashes
            self.sounds[name] = None 

    def play_sound(self, name):
        if self.sounds.get(name):
            self.sounds[name].play()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, is_echo=False):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        
        if is_echo:
            self.image.fill(COLOR_ECHO)
            self.image.set_alpha(128) # Semitransparente
        else:
            self.image.fill(COLOR_PLAYER)
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.is_echo = is_echo
        
        # Sistema de grabación (solo si NO es un eco)
        self.recording = [] # Lista de diccionarios: [{'x': 10, 'y': 20}, ...]
        self.playback_index = 0
        self.finished_playback = False

    def handle_input(self):
        """Manejo de teclas (solo para el jugador real)"""
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        if keys[pygame.K_LEFT]:
            self.velocity.x = -SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity.x = SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False

    def update(self, platforms):
        # 1. Aplicar input o reproducción
        if not self.is_echo:
            self.handle_input()
            # Grabar estado actual
            frame_data = {'x': self.rect.x, 'y': self.rect.y}
            self.recording.append(frame_data)
        else:
            # Lógica de reproducción de Eco
            if self.playback_index < len(self.recording):
                data = self.recording[self.playback_index]
                self.rect.x = data['x']
                self.rect.y = data['y']
                self.playback_index += 1
            else:
                self.finished_playback = True
                # Opcional: Reiniciar bucle o quedarse quieto
                # self.playback_index = 0 

        # 2. Aplicar Física (Solo si es jugador real para evitar desincronización)
        if not self.is_echo:
            self.velocity.y += GRAVITY
            
            # Movimiento X
            self.rect.x += self.velocity.x
            self.check_collisions(platforms, 'horizontal')
            
            # Movimiento Y
            self.rect.y += self.velocity.y
            self.check_collisions(platforms, 'vertical')

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

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, is_resonance=False):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.is_resonance = is_resonance
        
        if self.is_resonance:
            # Plataforma oculta/fantasma
            self.image.fill(COLOR_RESONANCE)
            self.image.set_alpha(50) # Muy transparente
        else:
            self.image.fill(COLOR_PLATFORM)
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = not is_resonance # Si es resonancia, empieza inactiva

    def update_resonance(self, active):
        if self.is_resonance:
            self.active = active
            self.image.set_alpha(255 if active else 50)

# ==========================================
# 3. GAME LOOP PRINCIPAL
# ==========================================

async def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eco Resonancia - Prototipo")
    clock = pygame.time.Clock()

    # --- Inicializar Assets ---
    assets = AssetManager()
    # Ejemplo: assets.load_sound('jump', 'assets/sounds/jump.wav')

    # --- Grupos de Sprites ---
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    echoes = [] # Lista simple para lógica de ecos

    # --- Crear Nivel de Prueba ---
    floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    p1 = Platform(200, 500, 200, 20)
    p2 = Platform(600, 400, 200, 20)
    
    # Esta plataforma solo se vuelve sólida con resonancia
    res_plat = Platform(450, 250, 100, 20, is_resonance=True)
    
    platforms.add(floor, p1, p2, res_plat)
    all_sprites.add(floor, p1, p2, res_plat)

    # --- Crear Jugador ---
    player = Player(100, SCREEN_HEIGHT - 150)
    all_sprites.add(player)

    running = True
    while running:
        # 1. Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Tecla R: Crear Eco y Reiniciar
                    if len(echoes) < MAX_ECHOES:
                        # Crear nuevo eco con los datos grabados
                        new_echo = Player(100, SCREEN_HEIGHT - 150, is_echo=True)
                        new_echo.recording = list(player.recording) # Copia profunda
                        echoes.append(new_echo)
                        all_sprites.add(new_echo)
                        
                        # Reiniciar jugador
                        player.rect.topleft = (100, SCREEN_HEIGHT - 150)
                        player.recording = []
                        player.velocity = pygame.math.Vector2(0, 0)
                        print(f"Eco creado. Total: {len(echoes)}")

                if event.key == pygame.K_c: # Tecla C: Limpiar Ecos
                    for e in echoes:
                        e.kill()
                    echoes.clear()

        # 2. Actualización (Update)
        
        # Detectar Resonancia
        resonance_active = False
        # Comparamos posición de jugador con ecos, y ecos entre sí
        active_entities = [player] + echoes
        
        for i in range(len(active_entities)):
            for j in range(i + 1, len(active_entities)):
                e1 = active_entities[i]
                e2 = active_entities[j]
                
                # Calcular distancia (Pítágoras)
                dist = math.hypot(e1.rect.centerx - e2.rect.centerx, 
                                  e1.rect.centery - e2.rect.centery)
                
                if dist < RESONANCE_DIST:
                    resonance_active = True
                    # Dibujar línea visual de conexión (debug)
                    pygame.draw.line(screen, COLOR_RESONANCE, e1.rect.center, e2.rect.center, 2)

        # Actualizar plataformas resonantes
        res_plat.update_resonance(resonance_active)
        
        # Colisiones: Solo colisionar con plataformas activas
        active_platforms = pygame.sprite.Group([p for p in platforms if p.active])
        player.update(active_platforms)
        
        for echo in echoes:
            echo.update(None) # Los ecos no necesitan colisiones, solo reproducen posición

        # 3. Dibujado (Draw)
        screen.fill(COLOR_BG)
        all_sprites.draw(screen)
        
        # HUD Básico
        font = pygame.font.SysFont("Arial", 18)
        info_text = font.render(f"Ecos: {len(echoes)}/5 | Resonancia: {'ACTIVA' if resonance_active else 'Inactiva'}", True, (255, 255, 255))
        screen.blit(info_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
        
        # CRÍTICO PARA WEB: Ceder control al navegador
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())