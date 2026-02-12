from mainclass import *
import random
import pygame
import os


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        self.en_cours = True

        # Se déclenche au démarrage du jeu, ajout Pokemon pour l'ordinateur

    def afficher_menu(self):
        pass

    def ajouter_pokemon(self):
        nb_total = len(liste_brute)
        for i, p in enumerate(liste_brute):
            # --- ÉCRAN DE CHARGEMENT ---
            self.screen.fill((0, 0, 0))  # Fond noir
            texte_load = self.font.render(
                f"Chargement des Pokemons... {i}/{nb_total}", True, (255, 255, 255)
            )
            self.screen.blit(texte_load, (250, 280))
            pygame.display.flip()
            nom_p = p["nom"]
            chemin_image = f"Assets/Images/{nom_p}.png"

            # On vérifie si l'image existe, sinon on met l'image par défaut
            if not os.path.exists(chemin_image):
                chemin_image = "Assets/Images/PokeDefaut.png"
            nouveau_p = Pokemon(
                nom=p["nom"],
                pv=p["pv"],
                attaque=p["attaque"],
                defense=p["defense"],
                vitesse=p.get("vitesse", 50),  # .get évite un crash si "vitesse" manque
                image_url=p.get(
                    "image", "Assets/Images/PokeDefaut.png"
                ),  # adapter selon ton JSON
                type_principal=p["types"][0],  # On prend le premier type de la liste
                evolution_nom=p["evolution"],
            )

            try:
                img = pygame.image.load(
                    chemin_image
                ).convert_alpha()  # .convert_alpha() gère la transparence
                nouveau_p.image_surface = pygame.transform.scale(img, (100, 100))
            except:
                # Si même le défaut bug, on crée un carré de couleur
                nouveau_p.image_surface = pygame.Surface((100, 100))
                nouveau_p.image_surface.fill((200, 200, 200))

            mes_pokemons.append(nouveau_p)

    def ajouter_utilisateur(self):
        choix_possibles = random.sample(mes_pokemons, 3)
        selectionne = False

        # On boucle TANT QUE l'utilisateur n'a pas fait de choix
        while not selectionne:
            # 1. On dessine l'interface (très important pour que l'écran ne soit pas noir)
            self.screen.fill((255, 255, 255))
            # Ici tu devrais ajouter tes self.screen.blit(...) pour afficher les noms
            titre = self.font.render("Choisissez votre Pokemon : ", True, (0, 0, 0))
            self.screen.blit(titre, (50, 30))

            for i, p in enumerate(choix_possibles):
                self.screen.blit(p.image_surface, (50, 80 + i * 150))
                y_bloc = 100 + i * 150
                pos_image = (50, y_bloc)
                pos_texte = (170, y_bloc + 40)
                if hasattr(p, "image_surface"):
                    self.screen.blit(p.image_surface, pos_image)
                texte = self.font.render(f"{i+1}. {p.nom}", True, (0, 0, 0))
                self.screen.blit(texte, pos_texte)

            # 2. On écoute les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.pokemon = choix_possibles[0]
                        selectionne = True
                    elif event.key == pygame.K_2:
                        self.pokemon = choix_possibles[1]
                        selectionne = True
                    elif event.key == pygame.K_3:
                        self.pokemon = choix_possibles[2]
                        selectionne = True

            # 3. On rafraîchit l'écran
            pygame.display.flip()
            self.clock.tick(60)  # Limite à 60 FPS pour ne pas surcharger ton processeur

        print(f"Bravo ! Tu as choisi : {self.pokemon.nom}")
        return self.pokemon

    def generer_adversaire(self):
        # Choix du pokemon de l'ordi, direct dans la liste totale des pokemons :
        self.pokemon_adversaire = random.choice(mes_pokemons)
        return self.pokemon_adversaire


if __name__ == "__main__":
    mon_menu = Menu()
    mon_menu.ajouter_pokemon()
    mon_menu.ajouter_utilisateur()
