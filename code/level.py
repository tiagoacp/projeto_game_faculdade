#!/usr/bin/python
# -*- coding: utf-8 -*-
# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from pygame import event, Surface, Rect
from pygame.font import Font

from assets.Const import COLOR_TEXT, WIN_HEIGHT
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.projectile import Projectile


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Carrega o cenário
        self.entity_list.extend(EntityFactory.get_entity("Level1Bg"))

        # Carrega e isola o Player para gerirmos a vida e o tiro facilmente
        self.player = EntityFactory.get_entity("Player1")
        self.entity_list.append(self.player)

        self.timeout = 20000
        self.spawn_timer = 0  # Temporizador para spawnar zumbis

    def run(self):
        pygame.mixer_music.load(f"./assets/{self.name}.mp3")  # Ou o formato que estiver usando
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.window.fill((0, 0, 0))

            # --- LÓGICA DE SPAWN DOS ZUMBIS ---
            self.spawn_timer += 1
            if self.spawn_timer >= 180:  # Spawna um zumbi a cada 3 segundos (60 fps * 3)
                self.spawn_timer = 0
                self.entity_list.append(EntityFactory.get_entity("Zombie2"))

            # --- VERIFICA SE O JOGADOR ATIROU ---
            shoot_trigger = False
            if hasattr(self.player, 'is_shooting') and self.player.is_shooting:
                spawn_pos = self.player.projectile_spawn_point
                facing = self.player.facing_right
                # crinando o projetio e add na list
                new_projectile = Projectile(position=spawn_pos, facing_right=facing)
                self.entity_list.append(new_projectile)
                # resetando a animacao
                self.player.is_shooting = False

            # Movimentação e Renderização das entidades
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if hasattr(ent, "update"):
                    ent.update()

                # --- SISTEMA DE COMBATE (Apenas zumbis) ---
                if ent.name == "Zombie2":

                    # 1. Zumbi atacando o Player
                    if pygame.sprite.collide_mask(ent, self.player):
                        ent.state = "Attack"
                        if ent.attack_cooldown <= 0:
                            self.player.health -= ent.damage
                            ent.attack_cooldown = 60
                    else:
                        ent.state = "Walk"

                    # 2. Player atacando o Zumbi (Tiro pega numa linha reta de 400 pixels)
                    if ent.name == "Projectile":
                        for target in self.entity_list:
                            if target.name == "Zombie2" and target.health > 0:
                                # colisao do inimigo
                                if ent.rect.colliderect(target.rect):
                                    target.health -= ent.damage  # 5 de dano
                                    ent.health = 0  # destroi projetio quando acerta
                                    break

            # --- LIMPEZA DE CADÁVERES ---
            # Remove da lista as entidades que têm vida igual ou menor que 0
            self.entity_list = [ent for ent in self.entity_list if getattr(ent, 'health', 1) > 0]

            # --- GAME OVER SE O JOGADOR MORRER ---
            if self.player.health <= 0:
                print("O Jogador Morreu! Game Over!")
                pygame.quit()
                sys.exit()  # Encerra o jogo abruptamente (temporário)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # --- TEXTOS DA TELA ---
            # Exibe a Vida na tela (Destacada em vermelho)
            self.level_text(text_size=20, text=f"HP Player: {self.player.health}/10", text_color=(255, 50, 50),
                            text_pos=(10, 40))

            # Textos padrões
            self.level_text(text_size=14, text=f"{self.name} - Timeout: {self.timeout / 1000 :.1f}s",
                            text_color=COLOR_TEXT, text_pos=(10, 5))
            self.level_text(text_size=14, text=f"fps: {clock.get_fps() : .0f}", text_color=COLOR_TEXT,
                            text_pos=(10, WIN_HEIGHT - 35))

            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)