import json
import pygame
import time
import sys

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
        except:
            print("Erreur: types.json introuvable.")
            return {}

    def calculer_efficacite(self, type_atk, type_def):
        # On met en majuscules pour correspondre au JSON (FEU, EAU...)
        t_atk = type_atk.upper()
        t_def = type_def.upper()
        
        if t_atk in self.table_types and t_def in self.table_types[t_atk]:
            return self.table_types[t_atk][t_def]
        return 1.0 # Par défaut (si type inconnu)

    def attaquer(self, attaquant, defenseur):
        """Calcule et applique une attaque"""
        
        # 1. Calcul des dégâts de base
        degats = attaquant.attaque - (defenseur.defense // 2)
        if degats < 1: degats = 1
        
        # 2. Gestion du Type (Feu vs Eau, etc.)
        coeff = self.calculer_efficacite(attaquant.type_principal, defenseur.type_principal)
        degats = int(degats * coeff)
        
        # 3. Application
        defenseur.subir_degats(degats)
        
        # 4. Message pour l'écran
        messages = [f"{attaquant.nom} attaque !"]
        
        if coeff > 1.0:
            messages.append("C'est super efficace !")
        elif coeff < 1.0 and coeff > 0:
            messages.append("Ce n'est pas très efficace...")
        elif coeff == 0:
            messages.append("Ça n'a aucun effet !")
            
        messages.append(f"{defenseur.nom} perd {degats} PV.")
        
        return messages

    def lancer_combat(self):
        """Boucle principale du combat"""
        en_cours = True
        tour_joueur = True 

        # Boucle tant que tout le monde est en vie
        while en_cours:
            # 1. Mise à jour visuelle
            self.interface.afficher_combattants(self.joueur, self.adversaire)
            
            # 2. Vérification Victoire/Défaite
            if self.adversaire.est_ko():
                self.interface.afficher_dialogue(f"Bravo ! {self.adversaire.nom} est K.O !")
                time.sleep(2)
                return "VICTOIRE"
            
            if self.joueur.est_ko():
                self.interface.afficher_dialogue(f"Oh non... {self.joueur.nom} est K.O.")
                time.sleep(2)
                return "DEFAITE"

            # 3. Gestion des tours
            if tour_joueur:
                self.interface.afficher_dialogue("Appuie sur ESPACE pour attaquer !")
                
                # Attente de l'action du joueur
                action_faite = False
                while not action_faite:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                # Le joueur attaque
                                logs = self.attaquer(self.joueur, self.adversaire)
                                for ligne in logs:
                                    self.interface.afficher_combattants(self.joueur, self.adversaire) # Refresh visuel
                                    self.interface.afficher_dialogue(ligne)
                                    time.sleep(1) # Petite pause pour lire
                                
                                action_faite = True
                                tour_joueur = False # Au tour de l'autre
            
            else:
                # Tour de l'IA (Adversaire)
                self.interface.afficher_dialogue(f"Au tour de {self.adversaire.nom}...")
                time.sleep(1)
                
                logs = self.attaquer(self.adversaire, self.joueur)
                for ligne in logs:
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(ligne)
                    time.sleep(1)
                
                tour_joueur = True # Au tour du joueur