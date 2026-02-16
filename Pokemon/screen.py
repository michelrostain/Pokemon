import pygame
import os
import requests

class Interface:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokémon Python Edition")

        # --- COULEURS ---
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS_FONCE = (50, 50, 50)
        self.GRIS_CLAIR = (200, 200, 200)
        self.BLEU_NUIT = (20, 20, 80)
        self.VERT = (50, 200, 50)
        self.ROUGE = (200, 50, 50)
        self.JAUNE = (255, 215, 0)

        # --- POLICES ---
        self.font_titre = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_texte = pygame.font.SysFont("Arial", 24)
        self.font_petit = pygame.font.SysFont("Arial", 18)
        
        # --- NOUVEAU : CACHE POUR EVITER LES BOUCLES DE TELECHARGEMENT ---
        self.cache_images = {}

        # Dictionnaire complet (Nom JSON -> ID PokéAPI)
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

    def afficher_texte_centre(self, texte, y, color, font):
        surface = font.render(texte, True, color)
        rect = surface.get_rect(center=(self.WIDTH // 2, y))
        self.screen.blit(surface, rect)

    # =========================================================
    # GESTION IMAGES AVEC CACHE (Correctif boucle)
    # =========================================================

    def preparer_image(self, nom_pokemon):
        # 1. On vérifie si l'image est déjà en mémoire (Cache)
        if nom_pokemon in self.cache_images:
            return self.cache_images[nom_pokemon]

        # 2. Si pas en cache, on définit le chemin
        dossier = "Assets/Images"
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            
        chemin_local = f"{dossier}/{nom_pokemon}.png"

        # 3. Si fichier absent, on télécharge (une seule fois)
        if not os.path.exists(chemin_local):
            print(f"Téléchargement pour : {nom_pokemon}...")
            self.telecharger_image_depuis_api(nom_pokemon, chemin_local)

        # 4. Chargement de l'image
        img_finale = None
        if os.path.exists(chemin_local):
            try:
                img = pygame.image.load(chemin_local)
                img.set_colorkey((0, 0, 0)) 
                img_finale = pygame.transform.scale(img, (150, 150))
            except:
                pass 
        
        # Si échec ou fichier corrompu, on met le carré gris
        if img_finale is None:
            img_finale = pygame.Surface((150, 150))
            img_finale.fill(self.GRIS_CLAIR)

        # 5. On sauvegarde le résultat dans le cache pour ne plus refaire tout ça
        self.cache_images[nom_pokemon] = img_finale
        return img_finale

    def telecharger_image_depuis_api(self, nom, chemin_destination):
        id_pokemon = self.DICO_ID.get(nom)
        if id_pokemon:
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id_pokemon}.png"
            try:
                reponse = requests.get(url, timeout=5) # Timeout pour ne pas bloquer trop longtemps
                if reponse.status_code == 200:
                    with open(chemin_destination, 'wb') as f:
                        f.write(reponse.content)
            except Exception as e:
                print(f"Erreur API: {e}")

    # =========================================================
    # ECRANS
    # =========================================================

    def afficher_splash_screen(self):
        self.screen.fill(self.BLEU_NUIT)
        self.afficher_texte_centre("POKÉMON PYTHON", self.HEIGHT // 2 - 50, self.BLANC, self.font_titre)
        self.afficher_texte_centre("Chargement...", self.HEIGHT // 2 + 20, self.GRIS_CLAIR, self.font_petit)
        pygame.display.flip()
        pygame.time.delay(1500)

    def afficher_menu_accueil(self):
        while True:
            self.screen.fill(self.NOIR)
            self.afficher_texte_centre("MENU PRINCIPAL", 80, self.BLANC, self.font_titre)
            self.afficher_texte_centre("(Tapez A, B, ou C)", 120, self.BLANC, self.font_texte)
            
            options = [
                ("A - NOUVELLE PARTIE", 200),
                ("B - REPRENDRE / CONTINUER", 300),
                ("C - POKÉDEX / AJOUT", 400)
            ]
            
            for texte, y in options:
                pygame.draw.rect(self.screen, self.GRIS_FONCE, (200, y, 400, 50))
                pygame.draw.rect(self.screen, self.BLANC, (200, y, 400, 50), 2)
                self.afficher_texte_centre(texte, y + 25, self.BLANC, self.font_texte)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: return "NOUVEAU"
                    if event.key == pygame.K_b: return "REPRENDRE"
                    if event.key == pygame.K_c: return "AJOUTER"

    def afficher_ecran_chargement(self, actuel, total):
        self.screen.fill(self.NOIR)
        pourcentage = actuel / total
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (100, 300, 600, 30))
        pygame.draw.rect(self.screen, self.VERT, (100, 300, 600 * pourcentage, 30))
        self.afficher_texte_centre(f"Chargement... {int(pourcentage*100)}%", 250, self.BLANC, self.font_texte)
        pygame.display.flip()

    def selectionner_starter_graphique(self, liste_candidats):
        running = True
        index_depart = 0 
        clock = pygame.time.Clock()
        
        # Variable pour savoir si on a besoin du scroll
        # C'est la clé de ta demande : Vrai seulement si on a + de 3 pokémons
        mode_scroll_actif = len(liste_candidats) > 3
        
        while running:
            # --- 1. GESTION DES EVENEMENTS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                
                # NAVIGATION CLAVIER (Seulement si scroll actif)
                if event.type == pygame.KEYDOWN and mode_scroll_actif:
                    if event.key == pygame.K_LEFT:
                        if index_depart > 0:
                            index_depart -= 1
                    elif event.key == pygame.K_RIGHT:
                        if index_depart + 3 < len(liste_candidats):
                            index_depart += 1
                
                # SOURIS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    
                    # Clic sur Flèches (Seulement si scroll actif)
                    if mode_scroll_actif:
                        # Flèche GAUCHE
                        if index_depart > 0:
                            if pygame.Rect(10, 260, 40, 50).collidepoint(mx, my):
                                index_depart -= 1
                                continue
                        # Flèche DROITE
                        if index_depart + 3 < len(liste_candidats):
                            if pygame.Rect(750, 260, 40, 50).collidepoint(mx, my):
                                index_depart += 1
                                continue

                    # Clic sur une Carte (Choix du Pokémon)
                    # On affiche toujours max 3 cartes
                    nb_a_afficher = min(3, len(liste_candidats) - index_depart)
                    positions_x = [50, 300, 550]
                    
                    for i in range(nb_a_afficher):
                        x = positions_x[i]
                        rect_carte = pygame.Rect(x, 150, 200, 300)
                        if rect_carte.collidepoint(mx, my):
                            # On retourne le pokémon cliqué
                            choix = liste_candidats[index_depart + i]
                            # Optionnel : Empêcher de choisir un KO ?
                            # if not choix.est_ko(): return choix
                            return choix

            # --- 2. AFFICHAGE ---
            self.screen.fill(self.BLANC)
            titre = "CHOISIS TON STARTER" if not mode_scroll_actif else "CHOISIS TON COMBATTANT"
            self.afficher_texte_centre(titre, 50, self.NOIR, self.font_titre)

            # On récupère les 3 (ou moins) pokémons à afficher selon l'index
            candidats_visibles = liste_candidats[index_depart : index_depart + 3]
            positions_x = [50, 300, 550]
            
            for i, p in enumerate(candidats_visibles):
                x = positions_x[i]
                y = 150
                
                # Couleur du cadre (Rouge si KO, Gris si OK)
                couleur_bord = self.ROUGE if p.est_ko() else self.NOIR
                
                # Fond et cadre
                rect_carte = pygame.Rect(x, y, 200, 300)
                pygame.draw.rect(self.screen, self.GRIS_CLAIR, rect_carte)
                pygame.draw.rect(self.screen, couleur_bord, rect_carte, 2)
                
                # Image
                if p.image_surface:
                    img = pygame.transform.scale(p.image_surface, (150, 150))
                    self.screen.blit(img, (x + 25, y + 20))
                
                # Stats
                nom_s = self.font_texte.render(p.nom, True, self.NOIR)
                self.screen.blit(nom_s, (x + (200 - nom_s.get_width())//2, y + 180))
                
                etat_pv = f"{p.pv}/{p.pv_max}" if not p.est_ko() else "KO"
                pv_s = self.font_petit.render(f"PV: {etat_pv}", True, couleur_bord)
                self.screen.blit(pv_s, (x + (200 - pv_s.get_width())//2, y + 215))

            # --- 3. INDICATEURS DE DEFILEMENT (UNIQUEMENT SI SCROLL ACTIF) ---
            if mode_scroll_actif:
                if index_depart > 0:
                    # Triangle Gauche
                    pygame.draw.polygon(self.screen, self.ROUGE, [(40, 300), (10, 280), (40, 260)])
                
                if index_depart + 3 < len(liste_candidats):
                    # Triangle Droit
                    pygame.draw.polygon(self.screen, self.ROUGE, [(760, 300), (790, 280), (760, 260)])

                msg = "Flèches GAUCHE/DROITE pour faire défiler"
                self.afficher_texte_centre(msg, 500, self.GRIS_FONCE, self.font_petit)
            
            # Mise à jour
            pygame.display.flip()
            clock.tick(60)
            
            # --- 4. GESTION ÉVÉNEMENTS ---
    def afficher_combattants(self, p_joueur, p_adversaire):
        self.screen.fill(self.BLANC)
        
        # Joueur
        if p_joueur.image_surface:
            img_j = pygame.transform.scale(p_joueur.image_surface, (250, 250))
            img_j = pygame.transform.flip(img_j, True, False)
            self.screen.blit(img_j, (80, 280))
        
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (450, 400, 300, 80))
        text_j = f"{p_joueur.nom} | PV: {p_joueur.pv}/{p_joueur.pv_max}"
        self.screen.blit(self.font_texte.render(text_j, True, self.BLANC), (460, 420))

        # Adversaire
        if p_adversaire.image_surface:
            img_a = pygame.transform.scale(p_adversaire.image_surface, (200, 200))
            self.screen.blit(img_a, (500, 50))
        
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (50, 50, 300, 80))
        text_a = f"{p_adversaire.nom} | PV: {p_adversaire.pv}/{p_adversaire.pv_max}"
        self.screen.blit(self.font_texte.render(text_a, True, self.BLANC), (60, 70))

        pygame.display.flip()

    def afficher_dialogue(self, texte):
        pygame.draw.rect(self.screen, self.NOIR, (0, 500, 800, 100))
        pygame.draw.rect(self.screen, self.BLANC, (5, 505, 790, 90), 3)
        surface = self.font_texte.render(texte, True, self.BLANC)
        self.screen.blit(surface, (30, 535))
        pygame.display.flip()

    def afficher_inventaire_joueur(self, liste_pokemons):
        index = 0
        nb_visibles = 5
        while True:
            self.screen.fill(self.GRIS_FONCE)
            self.afficher_texte_centre("MON POKÉDEX ACTUEL", 40, self.BLANC, self.font_titre)
            
            if not liste_pokemons:
                self.afficher_texte_centre("Votre Pokédex est vide.", 300, self.GRIS_CLAIR, self.font_texte)
            else:
                START_Y = 100; ROW_H = 80; MARGIN = 100
                for i in range(nb_visibles):
                    idx = index + i
                    if idx < len(liste_pokemons):
                        data = liste_pokemons[idx]
                        y = START_Y + i * ROW_H
                        
                        pygame.draw.rect(self.screen, self.BLANC, (MARGIN, y, 600, ROW_H - 5))
                        
                        # Ici, preparer_image utilisera le cache !
                        img = self.preparer_image(data['nom']) 
                        img = pygame.transform.scale(img, (60, 60))
                        self.screen.blit(img, (MARGIN + 10, y + 5))
                        
                        info = f"{data['nom']} (PV: {data['pv']})"
                        self.screen.blit(self.font_texte.render(info, True, self.NOIR), (MARGIN + 80, y + 25))

            pygame.draw.rect(self.screen, self.VERT, (200, 520, 400, 50))
            self.afficher_texte_centre("[A] AJOUTER UN POKÉMON", 545, self.BLANC, self.font_texte)
            self.afficher_texte_centre("ECHAP pour revenir", 580, self.GRIS_CLAIR, self.font_petit)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: return "RETOUR"
                    if event.key == pygame.K_a: return "ALLER_AJOUT"
                    if event.key == pygame.K_DOWN and liste_pokemons: 
                        index = min(index+1, max(0, len(liste_pokemons)-nb_visibles))
                    if event.key == pygame.K_UP: 
                        index = max(0, index-1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 200 <= x <= 600 and 520 <= y <= 570: return "ALLER_AJOUT"

    def afficher_liste_scrollable(self, catalogue, index_start, nb_visibles):
        self.screen.fill(self.GRIS_FONCE)
        self.afficher_texte_centre("CATALOGUE COMPLET (Flèches pour défiler)", 40, self.BLANC, self.font_texte)
        
        START_Y = 100; ROW_H = 80; MARGIN = 100
        for i in range(nb_visibles):
            idx = index_start + i
            if idx < len(catalogue):
                data = catalogue[idx]
                y = START_Y + i * ROW_H
                pygame.draw.rect(self.screen, self.BLANC, (MARGIN, y, 600, ROW_H - 5))
                
                img = self.preparer_image(data['nom']) # Utilise le cache
                img = pygame.transform.scale(img, (60, 60))
                self.screen.blit(img, (MARGIN + 10, y + 5))
                
                info = f"{data['nom']} (Type: {data['types'][0]})"
                self.screen.blit(self.font_texte.render(info, True, self.NOIR), (MARGIN + 80, y + 25))

        pygame.display.flip()

    def detecter_clic_liste_scroll(self, pos):
        x, y = pos
        if 100 <= x <= 700 and 100 <= y <= 500:
            rel_y = y - 100
            return rel_y // 80
        return -1