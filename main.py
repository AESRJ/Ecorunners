import pygame
import asyncio
import math

from src.settings import *
from src.player import Player
from src.platform import Platform
from src.assets import AssetManager # Importamos la nueva clase mejorada
from src.ui import UI
from src.collectibles import Crystal, Portal

async def main():
    pygame.init()
    # Nota: Ya no hacemos pygame.mixer.init() aquí, lo hace el AssetManager
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eco Resonancia")
    clock = pygame.time.Clock()

    # --- INICIALIZACIÓN DE ASSETS ---
    assets = AssetManager() # El gestor de audio se crea aquí
    
    ui = UI(screen)
    game_state = MENU
    
    # Iniciar música del menú usando el AssetManager
    assets.play_music("menu")

    # Fuente HUD
    try:
        hud_font = pygame.font.Font("assets/fonts/cyber.ttf", 20)
    except FileNotFoundError:
        hud_font = pygame.font.SysFont("Consolas", 20, bold=True)

    # Fondo Nivel
    try:
        level_bg = pygame.image.load('assets/images/level_bg.png').convert()
        level_bg = pygame.transform.scale(level_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        level_bg = None

    max_unlocked_level = 1
    current_level = 1

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    crystals = pygame.sprite.Group()
    echoes = [] 
    player = None 
    res_plat = None
    portal = None

    tutorial_step = 0
    show_popup = False
    popup_text = ""

    def reset_level(level_id):
        nonlocal player, res_plat, portal, tutorial_step, show_popup, popup_text
        all_sprites.empty()
        platforms.empty()
        crystals.empty()
        echoes.clear()
        
        # --- NUEVA LÓGICA DE MÚSICA ---
        # Delegamos la tarea al AssetManager
        if level_id == 1:
            assets.play_music("level_1")
        elif level_id == 2:
            assets.play_music("level_2")
        
        if level_id == 1:
            floor = Platform(0, SCREEN_HEIGHT - 60, type="piso", width=SCREEN_WIDTH)
            p1 = Platform(250, 550, type="normal")
            p2 = Platform(600, 420, type="chica")
            p3 = Platform(820, 350, type="normal") 
            res_plat = Platform(450, 250, width=100, is_resonance=True)
            
            platforms.add(floor, p1, p2, p3, res_plat)
            all_sprites.add(floor, p1, p2, p3, res_plat)
            
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
                
                if not show_popup: 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r and player:
                             if len(echoes) < MAX_ECHOES:
                                new_echo = Player(100, SCREEN_HEIGHT - 150, is_echo=True)
                                # Copiar grabación
                                new_echo.recording = list(player.recording)
                                echoes.append(new_echo)
                                all_sprites.add(new_echo)
                                # Reset jugador
                                player.rect.topleft = (100, SCREEN_HEIGHT - 150)
                                player.recording = []
                                player.velocity = pygame.math.Vector2(0, 0)
                        
                        if event.key == pygame.K_c:
                            for e in echoes: e.kill()
                            echoes.clear()

                        if event.key == pygame.K_ESCAPE:
                            game_state = MENU
                            assets.play_music("menu") # Cambio de música vía assets
                        
                        if event.key == pygame.K_p:
                             print("¡Truco activado!")
                             if current_level == max_unlocked_level:
                                max_unlocked_level += 1
                             game_state = LEVEL_SELECT
                             assets.play_music("menu") # Cambio de música vía assets

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
            active_platforms = pygame.sprite.Group([p for p in platforms if p.active])
            player.update(active_platforms)
            for echo in echoes: echo.update(None)

            hit_crystal = pygame.sprite.spritecollide(player, crystals, True)
            if hit_crystal:
                if tutorial_step == 0: 
                    tutorial_step = 2 
                    show_popup = True
                    popup_text = "FRAGMENTO DE ALMA ADQUIRIDO. SINCRONIZACIÓN... [ESPACIO]"
                
                if len(crystals) == 0:
                    portal.activate()

            if portal.active and player.rect.colliderect(portal.rect):
                print("¡NIVEL COMPLETADO!")
                if current_level == max_unlocked_level:
                    max_unlocked_level += 1
                game_state = LEVEL_SELECT
                assets.play_music("menu") # Volver a música de menú

            if level_bg:
                screen.blit(level_bg, (0,0))
            else:
                screen.fill(COLOR_BG)
                
            all_sprites.draw(screen)
            
            # HUD
            hud_panel = pygame.Surface((320, 40))
            hud_panel.set_alpha(180)
            hud_panel.fill((0, 0, 0))
            screen.blit(hud_panel, (10, 10))
            
            hud_color = COLOR_ECHO 
            score_text = hud_font.render(f"FRAGMENTOS DE ALMA: {3 - len(crystals)} / 3", True, hud_color)
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