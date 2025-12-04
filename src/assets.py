import pygame
import os

class AssetManager:
    def __init__(self):
        # Inicializamos el sistema de sonido
        try:
            pygame.mixer.init()
            print("Sistema de audio inicializado.")
        except pygame.error as e:
            print(f"Error al inicializar audio: {e}")

        # --- CONFIGURACIÓN DE MÚSICA ---
        # Mapeamos las claves "level_X" a los archivos "X_Nivel.mp3"
        self.music_tracks = {
            "menu": "assets/music/Main.mp3",
            
            # Nombres solicitados:
            "level_1": "assets/music/primer_Nivel.mp3",
            "level_2": "assets/music/segundo_Nivel.mp3",
            "level_3": "assets/music/tercer_Nivel.mp3",
            "level_4": "assets/music/cuarto_Nivel.mp3",  # Por si acaso
            "level_5": "assets/music/quinto_Nivel.mp3"   # Por si acaso
        }
        
        self.current_track = None
        self.music_volume = 0.4

    def play_music(self, track_key):
        """Gestiona el cambio de música inteligente con fadeout"""
        # 1. Si ya está sonando esa canción, no hacer nada
        if self.current_track == track_key:
            return

        # 2. Verificar si la clave existe
        path = self.music_tracks.get(track_key)
        if not path:
            print(f"Advertencia: No existe la pista '{track_key}' en la configuración.")
            return

        # 3. Intentar cargar y reproducir
        try:
            # Si hay música sonando, hacemos un fadeout suave
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(500)
            
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1) # Loop infinito
            
            self.current_track = track_key
            print(f"Reproduciendo música: {track_key} -> {path}")
            
        except pygame.error as e:
            print(f"Error al cargar música ({path}): {e}")

    def stop_music(self):
        pygame.mixer.music.stop()