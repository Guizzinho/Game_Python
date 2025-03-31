import pygame
import math
import random

class Enemy():
    def __init__(self, name: str, position: tuple, attack_damage: int):
        self.name = name
        self.sprite_sheet = pygame.image.load("./assets/Caracthers/"+ name +"/Idle.png")
        self.frame_width = 120
        self.frame_height = 128
        self.animations = {
            'idle': [(0, 0)],
            'run': [(1, 0), (2, 0), (3, 0)],
            'attack1': [(1, 0), (2, 0), (2, 0), (3, 0), (3, 0)],
            'attack2': [(1, 0), (2, 0), (3, 0), (4, 0)],
            'attack3': [(1, 0), (1, 0), (2, 0), (2, 0)],
        }
        self.current_animation = 'idle'
        self.current_frame = 0
        self.rect = pygame.Rect(position[0], position[1], self.frame_width, self.frame_height)
        self.speed = 1

        self.frame_index = 0
        self.animation_speed = 6
        self.animation_timer = 0
        self.facing_right = False

        self.frames = self.get_frames(self.animations[self.current_animation])
        self.image = self.frames[0]
        self.area_jogavel = pygame.Rect(5, 330, 1900, 750)
        self.idle_image = pygame.image.load("./assets/Caracthers/"+ name +"/Idle.png")
        self.run_image = pygame.image.load("./assets/Caracthers/"+ name +"/Run.png")
        self.attack1_image = pygame.image.load("./assets/Caracthers/"+ name +"/Attack_1.png")
        self.attack2_image = pygame.image.load("./assets/Caracthers/"+ name +"/Attack_2.png")
        self.attack3_image = pygame.image.load("./assets/Caracthers/"+ name +"/Attack_3.png")
        self.state = 'chasing'

        self.max_health = 3
        self.health = self.max_health
        self.attack_damage = attack_damage
        self.attack_cooldown = 2400
        self.last_attack_time = 0
        self.attack_range = 50
        self.stop_distance = 40
        self.is_alive = True

    def get_frames(self, animation_frames):
        frames = []
        for frame_pos in animation_frames:
            frame = self.sprite_sheet.subsurface((frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height,
            self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def update(self, player, current_time):
        if not self.is_alive:
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        if dist < self.attack_range and self.state != 'attacking':
             # Verifica cooldown ANTES de mudar para attacking para evitar ataque imediato
             if current_time - self.last_attack_time > self.attack_cooldown:
                 self.state = 'attacking'
                 self.current_animation = 'attack1' # Ou outra animação de ataque
                 try:
                      self.sprite_sheet = self.attack1_image # Carrega a spritesheet correta
                 except AttributeError:
                       self.sprite_sheet = self.idle_image # Fallback
                 self.frame_index = 0
                 self.animation_timer = 0
                 self.last_attack_time = current_time # Marca o início do cooldown do ataque
             else:
                  self.state = 'chasing' #
                  if self.current_animation != 'idle':
                       self.current_animation = 'idle'
                       self.sprite_sheet = self.idle_image
                       self.frame_index = 0
                       self.animation_timer = 0


        elif dist >= self.attack_range and self.state == 'attacking':
            print(f"{self.name} exiting attack state (out of range)") # Debug
            self.state = 'chasing'
            self.current_animation = 'run'
            self.sprite_sheet = self.run_image
            self.frame_index = 0
            self.animation_timer = 0

        elif self.state == 'chasing':
             if self.current_animation != 'run':
                 self.current_animation = 'run'
                 self.sprite_sheet = self.run_image
                 self.frame_index = 0
                 self.animation_timer = 0

             if dist > self.stop_distance:
                 if dist > 0:
                     dx = dx / dist
                     dy = dy / dist
                 else:
                     dx, dy = 0, 0

                 self.rect.x += dx * self.speed
                 self.rect.y += dy * self.speed
             else:
                  if self.current_animation != 'idle':
                        self.current_animation = 'idle'
                        self.sprite_sheet = self.idle_image
                        self.frame_index = 0
                        self.animation_timer = 0

    def update_animation(self):
        if not self.is_alive:
            return

        animation_config = self.animations.get(self.current_animation)
        if not animation_config: # Fallback seguro
            self.current_animation = 'idle'
            self.sprite_sheet = self.idle_image
            animation_config = self.animations['idle']

        num_frames = len(animation_config)
        if num_frames == 0: return # Evita erro se animação for vazia

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % num_frames

            # Se estava atacando e a animação terminou, volta a perseguir
            if self.state == 'attacking' and self.frame_index == 0:
                 print(f"{self.name} finished attack animation, back to chasing") # Debug
                 self.state = 'chasing' # Volta a perseguir após terminar a animação
                 self.current_animation = 'run' # Ou 'idle' se preferir
                 self.sprite_sheet = self.run_image # Ou self.idle_image
                 # Não resetamos last_attack_time aqui, o cooldown continua contando

        if self.frame_index >= num_frames:
            self.frame_index = 0

        frame_pos = animation_config[self.frame_index]
        try:
            self.image = self.sprite_sheet.subsurface((frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height, self.frame_width, self.frame_height))
        except ValueError as e:
             frame_pos = self.animations['idle'][0]
             self.sprite_sheet = self.idle_image
             self.image = self.sprite_sheet.subsurface((frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height, self.frame_width, self.frame_height))
             self.current_animation = 'idle'
             self.frame_index = 0
        except AttributeError:
             print(f"Erro: Spritesheet não carregada para animação {self.current_animation} do inimigo {self.name}")
             try:
                 self.sprite_sheet = self.idle_image
                 frame_pos = self.animations['idle'][0]
                 self.image = self.sprite_sheet.subsurface((frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height, self.frame_width, self.frame_height))
                 self.current_animation = 'idle'
                 self.frame_index = 0
             except:
                  self.image = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)

    def draw(self, surface, offset_x=0, offset_y=0):
        if not self.is_alive:
            return

        self.update_animation()
        image_to_draw = self.image
        if not self.facing_right:
            try:
                image_to_draw = pygame.transform.flip(self.image, True, False)
            except pygame.error as e:
                print(f"Erro ao flipar imagem do inimigo: {e}")
                image_to_draw = self.image

        surface.blit(image_to_draw, (self.rect.x - offset_x, self.rect.y - offset_y))


    def take_damage(self, amount):
        if self.is_alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_alive = False