import pygame
import os

class Interface:
    def __init__(self):
        pygame.init()
        # Dimensions de la fenêtre
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokémon - Projet Python")

        # --- COULEURS ---
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS_FONCE = (50, 50, 50)
        self.GRIS_CLAIR = (200, 200, 200)
        self.BLEU_NUIT = (20, 20, 80)
        self.VERT = (50, 200, 50)
        self.ROUGE = (200, 50, 50)

        # --- POLICES ---
        # On essaie de charger une police système, sinon défaut
        self.font_titre = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_texte = pygame.font.SysFont("Arial", 24)
        self.font_petit = pygame.font.SysFont("Arial", 18)

    def afficher_texte_centre(self, texte, y, color, font):
        """Méthode utilitaire pour centrer du texte"""
        surface = font.render(texte, True, color)
        rect = surface.get_rect(center=(self.WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def charger_image_safe(self, chemin, taille=None):
        """Charge une image sans faire planter le jeu si elle manque"""
        if os.path.exists(chemin):
            img = pygame.image.load(chemin)
        else:
            # Carré gris si pas d'image
            img = pygame.Surface((100, 100))
            img.fill(self.GRIS_CLAIR)
        
        if taille:
            img = pygame.transform.scale(img, taille)
        return img

    # =========================================================
    # 1. SPLASH SCREEN & ACCUEIL
    # =========================================================

    def afficher_splash_screen(self):
        """Affiche le titre pendant 2 secondes"""
        self.screen.fill(self.BLEU_NUIT)
        self.afficher_texte_centre("POKÉMON PYTHON", self.HEIGHT // 2 - 50, self.BLANC, self.font_titre)
        self.afficher_texte_centre("Chargement...", self.HEIGHT // 2 + 20, self.GRIS_CLAIR, self.font_petit)
        pygame.display.flip()
        pygame.time.delay(2000) # Pause de 2 secondes

    def afficher_menu_accueil(self):
        """Affiche le menu et attend une touche (bloquant pour simplifier ici)"""
        choix = None
        while choix is None:
            self.screen.fill(self.NOIR)
            
            self.afficher_texte_centre("MENU PRINCIPAL", 100, self.BLANC, self.font_titre)
            
            # Options
            # On dessine des rectangles simples pour faire "bouton"
            pygame.draw.rect(self.screen, self.GRIS_FONCE, (200, 200, 400, 50))
            self.afficher_texte_centre("A - NOUVELLE PARTIE", 225, self.BLANC, self.font_texte)

            pygame.draw.rect(self.screen, self.GRIS_FONCE, (200, 300, 400, 50))
            self.afficher_texte_centre("B - REPRENDRE", 325, self.BLANC, self.font_texte)

            pygame.draw.rect(self.screen, self.GRIS_FONCE, (200, 400, 400, 50))
            self.afficher_texte_centre("C - POKÉDEX / AJOUT", 425, self.BLANC, self.font_texte)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: return "NOUVEAU"
                    if event.key == pygame.K_b: return "REPRENDRE"
                    if event.key == pygame.K_c: return "AJOUTER"

    # =========================================================
    # 2. SAISIE & CHARGEMENT
    # =========================================================

    def afficher_saisie_nom(self, nom_actuel):
        self.screen.fill(self.NOIR)
        self.afficher_texte_centre("Comment t'appelles-tu ?", 200, self.BLANC, self.font_titre)
        
        # Zone de saisie
        pygame.draw.rect(self.screen, self.BLANC, (200, 300, 400, 50))
        text_surface = self.font_texte.render(nom_actuel, True, self.NOIR)
        self.screen.blit(text_surface, (210, 310))
        
        self.afficher_texte_centre("Appuie sur ENTRÉE pour valider", 500, self.GRIS_CLAIR, self.font_petit)
        pygame.display.flip()

    def afficher_ecran_chargement(self, actuel, total):
        self.screen.fill(self.NOIR)
        pourcentage = actuel / total
        largeur_barre = 600
        
        # Barre vide
        pygame.draw.rect(self.screen, self.GRIS_FONCE, (100, 300, largeur_barre, 30))
        # Barre remplie
        pygame.draw.rect(self.screen, self.VERT, (100, 300, largeur_barre * pourcentage, 30))
        
        self.afficher_texte_centre(f"Chargement des données... {int(pourcentage*100)}%", 250, self.BLANC, self.font_texte)
        pygame.display.flip()
        # Petite pause pour voir la barre (optionnel, sinon c'est trop rapide)
        pygame.time.delay(50) 

    def preparer_image(self, chemin):
        """Appelé par menu.py pour stocker l'image chargée dans l'objet Pokemon"""
        return self.charger_image_safe(chemin, (150, 150))

    # =========================================================
    # 3. SÉLECTION STARTER
    # =========================================================

    def afficher_menu_selection(self, liste_pokemons):
        self.screen.fill(self.BLEU_NUIT)
        self.afficher_texte_centre("CHOISIS TON POKÉMON", 50, self.BLANC, self.font_titre)

        # On affiche 3 colonnes
        positions_x = [100, 350, 600]
        
        for i, pok in enumerate(liste_pokemons):
            x = positions_x[i]
            y = 200
            
            # Cadre
            pygame.draw.rect(self.screen, self.BLANC, (x, y, 160, 250))
            pygame.draw.rect(self.screen, self.NOIR, (x+2, y+2, 156, 246)) # Contour
            
            # Image (si elle existe déjà dans l'objet)
            if hasattr(pok, 'image_surface') and pok.image_surface:
                self.screen.blit(pok.image_surface, (x+5, y+10))
            
            # Infos
            nom_txt = self.font_texte.render(pok.nom, True, self.BLANC)
            self.screen.blit(nom_txt, (x+10, y+170))
            
            touche_txt = self.font_titre.render(str(i+1), True, self.JAUNE if hasattr(self, 'JAUNE') else (255, 255, 0))
            self.screen.blit(touche_txt, (x+70, y+200))

        pygame.display.flip()
    
    def rafraichir(self):
        pygame.display.flip()

    # =========================================================
    # 4. LISTE SCROLLABLE (POKEDEX)
    # =========================================================

    def afficher_liste_scrollable(self, catalogue, index_start, nb_visibles):
        """
        Affiche une liste verticale avec barre de défilement logique.
        """
        self.screen.fill(self.GRIS_FONCE)
        self.afficher_texte_centre("CATALOGUE POKEMON (↑/↓ pour défiler, Clic pour ajouter)", 50, self.BLANC, self.font_texte)

        # Constantes de positionnement
        START_Y = 100
        ROW_HEIGHT = 80
        MARGIN_LEFT = 100
        WIDTH_ROW = 600

        # Boucle d'affichage
        for i in range(nb_visibles):
            index_reel = index_start + i
            
            if index_reel < len(catalogue):
                p_data = catalogue[index_reel]
                
                # Coordonnée Y de cette ligne
                y_pos = START_Y + (i * ROW_HEIGHT)
                
                # 1. Le fond de la ligne
                rect_ligne = pygame.Rect(MARGIN_LEFT, y_pos, WIDTH_ROW, ROW_HEIGHT - 5)
                pygame.draw.rect(self.screen, self.BLANC, rect_ligne)
                
                # 2. Image miniature
                chemin = f"Assets/Images/{p_data['nom']}.png"
                img = self.charger_image_safe(chemin, (60, 60))
                self.screen.blit(img, (MARGIN_LEFT + 10, y_pos + 5))
                
                # 3. Nom et Type
                texte_nom = f"{p_data['nom']} (Type: {p_data['types'][0]})"
                surface_nom = self.font_texte.render(texte_nom, True, self.NOIR)
                self.screen.blit(surface_nom, (MARGIN_LEFT + 80, y_pos + 10))

                # 4. Stats rapides
                texte_stats = f"PV: {p_data['pv']} | ATK: {p_data['attaque']} | DEF: {p_data['defense']}"
                surface_stats = self.font_petit.render(texte_stats, True, self.GRIS_FONCE)
                self.screen.blit(surface_stats, (MARGIN_LEFT + 80, y_pos + 40))

        # Indicateur de scroll (Barre à droite)
        if len(catalogue) > 0:
            hauteur_totale = nb_visibles * ROW_HEIGHT
            ratio = nb_visibles / len(catalogue)
            cursor_h = max(20, hauteur_totale * ratio)
            cursor_y = START_Y + (index_start / len(catalogue)) * hauteur_totale
            
            pygame.draw.rect(self.screen, self.NOIR, (MARGIN_LEFT + WIDTH_ROW + 10, START_Y, 10, hauteur_totale))
            pygame.draw.rect(self.screen, self.VERT, (MARGIN_LEFT + WIDTH_ROW + 10, cursor_y, 10, cursor_h))

        pygame.display.flip()

    def detecter_clic_liste_scroll(self, pos_souris):
        """
        Renvoie l'index RELATIF (0 à nb_visibles-1) si on clique sur une ligne.
        Renvoie -1 sinon.
        """
        x, y = pos_souris
        
        # Doit correspondre aux constantes de afficher_liste_scrollable
        START_Y = 100
        ROW_HEIGHT = 80
        MARGIN_LEFT = 100
        WIDTH_ROW = 600
        NB_VISIBLES_MAX = 5 # Ou la valeur passée en paramètre dans menu, ici on suppose 5

        # Est-ce qu'on est dans la colonne horizontale ?
        if MARGIN_LEFT <= x <= MARGIN_LEFT + WIDTH_ROW:
            # Est-ce qu'on est dans la zone verticale ?
            if START_Y <= y <= START_Y + (NB_VISIBLES_MAX * ROW_HEIGHT):
                # Calcul magique pour trouver la ligne
                distance_depuis_haut = y - START_Y
                index_trouve = distance_depuis_haut // ROW_HEIGHT
                return int(index_trouve)
        
        return -1

    # =========================================================
    # 5. COMBAT (Aperçu basique)
    # =========================================================
    
    def afficher_combattants(self, p_joueur, p_adversaire):
        self.screen.fill(self.BLANC)
        
        # JOUEUR (En bas à gauche)
        if p_joueur.image_surface:
            # On agrandit pour le combat
            img_j = pygame.transform.scale(p_joueur.image_surface, (250, 250))
            self.screen.blit(img_j, (100, 300))
        
        info_j = f"{p_joueur.nom} : {p_joueur.pv} PV"
        self.screen.blit(self.font_texte.render(info_j, True, self.NOIR), (100, 560))

        # ADVERSAIRE (En haut à droite)
        if p_adversaire.image_surface:
            img_a = pygame.transform.scale(p_adversaire.image_surface, (200, 200))
            self.screen.blit(img_a, (500, 50))
            
        info_a = f"{p_adversaire.nom} : {p_adversaire.pv} PV"
        self.screen.blit(self.font_texte.render(info_a, True, self.NOIR), (500, 260))

        pygame.display.flip()
        

    def afficher_dialogue(self, texte):
        """Affiche une boîte de texte en bas de l'écran par-dessus le combat"""
        # Fond de la boîte
        pygame.draw.rect(self.screen, self.NOIR, (50, 450, 700, 100))
        pygame.draw.rect(self.screen, self.BLANC, (52, 452, 696, 96)) # Bordure
        
        # Texte
        surface = self.font_texte.render(texte, True, self.NOIR)
        self.screen.blit(surface, (70, 480))
        
        pygame.display.flip()