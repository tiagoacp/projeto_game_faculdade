#!/usr/bin/python
# -*- coding: utf-8 -*-
from assets.Const import WIN_WIDTH, WIN_HEIGHT
from code.background import Background
from code.player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name:str, position=(0,0)):
        match entity_name:
            case "Level1_":
                list_bg = []
                for i in range(10):
                    list_bg.append(Background(f"Level1_{i}", position=(0,0)))
                    list_bg.append(Background(f"Level1_{i}", position=(WIN_WIDTH,0)))
                return list_bg
            case "Player1":
                return Player("Player1", position(10, WIN_HEIGHT/2))
