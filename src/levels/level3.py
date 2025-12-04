from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player
from src.mechanics import Lever, Gate, Spike, Barrier

def load_level_3(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    # Limpieza
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()
    
    hazards = [] 
    barriers = {} 
    specific_levers = {}

    # --- 1. EL PISO Y PLATAFORMAS ---
    
    # Suelo Base
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    # Plataforma INICIO (Izquierda)
    # La chica empieza aquí.
    p_start = Platform(50, 500, type="normal") 
    
    # Plataforma PEQUEÑA (Lila) - Izquierda Centro
    # Sirve para saltar desde el inicio y no caer a los pinchos.
    p_lila_bridge = Platform(280, 450, type="chica") 
    
    # Plataforma MÓVIL (Azul) - Centro     # "Donde esta la chica un poco a la derecha".
    # Funciona como ascensor: Empieza abajo (accesible desde p_lila) y sube a la zona superior.
    # Se mueve 300px hacia arriba (move_y=-300) cuando se activa la palanca.
    p_blue_moving = Gate(450, 450, width=120, height=20, move_y=-250)
    p_blue_moving.image.fill((135, 206, 235)) # Azul claro
    
    # Plataforma Superior Izquierda (Para la palanca 2)
    p_top_left = Platform(50, 200, type="chica")
    
    # Plataforma Superior Derecha (Decorativa o para un cristal)
    p_top_right = Platform(900, 250, type="normal")

    platforms.add(p_start, p_lila_bridge, p_top_left, p_top_right)
    gates.add(p_blue_moving)
    all_sprites.add(p_start, p_lila_bridge, p_top_left, p_top_right, p_blue_moving)

    # --- 2. PINCHOS (Solo 3 en el medio) ---
    # Justo debajo del hueco entre la plataforma lila y la móvil
    spike1 = Spike(350, floor.rect.top, width=50)
    spike2 = Spike(420, floor.rect.top, width=50)
    spike3 = Spike(490, floor.rect.top, width=50)
    
    hazards.extend([spike1, spike2, spike3])
    all_sprites.add(spike1, spike2, spike3)

    # --- 3. PALANCAS ---
    
    # Palanca 1 (Inferior Derecha) - EN EL PISO
    # Esta activa el ascensor azul y quita la barrera rosa.
    lev_floor_right = Lever(700, floor.rect.top)
    
    # Palanca 2 (Superior Izquierda) - ENCERRADA
    lev_top_left = Lever(80, p_top_left.rect.top)

    levers.add(lev_floor_right, lev_top_left)
    all_sprites.add(lev_floor_right, lev_top_left)
    
    specific_levers["bottom_right"] = lev_floor_right
    specific_levers["top_left"] = lev_top_left

    # --- 4. BARRERAS (CAMPOS DE FUERZA) ---
    
    # Barrera ROSA: Encierra la palanca de arriba a la izquierda
    # Cubo completo alrededor de p_top_left
    barrier_pink = Barrier(40, 120, 120, 150, color=(255, 105, 180)) 
    
    # Barrera VERDE: Encierra el portal en el piso
    # Cubo completo abajo a la derecha
    barrier_green = Barrier(1080, floor.rect.top - 120, 120, 120, color=(50, 205, 50)) 
    
    barriers["pink"] = barrier_pink
    barriers["green"] = barrier_green
    
    all_sprites.add(barrier_pink, barrier_green)

    # --- 5. CRISTALES ---
    c1 = Crystal(p_top_right.rect.centerx, p_top_right.rect.top - 20)
    c2 = Crystal(p_lila_bridge.rect.centerx, p_lila_bridge.rect.top - 20)
    crystals.add(c1, c2)
    all_sprites.add(c1, c2)

    # --- 6. PORTAL (EN EL PISO) ---
    portal = Portal(1130, floor.rect.top + 10)
    portal.rect.bottom = floor.rect.top
    all_sprites.add(portal)

    # Jugador empieza en la plataforma de inicio
    player = Player(80, p_start.rect.top - 50)
    all_sprites.add(player)

    return player, portal, None, {
        "tutorial_step": 0,
        "popup_text": "NIVEL 3: SINCRONIZACIÓN VERTICAL",
        "show_popup": True,
        "hazards": hazards,
        "barriers": barriers,
        "specific_levers": specific_levers,
        "moving_gate": p_blue_moving, 
        "moving_crystal": None
    }