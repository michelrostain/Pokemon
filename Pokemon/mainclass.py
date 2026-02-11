import json
import pygame
import random

chemin = "pokemon.json"
with open(chemin, "r", encoding="utf-8") as f:
    liste_brute = json.load(f)

chemin_types = "types.json"
with open(chemin_types, "r", encoding="utf-8") as f:
    table_types = json.load(f)

# 3. Création de tes objets
mes_pokemons = []

pygame.init


class Pokemon:
    def __init__(self, nom, pv, attaque, defense, image_url, type_principal, vitesse):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.image_url = image_url
        self.type_principal = type_principal
        self.evolution = 0
        self.ko = False

    def est_en_vie(self):
        if self.pv <= 0:
            self.ko = True
        if self.pv <= 0:
            self.ko = True
        return self.ko

    def est_ko(self):
        return self.pv <= 0

    def statistiques(self):
        print(
            f"{poke.nom} (Vie : {poke.pv}, Attaque: {poke.attaque}, Defense: {poke.defense}, Type: {poke.type_principal}, Vitesse: {poke.vitesse}) -> Évolution: {poke.evolution}"
        )
