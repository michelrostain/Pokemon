import json
import pygame
import time
import random

class Combat:
    def __init__(self, interface, joueur, adversaire):
        self.interface = interface
        self.joueur = joueur
        self.adversaire = adversaire
        self.table_types = self.charger_types()

    def charger_types(self):
        try:
            with open("types.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}

    def calculer_degats(self, atk, defe):
        coeff = 1.0
        t_atk = atk.type_principal.upper()
        t_def = defe.type_principal.upper()
        
        # Récupération du coefficient dans la table des types
        if t_atk in self.table_types:
            coeff = self.table_types[t_atk].get(t_def, 1.0)
        
        # Formule de dégâts simplifiée
        degats = int((atk.attaque - (defe.defense // 2)) * coeff)
        return max(1, degats), coeff

    def lancer_combat(self):
        tour_joueur = True
        
        # Boucle tant que personne n'est KO
        while not self.joueur.est_ko() and not self.adversaire.est_ko():
            self.interface.afficher_combattants(self.joueur, self.adversaire)
            
            if tour_joueur:
                # --- TOUR DU JOUEUR ---
                self.interface.afficher_dialogue(f"À toi ! (ESPACE pour attaquer)")
                attente = True
                while attente:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                             pygame.quit(); exit()
                        
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            # 1. Calcul de la chance de toucher (1 chance sur 10 de rater)
                            chance = random.randint(1, 10)
                            
                            if chance == 1:
                                # CAS : L'attaque échoue
                                self.interface.afficher_dialogue(f"Mince ! {self.joueur.nom} a raté son attaque !")
                                time.sleep(1.5)
                            else:
                                # CAS : L'attaque touche
                                dmg, c = self.calculer_degats(self.joueur, self.adversaire)
                                self.adversaire.subir_degats(dmg)
                                
                                msg = f"{self.joueur.nom} inflige {dmg} dégâts !"
                                if c > 1.5: msg += " (C'est super efficace !)"
                                elif c < 0.8: msg += " (Ce n'est pas très efficace...)"
                                
                                self.interface.afficher_dialogue(msg)
                                time.sleep(1.5)
                            
                            attente = False # Fin du tour du joueur
                tour_joueur = False
            
            else:
                # --- TOUR DE L'ADVERSAIRE ---
                self.interface.afficher_dialogue(f"{self.adversaire.nom} attaque...")
                time.sleep(1)
                
                # 1. Calcul de la chance de toucher
                chance = random.randint(1, 3)
                
                if chance == 1:
                    # CAS : L'attaque échoue
                    self.interface.afficher_dialogue(f"Chance ! {self.adversaire.nom} a raté son attaque !")
                    time.sleep(1.5)
                else:
                    # CAS : L'attaque touche
                    dmg, c = self.calculer_degats(self.adversaire, self.joueur)
                    self.joueur.subir_degats(dmg)
                    
                    msg = f"{self.adversaire.nom} inflige {dmg} dégâts !"
                    if c > 1.5: msg += " (C'est super efficace !)" # Aïe pour le joueur
                    elif c < 0.8: msg += " (Ce n'est pas très efficace...)"
                    
                    self.interface.afficher_dialogue(msg)
                    time.sleep(1.5)
                
                tour_joueur = True

        # Fin du combat
        if self.adversaire.est_ko(): return "VICTOIRE"
        return "DEFAITE"