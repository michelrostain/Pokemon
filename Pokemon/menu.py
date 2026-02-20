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
        
        # On récupère l'XP si elle existe dans le dictionnaire, sinon 0
        xp_sauvegardee = dictionnaire_stats.get("xp", 0)
        
        p = Pokemon(
            nom=nom_p,
            pv=dictionnaire_stats["pv"],
            attaque=dictionnaire_stats["attaque"],
            defense=dictionnaire_stats["defense"],
            vitesse=dictionnaire_stats.get("vitesse", 50),
            image_url=f"Assets/Images/{nom_p}.png",
            type_principal=dictionnaire_stats["types"][0],
            evolution_nom=dictionnaire_stats["evolution"],
            xp_actuel=xp_sauvegardee
        )
        p.image_surface = image_surface
        return p

    def choisir_pokemon(self, seulement_base=False):
        candidats = self.mes_pokemons
        
        # --- CAS 1 : NOUVELLE PARTIE (STARTERS) ---
        if seulement_base:
            # On ne garde que ceux qui peuvent évoluer (base)
            noms_evolues = [p.evolution_nom for p in self.mes_pokemons if p.evolution_nom]
            pool_starters = [p for p in self.mes_pokemons if p.nom not in noms_evolues]
            
            # ON PREND 3 AU HASARD (Comme tu le voulais)
            if len(pool_starters) >= 3:
                candidats = random.sample(pool_starters, 3)
            else:
                candidats = pool_starters
        
        # --- CAS 2 : CONTINUER (Toute la liste) ---
        else:
            # On prend tout l'inventaire sans limiter à 3
            candidats = self.mes_pokemons

        # On envoie la liste (soit de 3, soit de 20) à l'écran
        selection = self.interface.selectionner_starter_graphique(candidats)
        
        if selection is None:
            return False

        self.pokemon_joueur = selection
        return True

    def demarrer_cycle_combat(self):
        if not self.catalogue_global: return
        
        # Choix d'un adversaire au hasard
        data_adversaire = random.choice(self.catalogue_global)
        # On s'assure que l'adversaire a une image préparée (sinon bug d'affichage possible)
        self.interface.preparer_image(data_adversaire["nom"]) 
        self.pokemon_adversaire = self.creer_objet_pokemon(data_adversaire)
        
        # Lancement du combat
        combat = Combat(self.interface, self.pokemon_joueur, self.pokemon_adversaire)
        resultat = combat.lancer_combat()
        
        if resultat == "VICTOIRE":
            self.interface.afficher_dialogue(f"Victoire ! {self.pokemon_adversaire.nom} ajouté.")
            
            # --- 1. On enregistre l'adversaire capturé (XP = 0 par défaut) ---
            self.gestion_pokedex.enregistrer_pokemon(self.pokemon_adversaire.nom)
            pygame.time.delay(1000)
            
            # --- 2. Le joueur gagne de l'XP ---
            self.interface.afficher_dialogue(f"{self.pokemon_joueur.nom} gagne de l'expérience...")
            pygame.time.delay(1000)
            
            doit_evoluer = self.pokemon_joueur.gagner_xp(50)
            
            # --- 3. IMPORTANT : ON SAUVEGARDE L'XP DU JOUEUR ---
            self.gestion_pokedex.mettre_a_jour_progression(self.pokemon_joueur)
            # ---------------------------------------------------
            
            # Évolution
            if doit_evoluer:
                nom_evo = self.pokemon_joueur.evolution_nom
                stats_evo = next((p for p in self.catalogue_global if p["nom"] == nom_evo), None)
                
                if stats_evo:
                    # --- ETAPE 1 : ON MEMORISE L'ANCIEN NOM ---
                    ancien_nom = self.pokemon_joueur.nom
                    # ------------------------------------------

                    self.interface.afficher_dialogue(f"Quoi ? {ancien_nom} évolue !")
                    pygame.time.delay(2000)
                    
                    nouvelle_img = self.interface.preparer_image(nom_evo)
                    self.pokemon_joueur.evoluer(stats_evo, nouvelle_img)
                    
                    self.interface.afficher_dialogue(f"Félicitations ! C'est maintenant un {self.pokemon_joueur.nom} !")
                    pygame.time.delay(2000)
                    
                    # --- ETAPE 2 : NETTOYAGE DE LA SAUVEGARDE ---
                    # On supprime l'ancienne forme (ex: Bulbizarre)
                    self.gestion_pokedex.supprimer_pokemon(ancien_nom)
                    
                    # On sauvegarde la nouvelle forme (ex: Herbizarre) avec son XP
                    self.gestion_pokedex.mettre_a_jour_progression(self.pokemon_joueur)
                    # --------------------------------------------
            
        else:
            # --- CAS DE DÉFAITE ---
            self.interface.afficher_dialogue(f"Défaite... {self.pokemon_joueur.nom} retourne chez sa mère.")
            pygame.time.delay(2000)

            # 1. On le supprime de la sauvegarde (Le vrai juge de paix)
            self.gestion_pokedex.supprimer_pokemon(self.pokemon_joueur.nom)

            # 2. On vérifie ce qu'il reste VRAIMENT dans la sauvegarde
            survivants = self.gestion_pokedex.obtenir_pokedex_joueur()

            if not survivants:
                # C'est vide, c'est la fin
                self.interface.afficher_dialogue("Plus de Pokémon... !! GAME OVER !!")
                pygame.time.delay(3000)
                # Retour au menu principal (la boucle while du menu gèrera la suite)
                return 
            else:
                self.interface.afficher_dialogue("Attention, 1 pokemon en moins !")
                pygame.time.delay(2000)    
    def consulter_mon_pokedex(self):
        while True:
            mes_pokemons_data = self.gestion_pokedex.obtenir_pokedex_joueur()
            action = self.interface.afficher_inventaire_joueur(mes_pokemons_data)
            
            if action == "ALLER_AJOUT":
                self.lancer_ajout_via_pokedex()
            else:
                break

    def lancer_ajout_via_pokedex(self):
        catalogue_complet = self.gestion_pokedex.catalogue
        
        # --- ETAPE DE FILTRAGE : GARDER UNIQUEMENT LES NON-EVOLUES ---
        
        # 1. On liste tous les noms qui sont des évolutions (ex: Herbizarre, Dracaufeu...)
        # On regarde le champ "evolution" de tout le monde pour savoir qui est une "suite"
        noms_devenus_evolutions = [p['evolution'] for p in catalogue_complet if p['evolution'] is not None]
        
        # 2. On garde seulement les Pokémons dont le nom n'apparaît pas dans la liste des évolutions
        catalogue_filtre = [p for p in catalogue_complet if p['nom'] not in noms_devenus_evolutions]
        
        # -------------------------------------------------------------

        index = 0
        running = True
        while running:
            # ATTENTION : On utilise maintenant 'catalogue_filtre' pour l'affichage
            self.interface.afficher_liste_scrollable(catalogue_filtre, index, 5)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: running = False
                    # On borne l'index sur la taille de la liste FILTRÉE
                    if event.key == pygame.K_DOWN: index = min(index+1, max(0, len(catalogue_filtre)-5))
                    if event.key == pygame.K_UP: index = max(0, index-1)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ligne = self.interface.detecter_clic_liste_scroll(event.pos)
                    # On vérifie le clic par rapport à la liste FILTRÉE
                    if ligne != -1 and (index + ligne) < len(catalogue_filtre):
                        nom = catalogue_filtre[index+ligne]["nom"]
                        
                        self.gestion_pokedex.enregistrer_pokemon(nom)
                        self.interface.afficher_dialogue(f"{nom} ajouté au Pokedex !")
                        pygame.time.delay(1000)
                        running = False