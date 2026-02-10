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
        self.ko=False

    def est_ko(self):
        if self.pv<=0:
            ko=True
            return ko

    # -------------------------------> TEST <-----------------------------#
    # for poke in mes_pokemself.pokemon=ons:
    #     print(
    #         f"{poke.nom} (Vie : {poke.pv}, Attaque: {poke.attaque}, Defense: {poke.defense}, Type: {poke.type_principal}, Vitesse: {poke.vitesse}) -> Évolution: {poke.evolution}"
    #     )


class menu:
    def __init__(self):
        pass

        # Se déclenche au démarrage du jeu, ajout Pokemon pour l'ordinateur
    def ajouter_pokemon(self):
        for p in liste_brute:
            nouveau_p = Pokemon(
                p["name"],
                p["stats"]["HP"],
                p["stats"]["attack"],
                p["stats"]["defense"],
                p["stats"]["speed"],
                p["image"],
                p["apiTypes"][0]["name"]
                )
            mes_pokemons.append(nouveau_p)
    
    def ajouter_utilisateur(self):
        self.nom=str(input("Choisissez votre nom : "))
        
        #Choix random dans la liste des 151 pokemons, il y en a 3 de choisis
        choix_possibles=random.sample(mes_pokemons, 3)

        #Entrée utilisateur pour choisir lequel des trois :
        print(f"\nBonjour {self.nom} ! Choisissez votre premier Pokémon :")
        #L'utilisateur a sous les yeux les trois Pokemons disponibles :
        for i, p in enumerate(choix_possibles):
            print(f"{i} - {p.nom} (Type: {p.type})")
        #Entrée du choix de l'utilisateur, "-1" pour que le choix corresponde à l'index :
        index=int(input("Choisissez votre Pokemon (1, 2 ou 3) : "))-1 # "-1" pour que le choix corresponde à l'index
        #la variable self.pokemon est créée, grâce au choix de l'utilisateur :
        self.pokemon=choix_possibles[index]

        return self.pokemon
    
    def choix_ordi(self):
        # Choix du pokemon de l'ordi, direct dans la liste totale des pokemons :
        self.pokemon_adversaire=random.choice(mes_pokemons)
        return self.pokemon_adversaire
    

class combat:
    def __init__(self, pok1, pok2):
        self.pok1=pok1
        self.pok2=pok2
        self.ko=False

    def verif_ko(self):
        if self.pok1.pv<=0:
            self.ko=True
        if self.pok2.pv<=0:
            self.ko=True
        return self.ko
    
    def attaquer(self, assaillant, cible):
        # 1. On récupère le multiplicateur (ex: 2.0, 0.5 ou 1.0 par défaut)
        # On regarde dans le type de l'attaquant, puis si le type du défenseur y est
        attaquant_type = assaillant.type_principal.upper()
        defenseur_type = cible.type_principal.upper()
        
        # On cherche le multiplicateur, si pas trouvé on met 1.0 (neutre)
        multiplicateur = table_types.get(attaquant_type, {}).get(defenseur_type, 1.0)

        # 2. Calcul des dégâts avec le multiplicateur
        degats = (assaillant.attaque - cible.defense) * multiplicateur
        
        # Sécurité pour ne pas soigner le pokémon
        if degats < 1:
            degats = 1
            
        # 3. Application des dégâts
        cible.pv -= int(degats) # On transforme en entier pour les PV
        
        print(f"{assaillant.nom} attaque {cible.nom} !")
        if multiplicateur > 1:
            print("C'est très efficace !")
        elif multiplicateur < 1 and multiplicateur > 0:
            print("Ce n'est pas très efficace...")
        elif multiplicateur == 0:
            print("Ça n'affecte pas l'adversaire...")
            
        self.verif_ko()

# Appel des joueurs pok1 et pok2 : 