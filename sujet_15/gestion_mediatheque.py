import sqlite3

###############################################################################
# Données de la médiathèque
# Ce fichier reproduit la structure de la base mediatheque.sqlite
###############################################################################

# Table adherent : (id, nom, prenom, telephone)
adherents = [
    (1, "Martin",  "Alice", "06-12-34-56-78"),
    (2, "Dupont",  "Bob",   "07.98.76.54.32"),
    (3, "Lemaire", "Carla", "04 56 78 90 12"),
    (4, "Leroy",   "Denis", "0623456789"),
]

# Table livre : (id, titre, auteur, genre, isbn)
livres = [
    (1, "Asterix le Gaulois", "Goscinny",     "BD",    "9782012101418"),
    (2, "Lucky Luke",         "Morris",        "BD",    "9782884714006"),
    (3, "Le Petit Prince",    "Saint-Exupery", "Roman", "9782070408504"),
    (4, "Tintin au Tibet",    "Herge",         "BD",    "9782203001015"),
    (5, "1984",               "Orwell",        "Roman", "9782070368228"),
    (6, "Spirou et Fantasio", "Franquin",      "BD",    "9782800100012"),
    (7, "Gaston Lagaffe",     "Franquin",      "BD",    "9782800124056"),
    (8, "Les Miserables",     "Hugo",          "Roman", "9782070409228"),
]

# Table emprunt : (id, id_adherent, id_livre, date_emprunt, date_retour)
# date_emprunt et date_retour sont des chaines au format AAAAMMJJ
# date_retour vaut None si le livre n'a pas encore ete rendu
emprunts = [
    (1,  1, 1, "20240501", "20240515"),
    (2,  1, 3, "20240615", "20240630"),
    (3,  2, 2, "20240820", "20240905"),
    (4,  3, 4, "20230901", "20230915"),
    (5,  1, 4, "20241015", None),
    (6,  2, 1, "20241201", None),
    (7,  4, 6, "20240302", "20240320"),
    (8,  3, 7, "20241110", None),
    (9,  2, 5, "20240710", "20240730"),
    (10, 4, 8, "20231215", "20240103"),
    (11, 1, 2, "20240910", None),
    (12, 3, 1, "20240405", "20240420"),
]


###############################################################################
# Connexion a la base de donnees SQLite
# En situation reelle, la base est fournie dans le dossier de l'epreuve.
# Ce code cree une base en memoire a partir des donnees ci-dessus.
###############################################################################

def creer_base():
    """
    Cree et peuple une base SQLite en memoire.
    Renvoie la connexion.
    A utiliser uniquement pour les tests (remplace le fichier mediatheque.sqlite).
    """
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("""CREATE TABLE adherent (
                    id INTEGER PRIMARY KEY,
                    nom TEXT,
                    prenom TEXT,
                    telephone TEXT)""")
    c.execute("""CREATE TABLE livre (
                    id INTEGER PRIMARY KEY,
                    titre TEXT,
                    auteur TEXT,
                    genre TEXT,
                    isbn TEXT)""")
    c.execute("""CREATE TABLE emprunt (
                    id INTEGER PRIMARY KEY,
                    id_adherent INTEGER,
                    id_livre INTEGER,
                    date_emprunt TEXT,
                    date_retour TEXT)""")
    c.executemany("INSERT INTO adherent VALUES (?,?,?,?)", adherents)
    c.executemany("INSERT INTO livre    VALUES (?,?,?,?,?)", livres)
    c.executemany("INSERT INTO emprunt  VALUES (?,?,?,?,?)", emprunts)
    conn.commit()
    return conn


# Connexion utilisee dans tout le programme
# En examen : remplacer par sqlite3.connect("mediatheque.sqlite")
conn = creer_base()


###############################################################################
# Fonctions utilitaires fournies
###############################################################################

def validation_isbn(isbn):
    """
    Renvoie True si isbn est un ISBN-13 valide :
      - exactement 13 chiffres,
      - commence par '978' ou '979'.
    Renvoie False sinon.
    """
    if len(isbn) != 13:
        return False
    if not isbn.startswith("978") and not isbn.startswith("979"):
        return False
    return True


###############################################################################
# Question 1 : ecrire la fonction normalisation_isbn
###############################################################################

def normalisation_isbn(isbn):
    """
    Prend un ISBN sous forme de chaine quelconque
    (peut contenir des tirets, espaces, points...) et renvoie
    une chaine ne contenant que les chiffres, dans l'ordre.

    Exemples :
        normalisation_isbn("978-2-07-036024-5")  -> "9782070360245"
        normalisation_isbn("978 2 07 040850 4")  -> "9782070408504"
        normalisation_isbn("9782253004226")       -> "9782253004226"
    """
    pass  # A COMPLETER


###############################################################################
# Question 2 : ecrire le jeu de tests de validation_isbn
###############################################################################

def test_validation_isbn():
    """
    Jeu de tests pour la fonction validation_isbn.
    Chaque assertion doit verifier une condition de rejet distincte.
    La fonction validation_isbn est fournie et correcte.
    """
    # Cas valides - a completer
    assert validation_isbn("9782070360245") == True   # ISBN 978, 13 chiffres
    # ...

    # Condition 1 : longueur incorrecte (trop court) - a completer
    # ...

    # Condition 1 : longueur incorrecte (trop long) - a completer
    # ...

    # Condition 2 : mauvais prefixe (13 chiffres mais ne commence pas par 978/979)
    # ...

    print("Les tests de validation_isbn sont passes.")


###############################################################################
# Question 3 : ecrire la fonction emprunts_livre_bd
###############################################################################

def emprunts_livre_bd(conn, date):
    """
    Renvoie la liste des emprunts de livres de genre 'BD'
    effectues apres la date passee en parametre.

    Chaque element de la liste est un tuple :
    (adherent.id, adherent.nom, adherent.prenom,
     adherent.telephone, emprunt.date_emprunt)

    Les resultats sont tries par adherent.id puis par emprunt.date_emprunt.

    Parametres :
        conn : connexion SQLite
        date : chaine au format "AAAAMMJJ"
    """
    pass  # A COMPLETER


###############################################################################
# Question 4 : analyser et corriger dernier_emprunt
###############################################################################

def dernier_emprunt(emprunts):
    """
    Prend en parametre une liste de tuples
    (id_adherent, nom, prenom, telephone, date_emprunt)
    telle que celle renvoyee par emprunts_livre_bd.

    Renvoie un dictionnaire associant a chaque id_adherent
    le tuple correspondant a son dernier emprunt (date la plus recente).

    ATTENTION : cette fonction contient une erreur logique.
    Identifier et corriger cette erreur.
    """
    derniers = {}
    for e in emprunts:
        id_adh = e[0]
        date   = e[4]
        if id_adh not in derniers:
            derniers[id_adh] = e
        elif date < derniers[id_adh][4]:   # LIGNE A CORRIGER
            derniers[id_adh] = e
    return derniers


###############################################################################
# Jeux de tests fournis
###############################################################################

def test_normalisation_isbn():
    assert normalisation_isbn("978-2-07-036024-5")  == "9782070360245"
    assert normalisation_isbn("978 2 07 040850 4")  == "9782070408504"
    assert normalisation_isbn("978.2.07.040850.4")  == "9782070408504"
    assert normalisation_isbn("9782253004226")       == "9782253004226"
    assert normalisation_isbn("978207040")           == "978207040"
    assert normalisation_isbn("97820703602459")      == "97820703602459"
    print("Les tests de normalisation_isbn sont passes.")


def test_emprunts_livre_bd():
    res = emprunts_livre_bd(conn, "20240101")
    # 8 emprunts de BD apres le 01/01/2024 dans les donnees de test
    if len(res) != 8:
        print(f"test_emprunts_livre_bd : attendu 8, obtenu {len(res)}")
    # Le premier resultat doit concerner l'adherent 1 (Alice Martin)
    if res[0][0] != 1:
        print(f"test_emprunts_livre_bd : premier adherent attendu 1, obtenu {res[0][0]}")
    if len(res) == 8 and res[0][0] == 1:
        print("Les tests de emprunts_livre_bd sont passes.")


def test_dernier_emprunt():
    emprunts_test = [
        (1, "Martin",  "Alice", "0612345678", "20240501"),
        (1, "Martin",  "Alice", "0612345678", "20241015"),
        (1, "Martin",  "Alice", "0612345678", "20231201"),
        (2, "Dupont",  "Bob",   "0798765432", "20241201"),
        (3, "Lemaire", "Carla", "0456789012", "20230901"),
    ]
    d = dernier_emprunt(emprunts_test)
    if d[1][4] != "20241015":
        print(f"test_dernier_emprunt : pour id=1, attendu '20241015', obtenu '{d[1][4]}'")
        print("  -> Verifier la condition de comparaison dans la fonction.")
    else:
        print("Les tests de dernier_emprunt sont passes.")


###############################################################################
# Programme principal
###############################################################################

if __name__ == "__main__":
    # Question 1
    test_normalisation_isbn()

    # Question 2
    test_validation_isbn()

    # Question 3
    test_emprunts_livre_bd()

    # Question 4
    test_dernier_emprunt()
