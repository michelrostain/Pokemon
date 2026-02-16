import pygame
from screen import Screen

class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.interface = self.screen # LE MENU UTILISERA ÇA POUR DESSINER

    def run(self):
        """LA BOUCLE PRINCIPALE"""
        while self.running:
            # 1. ON GÈRE LES ÉVÉNEMENTS (CLIC, TOUCHE CLAVIER)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # 2. ON MET À JOUR L'ÉCRAN
            self.screen.update()

        pygame.quit()