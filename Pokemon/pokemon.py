import pygame

class Pokemon:
    def __init__(self, nom, pv, attaque, defense, vitesse, image_url, type_principal, evolution_nom):
        self.nom = nom
        self.pv_max = pv      # On retient les PV max pour soigner et évoluer
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.image_url = image_url
        self.type_principal = type_principal
        self.evolution_nom = evolution_nom
        
        # --- NOUVEAU : Gestion de l'XP ---
        self.point_exp = 0
        self.seuil_evolution = 100  # XP nécessaire pour évoluer
        
        self.ko = False
        self.image_surface = None

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

    # --- NOUVEAU : Méthodes pour l'évolution ---
    def gagner_xp(self, montant):
        """Ajoute de l'XP et renvoie True si le Pokémon doit évoluer"""
        self.point_exp += montant
        print(f"DEBUG: {self.nom} a {self.point_exp}/{self.seuil_evolution} XP")
        
        # Si on a assez d'XP et qu'une évolution existe
        if self.point_exp >= self.seuil_evolution and self.evolution_nom:
            return True
        return False

    def evoluer(self, nouvelles_stats, nouvelle_image):
        """Remplace les stats actuelles par celles de l'évolution"""
        self.nom = nouvelles_stats['nom']
        self.pv_max = nouvelles_stats['pv']
        self.pv = self.pv_max  # Soin complet à l'évolution !
        self.attaque = nouvelles_stats['attaque']
        self.defense = nouvelles_stats['defense']
        self.vitesse = nouvelles_stats.get('vitesse', 50)
        self.evolution_nom = nouvelles_stats['evolution']
        
        # Reset de l'XP et mise à jour de l'image
        self.point_exp = 0
        self.image_surface = nouvelle_image