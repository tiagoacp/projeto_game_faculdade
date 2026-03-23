#!/usr/bin/python
# -*- coding: utf-8 -*-

# !/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.entity import Entity


class Enemy(Entity):

    def __init__(self, name: str, position: tuple):
        self.name = name
        self.health = 5
        self.speed = 1.5
        self.damage = 1  # Dano que causa ao jogador
        self.attack_cooldown = 0
        # Carrega imagens do Zombie_2
        self.image_walk = pygame.image.load("./assets/Zombie_2/Walk.png").convert_alpha()
        self.image_attack = pygame.image.load("./assets/Zombie_2/Attack.png").convert_alpha()
        # ATENÇÃO: Se o seu zumbi ficar "piscando", ajuste a quantidade de quadros destas animações
        self.frames_walk = 10
        self.frames_attack = 5
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.state = "Walk"
        self.facing_right = True  # Zumbi nasce na esquerda e vai para a direita
        self.frame_width = self.image_walk.get_width() // self.frames_walk
        self.frame_height = self.image_walk.get_height()
        self.surf = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(left=position[0], bottom=position[1])

    def update(self):
        self.animation_timer += self.animation_speed

        if self.state == "Attack":
            frame_index = int(self.animation_timer) % self.frames_attack
            current_image = self.image_attack
            self.frame_width = current_image.get_width() // self.frames_attack
        else:  # Walk
            frame_index = int(self.animation_timer) % self.frames_walk
            current_image = self.image_walk
            self.frame_width = current_image.get_width() // self.frames_walk

        self.frame_height = current_image.get_height()

        self.surf = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        self.surf.blit(current_image, (0, 0), (frame_index * self.frame_width, 0, self.frame_width, self.frame_height))

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self.mask = pygame.mask.from_surface(self.surf)

    def move(self):
        # Só anda se não estiver atacando
        if self.state == "Walk":
            if self.facing_right:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        # Reduz o tempo de espera (cooldown) para o próximo ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1