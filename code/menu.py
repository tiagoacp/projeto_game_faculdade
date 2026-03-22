#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from assets.Const import WIN_WIDTH, COLOR_TEXT, MENU_OPTION, COLOR_YELLOW


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./assets/menu_1.png").convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)



    def run(self, ):
        menu_option = 0
        pygame.mixer.music.load("./assets/Menu_son.mp3")
        pygame.mixer_music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        while True:
            #imagens menu e nome do game
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(text_size=50, text="Survival in", text_color=COLOR_TEXT, text_center_pos=((WIN_WIDTH/2), 60))
            self.menu_text(text_size=50, text="The City", text_color=COLOR_TEXT, text_center_pos=((WIN_WIDTH / 2), 110))


            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(text_size=20, text=MENU_OPTION[i], text_color=COLOR_YELLOW, text_center_pos=((WIN_WIDTH/2), 300 + 30 * i))
                else:
                    self.menu_text(text_size=20, text=MENU_OPTION[i], text_color=COLOR_TEXT, text_center_pos=((WIN_WIDTH/2), 300 + 30 * i))

            pygame.display.flip()

#          check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: # DOWN KEY(para baixo)
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP: #UP KEY(para cima)
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN: #ENTER
                        return MENU_OPTION[menu_option]


    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)