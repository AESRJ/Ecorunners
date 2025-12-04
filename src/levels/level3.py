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
    barriers = []

    # 1. EL PISO (Nuevo)
    # Lo agregamos como base de todo el nivel
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    # 2. PLATAFORMAS
    # Plataforma inicial (un escalón sobre el piso)
    p_start = Platform(50, 550, type="normal") 
    
    # Plataforma Lila (arriba izquierda)
    p_lila = Platform(150, 300, type="chica")
    
    # Plataforma Violeta (arriba derecha)
    p_violet_top = Platform(900, 200, type="normal")
    
    # Plataforma Azul (Móvil)
    # Gate móvil que sirve de ascensor central
    p_blue_moving = Gate(600, 400, width=150, height=20, move_y=-250, color=(135, 206, 235)) 

    # Plataforma final (meta)
    p_end = Platform(1000, 550, type="normal")

    platforms.add(p_start, p_lila, p_violet_top, p_end)
    gates.add(p_blue_moving)
    
    # 3. PINCHOS (Trampas de suelo)
    # Los colocamos justo encima del piso (floor.rect.top)
    # Cubren el área bajo la plataforma móvil para obligarte a usarla
    spike1 = Spike(300, floor.rect.top, width=200) 
    spike2 = Spike(550, floor.rect.top, width=200)
    spike3 = Spike(800, floor.rect.top, width=200)
    
    hazards.extend([spike1, spike2, spike3])
    
    # 4. PALANCAS
    # Palanca 1: Abajo derecha (Mueve azul y quita barrera rosa)
    lev_bottom_right = Lever(650, 600) 
    # Plataforma pequeña para sostener la palanca entre los pinchos
    p_lev1 = Platform(630, 600, type="chica") 
    platforms.add(p_lev1)
    
    # Palanca 2: Arriba izquierda (Dentro de la caja rosa)
    lev_top_left = Lever(170, p_lila.rect.top)

    levers.add(lev_bottom_right, lev_top_left)

    # 5. BARRERAS
    # Barrera Rosa (Protege palanca arriba izq)
    barrier_pink = Barrier(130, 200, 20, 100, color=(255, 105, 180)) 
    
    # Barrera Verde (Protege portal)
    barrier_green = Barrier(1000, 450, 200, 20, color=(50, 205, 50)) 
    
    barriers.extend([barrier_pink, barrier_green])
    
    # Añadir todo a all_sprites
    all_sprites.add(p_start, p_lila, p_violet_top, p_end, p_blue_moving, p_lev1)
    all_sprites.add(spike1, spike2, spike3)
    all_sprites.add(lev_bottom_right, lev_top_left)
    all_sprites.add(barrier_pink, barrier_green)

    # 6. CRISTALES
    c1 = Crystal(p_start.rect.centerx, p_start.rect.top - 20)
    c2 = Crystal(p_violet_top.rect.centerx, p_violet_top.rect.top - 20)
    crystals.add(c1, c2)
    all_sprites.add(c1, c2)

    # 7. PORTAL
    portal = Portal(1100, p_end.rect.top + 10)
    portal.rect.bottom = p_end.rect.top
    all_sprites.add(portal)

    player = Player(100, p_start.rect.top - 50)
    all_sprites.add(player)

    return player, portal, None, {
        "tutorial_step": 0,
        "popup_text": "NIVEL 3: CUIDADO CON LOS PINCHOS",
        "show_popup": True,
        "hazards": hazards,
        "barriers": {"pink": barrier_pink, "green": barrier_green},
        "specific_levers": {"bottom_right": lev_bottom_right, "top_left": lev_top_left},
        "blue_platform": p_blue_moving
    }