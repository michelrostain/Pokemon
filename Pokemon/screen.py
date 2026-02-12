import pygame


class Screen:
    def __init__(self):
        self.display: pygame.Surface = pygame.display.set_mode(1280, 720)
        pygame.display.set.caption("Pokemon")  # nom de la fenetre
        self.clock = pygame.time.Clock()  # definir combien de fois par seconde action
        self.framerate = 60  # vitesse rafraichissment ecran

    def update(self):
        pygame.display.flip()
        pygame.display.update
        self.clock.tick(self.framerate)  # frequence rafraichissement
        self.display.fill(
            (0, 0, 0)
        )  # a chq tour ecran devient noir pour supprimer les elements

    def get_size(self):
        return self.display.get_size()

    def get_display(self):
        return self.display
