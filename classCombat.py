import random
import json

class combat:
    def __init__(self, pok1, pok2, pokedex_outil):
        self.pok1 = pok1
        self.pok2 = pok2
        self.pokedex = pokedex_outil # ON GARDE L'OUTIL POUR SAUVEGARDER

    def calculer_puissance_attaque(self, attaquant, defenseur, table_types):
        type_atk = attaquant.type_principal.lower()
        type_def = defenseur.type_principal.lower()
        
        # ON CHERCHE LE MULTIPLICATEUR DANS LA TABLE DES TYPES
        multi = table_types.get(type_atk, {}).get(type_def, 1.0)
        degats = (attaquant.attaque - defenseur.defense) * multi
        return max(1, int(degats))

    def gerer_fin_combat(self):
        """CETTE FONCTION ENREGISTRE LE GAGNANT"""
        gagnant = self.vainqueur()
        if gagnant:
            self.pokedex.enregistrer_pokemon(gagnant.nom)
            print(f"Victoire de {gagnant.nom} enregistrée !")

    def vainqueur(self):
        if self.pok1.pv <= 0: return self.pok2
        if self.pok2.pv <= 0: return self.pok1
        return None