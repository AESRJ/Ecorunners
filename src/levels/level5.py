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

    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    p_center = Platform(540, 300, type="normal")
    p_top_left = Platform(50, 150, type="chica")
    p_top_right = Platform(1000, 150, type="chica")
    p_bot_left = Platform(50, 500, type="chica")
    p_bot_right = Platform(1000, 500, type="chica")

    platforms.add(p_center, p_top_left, p_top_right, p_bot_left, p_bot_right)
    all_sprites.add(p_center, p_top_left, p_top_right, p_bot_left, p_bot_right)

    gate_left = Gate(300, 500, width=100, height=20, move_y=-350, loop=True)
    gate_right = Gate(800, 150, width=100, height=20, move_y=350, loop=True)
    gates.add(gate_left, gate_right)
    all_sprites.add(gate_left, gate_right)

    spike1 = Spike(400, floor.rect.top, width=100)
    spike2 = Spike(700, floor.rect.top, width=100)
    hazards.extend([spike1, spike2])
    all_sprites.add(spike1, spike2)

    l1 = Lever(80, p_top_left.rect.top)
    l2 = Lever(1030, p_top_right.rect.top)
    l3 = Lever(80, p_bot_left.rect.top)
    l4 = Lever(1030, p_bot_right.rect.top)
    levers.add(l1, l2, l3, l4)
    all_sprites.add(l1, l2, l3, l4)
    specific_levers["all"] = [l1, l2, l3, l4]

    c1 = Crystal(350, 450) 
    c2 = Crystal(850, 200) 
    c3 = Crystal(100, floor.rect.top - 20)
    c4 = Crystal(1100, floor.rect.top - 20)
    crystals.add(c1, c2, c3, c4)
    all_sprites.add(c1, c2, c3, c4)

    portal = Portal(640, p_center.rect.top + 10)
    portal.rect.bottom = p_center.rect.top
    all_sprites.add(portal)

    player = Player(100, floor.rect.top - 50)
    all_sprites.add(player)

    # --- BARRERA AJUSTADA ---
    # Portal y=300. Altura 150 -> Top=150.
    # Barrera y=140, Altura=160.
    barrier_center = Barrier(540, 140, 200, 160, color=(255, 50, 50))
    barriers["center"] = barrier_center
    all_sprites.add(barrier_center)

    return player, portal, None, {
        "tutorial_step": 0,
        "popup_text": "NIVEL 5: ACTIVACIÓN CUÁDRUPLE",
        "show_popup": True,
        "hazards": hazards,
        "barriers": barriers,
        "specific_levers": specific_levers,
        "moving_gate": None, 
        "moving_crystal": None
    }