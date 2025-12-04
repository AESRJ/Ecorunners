from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player
from src.mechanics import Lever, Gate, Spike, Barrier

def load_level_3(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()
    
    hazards = [] 
    barriers = {} 
    specific_levers = {}

    # --- 1. EL PISO Y PLATAFORMAS ---
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    # (Eliminé p_start porque causaba el error y no se usaba)
    
    # Plataforma PEQUEÑA (Lila) - Puente
    p_lila_bridge = Platform(250, 550, type="chica") 
    
    # Plataforma SEGURA sobre los picos (Nuevo)
    # Justo en medio para ayudar el salto
    p_safe_spike = Platform(320, 250, type="chica")

    # Plataforma MÓVIL (Azul) - Ascensor Bucle
    # Se mueve sola (loop=True)
    p_blue_moving = Gate(600, 550, width=120, height=20, move_y=-350, color=(135, 206, 235), loop=True)
    
    # Plataforma Superior Izquierda
    p_top_left = Platform(50, 200, type="chica")
    
    # Plataforma Superior Derecha
    p_top_right = Platform(900, 250, type="normal")

    platforms.add(p_lila_bridge, p_safe_spike, p_top_left, p_top_right)
    gates.add(p_blue_moving)
    all_sprites.add(p_lila_bridge, p_safe_spike, p_top_left, p_top_right, p_blue_moving)

    # --- 2. PINCHOS (3 en medio) ---
    spike1 = Spike(350, floor.rect.top, width=50)
    spike2 = Spike(420, floor.rect.top, width=50)
    spike3 = Spike(490, floor.rect.top, width=50)
    
    hazards.extend([spike1, spike2, spike3])
    all_sprites.add(spike1, spike2, spike3)

    # --- 3. PALANCAS ---
    # Palanca 1 (Piso)
    lev_floor_right = Lever(750, floor.rect.top)
    
    # Palanca 2 (Arriba Izq)
    lev_top_left = Lever(80, p_top_left.rect.top)

    levers.add(lev_floor_right, lev_top_left)
    all_sprites.add(lev_floor_right, lev_top_left)
    
    specific_levers["bottom_right"] = lev_floor_right
    specific_levers["top_left"] = lev_top_left

    # --- 4. BARRERAS ---
    barrier_pink = Barrier(40, 120, 120, 150, color=(255, 105, 180)) 
    barrier_green = Barrier(1080, floor.rect.top - 120, 120, 120, color=(50, 205, 50)) 
    
    barriers["pink"] = barrier_pink
    barriers["green"] = barrier_green
    all_sprites.add(barrier_pink, barrier_green)

    # --- 5. CRISTALES ---
    c1 = Crystal(p_top_right.rect.centerx, p_top_right.rect.top - 20)
    c2 = Crystal(p_lila_bridge.rect.centerx, p_lila_bridge.rect.top - 20)
    crystals.add(c1, c2)
    all_sprites.add(c1, c2)

    # --- 6. PORTAL ---
    portal = Portal(1130, floor.rect.top + 10)
    portal.rect.bottom = floor.rect.top
    all_sprites.add(portal)

    # --- JUGADOR ---
    player = Player(80, floor.rect.top - 50)
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