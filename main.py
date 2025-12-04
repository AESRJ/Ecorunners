import pygame
import asyncio
import math

from src.settings import *
from src.player import Player
from src.platform import Platform
from src.assets import AssetManager
from src.ui import UI
from src.collectibles import Crystal, Portal
from src.mechanics import Lever, Gate, Spike, Barrier # Importar nuevos

# IMPORTAR LOS NIVELES
from src.levels.level1 import load_level_1
from src.levels.level2 import load_level_2
from src.levels.level3 import load_level_3 # Nuevo

async def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eco Resonancia")
    clock = pygame.time.Clock()

    assets = AssetManager()
    ui = UI(screen)
    
    game_state = MENU
    current_level = 1
    max_unlocked_level = 3 # AHORA SON 3 NIVELES
    
    assets.play_music("menu")

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
    
    # Listas para objetos especiales del Nivel 3
    level_hazards = [] 
    level_barriers = {} 
    special_levers = {}
    
    echoes = [] 
    player = None 
    res_plat = None
    portal = None
    moving_crystal = None 

    tutorial_step = 0
    show_popup = False
    popup_text = ""
    collected_fragments = 0 

    def reset_level(level_id):
        nonlocal player, res_plat, portal, tutorial_step, show_popup, popup_text, moving_crystal
        nonlocal level_hazards, level_barriers, special_levers
        
        echoes.clear()
        
        # Música (Reutilizamos la del nivel 2 para el 3 por ahora)
        track = "level_1" if level_id == 1 else "level_2"
        assets.play_music(track)
        
        # Reiniciar referencias especiales
        moving_crystal = None
        level_hazards = []
        level_barriers = {}
        special_levers = {}

        level_data = None
        
        if level_id == 1:
            player, portal, res_plat, level_data = load_level_1(
                all_sprites, platforms, crystals, levers, gates, None
            )
        elif level_id == 2:
            player, portal, res_plat, level_data = load_level_2(
                all_sprites, platforms, crystals, levers, gates, None
            )
        elif level_id == 3:
            player, portal, res_plat, level_data = load_level_3(
                all_sprites, platforms, crystals, levers, gates, None
            )
            
        if level_data:
            tutorial_step = level_data.get("tutorial_step", 0)
            popup_text = level_data.get("popup_text", "")
            show_popup = level_data.get("show_popup", False)
            moving_crystal = level_data.get("moving_crystal", None)
            level_hazards = level_data.get("hazards", [])
            level_barriers = level_data.get("barriers", {})
            special_levers = level_data.get("specific_levers", {})

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == GAME:
                if show_popup and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        show_popup = False
                        if tutorial_step > 0: tutorial_step = 0
                
                if not show_popup: 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z and player:
                             if len(echoes) < MAX_ECHOES and collected_fragments > 0:
                                collected_fragments -= 1 
                                new_echo = Player(100, SCREEN_HEIGHT - 150, is_echo=True)
                                new_echo.recording = list(player.recording)
                                echoes.append(new_echo)
                                all_sprites.add(new_echo)
                                
                                start_pos = (player.recording[0]['x'], player.recording[0]['y']) if player.recording else (100, 500)
                                player.rect.topleft = start_pos
                                player.recording = []
                                player.velocity = pygame.math.Vector2(0, 0)
                             else:
                                 print("¡Sin fragmentos suficientes!")
                        
                        if event.key == pygame.K_c:
                            for e in echoes: e.kill()
                            echoes.clear()

                        if event.key == pygame.K_ESCAPE:
                            game_state = MENU
                            assets.play_music("menu")
                        
                        if event.key == pygame.K_p: 
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
            
            # --- LÓGICA ESPECÍFICA NIVEL 3 ---
            if current_level == 3:
                lev_br = special_levers.get("bottom_right")
                lev_tl = special_levers.get("top_left")
                
                # Acción 1: Palanca inf. derecha mueve plataforma azul Y quita barrera rosa
                if lev_br:
                    # Plataforma azul
                    blue_plat = gates.sprites()[0] if gates else None 
                    # Nota: En nivel 3 solo hay 1 gate (la azul), así que usamos index 0
                    if blue_plat:
                        # Si está activa, subir (open=True). 
                        # OJO: Gate.update_position con should_open=True mueve hacia target_y
                        # En level3 definimos move_y=-250 (hacia arriba)
                        riders = [e for e in active_entities if abs(e.rect.bottom - blue_plat.rect.top) < 6 and e.rect.right > blue_plat.rect.left and e.rect.left < blue_plat.rect.right]
                        dy = blue_plat.update_position(should_open=lev_br.activated)
                        if dy != 0:
                            for rider in riders:
                                rider.rect.y += dy
                                if dy > 0: rider.on_ground = True
                    
                    # Barrera Rosa
                    pink_b = level_barriers.get("pink")
                    if pink_b:
                        # Si la palanca está activa, la barrera se DESACTIVA (False)
                        pink_b.update_state(not lev_br.activated)

                # Acción 2: AMBAS palancas quitan barrera verde
                if lev_br and lev_tl:
                    green_b = level_barriers.get("green")
                    if green_b:
                        both_active = lev_br.activated and lev_tl.activated
                        green_b.update_state(not both_active)

            # --- LÓGICA GENERAL PARA OTROS NIVELES ---
            else:
                # Niveles 1 y 2 (Lógica estándar)
                all_levers_active = True
                if len(levers) > 0:
                    for lev in levers:
                        if not lev.activated:
                            all_levers_active = False
                            break
                else:
                    all_levers_active = False

                for gate in gates:
                    riders = [e for e in active_entities if abs(e.rect.bottom - gate.rect.top) < 6 and e.rect.right > gate.rect.left and e.rect.left < gate.rect.right]
                    dy = gate.update_position(should_open=all_levers_active)
                    if dy != 0:
                        for rider in riders:
                            rider.rect.y += dy
                            if dy > 0: rider.on_ground = True

            # Cristal móvil
            if moving_crystal and moving_crystal.alive():
                target_gate = gates.sprites()[0] if gates else None
                if target_gate:
                    moving_crystal.rect.centerx = target_gate.rect.centerx
                    moving_crystal.rect.bottom = target_gate.rect.top - 10

            # --- COLISIONES FÍSICAS ---
            physic_platforms = pygame.sprite.Group()
            for p in platforms: 
                if p.active: physic_platforms.add(p)
            for g in gates:
                physic_platforms.add(g)
            
            # Añadir barreras activas a la física
            for b in level_barriers.values():
                if b.active: physic_platforms.add(b)

            player.update(physic_platforms, input_active=not show_popup)
            for echo in echoes: echo.update(None)
            
            # --- COLISIÓN CON PINCHOS ---
            for hazard in level_hazards:
                if player.rect.colliderect(hazard.rect):
                    print("¡Moriste en los pinchos!")
                    reset_level(current_level)

            if player.rect.y > SCREEN_HEIGHT + 200:
                reset_level(current_level)

            hit_crystal = pygame.sprite.spritecollide(player, crystals, True)
            if hit_crystal:
                for c in hit_crystal:
                    collected_fragments += 1
                if current_level == 1 and len(crystals) == 0:
                    portal.activate()

            # Portal
            portal_open = False
            if current_level == 1:
                if len(crystals) == 0: portal_open = True
            elif current_level == 2:
                # Lógica Nivel 2
                all_active = all(l.activated for l in levers)
                if all_active: portal_open = True
            elif current_level == 3:
                # Lógica Nivel 3: El portal está detrás de la barrera verde.
                # Si la barrera verde está inactiva, el portal es accesible.
                # No necesita lógica extra para "abrirse", solo que no haya pared.
                # Pero podemos hacer que brille.
                lev_br = special_levers.get("bottom_right")
                lev_tl = special_levers.get("top_left")
                if lev_br and lev_tl and lev_br.activated and lev_tl.activated:
                    portal_open = True

            if portal_open:
                portal.activate()
            else:
                portal.active = False
                if portal.images: portal.image = portal.images['closed']

            if portal.active and player.rect.colliderect(portal.rect):
                if current_level == max_unlocked_level:
                    current_level = 1 
                    game_state = MENU
                    assets.play_music("menu")
                else:
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