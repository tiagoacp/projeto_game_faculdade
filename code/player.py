#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.entity import Entity

# !/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.entity import Entity
from assets.Const import WIN_WIDTH


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        # Ignoramos o super().__init__ aqui para carregar a spritesheet de forma personalizada
        self.name = name
        self.speed = 3  # Velocidade de movimento

        self.health = 10
        self.is_shooting = False
        self.projectile_spawn_point = (0, 0)

        # Carrega as spritesheets
        self.image_idle = pygame.image.load("./assets/Player_1/Idle.png").convert_alpha()
        self.image_walk = pygame.image.load("./assets/Player_1/Walk.png").convert_alpha()
        self.image_shoot = pygame.image.load("./assets/Player_1/Shot_2.png").convert_alpha()

        # Configurações de animação
        # Nota: Ajuste a quantidade de frames abaixo dependendo de quantos "bonecos" tem na sua imagem
        self.frames_idle = 8
        self.frames_walk = 8
        self.frames_shoot = 4

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.06  # Velocidade da troca de quadros

        self.state = "Idle"
        self.facing_right = True

        # Configura a superfície inicial
        self.frame_width = self.image_idle.get_width() // self.frames_idle
        self.frame_height = self.image_idle.get_height()
        self.surf = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(left=position[0], bottom=position[1])

    def update(self):
        # Só avança a animação se estiver andando
        if self.state == "Shoot":
            self.animation_timer += self.animation_speed
            frame_index = int(self.animation_timer)

            # Se a animação do disparo chegar ao fim, volta a ficar parado
            if frame_index >= self.frames_shoot:
                self.state = "Idle"
                self.animation_timer = 0
                frame_index = 0
                current_image = self.image_idle
                self.frame_width = current_image.get_width() // self.frames_idle
            else:
                current_image = self.image_shoot
                self.frame_width = current_image.get_width() // self.frames_shoot

        elif self.state == "Walk":
            self.animation_timer += self.animation_speed
            frame_index = int(self.animation_timer) % self.frames_walk
            current_image = self.image_walk
            self.frame_width = current_image.get_width() // self.frames_walk

        else:  # Estado Idle (Parado estático)
            frame_index = 0
            current_image = self.image_idle
            self.frame_width = current_image.get_width() // self.frames_idle

        self.frame_height = current_image.get_height()

        # Limpa e recorta o fotograma correto da spritesheet
        self.surf = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        self.surf.blit(current_image, (0, 0), (frame_index * self.frame_width, 0, self.frame_width, self.frame_height))

        # Inverte a imagem caso esteja voltado para a esquerda
        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self.mask = pygame.mask.from_surface(self.surf)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.state != "Shoot":
            self.state = "Shoot"
            self.animation_timer = 0

            # --- ATUALIZA A POSIÇÃO E AVISA QUE ATIROU ---
            self.is_shooting = True
            gun_x_offset = 55
            gun_y_offset = -22
            if self.facing_right:
                self.projectile_spawn_point = (self.rect.left + gun_x_offset, self.rect.top + gun_y_offset)
            else:
                self.projectile_spawn_point = (self.rect.right - gun_x_offset, self.rect.top + gun_y_offset)
            return

        # Só permite andar se não estiver a atirar
        if self.state != "Shoot":
            moving = False

            # Movimento Esquerda
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.state = "Walk"
                self.facing_right = False
                moving = True

            # Movimento Direita
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.speed
                self.state = "Walk"
                self.facing_right = True
                moving = True

            # Se não premiu nenhum botão de andar, fica parado
            if not moving:
                self.state = "Idle"

            # Limita o movimento para o jogador não sair do ecrã
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIN_WIDTH:
                self.rect.right = WIN_WIDTH