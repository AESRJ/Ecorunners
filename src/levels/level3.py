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

    p_lila_bridge = Platform(250, 550, type="chica") 
    p_safe_spike = Platform(350, 270, type="chica")
    p_blue_moving = Gate(600, 550, width=120, height=20, move_y=-350, color=(135, 206, 235), loop=True)
    p_top_left = Platform(50, 200, type="chica")
    p_top_right = Platform(900, 250, type="normal")

    platforms.add(p_lila_bridge, p_safe_spike, p_top_left, p_top_right)
    gates.add(p_blue_moving)
    all_sprites.add(p_lila_bridge, p_safe_spike, p_top_left, p_top_right, p_blue_moving)

    # --- 2. PINCHOS ---
    spike1 = Spike(350, floor.rect.top, width=50)
    spike2 = Spike(420, floor.rect.top, width=50)
    spike3 = Spike(490, floor.rect.top, width=50)
    hazards.extend([spike1, spike2, spike3])
    all_sprites.add(spike1, spike2, spike3)

    # --- 3. PALANCAS ---
    lev_floor_right = Lever(750, floor.rect.top)
    lev_top_left = Lever(80, p_top_left.rect.top)
    levers.add(lev_floor_right, lev_top_left)
    all_sprites.add(lev_floor_right, lev_top_left)
    
    specific_levers["bottom_right"] = lev_floor_right
    specific_levers["top_left"] = lev_top_left

    # --- 4. CRISTALES ---
    c1 = Crystal(p_top_right.rect.centerx, p_top_right.rect.top - 20)
    c2 = Crystal(p_lila_bridge.rect.centerx, p_lila_bridge.rect.top - 20)
    crystals.add(c1, c2)
    all_sprites.add(c1, c2)

    # --- 5. PORTAL ---
    # Portal grande (100x150)
    portal = Portal(1130, floor.rect.top + 10)
    portal.rect.bottom = floor.rect.top
    all_sprites.add(portal)

    # --- 6. JUGADOR ---
    player = Player(80, floor.rect.top - 50)
    all_sprites.add(player)

    # --- 7. BARRERAS (AJUSTADAS) ---
    barrier_pink = Barrier(40, 120, 120, 150, color=(255, 105, 180)) 
    
    # AJUSTE: Barrera verde más alta (160) y posicionada más arriba para cubrir el portal de 150px
    barrier_green = Barrier(1080, floor.rect.top - 160, 180, 160, color=(50, 205, 50)) 
    
    barriers["pink"] = barrier_pink
    barriers["green"] = barrier_green
    all_sprites.add(barrier_pink, barrier_green)

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