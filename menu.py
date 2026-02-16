import random
import os
from classPokemon import Pokemon

class Menu:
    def __init__(self, interface):
        self.interface = interface # L'OBJET QUI GÈRE L'ÉCRAN
        self.mes_pokemons = []
        self.pokemon_joueur = None

    def charger_donnees(self, pokedex_objet):
        """CRÉE LES OBJETS POKÉMON À PARTIR DU POKÉDEX"""
        liste_brute = pokedex_objet.catalogue
        
        for p in liste_brute:
            # ON PRÉPARE L'IMAGE
            nom_p = p["nom"]
            chemin_img = f"Assets/Images/{nom_p}.png"
            if not os.path.exists(chemin_img):
                chemin_img = "Assets/Images/PokeDefaut.png"

            # ON CRÉE LE POKÉMON AVEC TOUTES LES INFOS
            nouveau_p = Pokemon(
                nom=p["nom"],
                pv=p["pv"],
                attaque=p["attaque"],
                defense=p["defense"],
                vitesse=p.get("vitesse", 50),
                type_principal=p["types"][0],
                evolution=p["evolution"],
                image_url=chemin_img
            )
            # ON DIT À L'INTERFACE DE PRÉPARER L'IMAGE
            nouveau_p.image_surface = self.interface.preparer_image(chemin_img)
            self.mes_pokemons.append(nouveau_p)