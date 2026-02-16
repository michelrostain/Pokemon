import json
import pygame
import sys

# Importation de tes classes
from menu import Menu
from screen import Interface

def main():
    """
    Fonction principale qui démarre tout le programme.
    """
    
    # 1. On charge la liste globale des Pokémons (le catalogue)
    # C'est nécessaire pour que le Menu puisse créer les objets Pokemon
    try:
        with open("pokemon.json", "r", encoding="utf-8") as f:
            liste_globale = json.load(f)
            print(f"Chargement réussi : {len(liste_globale)} Pokémons trouvés.")
    except FileNotFoundError:
        print("ERREUR CRITIQUE : Le fichier 'pokemon.json' est introuvable.")
        print("Le jeu ne peut pas démarrer sans les données.")
        return
    except json.JSONDecodeError:
        print("ERREUR CRITIQUE : Le fichier 'pokemon.json' est mal formaté.")
        return

    # 2. On instancie l'Interface (La vue)
    # Cela va lancer pygame.init() et ouvrir la fenêtre
    gui = Interface()

    # 3. On instancie le Menu (Le contrôleur)
    # On lui donne 'gui' pour qu'il puisse contrôler l'écran
    jeu = Menu(gui)

    # 4. On lance la boucle principale du jeu
    # On passe la liste chargée à l'étape 1
    jeu.lancer_jeu(liste_globale)

    # 5. Fin propre (si on sort de lancer_jeu)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()