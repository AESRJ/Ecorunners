from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player
from src.mechanics import Lever, Gate

def load_level_2(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()

    # --- CONSTRUCCIÓN DEL NIVEL 2 ---
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    
    p_start = Platform(50, 520, type="normal")
    p_mid = Platform(450, 450, type="normal")
    p_far = Platform(1000, 350, type="normal")
    
    # Gate móvil (Ascensor/Puente)
    gate = Gate(700, 250, width=250, height=20, move_y=150) 
    
    lev1 = Lever(100, p_start.rect.top) 
    lev2 = Lever(500, p_mid.rect.top)   
    
    platforms.add(floor, p_start, p_mid, p_far)
    levers.add(lev1, lev2)
    gates.add(gate)
    all_sprites.add(floor, p_start, p_mid, p_far, lev1, lev2, gate)
    
    # Cristal fijo en el suelo
    c_floor = Crystal(1050, floor.rect.top - 20)
    crystals.add(c_floor)
    all_sprites.add(c_floor)
    
    # Cristal móvil (pegado al gate)
    moving_crystal = Crystal(gate.rect.centerx, gate.rect.top - 20)
    crystals.add(moving_crystal)
    all_sprites.add(moving_crystal)
    
    portal = Portal(1100, p_far.rect.top + 10)
    portal.rect.bottom = p_far.rect.top
    all_sprites.add(portal)
    
    player = Player(50, floor.rect.top - 50)
    all_sprites.add(player)
    
    return player, portal, None, {
        "tutorial_step": 3,
        "popup_text": "RECOGE FRAGMENTOS PARA CREAR ECOS CON [Z].",
        "show_popup": True,
        "moving_crystal": moving_crystal
    }