#!/usr/bin/python
# -*- coding: utf-8 -*-
from assets.Const import WIN_WIDTH
from code.entity import Entity


class Background(Entity):

    def __init__(self, name:str, position:tuple):
        super().__init__(name, position)

    def move(self, ):
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH

