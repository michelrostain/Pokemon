import json
import pygame

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
    def __init__(self, nom, pv, attaque, defense, vitesse, image_url, type_principal, evolution_nom):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.vitesse = vitesse
        self.image_url = image_url
        self.type_principal = type_principal
        self.evolution_nom = evolution_nom
        self.point_exp=0
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
            f"{self.nom} (Vie : {self.pv}, Attaque: {self.attaque}, Defense: {self.defense}, Type: {self.type_principal}, Vitesse: {self.vitesse}) -> Évolution: {self.evolution}"
        )

    def faire_evoluer(self):
    # On vérifie si une évolution est possible
        if self.evolution_nom is not None:
            # On cherche dans la liste globale le Pokémon qui porte ce nom
            for p in mes_pokemons:
                if p.nom == self.evolution_nom:
                    # On remplace les stats actuelles par celles de l'évolution
                    self.nom = p.nom
                    self.pv = p.pv
                    self.attaque = p.attaque
                    self.defense = p.defense
                    self.type_principal = p.type_principal
                    self.evolution_nom = p.evolution_nom # On récupère le nom de la PROCHAINE évolution
                    print(f"Incroyable ! Votre Pokémon a évolué en {self.nom} !")
                    break
