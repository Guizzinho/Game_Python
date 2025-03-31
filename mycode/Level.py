import pygame
import random
from mycode.Background import Background
from mycode.Cam import Camera
from mycode.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_TEXT, EVENT_ENEMY
from mycode.Player import Player
from mycode.EntityFactory import EntityFactory
from mycode.Enemy import Enemy


class Level:
    def __init__(self, window, name, background_path, music_level, attack_damage):
        self.window = window
        self.background = Background(background_path, 1920, 1080)
        player_start_x = 200
        player_start_y = 500
        self.player = EntityFactory.get_entity('player', (player_start_x, player_start_y))
        self.music_level_path = music_level
        self.attack_damage = attack_damage

        self.camera = Camera(1920, 1080)  # Tamanho do background/mundo

        self.enemy1 = None
        self.spawn_enemy()
        try:
            pygame.mixer.music.load(self.music_level_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar música {music_level}: {e}")
            self.music_level_path = None

        self.name = name
        self.timeout = 20000  # 20 segundos
        self.start_time = 0

        self.level_complete = False
        self.game_over = False

    def spawn_enemy(self):
        enemy_types = ['enemy1', 'enemy2', 'enemy3']
        chosen_type = random.choice(enemy_types)

        spawn_x = self.camera.offset_x + WIN_WIDTH + random.randint(50, 150)
        spawn_y = random.randint(self.player.area_jogavel.top, self.player.area_jogavel.bottom - 128)

        print(f"Spawning {chosen_type} at ({spawn_x}, {spawn_y})")
        self.enemy1 = EntityFactory.get_entity(chosen_type, (spawn_x, spawn_y), self.attack_damage)
        if not isinstance(self.enemy1, Enemy):
            self.enemy1 = None

    def run(self):
        running = True
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        # Toca a música em loop
        if self.music_level_path and pygame.mixer.music.get_busy() == False:
            try:
                pygame.mixer.music.load(self.music_level_path)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Erro ao tocar música: {e}")

        while running:
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()  # Encerra Pygame adequadamente
                    exit()  # Fecha o programa

            # Atualiza jogador (movimento)
            self.player.move(keys)
            self.camera.update(self.player)

            # Atualiza inimigo (movimento)
            if self.enemy1 and self.enemy1.is_alive:
                self.enemy1.update(self.player, current_time)

            # --- Lógica de Colisão e Dano ---

            # Jogador ataca inimigo?
            player_is_attacking_anim = self.player.current_animation.startswith('attack')
            if player_is_attacking_anim and not self.player.attack_hit and self.enemy1 and self.enemy1.is_alive:
                if self.player.rect.colliderect(self.enemy1.rect):
                    if current_time - self.player.last_attack_time > self.player.attack_cooldown:
                        self.enemy1.take_damage(1)
                        self.player.last_attack_time = current_time
                        self.player.attack_hit = True

            # Inimigo ataca jogador?
            if self.enemy1 and self.enemy1.is_alive and self.player.is_alive:
                if self.enemy1.state == 'attacking':
                    if self.enemy1.rect.colliderect(self.player.rect):
                        self.player.take_damage(self.enemy1.attack_damage)

            # --- Lógica de Morte e Respawn ---

            # Inimigo morreu?
            if self.enemy1 and not self.enemy1.is_alive:
                self.spawn_enemy()# Gera um novo inimigo

            # Jogador morreu?
            if not self.player.is_alive:
                self.game_over = True

            # --- Lógica do Timer e Fim de Nível ---
            elapsed_time = current_time - self.start_time
            remaining_time = max(0, self.timeout - elapsed_time)

            if remaining_time == 0 and not self.game_over:
                self.level_complete = True

            # --- Desenho ---
            self.window.fill((0, 0, 0))
            self.background.draw(self.window, self.camera.offset_x, self.camera.offset_y)

            if self.player.is_alive:
                self.player.draw(self.window, self.camera.offset_x, self.camera.offset_y)

            if self.enemy1 and self.enemy1.is_alive:
                self.enemy1.draw(self.window, self.camera.offset_x, self.camera.offset_y)

            # --- Textos ---
            timer_text = f'Tempo: {remaining_time / 1000 :.1f}s'
            self.level_text(25, timer_text, COLOR_TEXT, (10, 5))

            health_text = f'Vida: {self.player.health} / {self.player.max_health}'
            self.level_text(25, health_text, (0, 255, 0), (10, 35))

            if self.game_over:
                self.menu_text(60, "VOCÊ MORREU!", (255, 0, 0), (WIN_WIDTH / 2, WIN_HEIGHT / 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

            elif self.level_complete:
                self.menu_text(60, "NÍVEL COMPLETO!", (0, 255, 255), (WIN_WIDTH / 2, WIN_HEIGHT / 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

            pygame.display.flip()
            clock.tick(60)

        # Fim do loop principal
        print("Saindo do nível...")
        if self.game_over:
            return "game_over"
        elif self.level_complete:
            return "completed"
        else:
            return "quit"

        # Funções de texto (level_text, menu_text)
    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
            text_font: Font = pygame.font.Font("./assets/Fonts/MedievalSharp-Regular.ttf", text_size)
            text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
            text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
            self.window.blit(source=text_surf, dest=text_rect)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
            text_font: Font = pygame.font.Font("./assets/Fonts/MedievalSharp-Regular.ttf", text_size)
            text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
            text_rect: Rect = text_surf.get_rect(center=text_center_pos)
            self.window.blit(source=text_surf, dest=text_rect)