import pygame

class Pokemon:
    def __init__(self, nom, pv, attaque, defense, vitesse, image_url, type_principal, evolution_nom):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.image_url = image_url
        self.type_principal = type_principal
        self.evolution_nom = evolution_nom
        
        # Gestion de l'état
        self.point_exp = 0
        self.ko = False
        
        # Pour l'affichage (sera rempli par l'interface plus tard)
        self.image_surface = None

    def est_en_vie(self):
        """Retourne Vrai si le Pokémon a encore des PV"""
        return self.pv > 0

    def est_ko(self):
        """Retourne Vrai si le Pokémon est KO"""
        return self.pv <= 0

    def subir_degats(self, degats):
        """Applique les dégâts et vérifie le KO"""
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0
            self.ko = True
        return self.pv

    def statistiques(self):
        print(f"{self.nom} | PV:{self.pv} | ATK:{self.attaque} | DEF:{self.defense}")