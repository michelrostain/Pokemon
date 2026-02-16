import pygame

class Pokemon:
    def __init__(self, nom, pv, attaque, defense, vitesse, type_principal, evolution, image_url=None):
        # DONNÉES DE BASE
        self.nom = nom
        self.pv = pv
        self.pv_max = pv # ON GARDE LES PV MAX POUR LE SOIN
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.type_principal = type_principal
        self.evolution = evolution
        
        # PARTIE GRAPHIQUE
        self.image_url = image_url
        self.image_surface = None # L'IMAGE PYGAME SERA MISE ICI PLUS TARD
        self.ko = False

    def subir_degat(self, montant):
        """FONCTION POUR ENLEVER DE LA VIE"""
        self.pv -= montant
        if self.pv <= 0:
            self.pv = 0
            self.ko = True
        return self.pv

    def est_ko(self):
        """VÉRIFIE SI LE POKÉMON EST MORT"""
        return self.pv <= 0

    def statistiques(self):
        """AFFICHE LES INFOS DANS LA CONSOLE"""
        print(f"{self.nom} (Vie: {self.pv}, Atk: {self.attaque}, Def: {self.defense}, Type: {self.type_principal})")