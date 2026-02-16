import pygame

class Interface:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 750))
        self.font = pygame.font.SysFont("Arial", 30)

    def afficher_menu_accueil(self):
        choix = None
        while choix is None:
            self.screen.fill((30, 30, 30)) # Fond gris foncé
            
            # Dessin des options
            texte_1 = self.font.render("A : Nouvelle Partie", True, (255, 255, 255))
            texte_2 = self.font.render("B : Reprendre Partie", True, (255, 255, 255))
            texte_3 = self.font.render("C : Ajouter un Pokémon", True, (255, 255, 255))
            
            self.screen.blit(texte_1, (350, 250))
            self.screen.blit(texte_2, (350, 350))
            self.screen.blit(texte_3, (350, 450))
            
            pygame.display.flip()

            # Écoute des touches
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        choix = "NOUVEAU"
                    elif event.key == pygame.K_b:
                        choix = "REPRENDRE"
                    elif event.key == pygame.K_c:
                        choix = "AJOUTER"
        
        return choix # On renvoie la décision au Menu