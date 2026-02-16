import random
import pygame
import os
import sys
# On garde tes imports
from pokemon import Pokemon 
# On importe TA nouvelle classe qui gère les données
from pokedex import Pokedex 
from combat import Combat

class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.mes_pokemons = [] 
        self.pokemon_joueur = None
        self.pokemon_adversaire = None
        self.nom_dresseur = ""
        
        # --- NOUVEAUTÉ : On connecte le cerveau du Pokedex ---
        self.gestion_pokedex = Pokedex() 

    def lancer_jeu(self, liste_brute):
        self.interface.afficher_splash_screen()
        self.gerer_accueil(liste_brute)

    def gerer_accueil(self, liste_brute):
        decision = self.interface.afficher_menu_accueil()

        if decision == "NOUVEAU":
            self.nom_dresseur = self.saisir_nom_dresseur()
            self.charger_donnees(liste_brute) 
            self.choisir_pokemon()
            self.generer_adversaire()
            # On crée l'instance du combat
            combat_en_cours = Combat(self.interface, self.pokemon_joueur, self.pokemon_adversaire)

            # On lance la bagarre !
            resultat = combat_en_cours.lancer_combat()

            # Une fois le combat fini (return), on revient au menu ou on quitte
            print(f"Fin du combat : {resultat}")
            self.lancer_jeu(self.mes_pokemons) # Retour à l'accueil pour rejouer

        elif decision == "REPRENDRE":
            self.nom_dresseur = "Dresseur" 
            self.charger_donnees(liste_brute)
            self.choisir_pokemon()
            self.generer_adversaire()
            # On crée l'instance du combat
            combat_en_cours = Combat(self.interface, self.pokemon_joueur, self.pokemon_adversaire)

            # On lance la bagarre !
            resultat = combat_en_cours.lancer_combat()

            # Une fois le combat fini (return), on revient au menu ou on quitte
            print(f"Fin du combat : {resultat}")
            self.lancer_jeu(self.mes_pokemons) # Retour à l'accueil pour rejouer

        elif decision == "AJOUTER":
            # --- CHANGEMENT ICI ---
            # On n'appelle plus le formulaire manuel, mais le catalogue
            self.lancer_ajout_via_pokedex()

    def saisir_nom_dresseur(self):
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
                        if len(nom) > 0: saisie_en_cours = False
                    elif event.key == pygame.K_BACKSPACE:
                        nom = nom[:-1]
                    else:
                        if len(nom) < 15 and event.unicode.isprintable():
                            nom += event.unicode
        return nom

    def charger_donnees(self, liste_brute):
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
        return self.pokemon_joueur

    def generer_adversaire(self):
        self.pokemon_adversaire = random.choice(self.mes_pokemons)
        return self.pokemon_adversaire

    # =========================================================
    # NOUVELLE LOGIQUE QUI UTILISE TON FICHIER POKEDEX.PY
    # =========================================================
    def lancer_ajout_via_pokedex(self):
        """
        Affiche le catalogue (chargé par Pokedex class) et permet d'ajouter
        un Pokémon à la sauvegarde via la méthode enregistrer_pokemon.
        """
        # 1. On récupère la liste complète depuis ta classe Pokedex
        catalogue = self.gestion_pokedex.catalogue
        
        if not catalogue:
            print("Erreur : Impossible de charger le catalogue (pokemon.json absent ?)")
            return

        # Variables pour le scroll
        index_scroll = 0      
        nb_visibles = 5       
        choix_fait = False

        while not choix_fait:
            # On demande à l'interface d'afficher la liste (elle a besoin de savoir où on en est)
            self.interface.afficher_liste_scrollable(catalogue, index_scroll, nb_visibles)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # --- Scroll Clavier ---
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if index_scroll < len(catalogue) - nb_visibles:
                            index_scroll += 1
                    elif event.key == pygame.K_UP:
                        if index_scroll > 0:
                            index_scroll -= 1
                    elif event.key == pygame.K_ESCAPE:
                        choix_fait = True # Annuler

                # --- Scroll Souris ---
                elif event.type == pygame.MOUSEWHEEL:
                    index_scroll -= event.y 
                    index_scroll = max(0, min(index_scroll, len(catalogue) - nb_visibles))

                # --- Validation Souris ---
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # L'interface renvoie sur quelle ligne (0 à 4) on a cliqué
                        ligne = self.interface.detecter_clic_liste_scroll(event.pos)
                        
                        if ligne != -1:
                            index_reel = index_scroll + ligne
                            if 0 <= index_reel < len(catalogue):
                                # BINGO : On a choisi un pokémon
                                pokemon_choisi = catalogue[index_reel]
                                
                                # C'est ICI qu'on utilise ta classe Pokedex pour sauvegarder !
                                self.gestion_pokedex.enregistrer_pokemon(pokemon_choisi["nom"])
                                
                                choix_fait = True # Retour au menu