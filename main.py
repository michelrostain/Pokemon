import pygame
from classPokedex import Pokedex
from menu import Menu
from game import Game

def lancer_jeu():
    pygame.init()
    
    # 1. ON CRÉE LE POKÉDEX (LES DONNÉES)
    mon_pokedex = Pokedex()
    
    # 2. ON LANCE LE JEU
    game = Game()
    
    # 3. ON DONNE LES DONNÉES AU MENU
    mon_menu = Menu(game.interface)
    mon_menu.charger_donnees(mon_pokedex)
    
    game.run()

if __name__ == "__main__":
    lancer_jeu()