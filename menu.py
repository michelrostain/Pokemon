import random
import pygame

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
                    # Plus élégant avec un petit écran de fin de combat réutilisé pour l'info
                    self.interface.afficher_dialogue("Pokedex vide ! Commencez une nouvelle partie.")
                    pygame.time.delay(2000)
                    continue
                
                self.charger_donnees_dans_mes_pokemons(sauvegarde)
                
                if not self.choisir_pokemon(seulement_base=False):
                    continue
                
                self.demarrer_cycle_combat()

            elif decision == "AJOUTER":
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
        image_surface = self.interface.preparer_image(nom_p)
        xp_sauvegardee = dictionnaire_stats.get("xp", 0)
        
        p = Pokemon(
            nom=nom_p,
            pv=dictionnaire_stats["pv"],
            attaque=dictionnaire_stats["attaque"],
            defense=dictionnaire_stats["defense"],
            vitesse=dictionnaire_stats.get("vitesse", 50),
            image_url=f"Assets/Images/{nom_p}.png",
            type_principal=dictionnaire_stats["types"][0],
            evolution_nom=dictionnaire_stats.get("evolution"),
            xp_actuel=xp_sauvegardee
        )
        p.image_surface = image_surface
        return p

    def choisir_pokemon(self, seulement_base=False):
        candidats = self.mes_pokemons
        
        if seulement_base:
            noms_evolues = [p.evolution_nom for p in self.mes_pokemons if p.evolution_nom]
            pool_starters = [p for p in self.mes_pokemons if p.nom not in noms_evolues]
            
            if len(pool_starters) >= 3:
                candidats = random.sample(pool_starters, 3)
            else:
                candidats = pool_starters
        else:
            candidats = self.mes_pokemons

        selection = self.interface.selectionner_starter_graphique(candidats)
        
        if selection is None:
            return False

        self.pokemon_joueur = selection
        return True

    def demarrer_cycle_combat(self):
        if not self.catalogue_global: return
        
        data_adversaire = random.choice(self.catalogue_global)
        self.interface.preparer_image(data_adversaire["nom"]) 
        self.pokemon_adversaire = self.creer_objet_pokemon(data_adversaire)
        
        combat = Combat(self.interface, self.pokemon_joueur, self.pokemon_adversaire)
        resultat = combat.lancer_combat()
        
        if resultat == "VICTOIRE":
            self.interface.afficher_ecran_fin_combat("VICTOIRE", self.pokemon_joueur, self.pokemon_adversaire, xp_gagne=50)
            self.gestion_pokedex.enregistrer_pokemon(self.pokemon_adversaire.nom)
            
            doit_evoluer = self.pokemon_joueur.gagner_xp(50)
            
            if doit_evoluer:
                nom_evo = self.pokemon_joueur.evolution_nom
                stats_evo = next((p for p in self.catalogue_global if p["nom"].lower().strip() == nom_evo.lower().strip()), None)
                
                if stats_evo:
                    ancien_nom = self.pokemon_joueur.nom
                    ancienne_img = self.pokemon_joueur.image_surface
                    
                    nouvelle_img = self.interface.preparer_image(nom_evo)
                    
                    # --- NOUVEAU : Appel du super écran d'évolution ! ---
                    self.interface.afficher_ecran_evolution(ancien_nom, ancienne_img, nom_evo, nouvelle_img)
                    
                    self.pokemon_joueur.evoluer(stats_evo, nouvelle_img)
                    self.gestion_pokedex.supprimer_pokemon(ancien_nom)
                    self.gestion_pokedex.mettre_a_jour_progression(self.pokemon_joueur)
            else:
                self.gestion_pokedex.mettre_a_jour_progression(self.pokemon_joueur)

        else:
            self.interface.afficher_ecran_fin_combat("DEFAITE", self.pokemon_joueur, self.pokemon_adversaire)
            self.gestion_pokedex.supprimer_pokemon(self.pokemon_joueur.nom)
            survivants = self.gestion_pokedex.obtenir_pokedex_joueur()

            if not survivants:
                self.interface.afficher_dialogue("Plus de Pokémon... !! GAME OVER !!")
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
        
        noms_devenus_evolutions = [p['evolution'] for p in catalogue_complet if p['evolution'] is not None]
        catalogue_filtre = [p for p in catalogue_complet if p['nom'] not in noms_devenus_evolutions]

        index = 0
        running = True
        while running:
            self.interface.afficher_liste_scrollable(catalogue_filtre, index, 5)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: running = False
                    if event.key == pygame.K_DOWN: index = min(index+1, max(0, len(catalogue_filtre)-5))
                    if event.key == pygame.K_UP: index = max(0, index-1)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ligne = self.interface.detecter_clic_liste_scroll(event.pos)
                    if ligne != -1 and (index + ligne) < len(catalogue_filtre):
                        nom = catalogue_filtre[index+ligne]["nom"]
                        
                        self.gestion_pokedex.enregistrer_pokemon(nom)
                        self.interface.afficher_dialogue(f"{nom} ajouté au Pokedex !")
                        pygame.time.delay(1000)
                        running = False