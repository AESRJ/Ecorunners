from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player
from src.mechanics import Lever, Gate, Spike, Barrier

def load_level_5(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()
    
    hazards = [] 
    barriers = {} 
    specific_levers = {}

    # --- 1. ESTRUCTURA SIMÉTRICA ---
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    # Plataforma Central (Portal)
    p_center = Platform(540, 300, type="normal")
    
    # 4 Esquinas
    p_top_left = Platform(50, 150, type="chica")
    p_top_right = Platform(1000, 150, type="chica")
    p_bot_left = Platform(50, 520, type="chica")
    p_bot_right = Platform(1000, 550, type="chica")

    platforms.add(p_center, p_top_left, p_top_right, p_bot_left, p_bot_right)
    all_sprites.add(p_center, p_top_left, p_top_right, p_bot_left, p_bot_right)

    # --- 2. PLATAFORMAS MÓVILES (Cruces) ---
    # Dos plataformas que se cruzan para llegar al centro
    gate_h = Gate(200, 300, width=100, height=20, move_y=0, loop=True, color=(100, 100, 200)) # Se moverá horizontal con lógica especial en main? No, Gate solo mueve Y.
    # Usemos Gates verticales.
    gate_left = Gate(300, 500, width=100, height=20, move_y=-350, loop=True)
    gate_right = Gate(800, 150, width=100, height=20, move_y=350, loop=True)
    
    gates.add(gate_left, gate_right)
    all_sprites.add(gate_left, gate_right)

    # --- 3. PINCHOS ---
    # Foso alrededor del centro
    spike1 = Spike(400, floor.rect.top, width=100)
    spike2 = Spike(700, floor.rect.top, width=100)
    hazards.extend([spike1, spike2])
    all_sprites.add(spike1, spike2)

    # --- 4. PALANCAS (4 Esquinas) ---
    l1 = Lever(80, p_top_left.rect.top)
    l2 = Lever(1030, p_top_right.rect.top)
    l3 = Lever(80, p_bot_left.rect.top)
    l4 = Lever(1030, p_bot_right.rect.top)

    levers.add(l1, l2, l3, l4)
    all_sprites.add(l1, l2, l3, l4)
    
    # Todas las palancas son necesarias
    specific_levers["all"] = [l1, l2, l3, l4]

    # --- 5. BARRERA (Cubo central) ---
    # Protege el portal en el centro
    barrier_center = Barrier(540, 200, 200, 100, color=(255, 50, 50))
    barriers["center"] = barrier_center
    all_sprites.add(barrier_center)

    # --- 6. CRISTALES ---
    # Uno en cada plataforma móvil y uno en el suelo seguro
    c1 = Crystal(350, 450) # Flotando ruta izq
    c2 = Crystal(850, 200) # Flotando ruta der
    c3 = Crystal(100, floor.rect.top - 20)
    c4 = Crystal(1100, floor.rect.top - 20)
    crystals.add(c1, c2, c3, c4)
    all_sprites.add(c1, c2, c3, c4)

    # --- 7. PORTAL ---
    portal = Portal(640, p_center.rect.top + 10)
    portal.rect.bottom = p_center.rect.top
    all_sprites.add(portal)

    player = Player(100, floor.rect.top - 50)
    all_sprites.add(player)

    return player, portal, None, {
        "tutorial_step": 0,
        "popup_text": "NIVEL 5: ACTIVACIÓN CUÁDRUPLE",
        "show_popup": True,
        "hazards": hazards,
        "barriers": barriers,
        "specific_levers": specific_levers,
        "moving_gate": None, # Hay varias, se manejan genérico
        "moving_crystal": None
    }