import json
import pygame
import random
import os

# --- Gestion des chemins automatique ---
dossier_actuel = os.path.dirname(__file__)
chemin_poker = os.path.join(dossier_actuel, "pokemon.json")
chemin_types = os.path.join(dossier_actuel, "types.json")

with open(chemin_poker, "r", encoding="utf-8") as f:
    liste_brute = json.load(f)

with open(chemin_types, "r", encoding="utf-8") as f:
    table_types = json.load(f)

pygame.init


class Pokemon:
    def __init__(self, nom, pv, attaque, defense, type_principal, evolution):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.type_principal = type_principal
        self.evolution = evolution
        self.ko = False

    def subir_degat(self, montant):
        self.pv -= montant
        if self.pv < 0:
            self.pv = 0
        return self.pv

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


mes_pokemons = []

for p in liste_brute:
    nouveau_p = Pokemon(
        nom=p["nom"],
        pv=p["pv"],
        attaque=p["attaque"],
        defense=p["defense"],
        type_principal=p["types"][0],
        evolution=p["evolution"],
    )
    mes_pokemons.append(nouveau_p)


# Ajoute ce print pour vérifier dans ton terminal au lancement
print(f"DEBUG : {len(mes_pokemons)} Pokémon chargés dans la liste.")
