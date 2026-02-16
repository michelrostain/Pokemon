import json
import os

class Pokedex:
    def __init__(self):
        # CHEMINS VERS LES FICHIERS
        self.fichier_source = "pokemon.json"
        self.fichier_sauvegarde = "pokedex.json"
        # ON CHARGE TOUT DE SUITE LE CATALOGUE
        self.catalogue = self.charger_catalogue()

    def charger_catalogue(self):
        """LIT LE FICHIER JSON POUR REMPLIR LE CATALOGUE"""
        try:
            with open(self.fichier_source, "r", encoding="utf-8") as f:
                donnees = json.load(f)
            print("Catalogue chargé avec succès !")
            return donnees
        except FileNotFoundError:
            print("Attention : Fichier source introuvable")
            return []
        
    def rechercher_pokemon(self, nom_recherche):
        """RECHERCHE UN POKÉMON PAR SON NOM"""
        for p in self.catalogue:
            if p["nom"].lower() == nom_recherche.lower():
                return p
        return None

    def enregistrer_pokemon(self, nom_pokemon):
        """AJOUTE UN POKÉMON DANS TA SAUVEGARDE PERSO"""
        infos = self.rechercher_pokemon(nom_pokemon)
        if infos:
            save_data = []
            if os.path.exists(self.fichier_sauvegarde):
                with open(self.fichier_sauvegarde, "r", encoding="utf-8") as f:
                    try: save_data = json.load(f)
                    except: save_data = []

            # ON VÉRIFIE SI ON NE L'A PAS DÉJÀ
            if not any(p["nom"] == infos["nom"] for p in save_data):
                save_data.append(infos)
                with open(self.fichier_sauvegarde, "w", encoding="utf-8") as f:
                    json.dump(save_data, f, indent=4, ensure_ascii=False)
                print(f"{nom_pokemon} enregistré dans ton Pokedex !")