from mainclass import table_types
from mainclass import *
from menu import *


class combat:
    def __init__(self, pok1, pok2):
        self.pok1 = pok1
        self.pok2 = pok2
        self.ko = False

    def calculer_puissance_attaque(self, attaquant, defenseur):
        type_atk = attaquant.type_principal
        type_def = defenseur.type_principal
        # -> recupere le type principal de chq pokemon
        multiplicateur = table_types.get(type_atk, {}).get(type_def, 1.0)
        # -> determine leur puissance via types.json
        puissance_attaque = attaquant.attaque - defenseur.defense * multiplicateur
        # -> formule calcule de dégats
        return max(
            1, int(puissance_attaque)
        )  # au moins 1 de dégât si la défense est trop haute pour pas avoir de négatif

    def gerer_tour(self, attaquant, defenseur):
        if self.attaque_reussi():
            tour = self.calculer_puissance_attaque(attaquant, defenseur)
            defenseur.subir_degat(tour)
            print(f" {attaquant.nom} attaque ! {defenseur.nom} perd {tour} PV.")
        else:
            print("L'attaque a échoué")

    def vainqueur(self):
        if self.pok1.pv <= 0:
            return self.pok2
        elif self.pok2.pv <= 0:
            return self.pok1
        else:
            return None

    def attaque_reussi(self):
        precision = 85
        return (
            random.randint(1, 100) <= precision
        )  # 85 % de chance de reussir l attaque


bulbizarre = mes_pokemons[0]  # Bulbizarre
salameche = mes_pokemons[3]  # Herbizarre (index 1)

mon_combat = combat(bulbizarre, salameche)
mon_combat.gerer_tour(bulbizarre, salameche)
mon_combat.vainqueur()
