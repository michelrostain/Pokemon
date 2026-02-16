import random
import pygame
import os
import sys
import json
from Pokemon.pokemon import Pokemon 

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
        Orchestre tout le démarrage du jeu :
        Splash -> Accueil -> (Nom) -> Chargement -> Choix -> Combat
        """
        # 1. Ecran Splash Screen (3 secondes)
        self.interface.afficher_splash_screen()

        # 2. Ecran Accueil (Nouvelle / Reprendre / Ajouter)
        self.gerer_accueil(liste_brute)

    def gerer_accueil(self, liste_brute):
        """
        Gère la décision prise dans le menu principal.
        """
        decision = self.interface.afficher_menu_accueil()

        if decision == "NOUVEAU":
            # 3. Ecran Saisie du Nom
            self.nom_dresseur = self.saisir_nom_dresseur()
            
            # 4. Ecran Chargement
            self.charger_donnees(liste_brute) 
            
            # 5. Ecran Choix du Pokemon
            self.choisir_pokemon()
            
            # 6. Lancement du combat
            self.generer_adversaire()
            self.interface.afficher_combattants(self.pokemon_joueur, self.pokemon_adversaire)

        elif decision == "REPRENDRE":
            self.nom_dresseur = "Dresseur" # A améliorer avec une vraie sauvegarde plus tard
            
            self.charger_donnees(liste_brute)
            self.choisir_pokemon()
            
            self.generer_adversaire()
            self.interface.afficher_combattants(self.pokemon_joueur, self.pokemon_adversaire)

        elif decision == "AJOUTER":
            self.lancer_formulaire_ajout()

    def saisir_nom_dresseur(self):
        """
        Gère la boucle logique pour que l'utilisateur tape son nom.
        """
        nom = ""
        saisie_en_cours = True

        while saisie_en_cours:
            self.interface.afficher_saisie_nom(nom)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(nom) > 0:
                            saisie_en_cours = False
                    elif event.key == pygame.K_BACKSPACE:
                        nom = nom[:-1]
                    else:
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
            self.interface.afficher_ecran_chargement(i + 1, nb_total)
            
            nom_p = p["nom"]
            chemin_image = f"Assets/Images/{nom_p}.png"
            if not os.path.exists(chemin_image):
                chemin_image = "Assets/Images/PokeDefaut.png"

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
            
            nouveau_p.image_surface = self.interface.preparer_image(chemin_image)
            self.mes_pokemons.append(nouveau_p)

    def choisir_pokemon(self):
        """
        Gère la logique de sélection du Pokémon par le joueur.
        """
        choix_possibles = random.sample(self.mes_pokemons, 3)
        selectionne = False

        while not selectionne:
            self.interface.afficher_menu_selection(choix_possibles)

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
            
            self.interface.rafraichir()
            
        print(f"Joueur a choisi : {self.pokemon_joueur.nom}")
        return self.pokemon_joueur

    def generer_adversaire(self):
        self.pokemon_adversaire = random.choice(self.mes_pokemons)
        print(f"L'adversaire sera : {self.pokemon_adversaire.nom}")
        return self.pokemon_adversaire

    def lancer_formulaire_ajout(self):
        """
        Gère la boucle d'interaction pour le formulaire de création.
        """
        nouvel_ajout = {
            "nom": "",
            "type": "",
            "pv": "",
            "attaque": "",
            "defense": ""
        }
        
        champ_actif = None 
        en_creation = True

        while en_creation:
            # On envoie les données et l'état (quel champ est actif) à l'interface
            self.interface.afficher_formulaire(nouvel_ajout, champ_actif)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # --- SOURIS ---
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # L'interface doit nous dire sur quoi on a cliqué
                    zone_cliquee = self.interface.detecter_clic_formulaire(event.pos)
                    
                    if zone_cliquee == "VALIDER":
                        if all(valeur != "" for valeur in nouvel_ajout.values()):
                            self.sauvegarder_nouveau_pokemon(nouvel_ajout)
                            en_creation = False
                    
                    elif zone_cliquee == "RETOUR":
                        en_creation = False
                        
                    else:
                        champ_actif = zone_cliquee

                # --- CLAVIER ---
                if event.type == pygame.KEYDOWN and champ_actif is not None:
                    if event.key == pygame.K_BACKSPACE:
                        nouvel_ajout[champ_actif] = nouvel_ajout[champ_actif][:-1]
                    
                    elif event.key == pygame.K_TAB:
                        pass 

                    else:
                        # Filtre chiffres pour les stats
                        if champ_actif in ["pv", "attaque", "defense"]:
                            if event.unicode.isdigit() and len(nouvel_ajout[champ_actif]) < 3:
                                nouvel_ajout[champ_actif] += event.unicode
                        # Filtre texte pour le reste
                        else:
                            if len(nouvel_ajout[champ_actif]) < 12:
                                nouvel_ajout[champ_actif] += event.unicode

    def sauvegarder_nouveau_pokemon(self, donnees):
        """
        Ecrit le nouveau pokemon dans le fichier JSON.
        """
        try:
            pokemon_propre = {
                "nom": donnees["nom"],
                "types": [donnees["type"]],
                "pv": int(donnees["pv"]),
                "attaque": int(donnees["attaque"]),
                "defense": int(donnees["defense"]),
                "vitesse": 50,
                "evolution": None,
                "image": "Assets/Images/PokeDefaut.png" 
            }

            with open("pokedex.json", "r", encoding="utf-8") as f:
                contenu_json = json.load(f)

            contenu_json.append(pokemon_propre)

            with open("pokedex.json", "w", encoding="utf-8") as f:
                json.dump(contenu_json, f, indent=4, ensure_ascii=False)
            
            print(f"Succès : {donnees['nom']} a été ajouté au Pokédex !")

        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")