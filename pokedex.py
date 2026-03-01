import json
import os

class Pokedex:
    def __init__(self):
        self.fichier_source = "pokemon.json"
        self.fichier_sauvegarde = "pokedex.json"
        self.catalogue = self.charger_catalogue()

    def charger_catalogue(self):
        try:
            with open(self.fichier_source, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def vider_pokedex(self):
        """Réinitialise le fichier de sauvegarde (Nouvelle Partie)"""
        with open(self.fichier_sauvegarde, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        print("Pokedex vidé.")

    def obtenir_pokedex_joueur(self):
        """Lit les pokémons possédés dans pokedex.json"""
        if not os.path.exists(self.fichier_sauvegarde):
            return []
        try:
            with open(self.fichier_sauvegarde, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def rechercher_pokemon(self, nom_recherche):
        for p in self.catalogue:
            if p["nom"].lower() == nom_recherche.lower():
                return p
        return None

    def enregistrer_pokemon(self, nom_pokemon):
        """Ajoute un pokemon à la sauvegarde s'il n'y est pas déjà"""
        infos = self.rechercher_pokemon(nom_pokemon)
        if infos:
            save_data = self.obtenir_pokedex_joueur()
            if not any(p["nom"] == infos["nom"] for p in save_data):
                save_data.append(infos)
                with open(self.fichier_sauvegarde, "w", encoding="utf-8") as f:
                    json.dump(save_data, f, indent=4, ensure_ascii=False)
                print(f"{nom_pokemon} sauvegardé !")

    def supprimer_pokemon(self, nom_pokemon):
        """Supprime un pokemon précis du fichier de sauvegarde"""
        # 1. On charge la liste actuelle
        data = self.obtenir_pokedex_joueur()
        
        # 2. On garde tous ceux qui N'ONT PAS ce nom
        # (Cela supprime donc celui qui a ce nom)
        nouvelle_liste = [p for p in data if p['nom'] != nom_pokemon]
        
        # 3. On écrase le fichier avec la nouvelle liste
        with open(self.fichier_sauvegarde, "w", encoding="utf-8") as f:
            json.dump(nouvelle_liste, f, indent=4)
        
        print(f"{nom_pokemon} a été supprimé de la sauvegarde.")

    def mettre_a_jour_progression(self, pokemon_objet):
        """Met à jour l'XP d'un Pokémon existant dans la sauvegarde"""
        data = self.obtenir_pokedex_joueur()
        
        trouve = False
        for p in data:
            if p['nom'] == pokemon_objet.nom:
                # On met à jour l'XP dans le fichier JSON
                p['xp'] = pokemon_objet.point_exp
                trouve = True
                break
        
        # Si on ne l'a pas trouvé (ex: nouvelle capture), on l'ajoute proprement avec son XP
        if not trouve:
            infos = self.rechercher_pokemon(pokemon_objet.nom)
            if infos:
                infos['xp'] = pokemon_objet.point_exp # On injecte l'XP
                data.append(infos)

        # On sauvegarde le tout
        with open(self.fichier_sauvegarde, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Progression sauvegardée pour {pokemon_objet.nom} (XP: {pokemon_objet.point_exp})")