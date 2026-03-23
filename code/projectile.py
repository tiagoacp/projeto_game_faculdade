#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.entity import Entity
from assets.Const import WIN_WIDTH


class Projectile(Entity):
    def __init__(self, position: tuple, facing_right: bool):
        # Desenhando o projétil via código (um retângulo amarelo)
        self.surf = pygame.Surface((10, 4))
        self.surf.fill((255, 200, 0))
        self.rect = self.surf.get_rect(center=position)

        self.name = "Projectile"
        self.health = 1  # Para ser destruído ao bater
        self.damage = 5  # Dano que causa
        self.speed = 15
        self.facing_right = facing_right

        # --- NOVO: Lógica de distância ---
        self.start_x = position[0]
        self.max_distance = 350  # Distância máxima que o tiro vai percorrer (ajuste como quiser)

    def update(self):
        # Movimentação
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Destrói se sair da tela OU se passar da distância máxima
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH:
            self.health = 0

        if abs(self.rect.x - self.start_x) > self.max_distance:
            self.health = 0

    def move(self):
        pass