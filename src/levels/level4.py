from src.settings import *
from src.platform import Platform
from src.collectibles import Crystal, Portal
from src.player import Player
from src.mechanics import Lever, Gate, Spike, Barrier

def load_level_4(all_sprites, platforms, crystals, levers, gates, enemies, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
    all_sprites.empty()
    platforms.empty()
    crystals.empty()
    levers.empty()
    gates.empty()
    
    hazards = [] 
    barriers = {} 
    specific_levers = {}

    # --- 1. ESTRUCTURA (DOS PISOS) ---
    
    # Piso Base (Lleno de muerte)
    floor = Platform(0, screen_height - 60, type="piso", width=screen_width)
    platforms.add(floor)
    all_sprites.add(floor)

    # --- PISO SUPERIOR ---
    # Inicio (Arriba Izquierda)
    p_start = Platform(50, 200, type="normal")
    
    # Islas superiores (Parkour difícil)
    p_up_1 = Platform(300, 200, type="chica")
    p_up_2 = Platform(500, 150, type="chica")
    p_up_3 = Platform(800, 200, type="chica")
    
    # Plataforma Palanca 1 (Arriba Derecha)
    p_lev_top = Platform(1050, 200, type="chica")

    # --- PISO INFERIOR ---
    # Plataforma Palanca 2 (Abajo Izquierda - Isla segura)
    p_lev_bot = Platform(50, 500, type="normal")
    
    # Plataforma Portal (Abajo Derecha - Meta)
    p_end = Platform(1050, 500, type="normal")

    platforms.add(p_start, p_up_1, p_up_2, p_up_3, p_lev_top, p_lev_bot, p_end)
    all_sprites.add(p_start, p_up_1, p_up_2, p_up_3, p_lev_top, p_lev_bot, p_end)

    # --- 2. EL ASCENSOR (GATE) ---
    # Conecta el piso de abajo con el de arriba en el centro.
    # Empieza ABAJO (y=550) y sube a (y=200) cuando se activa la palanca.
    # Está ubicado en x=650 (entre las islas).
    gate_elevator = Gate(650, 550, width=150, height=20, move_y=-350)
    gate_elevator.image.fill((255, 165, 0)) # Naranja para distinguir
    gates.add(gate_elevator)
    all_sprites.add(gate_elevator)

    # --- 3. PINCHOS (TODO EL PISO EXCEPTO ISLAS) ---
    # Zona 1: Centro y derecha
    for x in range(250, 1000, 50):
        s = Spike(x, floor.rect.top, width=50)
        hazards.append(s)
        all_sprites.add(s)

    # --- 4. PALANCAS ---
    
    # Palanca ARRIBA (Derecha): Controla el Ascensor
    lev_top = Lever(1080, p_lev_top.rect.top)
    
    # Palanca ABAJO (Izquierda): Quita la barrera del portal
    lev_bot = Lever(100, p_lev_bot.rect.top)

    levers.add(lev_top, lev_bot)
    all_sprites.add(lev_top, lev_bot)
    
    specific_levers["top"] = lev_top
    specific_levers["bottom"] = lev_bot

    # --- 5. BARRERA (Protege el Portal) ---
    # Cubo verde en la meta
    barrier_final = Barrier(1040, 380, 150, 120, color=(50, 205, 50))
    barriers["final"] = barrier_final
    all_sprites.add(barrier_final)

    # --- 6. CRISTALES (Estratégicos) ---
    c1 = Crystal(p_up_2.rect.centerx, p_up_2.rect.top - 20) # En el salto difícil arriba
    c2 = Crystal(gate_elevator.rect.centerx, 500) # En el aire, donde pasa el ascensor
    c3 = Crystal(p_lev_bot.rect.centerx + 50, p_lev_bot.rect.top - 20) # Abajo
    crystals.add(c1, c2, c3)
    all_sprites.add(c1, c2, c3)

    # --- 7. PORTAL ---
    portal = Portal(1100, p_end.rect.top + 10)
    portal.rect.bottom = p_end.rect.top
    all_sprites.add(portal)

    # Jugador empieza Arriba Izquierda
    player = Player(80, p_start.rect.top - 50)
    all_sprites.add(player)

    return player, portal, None, {
        "tutorial_step": 0,
        "popup_text": "NIVEL 4: EL FOSO SINCRONIZADO",
        "show_popup": True,
        "hazards": hazards,
        "barriers": barriers,
        "specific_levers": specific_levers,
        "moving_gate": gate_elevator, 
        "moving_crystal": None
    }