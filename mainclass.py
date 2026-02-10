import json


class Pokemon:
    def __init__(
        self, nom, pv, attaque, defense, image_url, type_principal, evolution, vitesse
    ):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.image_url = image_url
        self.type_principal = type_principal
        self.evolution = evolution
        self.vitesse = vitesse


chemin = "pokemon.json"

with open(chemin, "r", encoding="utf-8") as f:
    liste_brute = json.load(f)

# 3. Création de tes objets
mes_pokemons = []


for p in liste_brute:
    # On vérifie si une évolution existe
    if p["apiEvolutions"] != "none" and len(p["apiEvolutions"]) > 0:
        nom_evolution = p["apiEvolutions"][0]["name"]
    else:
        nom_evolution = "Pas d'évolution"

    nouveau_p = Pokemon(
        nom=p["name"],
        pv=p["stats"]["HP"],
        attaque=p["stats"]["attack"],
        defense=p["stats"]["defense"],
        vitesse=p["stats"]["speed"],
        image_url=p["image"],
        type_principal=p["apiTypes"][0]["name"],
        evolution=nom_evolution,
    )
    mes_pokemons.append(nouveau_p)

    def attaque(self, puissance):
      return self.attaque


      self.pv -= puissance
      if self.pv < 0:
        self.pv = 0
      return self.pv

    def est_ko(self):
        return self.pv <=0

    def subir_degat(self):

    # -------------------------------> TEST <-----------------------------#
    for poke in mes_pokemons:
        print(
            f"{poke.nom} (Vie : {poke.pv}, Attaque: {poke.attaque}, Defense: {poke.defense}, Type: {poke.type_principal}, Vitesse: {poke.vitesse}) -> Évolution: {poke.evolution}"
        )
