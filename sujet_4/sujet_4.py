class Plante:
    def __init__(self, nom, espece, croissance, taille, exposition):
        self.nom        = nom         # chaîne : nom courant
        self.espece     = espece      # chaîne : nom latin
        self.croissance = croissance  # entier : durée en jours
        self.taille     = taille      # entier : hauteur maximale en cm
        self.exposition = exposition  # chaîne : "ombre", "mi-ombre" ou "plein soleil"
        
if __name__ == "__main__":
    basilic = Plante("Basilic", "Ocimum basilicum", 60, 40, "plein soleil")
    tomate = Plante("Tomate", "Solanum lycopersicum", 80, 100, "plein soleil")
    menthe = Plante("Menthe", "Mentha spicata", 80, 50, "mi-ombre")
    plantes = [basilic, tomate, menthe]
    somme_croissance = 0
    for plante in plantes:
        somme_croissance += plante.croissance
    print(float(f"{somme_croissance/len(plantes):0.2f}"))