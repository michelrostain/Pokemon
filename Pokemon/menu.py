import random
import pygame
import os
from mainclass import Pokemon # Import de ta classe Pokemon

class Menu:
    def __init__(self, interface):
        """
        Le constructeur reçoit l'objet 'interface' qui gère Pygame.
        Cela permet de séparer la logique du visuel.
        """
        self.interface = interface
        self.mes_pokemons = [] # Liste des instances de Pokemon créées
        self.pokemon_joueur = None
        self.pokemon_adversaire = None
            

    def charger_donnees(self, liste_brute):
        """
        Parcourt le JSON brut, crée les objets Pokemon et 
        demande à l'interface d'afficher la progression.
        """
        nb_total = len(liste_brute)
        
        for i, p in enumerate(liste_brute):
            # 1. Mise à jour visuelle du chargement via l'interface
            self.interface.afficher_ecran_chargement(i + 1, nb_total)
            
            # 2. Préparation des données du Pokémon
            nom_p = p["nom"]
            chemin_image = f"Assets/Images/{nom_p}.png"
            if not os.path.exists(chemin_image):
                chemin_image = "Assets/Images/PokeDefaut.png"

            # 3. Création de l'instance Pokemon
            nouveau_p = Pokemon(
                nom=p["nom"],
                pv=p["pv"],
                attaque=p["attaque"],
                defense=p["defense"],
                vitesse=p.get("vitesse", 50),
                image_url=chemin_image,
                type_principal=p["types"][0],
                evolution_nom=p["evolution"]
            )
            
            # On demande à l'interface de préparer la surface de l'image
            nouveau_p.image_surface = self.interface.preparer_image(chemin_image)
            
            self.mes_pokemons.append(nouveau_p)

    def choisir_pokemon(self):
        """
        Gère la logique de sélection du Pokémon par le joueur.
        """
        choix_possibles = random.sample(self.mes_pokemons, 3)
        selectionne = False

        while not selectionne:
            # On délègue l'affichage des 3 choix à l'interface
            self.interface.afficher_menu_selection(choix_possibles)

            # On gère uniquement les entrées clavier ici
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.pokemon_joueur = choix_possibles[0]
                        selectionne = True
                    elif event.key == pygame.K_2:
                        self.pokemon_joueur = choix_possibles[1]
                        selectionne = True
                    elif event.key == pygame.K_3:
                        self.pokemon_joueur = choix_possibles[2]
                        selectionne = True
            
            self.interface.rafraichir()
            
        print(f"Joueur a choisi : {self.pokemon_joueur.nom}")
        return self.pokemon_joueur

    def generer_adversaire(self):
        """
        Choisit un adversaire au hasard.
        """
        self.pokemon_adversaire = random.choice(self.mes_pokemons)
        print(f"L'adversaire sera : {self.pokemon_adversaire.nom}")
        return self.pokemon_adversaire