import pygame

class Screen:
    def __init__(self):
        # ON DÉFINIT LA TAILLE DE LA FENÊTRE
        self.display = pygame.display.set_mode((1280, 720))
        # NOM DE LA FENÊTRE (CORRIGÉ)
        pygame.display.set_caption("Mon Jeu Pokemon")
        
        # GESTION DU TEMPS ET DE LA VITESSE (60 IMAGES PAR SECONDE)
        self.clock = pygame.time.Clock()
        self.framerate = 60

    def update(self):
        """MET À JOUR L'AFFICHAGE ET NETTOIE L'ÉCRAN"""
        pygame.display.flip()
        self.clock.tick(self.framerate)
        # ON REMPLIT EN NOIR POUR TOUT EFFACER AVANT DE RE-DESSINER
        self.display.fill((0, 0, 0))

    def preparer_image(self, chemin):
        """CHARGE UNE IMAGE ET LA PRÉPARE POUR PYGAME"""
        try:
            image = pygame.image.load(chemin)
            return image.convert_alpha() # OPTIMISE L'IMAGE
        except:
            # SI L'IMAGE N'EXISTE PAS, ON CHARGE UN CARRÉ VIDE
            return pygame.Surface((100, 100))

    def afficher_ecran_chargement(self, actuel, total):
        """AFFICHE UNE PETITE BARRE DE CHARGEMENT DANS LA CONSOLE"""
        print(f"Chargement : {actuel}/{total} Pokémon...")