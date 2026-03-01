#Module principal pour lancer le jeu Pokémon.
import pygame
import json
from menu import Menu
from screen import Interface

def main():
    # Point d'entrée principal de l'application.Charge les données et initialise l'interface et le menu.
    try:
        with open("pokemon.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Erreur: pokemon.json manquant")
        return

    gui = Interface()

    pygame.mixer.music.load("Assets/Sounds/generique.mp3")
    pygame.mixer.music.play(-1)  # -1 = boucle infinie

    app = Menu(gui)
    app.lancer_jeu(data)

if __name__ == "__main__":
    main()
    