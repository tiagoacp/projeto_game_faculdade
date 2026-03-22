#!/usr/bin/python
# -*- coding: utf-8 -*-
# code/entityFactory.py
from assets.Const import WIN_WIDTH, WIN_HEIGHT
from code.background import Background
from code.player import Player

class EntityFactory:

    @staticmethod
    def get_entity(entity_name:str, position=(0,0)):
        match entity_name:
            case "Level1Bg":  # <--- VEJA AQUI O NOME EXATO
                list_bg = []
                list_bg.append(Background("img_fase1", position=(0,0)))
                list_bg.append(Background("img_fase1", position=(WIN_WIDTH,0)))
                return list_bg
            case "Player1":
                return Player("Player1", position=(10, WIN_HEIGHT))
