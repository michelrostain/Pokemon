import json
import pygame
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

    def calculer_degats(self, atk, defe, puissance=1.0):
        coeff = 1.0
        t_atk = atk.type_principal.upper()
        t_def = defe.type_principal.upper()
        
        if t_atk in self.table_types:
            coeff = self.table_types[t_atk].get(t_def, 1.0)
        
        degats = int(((atk.attaque * puissance) - (defe.defense // 2)) * coeff)
        return max(1, degats), coeff

    def lancer_combat(self):
        
        pygame.mixer.music.fadeout(2000)
        pygame.mixer.music.load("Assets/Sounds/combat.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)


        tour_joueur = True
        while not self.joueur.est_ko() and not self.adversaire.est_ko():
            if tour_joueur:
                # NOUVEAU : Affichage des types d'attaque !
                type_atk_2 = self.joueur.type_principal.upper()
                msg_choix = f"[1] {self.joueur.attaque_1} (NORMAL) - [2] {self.joueur.attaque_2} ({type_atk_2})"
                
                attente = True
                choix_attaque = None
                
                while attente:
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(msg_choix)
                    pygame.time.delay(16) 
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                             pygame.quit(); exit()
                        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                choix_attaque = (self.joueur.attaque_1, 1.0)
                                attente = False
                            elif event.key == pygame.K_2:
                                choix_attaque = (self.joueur.attaque_2, 1.3)
                                attente = False

                nom_attaque_choisie = choix_attaque[0]
                puissance_choisie = choix_attaque[1]

                if puissance_choisie ==1.3:
                    chance = random.randint(1, 4)  # 25% de chance de rater
                else:
                    chance = random.randint(1, 10)  # 10% de chance de rater
                
                if chance == 1:
                    pygame.mixer.Sound("Assets/Sounds/attaque_ratee.mp3").play()
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(f"Mince ! {self.joueur.nom} a raté {nom_attaque_choisie} !")
                    pygame.time.delay(1500)
                else:
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(f"{self.joueur.nom} lance {nom_attaque_choisie} !")
                    pygame.time.delay(800)
                    
                    self.interface.animer_degats()
                    
                    dmg, c = self.calculer_degats(self.joueur, self.adversaire, puissance_choisie)
                    self.adversaire.subir_degats(dmg)
                    son_attaque=pygame.mixer.Sound("Assets/Sounds/degats.mp3")
                    son_attaque.play()
                    pygame.time.delay(int(son_attaque.get_length() * 1000))  # attend la fin du son
                    msg = f"Ça inflige {dmg} dégâts !"
                    if c > 1.5: msg += " (C'est super efficace !)"
                    elif c < 0.8: msg += " (Ce n'est pas très efficace...)"
                    
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(msg)
                    pygame.time.delay(1500)
                
                tour_joueur = False
            
            else:
                atk_adv_nom = random.choice([self.adversaire.attaque_1, self.adversaire.attaque_2])
                puissance_adv = 1.3 if atk_adv_nom == self.adversaire.attaque_2 else 1.0
                
                self.interface.afficher_combattants(self.joueur, self.adversaire)
                self.interface.afficher_dialogue(f"{self.adversaire.nom} utilise {atk_adv_nom}...")
                pygame.time.delay(1000)
                
                chance = random.randint(1, 3)
                
                if chance == 1:
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(f"Chance ! {self.adversaire.nom} a raté !")
                    pygame.time.delay(1500)
                else:
                    self.interface.animer_degats()
                    
                    dmg, c = self.calculer_degats(self.adversaire, self.joueur, puissance_adv)
                    self.joueur.subir_degats(dmg)
                    
                    msg = f"{self.adversaire.nom} inflige {dmg} dégâts !"
                    if c > 1.5: msg += " (C'est super efficace !)"
                    elif c < 0.8: msg += " (Ce n'est pas très efficace...)"
                    
                    self.interface.afficher_combattants(self.joueur, self.adversaire)
                    self.interface.afficher_dialogue(msg)
                    pygame.time.delay(1500)
                
                tour_joueur = True

        if self.adversaire.est_ko(): 
            pygame.mixer.music.fadeout(1000)
            son_victoire = pygame.mixer.Sound("Assets/Sounds/gagne.mp3")
            son_victoire.play()
            pygame.time.delay(int(son_victoire.get_length() * 1000))  # attend la fin du son
            pygame.mixer.music.load("Assets/Sounds/generique.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            return "VICTOIRE"
        pygame.mixer.music.fadeout(1000)
        son_defaite = pygame.mixer.Sound("Assets/Sounds/perdu.mp3")
        son_defaite.play()
        pygame.time.delay(int(son_defaite.get_length() * 1000))
        pygame.mixer.music.load("Assets/Sounds/generique.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)        # pygame.mixer.music.play(-1)
        return "DEFAITE"