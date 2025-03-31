import pygame
from pygame.examples.midi import null_key
from mycode.Const import WIN_WIDTH, WIN_HEIGHT

class Player():
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.sprite_sheet = pygame.image.load("./assets/Caracthers/Samurai/Idle.png")
        self.frame_width = 120
        self.frame_height = 128
        self.animations = {
            'idle': [(0, 0)],  # Exemplo de animação 'idle'
            'run': [(1, 0), (2, 0), (3, 0)],  # Exemplo de animação 'walk'  # Exemplo de animação 'attack'
            'attack1': [(1, 0), (1, 0), (2, 0), (2, 0)],
            'attack2': [(1, 0), (2, 0), (3, 0), (4, 0)],
            'attack3': [(1, 0), (1, 0), (2, 0), (2, 0)],
        }
        self.current_animation = 'idle'
        self.current_frame = 0
        offset_x = 10  # Ajuste horizontal
        offset_y = 10  # Ajuste vertical

        self.rect = pygame.Rect(position[0] + offset_x, position[1] + offset_y, self.frame_width + 10,
                                self.frame_height - 20)
        self.speed = 5

        self.max_health = 100
        self.health = self.max_health
        self.attack_cooldown = 500
        self.last_attack_time = 0
        self.is_alive = True
        self.attack_hit = False

        self.invincibility_duration = 750
        self.last_hit_time = -self.invincibility_duration

        self.frame_index = 0
        self.animation_speed = 6
        self.animation_timer = 0
        self.facing_right = False

        self.frames = self.get_frames(self.animations[self.current_animation])
        self.image = self.frames[0]
        self.area_jogavel = pygame.Rect(5, 330, 1900, 750)
        self.idle_image = pygame.image.load("./assets/Caracthers/Samurai/Idle.png")
        self.run_image = pygame.image.load("./assets/Caracthers/Samurai/Run.png")
        self.attack1_image = pygame.image.load("./assets/Caracthers/Samurai/Attack_1.png")
        self.attack2_image = pygame.image.load("./assets/Caracthers/Samurai/Attack_2.png")
        self.attack3_image = pygame.image.load("./assets/Caracthers/Samurai/Attack_3.png")


    def get_frames(self, animation_frames):
        frames = []
        for frame_pos in animation_frames:
            frame = self.sprite_sheet.subsurface((frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height,
            self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def move(self, keys):
        if not self.is_alive:
            return
        dx, dy = 0, 0
        is_moving = False
        is_attacking = False

        if keys[pygame.K_j]:
            is_attacking = True
            if self.current_animation != 'attack1':
                self.current_animation = 'attack1'
                self.sprite_sheet = self.attack1_image
                self.frame_index = 0
                self.animation_timer = 0
                self.attack_hit = False
        elif keys[pygame.K_k]:
            is_attacking = True
            if self.current_animation != 'attack2':
                self.current_animation = 'attack2'
                self.sprite_sheet = self.attack2_image
                self.frame_index = 0
                self.animation_timer = 0
                self.attack_hit = False
        elif keys[pygame.K_l]:
            is_attacking = True
            if self.current_animation != 'attack3':
                self.current_animation = 'attack3'
                self.sprite_sheet = self.attack3_image
                self.frame_index = 0
                self.animation_timer = 0
                self.attack_hit = False

        if not is_attacking or self.animation_timer > self.animation_speed * (
                len(self.animations[self.current_animation]) // 2):
            if keys[pygame.K_a]:
                dx = -self.speed
                self.facing_right = False
                is_moving = True
            if keys[pygame.K_d]:
                dx = self.speed
                self.facing_right = True
                is_moving = True
            if keys[pygame.K_w]:
                dy = -self.speed
                is_moving = True
            if keys[pygame.K_s]:
                dy = self.speed
                is_moving = True

        new_rect_x = self.rect.move(dx, 0)
        if self.area_jogavel.contains(new_rect_x):
            self.rect.x += dx
        else:
            if dx < 0: self.rect.left = self.area_jogavel.left
            if dx > 0: self.rect.right = self.area_jogavel.right

        new_rect_y = self.rect.move(0, dy)
        if self.area_jogavel.contains(new_rect_y):
            self.rect.y += dy
        else:
            if dy < 0: self.rect.top = self.area_jogavel.top
            if dy > 0: self.rect.bottom = self.area_jogavel.bottom

        if not is_attacking:
            if is_moving:
                if self.current_animation != 'run':
                    self.current_animation = 'run'
                    self.sprite_sheet = self.run_image
                    self.frame_index = 0
                    self.animation_timer = 0
            else:
                if self.current_animation != 'idle':
                    self.current_animation = 'idle'
                    self.sprite_sheet = self.idle_image
                    self.frame_index = 0
                    self.animation_timer = 0
                    self.attack_hit = False  # Garante reset se parar moviment


    def update_animation(self):
        if not self.is_alive:
            return

        animation_config = self.animations.get(self.current_animation)
        if not animation_config:
            self.current_animation = 'idle'
            self.sprite_sheet = self.idle_image
            animation_config = self.animations['idle']

        num_frames = len(animation_config)

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % num_frames

            if self.current_animation.startswith(
                    'attack') and self.frame_index == 0:
                self.current_animation = 'idle'
                self.sprite_sheet = self.idle_image
                self.attack_hit = False
                animation_config = self.animations['idle']
                num_frames = len(animation_config)

        frame_pos = animation_config[self.frame_index]
        try:
            self.image = self.sprite_sheet.subsurface((
                                                      frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height,
                                                      self.frame_width, self.frame_height))
        except ValueError as e:
            frame_pos = self.animations['idle'][0]
            self.sprite_sheet = self.idle_image
            self.image = self.sprite_sheet.subsurface((
                                                      frame_pos[0] * self.frame_width, frame_pos[1] * self.frame_height,
                                                      self.frame_width, self.frame_height))
            self.current_animation = 'idle'
            self.frame_index = 0


    def draw(self, surface, offset_x, offset_y=0):
        if not self.is_alive:
            return

        self.update_animation()
        image_to_draw = self.image
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        surface.blit(image_to_draw, (self.rect.x - offset_x, self.rect.y - offset_y))

    def take_damage(self, amount):
        if self.is_alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_alive = False