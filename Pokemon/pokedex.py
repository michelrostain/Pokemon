import json

class Pokedex:
    def __init__(self, fichier="pokedex.json"):
        self.fichier = fichier

    # Enregistrement pokemon en vérifiant qu'il n'y a pas de doublons, et gère toutes les écritures sur le fichier :
    def enregistrer(self, pokemon):
    # 1. Lire le contenu actuel du Pokédex
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees = []

    # 2. Vérification des doublons (exigé par le sujet )
    # On vérifie si le nom du Pokémon est déjà présent dans la liste
        deja_present = False
        for p in donnees:
            if p["nom"] == pokemon.nom:
                deja_present = True
                break

    # 3. Ajouter et sauvegarder si c'est un nouveau Pokémon
        if not deja_present:
    # On crée le dictionnaire avec les infos demandées 
            nouvel_entree = {
                "nom": pokemon.nom,
                "type": pokemon.type_principal,
                "pv": pokemon.pv,
                "attaque": pokemon.attaque,
                "defense": pokemon.defense
            }
            donnees.append(nouvel_entree)
            
    # Ecriture dans le fichier json [cite: 21, 69]
            with open(self.fichier, "w", encoding="utf-8") as f:
                json.dump(donnees, f, indent=4, ensure_ascii=False)
            print(f"{pokemon.nom} a été ajouté au Pokédex !")
        else:
            print(f"{pokemon.nom} est déjà enregistré dans le Pokédex.")



    def sauvegarder_pokemon_combatu():
    #DANS POKEDEX combattus.(nom, type, défense, puissance
    #d'attaque et point de vie).##
      pass



    def choix_pokemon_pour_combat():
      pass

