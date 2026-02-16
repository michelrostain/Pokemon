import random
import pygame
import os
import sys # Pour quitter proprement
from mainclass import Pokemon 

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
        self.nom_dresseur = "" # Variable pour stocker le nom du joueur

    def lancer_jeu(self, liste_brute):
        """
        Cette méthode orchestre tout le démarrage du jeu :
        Splash -> Accueil -> (Nom) -> Chargement -> Choix -> Combat
        """
        # 1. Ecran Splash Screen (3 secondes)
        self.interface.afficher_splash_screen()

        # 2. Ecran Accueil (Nouvelle / Reprendre / Ajouter)
        # On passe la liste_brute car on en aura besoin plus tard
        self.gerer_accueil(liste_brute)

    def gerer_accueil(self, liste_brute):
        """
        Gère la décision prise dans le menu principal.
        """
        # On demande à l'interface d'afficher les choix et d'attendre une réponse
        decision = self.interface.afficher_menu_accueil()

        if decision == "NOUVEAU":
            # 3. Ecran Saisie du Nom
            self.nom_dresseur = self.saisir_nom_dresseur()
            
            # 4. Ecran Chargement
            # Ici, tu pourras ajouter la ligne pour vider le JSON si nécessaire
            self.charger_donnees(liste_brute) 
            
            # 5. Ecran Choix du Pokemon
            self.choisir_pokemon()
            
            # 6. Lancement du combat (Génération adversaire + Affichage)
            self.generer_adversaire()
            self.interface.afficher_combattants(self.pokemon_joueur, self.pokemon_adversaire)

        elif decision == "REPRENDRE":
            # Simulation du chargement du nom (à connecter à ton JSON de sauvegarde plus tard)
            self.nom_dresseur = "Dresseur" 
            
            # On charge directement les données sans demander le nom
            self.charger_donnees(liste_brute)
            self.choisir_pokemon()
            
            self.generer_adversaire()
            self.interface.afficher_combattants(self.pokemon_joueur, self.pokemon_adversaire)

        elif decision == "AJOUTER":
            # On lance ton formulaire spécial
            self.lancer_formulaire_ajout()

    def saisir_nom_dresseur(self):
        """
        Gère la boucle logique pour que l'utilisateur tape son nom.
        """
        nom = ""
        saisie_en_cours = True

        while saisie_en_cours:
            # On envoie le texte actuel à l'interface pour qu'elle l'affiche
            self.interface.afficher_saisie_nom(nom)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # On valide si le nom n'est pas vide
                        if len(nom) > 0:
                            saisie_en_cours = False
                    elif event.key == pygame.K_BACKSPACE:
                        # On efface le dernier caractère
                        nom = nom[:-1]
                    else:
                        # On ajoute le caractère s'il est valide et si le nom n'est pas trop long
                        if len(nom) < 15 and event.unicode.isprintable():
                            nom += event.unicode
        
        return nom

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
                    sys.exit()

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
            
            self.interface.rafraichir() # Si besoin de rafraichir spécifiquement ici
            
        print(f"Joueur a choisi : {self.pokemon_joueur.nom}")
        return self.pokemon_joueur

    def generer_adversaire(self):
        """
        Choisit un adversaire au hasard.
        """
        self.pokemon_adversaire = random.choice(self.mes_pokemons)
        print(f"L'adversaire sera : {self.pokemon_adversaire.nom}")
        return self.pokemon_adversaire

    def lancer_formulaire_ajout(self):
        """
        Méthode placeholder pour l'ajout de Pokémon via formulaire.
        """
        print("Lancement du formulaire d'ajout...")
        # Ici tu appelleras la méthode de l'interface correspondante
        # self.interface.afficher_formulaire_ajout()