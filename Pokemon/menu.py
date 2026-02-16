import random
import pygame
import sys
from pokemon import Pokemon
from pokedex import Pokedex
from combat import Combat

class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.gestion_pokedex = Pokedex()
        self.mes_pokemons = []        
        self.catalogue_global = []    
        
        self.pokemon_joueur = None
        self.pokemon_adversaire = None

    def lancer_jeu(self, liste_brute):
        self.catalogue_global = liste_brute
        self.interface.afficher_splash_screen()
        self.gerer_accueil(liste_brute)

    def gerer_accueil(self, liste_brute):
        while True:
            decision = self.interface.afficher_menu_accueil()
            self.mes_pokemons = [] 

            if decision == "NOUVEAU":
                self.gestion_pokedex.vider_pokedex()
                self.charger_donnees_dans_mes_pokemons(liste_brute)
                
                if not self.choisir_pokemon(seulement_base=True):
                    continue
                
                self.gestion_pokedex.enregistrer_pokemon(self.pokemon_joueur.nom)
                self.demarrer_cycle_combat()

            elif decision == "REPRENDRE":
                sauvegarde = self.gestion_pokedex.obtenir_pokedex_joueur()
                if not sauvegarde:
                    self.interface.afficher_dialogue("Pokedex vide ! Commencez une nouvelle partie.")
                    pygame.time.delay(2000)
                    continue
                
                self.charger_donnees_dans_mes_pokemons(sauvegarde)
                
                if not self.choisir_pokemon(seulement_base=False):
                    continue
                
                self.demarrer_cycle_combat()

            elif decision == "AJOUTER":
                # CORRECTION : On appelle bien la consultation avant l'ajout
                self.consulter_mon_pokedex()

    def charger_donnees_dans_mes_pokemons(self, liste_source):
        self.mes_pokemons = []
        for i, p in enumerate(liste_source):
            if len(liste_source) > 5:
                self.interface.afficher_ecran_chargement(i + 1, len(liste_source))
            new_p = self.creer_objet_pokemon(p)
            self.mes_pokemons.append(new_p)

    def creer_objet_pokemon(self, dictionnaire_stats):
        nom_p = dictionnaire_stats["nom"]
        
        # On passe le NOM (pas le chemin) pour utiliser le cache
        image_surface = self.interface.preparer_image(nom_p)
        
        p = Pokemon(
            nom=nom_p,
            pv=dictionnaire_stats["pv"],
            attaque=dictionnaire_stats["attaque"],
            defense=dictionnaire_stats["defense"],
            vitesse=dictionnaire_stats.get("vitesse", 50),
            image_url=f"Assets/Images/{nom_p}.png",
            type_principal=dictionnaire_stats["types"][0],
            evolution_nom=dictionnaire_stats["evolution"]
        )
        p.image_surface = image_surface
        return p

    def choisir_pokemon(self, seulement_base=False):
        candidats = self.mes_pokemons
        if seulement_base:
            noms_evolues = [p.evolution_nom for p in self.mes_pokemons if p.evolution_nom]
            candidats = [p for p in self.mes_pokemons if p.nom not in noms_evolues]
        
        if not candidats: candidats = self.mes_pokemons
        
        choix = random.sample(candidats, 3) if len(candidats) > 3 else candidats
        
        selection = self.interface.selectionner_starter_graphique(choix)
        if selection is None: return False

        self.pokemon_joueur = selection
        return True

    def demarrer_cycle_combat(self):
        if not self.catalogue_global: return
        
        # Choix d'un adversaire au hasard
        data_adversaire = random.choice(self.catalogue_global)
        self.pokemon_adversaire = self.creer_objet_pokemon(data_adversaire)
        
        # Lancement du combat
        combat = Combat(self.interface, self.pokemon_joueur, self.pokemon_adversaire)
        resultat = combat.lancer_combat()
        
        if resultat == "VICTOIRE":
            # 1. Message de victoire
            self.interface.afficher_dialogue(f"Victoire ! {self.pokemon_adversaire.nom} ajouté.")
            self.gestion_pokedex.enregistrer_pokemon(self.pokemon_adversaire.nom)
            pygame.time.delay(1000) # Petite pause pour lire
            
            # 2. Gain d'XP (50 points par victoire -> évolution en 2 combats)
            self.interface.afficher_dialogue(f"{self.pokemon_joueur.nom} gagne de l'expérience...")
            pygame.time.delay(1000)
            
            doit_evoluer = self.pokemon_joueur.gagner_xp(50)
            
            # 3. Vérification de l'évolution
            if doit_evoluer:
                # On cherche les stats du Pokémon suivant (ex: "Herbizarre") dans la liste globale
                nom_evo = self.pokemon_joueur.evolution_nom
                stats_evo = next((p for p in self.catalogue_global if p["nom"] == nom_evo), None)
                
                if stats_evo:
                    self.interface.afficher_dialogue(f"Quoi ? {self.pokemon_joueur.nom} évolue !")
                    pygame.time.delay(2000)
                    
                    # On prépare la nouvelle image (grâce au cache de screen.py)
                    nouvelle_img = self.interface.preparer_image(nom_evo)
                    
                    # On applique la transformation
                    self.pokemon_joueur.evoluer(stats_evo, nouvelle_img)
                    
                    self.interface.afficher_dialogue(f"Félicitations ! Ton Pokémon est maintenant un {self.pokemon_joueur.nom} !")
                    pygame.time.delay(2000)
                    
                    # On met à jour le Pokedex du joueur avec le nouveau nom
                    self.gestion_pokedex.enregistrer_pokemon(self.pokemon_joueur.nom)
            
        else:
            # --- CAS DE DÉFAITE (MORT DU POKÉMON) ---
            self.interface.afficher_dialogue(f"Défaite... {self.pokemon_joueur.nom} nous a quitté.")
            pygame.time.delay(2000)

            # 1. On le supprime de la sauvegarde (JSON)
            self.gestion_pokedex.supprimer_pokemon(self.pokemon_joueur.nom)

            # 2. On le supprime de la liste en mémoire (RAM)
            # On utilise .remove() au lieu de .pop() pour cibler le bon !
            if self.pokemon_joueur in self.mes_pokemons:
                self.mes_pokemons.remove(self.pokemon_joueur)

            # 3. Vérification : Reste-t-il des survivants ?
            if not self.mes_pokemons:
                self.interface.afficher_dialogue("Tu n'as plus de Pokémon... !!GAME OVER !!")
                pygame.time.delay(3000)
                # On pourrait ici retourner au menu principal ou quitter
                # Pour l'instant, on laisse la boucle while du menu gérer le retour
                return 
            else:
                self.interface.afficher_dialogue("Attention, il ne te reste plus beaucoup de choix.")
                pygame.time.delay(2000)    # CORRECTION : Cette méthode gère l'écran "Mon Pokedex"
    
    def consulter_mon_pokedex(self):
        while True:
            mes_pokemons_data = self.gestion_pokedex.obtenir_pokedex_joueur()
            action = self.interface.afficher_inventaire_joueur(mes_pokemons_data)
            
            if action == "ALLER_AJOUT":
                self.lancer_ajout_via_pokedex()
            else:
                break

    def lancer_ajout_via_pokedex(self):
        catalogue = self.gestion_pokedex.catalogue
        index = 0
        running = True
        while running:
            self.interface.afficher_liste_scrollable(catalogue, index, 5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: running = False
                    if event.key == pygame.K_DOWN: index = min(index+1, len(catalogue)-5)
                    if event.key == pygame.K_UP: index = max(0, index-1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ligne = self.interface.detecter_clic_liste_scroll(event.pos)
                    if ligne != -1 and (index + ligne) < len(catalogue):
                        nom = catalogue[index+ligne]["nom"]
                        self.gestion_pokedex.enregistrer_pokemon(nom)
                        self.interface.afficher_dialogue(f"{nom} ajouté au Pokedex !")
                        pygame.time.delay(1000)
                        running = False