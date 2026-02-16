from Pokemon.pokemon import *
from menu import *


class combat:
    def __init__(self, pok1, pok2):
        self.pok1 = pok1
        self.pok2 = pok2
        self.ko = False



    # def get_adversaire(self, type, puissance):
    #     type = self.type_principal.upper()
    #     puissance = table_types.get(type, {}).get(type, 1.0)

    def multiplicateur

    def subir_degat(self, montant):
        self.pv -= montant
        if self.pv < 0:
            self.pv = 0
        return self.pv

    def attaque(self, adversaire):
        degats = self.attaque - adversaire.defense
        if degats <= 0:
            degats = 1
        return adversaire.subir_degat(degats)#POSSIBILIT2 DE RATE L ASSAULT

    def gerer_tour():
        #tour+mise à jour des points de vie

    def vainqueur():
