import json
from menu import Menu
from screen import Interface

def main():
    try:
        with open("pokemon.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Erreur: pokemon.json manquant")
        return

    gui = Interface()
    app = Menu(gui)
    app.lancer_jeu(data)

if __name__ == "__main__":
    main()