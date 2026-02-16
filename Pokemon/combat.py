import json
import pygame
import time

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
        if t_atk in self.table_types:
            coeff = self.table_types[t_atk].get(t_def, 1.0)
        
        degats = int((atk.attaque - (defe.defense // 2)) * coeff)
        return max(1, degats), coeff

    def lancer_combat(self):
        tour_joueur = True
        while not self.joueur.est_ko() and not self.adversaire.est_ko():
            self.interface.afficher_combattants(self.joueur, self.adversaire)
            
            if tour_joueur:
                self.interface.afficher_dialogue(f"À toi ! (ESPACE pour attaquer)")
                attente = True
                while attente:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                             pygame.quit(); exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            dmg, c = self.calculer_degats(self.joueur, self.adversaire)
                            self.adversaire.subir_degats(dmg)
                            
                            msg = f"{self.joueur.nom} inflige {dmg} dégâts !"
                            if c > 1.5: msg += " (Super efficace!)"
                            elif c < 0.8: msg += " (Pas très efficace...)"
                            
                            self.interface.afficher_dialogue(msg)
                            time.sleep(1.5)
                            attente = False
                tour_joueur = False
            else:
                self.interface.afficher_dialogue(f"{self.adversaire.nom} attaque...")
                time.sleep(1)
                dmg, c = self.calculer_degats(self.adversaire, self.joueur)
                self.joueur.subir_degats(dmg)
                self.interface.afficher_dialogue(f"{self.adversaire.nom} inflige {dmg} dégâts !")
                time.sleep(1.5)
                tour_joueur = True

        if self.adversaire.est_ko(): return "VICTOIRE"
        return "DEFAITE"