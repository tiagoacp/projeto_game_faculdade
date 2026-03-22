#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.entity import Entity
from assets.Const import WIN_WIDTH


class Projectile(Entity):
    def __init__(self, position: tuple, facing_right: bool):
        # Em vez de carregar uma imagem, criamos um retângulo de 10x4 pixels
        self.surf = pygame.Surface((10, 4))
        self.surf.fill((255, 200, 0))  # Cor RGB: Amarelo/Laranja

        self.rect = self.surf.get_rect(center=position)

        # Novos atributos
        self.name = "Projectile"
        self.health = 1  # Vida de 1, para ser destruído ao bater
        self.damage = 10  # Dano que causa ao Zumbi
        self.speed = 15  # Velocidade do tiro (aumentei um pouco para ficar mais real)
        self.facing_right = facing_right

    def update(self):
        # Movimento
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Remove o tiro se ele sair da tela
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH:
            self.health = 0

    def move(self):
        pass