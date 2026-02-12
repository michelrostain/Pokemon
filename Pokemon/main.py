from mainclass import *
from menu import Menu
from combat import combat
import pygame
from game import Game

pygame.init()
if __name__ == "__main__":
    game = Game()
    game.run()


def lancer_jeu():
    # 1. Initialisation du Menu et de Pygame
    mon_menu = Menu()
