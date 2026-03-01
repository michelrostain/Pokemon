import pygame
import os
import requests
import sys
import math 

class Interface:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() # Initialisation du moteur audio
        
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokémon Python Edition")

        # --- COULEURS ---
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS_FONCE = (50, 50, 50)
        self.GRIS_CLAIR = (220, 220, 220)
        self.BLEU_NUIT = (20, 20, 80)
        self.VERT = (50, 200, 50)
        self.ROUGE = (200, 50, 50)
        self.ROUGE_POKEDEX = (220, 20, 30) 
        self.JAUNE = (255, 215, 0)
        self.OR = (255, 215, 0)      
        self.CYAN = (100, 200, 220)

        # --- POLICES ---
        self.font_titre = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_texte = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_petit = pygame.font.SysFont("Arial", 18)
        
        self.cache_images = {}
        
        # Création automatique du dossier pour la musique
        if not os.path.exists("Assets/Sounds"):
            os.makedirs("Assets/Sounds")

        self.DICO_ID = {
            "Bulbizarre": 1, "Herbizarre": 2, "Florizarre": 3,
            "Salamèche": 4, "Reptincel": 5, "Dracaufeu": 6,
            "Carapuce": 7, "Carabaffe": 8, "Tortank": 9,
            "Chenipan": 10, "Chrysacier": 11, "Papilusion": 12,
            "Aspicot": 13, "Coconfort": 14, "Dardargnan": 15,
            "Roucool": 16, "Roucoups": 17, "Roucarnage": 18,
            "Rattata": 19, "Rattatac": 20,
            "Pikachu": 25, "Raichu": 26,
            "Mélofée": 35, "Mélodelfe": 36,
            "Goupix": 37, "Feunard": 38,
            "Rondoudou": 39, "Grodoudou": 40,
            "Nosferapti": 41, "Nosferalto": 42,
            "Mystherbe": 43, "Ortide": 44, "Rafflesia": 45,
            "Miaouss": 52, "Persian": 53,
            "Psykokwak": 54, "Akwakwak": 55,
            "Férosinge": 56, "Colossinge": 57,
            "Caninos": 58, "Arcanin": 59,
            "Ptitard": 60, "Têtarte": 61, "Tartard": 62,
            "Abra": 63, "Kadabra": 64, "Alakazam": 65,
            "Machoc": 66, "Machopeur": 67, "Mackogneur": 68,
            "Racaillou": 74, "Gravalanch": 75, "Grolem": 76,
            "Ponyta": 77, "Galopa": 78,
            "Ramoloss": 79, "Flagadoss": 80,
            "Magnéti": 81, "Magnéton": 82,
            "Fantominus": 92, "Spectrum": 93, "Ectoplasma": 94,
            "Onix": 95,
            "Soporifik": 96, "Hypnomade": 97,
            "Voltorbe": 100, "Électrode": 101,
            "Noeunoeuf": 102, "Noadkoko": 103,
            "Oselet": 104, "Ossatueur": 105,
            "Smogo": 109, "Smogogo": 110,
            "Rhinocorne": 111, "Rhinoféros": 112,
            "Leveinard": 113,
            "Kangourex": 115,
            "Hypotrempe": 116, "Hypocéan": 117,
            "Stari": 120, "Staross": 121,
            "M. Mime": 122,
            "Insécateur": 123,
            "Élektek": 125,
            "Magmar": 126,
            "Scarabrute": 127,
            "Tauros": 128,
            "Magicarpe": 129, "Léviator": 130,
            "Lokhlass": 131,
            "Métamorph": 132,
            "Évoli": 133, "Aquali": 134, "Voltali": 135, "Pyroli": 136,
            "Porygon": 137,
            "Ronflex": 143,
            "Artikodin": 144,
            "Électhor": 145,
            "Sulfura": 146,
            "Minidraco": 147, "Draco": 148, "Dracolosse": 149,
            "Mewtwo": 150, "Mew": 151
        }

    # =========================================================
    # GESTION DU SON
    # =========================================================
    def jouer_musique(self, nom_fichier, boucle=-1):
        chemin = f"Assets/Sounds/{nom_fichier}"
        if os.path.exists(chemin):
            try:
                pygame.mixer.music.load(chemin)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(boucle)
            except:
                pass

    def jouer_son(self, nom_fichier):
        chemin = f"Assets/Sounds/{nom_fichier}"
        if os.path.exists(chemin):
            try:
                son = pygame.mixer.Sound(chemin)
                son.set_volume(0.6)
                son.play()
            except:
                pass

    # =========================================================
    # AFFICHAGE
    # =========================================================

    def afficher_image_splash_screen(self):
        try:
            surface = pygame.image.load("Assets/Images/Background/ImageAccueil.png")
            # --- CORRECTION ICI : Redimensionnement à la taille de l'écran ---
            surface = pygame.transform.scale(surface, (self.WIDTH, self.HEIGHT))
            self.screen.blit(surface, (0, 0))
        except:
            self.screen.fill(self.BLEU_NUIT)

    def afficher_image_combat(self):
        try:
            surface = pygame.image.load("Assets/Images/Background/ImageArene.png")
            # --- CORRECTION ICI : Redimensionnement à la taille de l'écran ---
            surface = pygame.transform.scale(surface, (self.WIDTH, self.HEIGHT))
            self.screen.blit(surface, (0, 0))
        except:
            self.screen.fill(self.GRIS_FONCE)

    def afficher_texte_centre(self, texte, y, color, font):
        surface = font.render(texte, True, color)
        rect = surface.get_rect(center=(self.WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def afficher_texte_dans_rect(self, texte, rect, color, font):
        surface = font.render(texte, True, color)
        self.screen.blit(surface, surface.get_rect(center=rect.center))

    def preparer_image(self, nom_pokemon):
        if nom_pokemon in self.cache_images:
            return self.cache_images[nom_pokemon]

        dossier = "Assets/Images"
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            
        chemin_local = f"{dossier}/{nom_pokemon}.png"

        if not os.path.exists(chemin_local):
            self.telecharger_image_depuis_api(nom_pokemon, chemin_local)

        img_finale = None
        if os.path.exists(chemin_local):
            try:
                img = pygame.image.load(chemin_local)
                img.set_colorkey((0, 0, 0)) 
                img_finale = pygame.transform.scale(img, (150, 150))
            except: pass 
        
        if img_finale is None:
            img_finale = pygame.Surface((150, 150))
            img_finale.fill(self.GRIS_CLAIR)

        self.cache_images[nom_pokemon] = img_finale
        return img_finale

    def telecharger_image_depuis_api(self, nom, chemin_destination):
        id_pokemon = self.DICO_ID.get(nom)
        if id_pokemon:
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id_pokemon}.png"
            try:
                reponse = requests.get(url, timeout=5)
                if reponse.status_code == 200:
                    with open(chemin_destination, 'wb') as f:
                        f.write(reponse.content)
            except Exception as e:
                pass

    def afficher_splash_screen(self):
        self.afficher_image_splash_screen()
        pygame.display.flip()
        pygame.time.delay(2000)

    def afficher_ecran_evolution(self, ancien_nom, img_ancienne, nouveau_nom, img_nouvelle):
        self.jouer_musique("evolution.mp3", boucle=0) 
        
        self.screen.fill(self.BLEU_NUIT)
        self.afficher_texte_centre(f"Quoi ? {ancien_nom} évolue !", 100, self.BLANC, self.font_titre)
        
        if img_ancienne:
            img_a = pygame.transform.scale(img_ancienne, (250, 250))
            self.screen.blit(img_a, (self.WIDTH//2 - 125, 200))
            
        pygame.display.flip()
        pygame.time.delay(2000)
        
        for _ in range(4):
            self.screen.fill(self.BLANC)
            pygame.display.flip()
            pygame.time.delay(100)
            
            self.screen.fill(self.BLEU_NUIT)
            self.afficher_texte_centre(f"Quoi ? {ancien_nom} évolue !", 100, self.BLANC, self.font_titre)
            if img_ancienne:
                self.screen.blit(img_a, (self.WIDTH//2 - 125, 200))
            pygame.display.flip()
            pygame.time.delay(150)
            
        self.screen.fill(self.BLEU_NUIT)
        self.afficher_texte_centre(f"Félicitations !", 70, self.JAUNE, self.font_titre)
        self.afficher_texte_centre(f"Ton {ancien_nom} a évolué en {nouveau_nom} !", 130, self.BLANC, self.font_texte)
        
        if img_nouvelle:
            img_n = pygame.transform.scale(img_nouvelle, (300, 300))
            self.screen.blit(img_n, (self.WIDTH//2 - 150, 200))
            
        self.afficher_texte_centre("(Appuyez sur ESPACE pour continuer)", 550, self.GRIS_CLAIR, self.font_petit)
        pygame.display.flip()
        
        attente = True
        while attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    attente = False

    def afficher_ecran_fin_combat(self, resultat, p_joueur, p_adversaire, xp_gagne=0):
        if resultat == "VICTOIRE":
            self.jouer_musique("victoire.mp3", boucle=0)
        else:
            self.jouer_musique("defaite.mp3", boucle=0)

        largeur, hauteur = 500, 300
        x = (self.WIDTH - largeur) // 2
        y = (self.HEIGHT - hauteur) // 2

        pygame.draw.rect(self.screen, self.BLEU_NUIT, (x, y, largeur, hauteur), border_radius=15)
        pygame.draw.rect(self.screen, self.BLANC, (x, y, largeur, hauteur), 4, border_radius=15)

        if resultat == "VICTOIRE":
            self.afficher_texte_centre("VICTOIRE !", y + 50, self.VERT, self.font_titre)
            self.afficher_texte_centre(f"+ {p_adversaire.nom} ajouté au Pokédex !", y + 130, self.BLANC, self.font_texte)
            self.afficher_texte_centre(f"+ {p_joueur.nom} a gagné {xp_gagne} XP !", y + 180, self.JAUNE, self.font_texte)
        else:
            self.afficher_texte_centre("DÉFAITE...", y + 50, self.ROUGE, self.font_titre)
            self.afficher_texte_centre(f"{p_joueur.nom} est KO...", y + 130, self.BLANC, self.font_texte)
            self.afficher_texte_centre("Il quitte votre équipe.", y + 180, self.GRIS_CLAIR, self.font_texte)

        self.afficher_texte_centre("(Appuyez sur ESPACE pour continuer)", y + 260, self.GRIS_CLAIR, self.font_petit)
        pygame.display.flip()

        attente = True
        while attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    attente = False

    def afficher_menu_accueil(self):
        clock = pygame.time.Clock()
        while True:
            mx, my = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: return "NOUVEAU"
                    if event.key == pygame.K_b: return "REPRENDRE"
                    if event.key == pygame.K_c: return "AJOUTER"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 200 <= mx <= 600:
                        if 210 <= my <= 270: return "NOUVEAU"
                        elif 300 <= my <= 360: return "REPRENDRE"
                        elif 390 <= my <= 450: return "AJOUTER"

            self.afficher_image_splash_screen()
            
            voile = pygame.Surface((self.WIDTH, self.HEIGHT))
            voile.set_alpha(100)
            voile.fill(self.NOIR)
            self.screen.blit(voile, (0,0))
            
            self.afficher_texte_centre("MENU PRINCIPAL", 80, self.BLANC, self.font_titre)
            
            options = [
                ("NOUVELLE PARTIE", 210),
                ("REPRENDRE / CONTINUER", 300),
                ("POKÉDEX / AJOUT", 390)
            ]
            
            for texte, y in options:
                rect = pygame.Rect(200, y, 400, 60)
                
                if rect.collidepoint((mx, my)):
                    couleur_fond = self.BLANC
                    couleur_texte = self.BLEU_NUIT
                else:
                    couleur_fond = self.BLEU_NUIT
                    couleur_texte = self.BLANC

                pygame.draw.rect(self.screen, self.NOIR, (204, y + 4, 400, 60), border_radius=15)
                pygame.draw.rect(self.screen, couleur_fond, rect, border_radius=15)
                pygame.draw.rect(self.screen, self.BLANC, rect, 3, border_radius=15)
                
                self.afficher_texte_dans_rect(texte, rect, couleur_texte, self.font_texte)

            pygame.display.flip()
            clock.tick(60)

    def afficher_ecran_chargement(self, actuel, total):
        self.screen.fill(self.NOIR)
        pourcentage = actuel / total
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (100, 300, 600, 30), border_radius=10)
        pygame.draw.rect(self.screen, self.VERT, (100, 300, 600 * pourcentage, 30), border_radius=10)
        self.afficher_texte_centre(f"Chargement... {int(pourcentage*100)}%", 250, self.BLANC, self.font_texte)
        pygame.display.flip()

    def selectionner_starter_graphique(self, liste_candidats):
        running = True
        index_depart = 0 
        clock = pygame.time.Clock()
        mode_scroll_actif = len(liste_candidats) > 3
        
        while running:
            temps = pygame.time.get_ticks()
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN and mode_scroll_actif:
                    if event.key == pygame.K_LEFT and index_depart > 0: index_depart -= 1
                    elif event.key == pygame.K_RIGHT and index_depart + 3 < len(liste_candidats): index_depart += 1
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mode_scroll_actif:
                        if index_depart > 0 and pygame.Rect(10, 260, 40, 50).collidepoint((mx, my)):
                            index_depart -= 1
                            continue
                        if index_depart + 3 < len(liste_candidats) and pygame.Rect(750, 260, 40, 50).collidepoint((mx, my)):
                            index_depart += 1
                            continue

                    nb_a_afficher = min(3, len(liste_candidats) - index_depart)
                    positions_x = [50, 300, 550]
                    for i in range(nb_a_afficher):
                        if pygame.Rect(positions_x[i], 150, 200, 300).collidepoint((mx, my)):
                            return liste_candidats[index_depart + i]

            self.afficher_image_splash_screen()
            
            voile = pygame.Surface((self.WIDTH, self.HEIGHT))
            voile.set_alpha(150)
            voile.fill(self.NOIR)
            self.screen.blit(voile, (0,0))
            
            titre = "CHOISIS TON POKÉMON" if not mode_scroll_actif else "CHOISIS TON COMBATTANT"
            self.afficher_texte_centre(titre, 50, self.BLANC, self.font_titre)

            candidats_visibles = liste_candidats[index_depart : index_depart + 3]
            positions_x = [50, 300, 550]
            
            for i, p in enumerate(candidats_visibles):
                x = positions_x[i]
                y = 150
                rect_carte = pygame.Rect(x, y, 200, 300)
                
                couleur_fond = self.BLANC
                if p.point_exp >= 200 and p.evolution_nom is not None: couleur_fond = self.OR    
                elif p.point_exp >= 100 and p.evolution_nom is not None: couleur_fond = self.CYAN  
                
                couleur_bord = self.ROUGE if p.est_ko() else self.NOIR
                
                if rect_carte.collidepoint((mx, my)):
                    pygame.draw.rect(self.screen, self.JAUNE, rect_carte.inflate(10, 10), border_radius=15)

                pygame.draw.rect(self.screen, couleur_fond, rect_carte, border_radius=15)
                pygame.draw.rect(self.screen, couleur_bord, rect_carte, 4, border_radius=15)
                
                if p.image_surface:
                    img = pygame.transform.scale(p.image_surface, (150, 150))
                    self.screen.blit(img, (x + 25, y + 20))
                
                nom_s = self.font_texte.render(p.nom, True, self.NOIR)
                self.screen.blit(nom_s, (x + (200 - nom_s.get_width())//2, y + 180))
                
                etat_pv = f"{p.pv}/{p.pv_max}" if not p.est_ko() else "KO"
                pv_s = self.font_petit.render(f"PV: {etat_pv} | XP: {p.point_exp}", True, self.NOIR)
                self.screen.blit(pv_s, (x + (200 - pv_s.get_width())//2, y + 215))

            if mode_scroll_actif:
                if index_depart > 0:
                    pygame.draw.polygon(self.screen, self.ROUGE, [(40, 300), (10, 280), (40, 260)])
                if index_depart + 3 < len(liste_candidats):
                    pygame.draw.polygon(self.screen, self.ROUGE, [(760, 300), (790, 280), (760, 260)])
                
                msg = f"Affichage {index_depart+1}-{min(index_depart+3, len(liste_candidats))} sur {len(liste_candidats)}"
                self.afficher_texte_centre(msg, 100, self.BLANC, self.font_petit)
            
            if (temps // 500) % 2 == 0:
                couleur_clignotante = self.JAUNE
            else:
                couleur_clignotante = self.BLANC    

            instruction = "Flèches GAUCHE/DROITE pour défiler - CLIC pour choisir"
            texte_surface = self.font_texte.render(instruction, True, couleur_clignotante)  
            self.screen.blit(texte_surface, texte_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 30)))

            pygame.display.flip()
            clock.tick(60)

    def dessiner_barre_vie(self, x, y, pv_actuel, pv_max):
        ratio = max(0, pv_actuel / pv_max)
        couleur = self.VERT if ratio > 0.5 else self.JAUNE if ratio > 0.2 else self.ROUGE
        
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (x, y, 200, 15), border_radius=5)
        pygame.draw.rect(self.screen, couleur, (x, y, int(200 * ratio), 15), border_radius=5)
        pygame.draw.rect(self.screen, self.BLANC, (x, y, 200, 15), 2, border_radius=5)

    def animer_degats(self):
        self.jouer_son("degats.wav") 
        for _ in range(2):
            self.screen.fill((150, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            pygame.display.flip()
            pygame.time.delay(50)

    def afficher_combattants(self, p_joueur, p_adversaire):
        self.afficher_image_combat()
        temps = pygame.time.get_ticks()

        offset_y_joueur = math.sin(temps * 0.005) * 8
        offset_y_adv = math.cos(temps * 0.005) * 8
        
        if p_joueur.image_surface:
            img_j = pygame.transform.scale(p_joueur.image_surface, (250, 250))
            img_j = pygame.transform.flip(img_j, True, False)
            self.screen.blit(img_j, (80, 280 + offset_y_joueur))
        
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (450, 400, 300, 80), border_radius=10)
        pygame.draw.rect(self.screen, self.BLANC, (450, 400, 300, 80), 2, border_radius=10)
        self.screen.blit(self.font_texte.render(p_joueur.nom, True, self.BLANC), (460, 410))
        self.dessiner_barre_vie(460, 450, p_joueur.pv, p_joueur.pv_max)

        if p_adversaire.image_surface:
            img_a = pygame.transform.scale(p_adversaire.image_surface, (200, 200))
            self.screen.blit(img_a, (500, 50 + offset_y_adv))
        
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (50, 50, 300, 80), border_radius=10)
        pygame.draw.rect(self.screen, self.BLANC, (50, 50, 300, 80), 2, border_radius=10)
        self.screen.blit(self.font_texte.render(p_adversaire.nom, True, self.BLANC), (60, 60))
        self.dessiner_barre_vie(60, 100, p_adversaire.pv, p_adversaire.pv_max)

    def afficher_dialogue(self, texte):
        pygame.draw.rect(self.screen, self.NOIR, (0, 500, 800, 100))
        pygame.draw.rect(self.screen, self.BLANC, (5, 505, 790, 90), 3)
        surface = self.font_texte.render(texte, True, self.BLANC)
        self.screen.blit(surface, (30, 535))
        pygame.display.flip()

    def afficher_inventaire_joueur(self, liste_pokemons):
        index = 0
        nb_visibles = 5
        clock = pygame.time.Clock()
        
        while True:
            mx, my = pygame.mouse.get_pos()
            self.screen.fill(self.ROUGE_POKEDEX)
            
            pygame.draw.rect(self.screen, self.NOIR, (0, 0, 800, 80))
            self.afficher_texte_centre("MON POKÉDEX", 40, self.BLANC, self.font_titre)
            
            pygame.draw.rect(self.screen, self.GRIS_CLAIR, (80, 100, 640, 410), border_radius=10)
            pygame.draw.rect(self.screen, self.NOIR, (80, 100, 640, 410), 4, border_radius=10)
            
            if not liste_pokemons:
                self.afficher_texte_centre("Le Pokédex est vide.", 300, self.GRIS_FONCE, self.font_texte)
            else:
                START_Y = 110; ROW_H = 75; MARGIN = 100
                for i in range(nb_visibles):
                    idx = index + i
                    if idx < len(liste_pokemons):
                        data = liste_pokemons[idx]
                        y = START_Y + i * ROW_H
                        
                        pygame.draw.rect(self.screen, self.BLANC, (MARGIN, y, 600, ROW_H - 10), border_radius=8)
                        pygame.draw.rect(self.screen, self.GRIS_FONCE, (MARGIN, y, 600, ROW_H - 10), 2, border_radius=8)
                        
                        img = self.preparer_image(data['nom']) 
                        img = pygame.transform.scale(img, (60, 60))
                        self.screen.blit(img, (MARGIN + 10, y + 2))
                        
                        info = f"{data['nom']} - PV: {data['pv']} | XP: {data.get('xp', 0)}"
                        self.screen.blit(self.font_texte.render(info, True, self.NOIR), (MARGIN + 90, y + 20))

            btn_ajout = pygame.Rect(100, 530, 300, 50)
            btn_retour = pygame.Rect(420, 530, 280, 50)
            
            c_ajout = self.JAUNE if btn_ajout.collidepoint((mx, my)) else self.VERT
            c_retour = self.JAUNE if btn_retour.collidepoint((mx, my)) else self.GRIS_FONCE
            
            pygame.draw.rect(self.screen, c_ajout, btn_ajout, border_radius=10)
            pygame.draw.rect(self.screen, self.BLANC, btn_ajout, 2, border_radius=10)
            self.afficher_texte_dans_rect("AJOUTER UN POKÉMON", btn_ajout, self.NOIR if c_ajout == self.JAUNE else self.BLANC, self.font_texte)
            
            pygame.draw.rect(self.screen, c_retour, btn_retour, border_radius=10)
            pygame.draw.rect(self.screen, self.BLANC, btn_retour, 2, border_radius=10)
            self.afficher_texte_dans_rect("RETOUR (Echap)", btn_retour, self.NOIR if c_retour == self.JAUNE else self.BLANC, self.font_texte)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: return "RETOUR"
                    if event.key == pygame.K_a: return "ALLER_AJOUT"
                    if event.key == pygame.K_DOWN and liste_pokemons: 
                        index = min(index+1, max(0, len(liste_pokemons)-nb_visibles))
                    if event.key == pygame.K_UP: 
                        index = max(0, index-1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_ajout.collidepoint(event.pos): return "ALLER_AJOUT"
                    if btn_retour.collidepoint(event.pos): return "RETOUR"
            
            clock.tick(60)

    def afficher_liste_scrollable(self, catalogue, index_start, nb_visibles):
        mx, my = pygame.mouse.get_pos()
        self.screen.fill(self.ROUGE_POKEDEX)
        
        pygame.draw.rect(self.screen, self.NOIR, (0, 0, 800, 80))
        self.afficher_texte_centre("CATALOGUE COMPLET (Flèches haut/bas)", 40, self.BLANC, self.font_texte)
        
        pygame.draw.rect(self.screen, self.GRIS_CLAIR, (80, 100, 640, 410), border_radius=10)
        pygame.draw.rect(self.screen, self.NOIR, (80, 100, 640, 410), 4, border_radius=10)
        
        START_Y = 110; ROW_H = 75; MARGIN = 100
        for i in range(nb_visibles):
            idx = index_start + i
            if idx < len(catalogue):
                data = catalogue[idx]
                y = START_Y + i * ROW_H
                
                rect_carte = pygame.Rect(MARGIN, y, 600, ROW_H - 10)
                
                c_fond = self.JAUNE if rect_carte.collidepoint((mx, my)) else self.BLANC
                
                pygame.draw.rect(self.screen, c_fond, rect_carte, border_radius=8)
                pygame.draw.rect(self.screen, self.GRIS_FONCE, rect_carte, 2, border_radius=8)
                
                img = self.preparer_image(data['nom'])
                img = pygame.transform.scale(img, (60, 60))
                self.screen.blit(img, (MARGIN + 10, y + 2))
                
                info = f"{data['nom']} (Type: {data['types'][0]})"
                self.screen.blit(self.font_texte.render(info, True, self.NOIR), (MARGIN + 90, y + 20))

        pygame.draw.rect(self.screen, self.GRIS_FONCE, (250, 530, 300, 50), border_radius=10)
        self.afficher_texte_centre("CLIQUEZ POUR AJOUTER", 555, self.BLANC, self.font_texte)

        pygame.display.flip()

    def detecter_clic_liste_scroll(self, pos):
        x, y = pos
        START_Y = 110; ROW_H = 75; MARGIN = 100
        
        if MARGIN <= x <= MARGIN + 600 and START_Y <= y <= START_Y + (5 * ROW_H):
            rel_y = y - START_Y
            if rel_y % ROW_H <= (ROW_H - 10):
                return rel_y // ROW_H
        return -1