from mainclass import *


class menu:
    def __init__(self):
        pass

        # Se déclenche au démarrage du jeu, ajout Pokemon pour l'ordinateur
    def afficher_menu(self):

    def ajouter_pokemon(self):
        for p in liste_brute:
            nouveau_p = Pokemon(
                p["name"],
                p["stats"]["HP"],
                p["stats"]["attack"],
                p["stats"]["defense"],
                p["stats"]["speed"],
                p["image"],
                p["apiTypes"][0]["name"],
            )
            mes_pokemons.append(nouveau_p)

    def ajouter_utilisateur(self):#selectionnner pokemon
        self.nom = str(input("Choisissez votre nom : "))

        # Choix random dans la liste des 151 pokemons, il y en a 3 de choisis
        choix_possibles = random.sample(mes_pokemons, 3)

        # Entrée utilisateur pour choisir lequel des trois :
        print(f"\nBonjour {self.nom} ! Choisissez votre premier Pokémon :")
        # L'utilisateur a sous les yeux les trois Pokemons disponibles :
        for i, p in enumerate(choix_possibles):
            print(f"{i} - {p.nom} (Type: {p.type})")
        # Entrée du choix de l'utilisateur, "-1" pour que le choix corresponde à l'index :
        index = (
            int(input("Choisissez votre Pokemon (1, 2 ou 3) : ")) - 1
        )  # "-1" pour que le choix corresponde à l'index
        # la variable self.pokemon est créée, grâce au choix de l'utilisateur :
        self.pokemon = choix_possibles[index]

        return self.pokemon

    def generer_adversaire(self):
        # Choix du pokemon de l'ordi, direct dans la liste totale des pokemons :
        self.pokemon_adversaire = random.choice(mes_pokemons)
        return self.pokemon_adversaire
