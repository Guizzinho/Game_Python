import random
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from mycode.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_TEXT, MENU_OPTIONS


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./assets/Background/PNG/Throne/throne room.png")
        self.scaled_image = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(left=0, top=0)
        self.particles = []


    def run(self):
        # Sound menu
        pygame.mixer_music.load('./assets/Sounds/menu_sound.wav')
        # pygame.mixer_music.play(-1)

        dark_overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        dark_overlay.set_alpha(60)  # Valor entre 0 (totalmente transparente) e 255 (totalmente opaco)
        dark_overlay.fill((0, 0, 0))  # Preenchendo com preto

        while True:
            self.window.blit(self.scaled_image, (0, 0)) # Background
            self.window.blit(dark_overlay, (0, 0)) # Overlay

            self.menu_text(80, "Forgotten Lord", COLOR_TEXT, (WIN_WIDTH / 2, 80)) # titulo

            # Adicionando dinamicamente as opções do menu
            for i in range(len(MENU_OPTIONS)):
                self.menu_text(25, MENU_OPTIONS[i], COLOR_TEXT, (WIN_WIDTH / 2, 300 + 40 * i))


            self.draw_particles()  # Desenhar partículas
            self.update_particles()  # Atualizar partículas

            pygame.display.flip()

            # Check for all the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # End Pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.Font("./assets/Fonts/MedievalSharp-Regular.ttf", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

        # Renderizar sombra do texto
        shadow_surf = text_font.render(text, True, (0, 0, 0))  # Preto para a sombra
        shadow_rect = shadow_surf.get_rect(center=(text_center_pos[0] + 3, text_center_pos[1] + 3))
        self.window.blit(shadow_surf, shadow_rect)

        # Renderizar texto principal por cima, com brilho
        text_surf: pygame.Surface = text_font.render(text, True, text_color)
        text_rect: pygame.Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)

    def draw_particles(self):
        for particle in self.particles:
            pygame.draw.circle(self.window, (255, 100, 0), (particle[0], particle[1]), particle[2])

    def update_particles(self):

        # Adicionar novas partículas aleatoriamente
        if len(self.particles) < 50:
            x = random.randint(0, WIN_WIDTH)
            y = WIN_HEIGHT - 20  # Começam perto do chão
            radius = random.randint(2, 4)  # Tamanho aleatório
            self.particles.append([x, y, radius])

        # Atualizar posição (subir lentamente) e reduzir tamanho
        for particle in self.particles:
            particle[1] -= random.randint(1, 3)  # Subir
            particle[0] += random.choice([-1, 1])  # Movimento horizontal aleatório
            particle[2] -= 0.05  # Diminuir o tamanho

        # Remover partículas que desapareceram
        self.particles = [p for p in self.particles if p[2] > 0]


