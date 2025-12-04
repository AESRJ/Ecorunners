from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player

def load_level_1(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    # Limpieza previa (por seguridad)
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()
    
    # --- CONSTRUCCIÓN DEL NIVEL 1 ---
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    p1 = Platform(250, 550, type="normal")
    p2 = Platform(600, 420, type="chica")
    p3 = Platform(820, 350, type="normal") 
    res_plat = Platform(450, 250, width=100, is_resonance=True)
    
    platforms.add(floor, p1, p2, p3, res_plat)
    all_sprites.add(floor, p1, p2, p3, res_plat)
    
    # 3 Cristales básicos
    c1 = Crystal(p1.rect.centerx, p1.rect.top - 20) 
    c2 = Crystal(p2.rect.centerx, p2.rect.top - 20) 
    c3 = Crystal(p3.rect.centerx, p3.rect.top - 20) 
    crystals.add(c1, c2, c3)
    all_sprites.add(c1, c2, c3)
    
    portal = Portal(1150, floor.rect.top + 10) 
    all_sprites.add(portal)
    
    player = Player(100, floor.rect.top - 50)
    all_sprites.add(player)
    
    # Retornamos el jugador, el portal y datos del tutorial
    return player, portal, res_plat, {
        "tutorial_step": 1,
        "popup_text": "SISTEMA: INICIANDO... [A/D] MOVER - [W] SALTAR",
        "show_popup": True,
        "moving_crystal": None
    }