import pygame
import asyncio
import math

from src.settings import *
from src.player import Player
from src.platform import Platform
from src.assets import AssetManager
from src.ui import UI
from src.collectibles import Crystal, Portal
from src.mechanics import Lever, Gate

async def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eco Resonancia")
    clock = pygame.time.Clock()

    assets = AssetManager()
    ui = UI(screen)
    
    # --- ESTADO INICIAL ---
    game_state = MENU
    current_level = 1
    max_unlocked_level = 2 # Solo 2 niveles
    
    assets.play_music("menu")

    # Fuentes
    try:
        hud_font = pygame.font.Font("assets/fonts/cyber.ttf", 20)
    except FileNotFoundError:
        hud_font = pygame.font.SysFont("Consolas", 20, bold=True)

    try:
        level_bg = pygame.image.load('assets/images/level_bg.png').convert()
        level_bg = pygame.transform.scale(level_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        level_bg = None

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    crystals = pygame.sprite.Group()
    levers = pygame.sprite.Group() 
    gates = pygame.sprite.Group()  
    
    echoes = [] 
    player = None 
    res_plat = None
    portal = None
    
    moving_crystal = None 

    # Variables de estado
    tutorial_step = 0
    show_popup = False
    popup_text = ""
    
    collected_fragments = 0 # Recursos para ecos

    def reset_level(level_id):
        nonlocal player, res_plat, portal, tutorial_step, show_popup, popup_text, moving_crystal
        
        # Limpieza
        all_sprites.empty()
        platforms.empty()
        crystals.empty()
        levers.empty()
        gates.empty()
        echoes.clear()
        
        moving_crystal = None 
        
        # Música
        if level_id == 1:
            assets.play_music("level_1")
        else:
            assets.play_music("level_2")
        
        # ==========================================
        # NIVEL 1: TUTORIAL BÁSICO
        # ==========================================
        if level_id == 1:
            floor = Platform(0, SCREEN_HEIGHT - 60, type="piso", width=SCREEN_WIDTH)
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
            
            tutorial_step = 1
            show_popup = True
            popup_text = "SISTEMA: INICIANDO... [A/D] MOVER - [W] SALTAR"

        # ==========================================
        # NIVEL 2: PUZLE ECOS + PLATAFORMA MÓVIL
        # ==========================================
        elif level_id == 2:
            floor = Platform(0, SCREEN_HEIGHT - 60, type="piso", width=SCREEN_WIDTH)
            
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
            
            tutorial_step = 3
            show_popup = True
            popup_text = "RECOGE FRAGMENTOS PARA CREAR ECOS CON [Z]."

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == GAME:
                if show_popup and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        show_popup = False
                        if tutorial_step == 1: tutorial_step = 0 
                        elif tutorial_step == 2: tutorial_step = 3 
                        elif tutorial_step == 3: tutorial_step = 4
                
                if not show_popup: 
                    if event.type == pygame.KEYDOWN:
                        # --- TECLA Z: CREAR ECO (CON COSTO) ---
                        if event.key == pygame.K_z and player:
                             if len(echoes) < MAX_ECHOES and collected_fragments > 0:
                                collected_fragments -= 1 # GASTAR 1 CRISTAL
                                
                                new_echo = Player(100, SCREEN_HEIGHT - 150, is_echo=True)
                                new_echo.recording = list(player.recording)
                                echoes.append(new_echo)
                                all_sprites.add(new_echo)
                                
                                start_pos = (player.recording[0]['x'], player.recording[0]['y']) if player.recording else (100, 500)
                                player.rect.topleft = start_pos
                                player.recording = []
                                player.velocity = pygame.math.Vector2(0, 0)
                                print(f"Eco creado. Fragmentos restantes: {collected_fragments}")
                             else:
                                 print("¡No tienes suficientes fragmentos para crear un Eco!")
                        
                        if event.key == pygame.K_c:
                            for e in echoes: e.kill()
                            echoes.clear()

                        if event.key == pygame.K_ESCAPE:
                            game_state = MENU
                            assets.play_music("menu")
                        
                        if event.key == pygame.K_p:
                             print("¡Truco activado!")
                             if current_level < max_unlocked_level: 
                                current_level += 1
                             else:
                                current_level = 1
                             game_state = LEVEL_SELECT
                             assets.play_music("menu")

        if game_state == GAME:
            if tutorial_step == 1 and show_popup:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]:
                    show_popup = False
                    tutorial_step = 0

            resonance_active = False 
            active_entities = [player] + echoes
            
            for i in range(len(active_entities)):
                for j in range(i + 1, len(active_entities)):
                    e1 = active_entities[i]
                    e2 = active_entities[j]
                    dist = math.hypot(e1.rect.centerx - e2.rect.centerx, e1.rect.centery - e2.rect.centery)
                    if dist < RESONANCE_DIST:
                        resonance_active = True
                        pygame.draw.line(screen, COLOR_RESONANCE, e1.rect.center, e2.rect.center, 2)

            if res_plat: res_plat.update_resonance(resonance_active)
            
            levers.update(active_entities)
            
            all_levers_active = True
            if len(levers) > 0:
                for lev in levers:
                    if not lev.activated:
                        all_levers_active = False
                        break
            else:
                all_levers_active = False

            # --- ARREGLO DE CAÍDA (Sticky Platform) ---
            # Esto evita que el jugador se caiga de la plataforma móvil
            for gate in gates:
                # 1. Detectar pasajeros
                riders = []
                for entity in active_entities:
                    if abs(entity.rect.bottom - gate.rect.top) < 6:
                        if entity.rect.right > gate.rect.left and entity.rect.left < gate.rect.right:
                            riders.append(entity)
                
                # 2. Mover la plataforma y obtener dy
                # Asegúrate de que mechanics.py devuelva dy
                dy = gate.update_position(should_open=all_levers_active)
                
                # 3. Mover a los pasajeros junto con la plataforma
                if dy != 0:
                    for rider in riders:
                        rider.rect.y += dy
                        if dy > 0: rider.on_ground = True

            # Cristal Móvil (Nivel 2)
            if moving_crystal and moving_crystal.alive():
                target_gate = None
                for g in gates: target_gate = g
                if target_gate:
                    moving_crystal.rect.centerx = target_gate.rect.centerx
                    moving_crystal.rect.bottom = target_gate.rect.top - 10

            physic_platforms = pygame.sprite.Group()
            for p in platforms: 
                if p.active: physic_platforms.add(p)
            for g in gates:
                physic_platforms.add(g)

            player.update(physic_platforms, input_active=not show_popup)
            for echo in echoes: echo.update(None)
            
            # Caída al vacío (Reinicia nivel)
            if player.rect.y > SCREEN_HEIGHT + 200:
                reset_level(current_level)

            hit_crystal = pygame.sprite.spritecollide(player, crystals, True)
            if hit_crystal:
                for c in hit_crystal:
                    collected_fragments += 1
                    
                if tutorial_step == 0 and current_level == 1: 
                    tutorial_step = 2 
                    show_popup = True
                    popup_text = "FRAGMENTO ADQUIRIDO. [Z] PARA ECO (COSTO: 1)."
                
                # En nivel 1, el portal se abre al limpiar cristales
                if current_level == 1 and len(crystals) == 0:
                    portal.activate()

            # Lógica de portal
            portal_open = False
            if current_level == 1:
                if len(crystals) == 0: portal_open = True
            else:
                # En Nivel 2, requiere palancas
                if all_levers_active: portal_open = True
            
            if portal_open:
                portal.activate()
            else:
                portal.active = False
                if portal.images: portal.image = portal.images['closed']

            if portal.active and player.rect.colliderect(portal.rect):
                print("¡NIVEL COMPLETADO!")
                if current_level == max_unlocked_level:
                    # Fin del juego (vuelve al menú)
                    current_level = 1 
                    game_state = MENU
                    assets.play_music("menu")
                else:
                    # Avanzar nivel
                    current_level += 1
                    reset_level(current_level)

            if level_bg:
                screen.blit(level_bg, (0,0))
            else:
                screen.fill(COLOR_BG)
                
            all_sprites.draw(screen)
            
            # HUD
            hud_panel = pygame.Surface((350, 40))
            hud_panel.set_alpha(180)
            hud_panel.fill((0, 0, 0))
            screen.blit(hud_panel, (10, 10))
            
            hud_color = COLOR_ECHO 
            
            info_text = f"NIVEL {current_level} | ECOS: {collected_fragments}"
            score_text = hud_font.render(info_text, True, hud_color)
            screen.blit(score_text, (20, 20))
            
            if show_popup:
                overlay = pygame.Surface((SCREEN_WIDTH, 80))
                overlay.set_alpha(220)
                overlay.fill((10, 10, 20))
                overlay.set_colorkey((0,0,0)) 
                pygame.draw.rect(overlay, COLOR_PLAYER, (0,0, SCREEN_WIDTH, 80), 2)
                screen.blit(overlay, (0, 60))
                
                pop_text_surf = hud_font.render(popup_text, True, (255, 255, 255))
                pop_rect = pop_text_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
                screen.blit(pop_text_surf, pop_rect)

        elif game_state == MENU:
            action = ui.draw_main_menu()
            if action == "goto_select": game_state = LEVEL_SELECT
            elif action == "exit": running = False

        elif game_state == LEVEL_SELECT:
            action = ui.draw_level_select(max_unlocked_level)
            if action and action.startswith("start_game_"):
                current_level = int(action.split("_")[-1])
                reset_level(current_level)
                game_state = GAME
            elif action == "goto_menu": game_state = MENU

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())