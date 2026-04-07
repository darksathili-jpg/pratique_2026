# NSI Terminale – Sujet pratique n°16 – BAC 2026
## Warming Stripes — Réchauffement climatique, CSV, bug, régression, visualisation

---

## MÉTADONNÉES DU DOCUMENT

- **Matière** : Numérique et Sciences Informatiques (NSI)
- **Niveau** : Terminale générale
- **Type d'épreuve** : Partie pratique du baccalauréat — durée 1 heure
- **Session** : 2026 — Sujet n°16
- **Thème du programme** : Traitement de données CSV, algorithmique, visualisation matplotlib
- **Langage** : Python 3
- **Fichiers fournis à l'examen** : `warming_stripes.py`, `datas.csv`, `warming_stripes.png`
- **Modules Python requis** : `csv`, `matplotlib.pyplot`

---

## PARTIE 1 — CONTEXTE ET PROBLÉMATIQUE

### Les warming stripes

Conçues par le climatologue Ed Hawkins en 2018, les *warming stripes* (bandes de réchauffement) représentent visuellement l'évolution des températures au fil du temps par rapport à une moyenne historique. Chaque bande verticale correspond à une année : les tons bleus indiquent des températures inférieures à la référence, les tons rouges indiquent des températures supérieures.

### Source des données

Le fichier `datas.csv` est issu de la NOAA (agence américaine d'observation océanique et atmosphérique). Il contient les **écarts de températures mondiales** (terres et océans) par rapport à la moyenne du 20ème siècle (1901-2000), pour chaque année de **1851 à 2025**.

Exemple : la ligne `2020,1.01` signifie qu'en 2020, la température mondiale était supérieure de **1,01 °C** à la moyenne de référence.

### Objectifs du script

1. Écrire une fonction de recherche dans la liste de données.
2. Utiliser une fonction existante pour trouver la dernière année froide.
3. Identifier et corriger un bug de logique dans le calcul de moyenne.
4. Compléter la génération des listes pour le graphique matplotlib.

---

## PARTIE 2 — DONNÉES DU FICHIER `datas.csv`

### Structure du fichier

Séparateur : virgule (`,`). Deux colonnes : `Year` (année entière) et `Anomaly` (écart en °C, flottant).

La fonction `charger(nom_fichier)` fournie convertit ce CSV en **liste de dictionnaires** avec les clés `'année'` (int) et `'écart'` (float) — **les accents dans les noms de clés sont intentionnels** dans le code fourni.

```python
# Résultat de charger("datas.csv") — extrait
[
    {"année": 1851, "écart": -0.15},
    {"année": 1852, "écart": -0.05},
    ...
    {"année": 2024, "écart": 1.22},
    {"année": 2025, "écart": 1.29},
]
```

### Statistiques clés

- **Nombre de relevés** : 175 (1851 à 2025)
- **Première année** : 1851, écart = −0.15 °C
- **Dernière année** : 2025, écart = +1.29 °C (record)
- **Années à écart exactement nul** : 1938 et 1939 (important pour la Q1)
- **Dernière année à écart négatif** : **1977** (écart = −0.03 °C)
- **Première année à écart positif après 1977** : 1978 (écart = +0.20 °C)

### Tableau des valeurs clés pour les assertions

| Année | Écart (°C) | Type |
|-------|-----------|------|
| 1851  | -0.15 | Négatif (froid) |
| 1877  | -0.23 | Négatif |
| 1878  | +0.14 | Positif (premier pic chaud du XIXe) |
| 1938  | 0.00 | Neutre (valeur zéro exacte) |
| 1939  | 0.00 | Neutre (valeur zéro exacte) |
| 1977  | -0.03 | **Dernière année négative** |
| 1978  | +0.20 | Positive (depuis, toutes positives) |
| 2020  | +1.01 | Positif |
| 2024  | +1.22 | Positif |
| 2025  | +1.29 | Positif — maximum actuel |
| 1800  | N/A | **Absent → None** |

### Contenu intégral du fichier `datas.csv`

```
Year,Anomaly
1851,-0.15
1852,-0.05
1853,-0.03
1854,-0.09
1855,-0.02
1856,-0.03
1857,-0.15
1858,-0.17
1859,-0.16
1860,-0.03
1861,-0.25
1862,-0.25
1863,-0.31
1864,-0.21
1865,-0.15
1866,-0.09
1867,-0.11
1868,-0.2
1869,-0.1
1870,-0.08
1871,-0.18
1872,-0.15
1873,-0.19
1874,-0.2
1875,-0.22
1876,-0.23
1877,-0.23
1878,0.14
1879,0.11
1880,-0.16
1881,-0.16
1882,-0.08
1883,-0.18
1884,-0.19
1885,-0.31
1886,-0.27
1887,-0.3
1888,-0.29
1889,-0.08
1890,-0.07
1891,-0.32
1892,-0.21
1893,-0.28
1894,-0.32
1895,-0.3
1896,-0.19
1897,-0.1
1898,-0.1
1899,-0.26
1900,-0.15
1901,-0.05
1902,-0.1
1903,-0.22
1904,-0.39
1905,-0.4
1906,-0.25
1907,-0.16
1908,-0.36
1909,-0.43
1910,-0.4
1911,-0.39
1912,-0.38
1913,-0.34
1914,-0.29
1915,-0.15
1916,-0.09
1917,-0.34
1918,-0.43
1919,-0.27
1920,-0.24
1921,-0.23
1922,-0.18
1923,-0.25
1924,-0.24
1925,-0.25
1926,-0.16
1927,-0.11
1928,-0.16
1929,-0.18
1930,-0.32
1931,-0.09
1932,-0.04
1933,-0.15
1934,-0.25
1935,-0.11
1936,-0.15
1937,-0.09
1938,0
1939,0
1940,0.03
1941,0.15
1942,0.24
1943,0.06
1944,0.1
1945,0.23
1946,0.15
1947,-0.05
1948,0
1949,-0.06
1950,-0.09
1951,-0.14
1952,0.01
1953,0.04
1954,0.08
1955,-0.07
1956,-0.14
1957,-0.16
1958,0.09
1959,0.07
1960,0.07
1961,0.01
1962,0.07
1963,0.05
1964,0.07
1965,-0.17
1966,-0.08
1967,-0.02
1968,0
1969,-0.04
1970,0.12
1971,0.04
1972,-0.07
1973,0.1
1974,0.17
1975,-0.04
1976,0.01
1977,-0.03
1978,0.2
1979,0.11
1980,0.22
1981,0.32
1982,0.32
1983,0.21
1984,0.33
1985,0.19
1986,0.16
1987,0.23
1988,0.36
1989,0.37
1990,0.31
1991,0.45
1992,0.42
1993,0.23
1994,0.26
1995,0.35
1996,0.46
1997,0.35
1998,0.52
1999,0.62
2000,0.4
2001,0.42
2002,0.57
2003,0.62
2004,0.62
2005,0.57
2006,0.68
2007,0.68
2008,0.59
2009,0.58
2010,0.68
2011,0.72
2012,0.61
2013,0.67
2014,0.69
2015,0.76
2016,0.95
2017,1.02
2018,0.92
2019,0.88
2020,1.01
2021,0.99
2022,0.88
2023,0.9
2024,1.22
2025,1.29
```

---

## PARTIE 3 — FICHIER DE DÉPART `warming_stripes.py`

### Fonctions déjà fournies et fonctionnelles

#### `charger(nom_fichier)` — lit le CSV et retourne la liste de dicos

```python
def charger(nom_fichier):
    donnees = []
    with open(nom_fichier, mode='r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            annee = int(ligne["Year"])
            ecart = float(ligne["Anomaly"])
            donnees.append({"année": annee, "écart": ecart})
    return donnees

datas_temperature = charger("datas.csv")
```

#### `derniere_annee_ecart_negatif(datas)` — utilise ecart_temperature (Q1)

```python
def derniere_annee_ecart_negatif(datas):
    annee = max([element["année"] for element in datas])  # part de 2025
    ecart = ecart_temperature(datas, annee)
    while ecart >= 0:      # remonte tant que l'écart est positif ou nul
        annee = annee - 1
        ecart = ecart_temperature(datas, annee)
    return annee
```

**Attention** : cette fonction dépend de `ecart_temperature`. Si cette dernière retourne `0` au lieu de `None` pour une année absente, la boucle `while` ne s'arrêtera pas correctement.

#### `prevision(datas, annee, n)` — régression linéaire sur n dernières années

Cette fonction est fournie et correcte dans sa logique générale. Elle dépend de `moyenne_ecarts` pour calculer la moyenne des températures — c'est cette dépendance qui est buguée (Q3).

#### `moyenne_ecarts(annee_debut, annee_fin, datas)` — VERSION BUGUÉE FOURNIE

```python
def moyenne_ecarts(annee_debut, annee_fin, datas):
    somme = 0
    compteur = 0
    for dico in datas:
        if annee_debut <= dico["année"] and dico["année"] <= annee_fin:
            somme = somme - dico["écart"]    # ← LIGNE BUGUÉE : - au lieu de +
            compteur += 1
    return somme / compteur
```

#### `graphique(datas)` — à compléter (Q4)

```python
def graphique(datas):
    fig, ax = plt.subplots(figsize=(10, 2))
    cmap = plt.get_cmap("seismic")
    temperatures = [dico["écart"] for dico in datas]
    max_val = max(max(temperatures), -min(temperatures))
    norm = plt.Normalize(-max_val, max_val)

    annees    = []   # ← À COMPLÉTER
    ordonnees = []   # ← À COMPLÉTER

    ax.bar(annees, ordonnees, width=1.0, color=cmap(norm(temperatures)))
    ax.set_title("Warming Stripes mondiales - Base 1901-2000")
    plt.yticks([], [])
    ax.set_xlabel("Année")
    plt.tight_layout()
    plt.show()
```

---

## PARTIE 4 — QUESTIONS ET CORRECTIONS COMPLÈTES

---

### QUESTION 1 — Écrire `ecart_temperature` et ses tests

**Énoncé** : Écrire la fonction `ecart_temperature(datas, annee)` qui prend en paramètres la liste des données et une année cible. Elle doit renvoyer l'écart de température correspondant à cette année, ou `None` si l'année n'est pas présente. Rédiger ensuite un jeu de tests avec des assertions.

**Démarche** :
1. Parcourir `datas` avec une boucle `for`.
2. Pour chaque `dico`, tester `dico["année"] == annee`.
3. Si correspondance : `return dico["écart"]`.
4. Après la boucle : `return None` (année absente).

**Correction** :

```python
def ecart_temperature(datas, annee):
    for dico in datas:
        if dico["année"] == annee:
            return dico["écart"]
    return None
```

**Jeu de tests avec assertions** :

```python
def test_ecart_temperature():
    assert ecart_temperature(datas_temperature, 1851) == -0.15
    assert ecart_temperature(datas_temperature, 1878) == 0.14
    assert ecart_temperature(datas_temperature, 2020) == 1.01
    assert ecart_temperature(datas_temperature, 2025) == 1.29
    assert ecart_temperature(datas_temperature, 1800) is None   # absente → None
    print("Les tests sont validés.")

test_ecart_temperature()
```

**Points de vigilance** :
- Retourner `None` (pas `0`) pour une année absente — `0` est une vraie valeur dans le CSV (1938, 1939).
- Tester `None` avec `is None`, pas `== None`.
- Les clés du dictionnaire ont des accents : `"année"` et `"écart"`.

---

### QUESTION 2 — Utiliser `derniere_annee_ecart_negatif`

**Énoncé** : En utilisant la fonction `derniere_annee_ecart_negatif` (déjà fournie), déterminer quelle a été la dernière année où la température mondiale était inférieure à la moyenne de référence.

**Code à écrire** :

```python
print(derniere_annee_ecart_negatif(datas_temperature))
# → 1977
```

**Réponse attendue** : **1977** (écart = −0,03 °C).

**Réponse rédigée pour l'examinateur** : La dernière année où la température mondiale était inférieure à la moyenne de référence (1901–2000) est 1977, avec un écart de −0,03 °C. Depuis 1978, chaque année enregistre une anomalie positive ou nulle, ce qui illustre le réchauffement climatique continu sur presque 50 ans.

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 3 — Identifier et corriger le bug de `moyenne_ecarts`

**Énoncé** : En exécutant `prevision(datas, 2040, 20)`, le résultat semble absurde. Cette absurdité provient d'une erreur dans `moyenne_ecarts`. Analyser, identifier, corriger. Que devient la prévision pour 2040 ?

**Identification du bug** :

La ligne problématique est :
```python
somme = somme - dico["écart"]    # soustraction → accumule l'opposé
```

Au lieu de **additionner** chaque écart à la somme, le code le **soustrait**. Pour des données récentes toutes positives (2006–2025 : entre +0.58 et +1.29), la somme accumulée est très négative, la moyenne calculée est −0,836 au lieu de +0,836. La régression linéaire calcule alors une tendance décroissante, et prédit −0,1054 pour 2040 — absurde, incompatible avec le réchauffement observé.

**Effet sur les chiffres** :

| Version | Formule | Moyenne 2006–2025 | Prévision 2040 |
|---------|---------|------------------|---------------|
| Buguée | `somme - écart` | **−0.836 °C** (faux) | **−0.1054 °C** (absurde) |
| Corrigée | `somme + écart` | **+0.836 °C** ✓ | **+1.5666 °C** ✓ |

**Correction — une seule ligne à modifier** :

```python
# AVANT (buggé) :
somme = somme - dico["écart"]

# APRÈS (corrigé) :
somme = somme + dico["écart"]
```

**Fonction corrigée complète** :

```python
def moyenne_ecarts(annee_debut, annee_fin, datas):
    somme = 0
    compteur = 0
    for dico in datas:
        if annee_debut <= dico["année"] and dico["année"] <= annee_fin:
            somme = somme + dico["écart"]    # ← CORRIGÉ
            compteur += 1
    return somme / compteur
```

**Vérification** :

```python
print(prevision(datas_temperature, 2040, 20))
# → 1.5666...   (environ +1,57 °C — cohérent avec le réchauffement actuel)
```

**Fonction de test** :

```python
def test_moyenne_ecarts():
    d = [{"année": 2000, "écart": 1.0}, {"année": 2001, "écart": 3.0}]
    assert moyenne_ecarts(2000, 2001, d) == 2.0
    d2 = [{"année": 2006, "écart": 0.68}, {"année": 2007, "écart": 0.68}]
    assert moyenne_ecarts(2006, 2007, d2) == 0.68
    assert moyenne_ecarts(2006, 2007, d2) > 0   # doit être positif
    print("Les tests sont validés.")

test_moyenne_ecarts()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 4 — Compléter `graphique` — les listes `annees` et `ordonnees`

**Énoncé** : Compléter la fonction `graphique(datas)` en générant les listes `annees` et `ordonnees`. La liste `ordonnees` doit contenir la valeur 1 pour chaque année.

**Explication** : `ax.bar(annees, ordonnees, ...)` dessine des barres verticales. Les warming stripes encodent l'information dans la **couleur** (déjà gérée par `cmap` et `norm`), pas dans la **hauteur**. Toutes les barres ont donc la même hauteur (1), créant l'effet de bandes uniformes.

**Correction** :

```python
# Version boucle classique
annees    = []
ordonnees = []
for dico in datas:
    annees.append(dico["année"])
    ordonnees.append(1)

# Version compréhension de liste (équivalente, préférée)
annees    = [dico["année"] for dico in datas]
ordonnees = [1 for dico in datas]

# Version la plus concise
ordonnees = [1] * len(datas)
```

**Vérifications** :
- `len(annees) == 175`
- `annees[0] == 1851` et `annees[-1] == 2025`
- `ordonnees == [1] * 175`
- `len(annees) == len(ordonnees)`

**Fonction de test** :

```python
def test_listes_graphique():
    datas_mini = [
        {"année": 1851, "écart": -0.15},
        {"année": 2000, "écart": 0.40},
        {"année": 2025, "écart": 1.29},
    ]
    ann  = [dico["année"] for dico in datas_mini]
    ord_ = [1] * len(datas_mini)
    assert ann  == [1851, 2000, 2025]
    assert ord_ == [1, 1, 1]
    assert len(ann) == len(ord_)
    print("Les tests sont validés.")

test_listes_graphique()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

## PARTIE 5 — CODE COMPLET ET FONCTIONNEL (SOLUTION DE RÉFÉRENCE)

```python
import csv
import matplotlib.pyplot as plt


def charger(nom_fichier):
    donnees = []
    with open(nom_fichier, mode='r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            donnees.append({"année": int(ligne["Year"]), "écart": float(ligne["Anomaly"])})
    return donnees


datas_temperature = charger("datas.csv")


# QUESTION 1
def ecart_temperature(datas, annee):
    for dico in datas:
        if dico["année"] == annee:
            return dico["écart"]
    return None


# QUESTION 1 — Tests
def test_ecart_temperature():
    assert ecart_temperature(datas_temperature, 1851) == -0.15
    assert ecart_temperature(datas_temperature, 1878) == 0.14
    assert ecart_temperature(datas_temperature, 2020) == 1.01
    assert ecart_temperature(datas_temperature, 2025) == 1.29
    assert ecart_temperature(datas_temperature, 1800) is None
    print("Les tests sont validés.")

test_ecart_temperature()


def derniere_annee_ecart_negatif(datas):
    annee = max([element["année"] for element in datas])
    ecart = ecart_temperature(datas, annee)
    while ecart >= 0:
        annee = annee - 1
        ecart = ecart_temperature(datas, annee)
    return annee


# QUESTION 2
print(derniere_annee_ecart_negatif(datas_temperature))   # → 1977


# QUESTION 3 — version corrigée
def moyenne_ecarts(annee_debut, annee_fin, datas):
    somme = 0
    compteur = 0
    for dico in datas:
        if annee_debut <= dico["année"] and dico["année"] <= annee_fin:
            somme = somme + dico["écart"]    # ← CORRIGÉ (était -)
            compteur += 1
    return somme / compteur


def prevision(datas, annee, n):
    longueur = len(datas)
    annee_debut = datas[longueur-n]["année"]
    annee_fin   = datas[longueur-1]["année"]
    moy_annees       = (annee_debut + annee_fin) / 2
    moy_temperatures = moyenne_ecarts(annee_debut, annee_fin, datas)
    numerateur = 0
    denominateur = 0
    for i in range(1, n+1):
        ecart_annee = datas[longueur-i]["année"] - moy_annees
        ecart_temp  = datas[longueur-i]["écart"] - moy_temperatures
        numerateur   += ecart_annee * ecart_temp
        denominateur += ecart_annee ** 2
    a = numerateur / denominateur
    b = moy_temperatures - a * moy_annees
    return a * annee + b

print(prevision(datas_temperature, 2040, 20))   # → ≈ 1.5666


# QUESTION 4
def graphique(datas):
    fig, ax = plt.subplots(figsize=(10, 2))
    cmap = plt.get_cmap("seismic")
    temperatures = [dico["écart"] for dico in datas]
    max_val = max(max(temperatures), -min(temperatures))
    norm = plt.Normalize(-max_val, max_val)

    annees    = [dico["année"] for dico in datas]   # ← AJOUTÉ
    ordonnees = [1] * len(datas)                     # ← AJOUTÉ

    ax.bar(annees, ordonnees, width=1.0, color=cmap(norm(temperatures)))
    ax.set_title("Warming Stripes mondiales - Base 1901-2000")
    plt.yticks([], [])
    ax.set_xlabel("Année")
    plt.tight_layout()
    plt.show()

graphique(datas_temperature)
```

---

## PARTIE 6 — ERREURS FRÉQUENTES ET PIÈGES

### Piège 1 — Retourner 0 au lieu de None pour une année absente (Q1)

Les années 1938 et 1939 ont un écart de 0.0 dans le CSV. Retourner `0` pour une année absente est incorrect et dangereux : la fonction `derniere_annee_ecart_negatif` utilise `while ecart >= 0`, donc si `ecart_temperature` retourne `0` pour une année absente, la boucle continuera à chercher indéfiniment.

```python
# ERREUR : 0 est ambigu
return 0

# CORRECT
return None
```

### Piège 2 — Tester None avec == au lieu de is

```python
# DÉCONSEILLÉ
assert ecart_temperature(datas, 1800) == None

# CORRECT
assert ecart_temperature(datas, 1800) is None
```

### Piège 3 — Accents manquants dans les clés de dictionnaire

```python
# KeyError ! Pas d'accent dans la clé
dico["annee"]   # ← KeyError
dico["ecart"]   # ← KeyError

# Correct (avec accents, comme créé par charger())
dico["année"]
dico["écart"]
```

### Piège 4 — Ne pas voir le signe - dans moyenne_ecarts (Q3)

Le bug est un seul caractère. Pour le détecter : calculer à la main la moyenne de 2 valeurs connues et vérifier que le résultat de la fonction correspond. Avec des données toutes positives, toute moyenne négative signale un bug de signe.

### Piège 5 — Mettre les vraies valeurs d'écart dans ordonnees (Q4)

```python
# ERREUR : barres de hauteurs différentes, certaines négatives
ordonnees = [dico["écart"] for dico in datas]

# CORRECT : toutes les barres à hauteur 1
ordonnees = [1] * len(datas)
```

L'information est encodée dans la **couleur**, pas dans la hauteur. L'énoncé l'indique explicitement dans l'indication.

---

## PARTIE 7 — RAPPELS DE COURS

### Recherche dans une liste de dictionnaires

```python
def chercher(liste, cle, valeur_cible):
    for dico in liste:
        if dico[cle] == valeur_cible:
            return dico   # ou dico["autre_cle"]
    return None           # pas trouvé
```

### La valeur None et son test

```python
resultat = chercher(...)
if resultat is None:
    print("Pas trouvé")
if resultat is not None:
    print("Trouvé :", resultat)
```

### Compréhension de liste

```python
# Extraire une colonne
annees    = [dico["année"] for dico in datas]

# Filtrer
positifs  = [dico["écart"] for dico in datas if dico["écart"] > 0]

# Créer une liste constante
ordonnees = [1 for _ in datas]    # ou : [1] * len(datas)
```

### Régression linéaire — intuition

La fonction `prevision(datas, annee_cible, n)` trace une droite qui passe au plus proche des n dernières années de données (méthode des moindres carrés), puis lit la valeur prévue sur cette droite pour l'année cible. Elle dépend de `moyenne_ecarts` pour centrer les données.

### Matplotlib — `ax.bar(x, height, ...)`

- `x` : liste des positions horizontales (ici les années)
- `height` : liste des hauteurs des barres (ici toutes égales à 1)
- `color` : liste des couleurs calculées par la palette `seismic`
- `width=1.0` : chaque barre a une largeur d'1 an — les barres se touchent

---

## PARTIE 8 — CHECKLIST AVANT DE RENDRE LE CODE

- [ ] Q1 : `ecart_temperature` retourne `None` (pas `0`) pour une année absente
- [ ] Q1 : les assertions testent `is None` pour l'année absente
- [ ] Q1 : les clés utilisées sont `"année"` et `"écart"` (avec accents)
- [ ] Q2 : `derniere_annee_ecart_negatif` est appelée et retourne 1977
- [ ] Q2 : une phrase d'interprétation est rédigée pour l'examinateur
- [ ] Q3 : la ligne `somme = somme - dico["écart"]` est corrigée en `+`
- [ ] Q3 : `prevision(datas_temperature, 2040, 20)` retourne environ +1,57
- [ ] Q4 : `annees` est une liste des années (ints), de 1851 à 2025
- [ ] Q4 : `ordonnees` est `[1] * 175` (ou équivalent)
- [ ] Q4 : `len(annees) == len(ordonnees)`

---

## PARTIE 9 — GLOSSAIRE

**Warming stripes** : visualisation des écarts de température par des bandes colorées, du bleu (froid) au rouge (chaud), créée par Ed Hawkins en 2018.

**Anomalie de température** : écart entre la température d'une année et une température de référence historique. Positive = plus chaud que la référence.

**NOAA** : National Oceanic and Atmospheric Administration, agence américaine qui collecte les données climatiques mondiales.

**Régression linéaire** : méthode statistique qui trouve la droite passant au plus proche d'un nuage de points, utilisée ici pour extrapoler l'évolution future des températures.

**`None`** : valeur Python spéciale signifiant « rien » ou « absent ». Testée avec `is None` ou `is not None`.

**`csv.DictReader`** : classe Python qui lit un fichier CSV et retourne chaque ligne comme un dictionnaire `{nom_colonne: valeur_str}`.

**`plt.get_cmap("seismic")`** : palette de couleurs matplotlib allant du bleu pur (valeurs négatives) au rouge pur (valeurs positives), en passant par le blanc (zéro).

**`plt.Normalize(vmin, vmax)`** : objet matplotlib qui normalise des valeurs entre 0 et 1 pour les mapper sur une palette de couleurs.

**Compréhension de liste** : syntaxe Python `[expression for element in iterable]` pour construire une liste en une ligne.

**Erreur logique** : erreur qui ne produit pas d'exception Python mais donne un résultat mathématiquement incorrect. Exemple : `somme - écart` au lieu de `somme + écart`.

---

*Document produit pour une utilisation pédagogique dans NotebookLM. Lycée Antoine Watteau — DarkSATHI Li*
