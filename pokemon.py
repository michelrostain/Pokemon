class Pokemon:
    def __init__(self, nom, pv, attaque, defense, vitesse, image_url, type_principal, evolution_nom, xp_actuel=0):
        self.nom = nom
        self.pv_max = pv      # On retient les PV max pour soigner et évoluer
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.image_url = image_url
        self.type_principal = type_principal
        self.evolution_nom = evolution_nom
        
        # --- Gestion de l'XP ---
        self.point_exp = xp_actuel
        self.seuil_evolution = 100  # XP nécessaire pour évoluer
        
        self.ko = False
        self.image_surface = None

        # --- Ajout de noms d'attaques simples ---
        self.attaque_1 = "Charge"
        
        # L'attaque 2 dépend du type du Pokémon
        attaques_speciales = {
            "FEU": "Flammèche", "EAU": "Pistolet à O", "PLANTE": "Fouet Lianes",
            "ELECTRIK": "Éclair", "NORMAL": "Vive-Attaque", "POISON": "Dard-Venin"
        }
        self.attaque_2 = attaques_speciales.get(self.type_principal.upper(), "Coup d'Boule")

    def est_en_vie(self):
        return self.pv > 0

    def est_ko(self):
        return self.pv <= 0

    def subir_degats(self, degats):
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0
            self.ko = True
        return self.pv

    def soigner(self):
        self.pv = self.pv_max
        self.ko = False

    def gagner_xp(self, montant):
        self.point_exp += montant
        
        # CORRECTION BUG EVOLUTION : On vérifie que le champ n'est pas vide, "null" ou "None"
        if not self.evolution_nom or str(self.evolution_nom).strip().lower() in ["none", "null", ""]:
            return False

        if self.point_exp >= self.seuil_evolution:
            return True
            
        return False

    def evoluer(self, nouvelles_stats, nouvelle_image):
        self.nom = nouvelles_stats['nom']
        self.pv_max = nouvelles_stats['pv']
        self.pv = self.pv_max  
        self.attaque = nouvelles_stats['attaque']
        self.defense = nouvelles_stats['defense']
        self.vitesse = nouvelles_stats.get('vitesse', 50)
        self.evolution_nom = nouvelles_stats['evolution']
        
        self.point_exp = 0
        self.image_surface = nouvelle_image
        
        # On met à jour l'attaque 2 avec le nouveau type éventuel
        attaques_speciales = {
            "FEU": "Flammèche", "EAU": "Pistolet à O", "PLANTE": "Fouet Lianes",
            "ELECTRIK": "Éclair", "NORMAL": "Vive-Attaque", "POISON": "Dard-Venin"
        }
        self.attaque_2 = attaques_speciales.get(self.type_principal.upper(), "Coup d'Boule")