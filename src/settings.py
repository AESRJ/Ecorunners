# Constantes globales del juego

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Paleta Cyberpunk
COLOR_BG = (13, 12, 34)       # Azul casi negro
COLOR_PLAYER = (255, 0, 255)  # Magenta
COLOR_ECHO = (0, 255, 255)    # Cian
COLOR_RESONANCE = (255, 255, 0) # Amarillo
COLOR_PLATFORM = (50, 50, 70)

# Físicas y Mecánicas
GRAVITY = 0.8
JUMP_FORCE = -16
SPEED = 5
MAX_ECHOES = 5
RESONANCE_DIST = 100 # Distancia en píxeles para activar resonancia

# ==========================================
# LO NUEVO: ESTADOS DEL JUEGO Y UI
# ==========================================

# Estados (Modos en los que puede estar el juego)
MENU = "menu"
LEVEL_SELECT = "level_select"
GAME = "game"

# Interfaz de Usuario (UI)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (50, 50, 70)       # Color normal del botón
COLOR_BUTTON_HOVER = (0, 200, 200) # Color cuando pasas el mouse por encima
COLOR_LOCKED = (50, 50, 50) 