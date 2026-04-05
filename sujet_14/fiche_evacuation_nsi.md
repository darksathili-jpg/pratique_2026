# Fiche de révision — BAC NSI 2026 — Sujet n°14 : Simulation d'évacuation

**Niveau :** Terminale NSI  
**Thèmes :** POO · Tableaux 2D · Distance de Manhattan · Algorithme du minimum · Débogage  
**Source :** Épreuve pratique BAC NSI 2026, sujet n°14  
**Lycée Antoine Watteau — DarkSATHI Li**

---

## Analyse critique — Bugs identifiés dans le code fourni

Le code de `choix_sortie` contient **deux bugs distincts** à identifier et corriger en Question 4 :

**Bug 1 — Condition logiquement impossible :**  
La condition `if k < 0` est *toujours fausse* car `k` part de 1 dans `range(1, len(self.sorties))` et ne peut jamais être négatif. Le corps du `if` ne s'exécute jamais. La méthode renvoie donc systématiquement `self.sorties[0]`, ignorant toutes les autres sorties.

**Bug 2 — Variable non définie :**  
`distance = d2` utilise `d2` qui n'a jamais été initialisée. Cela aurait provoqué une `NameError` si la condition avait pu être vraie.

**Corrections :**
- Ajouter `d2 = distance_de_manhattan(autre_sortie)` avant le test
- Remplacer `if k < 0` par `if d2 < distance`

---

## Contexte du sujet

Ce sujet modélise l'évacuation d'une pièce rectangulaire. La pièce est découpée en cases, chaque case pouvant contenir de 0 à 5 occupants. Des sorties sont placées sur les murs. Lors d'une alerte, chaque occupant avance d'un pas vers la sortie la plus proche.

Le fichier `simulation_evacuation.py` contient la classe `Piece` à compléter et corriger. Le fichier `IHM_evacuation.py` fournit une interface graphique (Tkinter) pour tester — à utiliser sans modification.

---

## Rappels de cours indispensables

### Tableaux 2D en Python

Une grille est une **liste de listes**. `grille[i][j]` est la case à la ligne `i`, colonne `j`.

```python
# Créer une grille 3×4 initialisée à 0
grille = [[0 for _ in range(4)] for _ in range(3)]

# Accès à une case
grille[1][2] = 5    # ligne 1, colonne 2

# Trois façons de sommer tous les éléments
total = 0
for ligne in grille:
    for valeur in ligne:
        total += valeur

# Version compacte (recommandée)
total = sum(sum(ligne) for ligne in grille)

# Version avec double boucle dans la compréhension
total = sum(v for ligne in grille for v in ligne)
```

### Distance de Manhattan

La distance de Manhattan entre deux cases `(i1, j1)` et `(i2, j2)` est :

$$d = |i_1 - i_2| + |j_1 - j_2|$$

Elle représente le nombre minimal de déplacements (haut/bas/gauche/droite) pour aller d'une case à l'autre.

```python
def distance_de_manhattan(destination):
    """Fonction interne — i et j sont capturés depuis le contexte."""
    return abs(i - destination[0]) + abs(j - destination[1])
```

**Exemple :** depuis (3, 4), la distance vers (0, 5) est |3−0| + |4−5| = 3 + 1 = **4**.

### Algorithme du minimum — patron fondamental

Ce schéma apparaît dans `choix_sortie` : trouver l'élément d'une liste qui minimise un critère.

```python
meilleur      = liste[0]            # initialiser avec le premier élément
meilleure_val = critere(liste[0])   # valeur correspondante

for element in liste[1:]:           # parcourir le reste
    val = critere(element)
    if val < meilleure_val:         # on a trouvé mieux
        meilleur      = element
        meilleure_val = val

return meilleur
```

---

## Architecture du programme

### Attributs de la classe `Piece`

| Attribut | Type | Description |
|---|---|---|
| `grille` | `list[list[int]]` | Tableau 2D — `grille[i][j]` = nb d'occupants (0 à 5) |
| `i_max` | `int` | Indice maximal de ligne = profondeur − 1 |
| `j_max` | `int` | Indice maximal de colonne = largeur − 1 |
| `capacite` | `int` | Capacité totale = profondeur × largeur × 5 |
| `sorties` | `list[tuple]` | Liste de tuples `(ligne, colonne)` représentant les sorties |

### Statut de chaque méthode

| Méthode | Statut | Ce qu'il faut faire |
|---|---|---|
| `nb_occupants_restants()` | À écrire (Q1) | `sum(sum(ligne) for ligne in self.grille)` |
| `evacuation(p, silencieux)` | À écrire (Q2) | Boucle `while p.alerter(silencieux)` |
| `ajouter_sortie(dir, pos)` | À compléter (Q3) | Ajouter `"S"` et `"E"` |
| `choix_sortie(i, j)` | À corriger (Q4) | Corriger 2 bugs |
| `ajouter_occupants(i, j, nb)` | Fournie ✓ | Ajoute des occupants (max 5 par case) |
| `alerter(silencieux)` | Fournie ✓ | Simule 1 tour — renvoie True si mouvement |
| `deplacer(i, j, nb, dir)` | Fournie ✓ | Déplace des occupants dans une direction |

### Coordonnées des sorties — convention critique

Une sortie est un tuple `(ligne, colonne)`. Pour une pièce `Piece(5, 7)` (i_max=4, j_max=6) :

| Direction | Tuple sortie | Raisonnement |
|---|---|---|
| `"N"` Nord | `(0, position)` | Ligne 0, colonne = position |
| `"S"` Sud | `(i_max, position)` | Dernière ligne, colonne = position |
| `"O"` Ouest | `(position, 0)` | Colonne 0, ligne = position |
| `"E"` Est | `(position, j_max)` | Dernière colonne, ligne = position |

**Mnémotechnique :** N et S → même colonne, ligne extrême. O et E → même ligne, colonne extrême.

---

## Question 1 — `nb_occupants_restants`

### Énoncé

Écrire le corps de `nb_occupants_restants` qui renvoie le nombre total d'occupants dans la pièce.

### Solution

```python
def nb_occupants_restants(self) -> int:
    """Renvoie le nombre total d'occupants dans la pièce."""
    return sum(sum(ligne) for ligne in self.grille)
```

### Explication

- `sum(ligne)` somme les éléments d'une ligne (ex : `[0, 2, 0, 0]` → 2)
- `for ligne in self.grille` parcourt chaque ligne
- `sum(... for ...)` additionne les sommes de chaque ligne

### Fonction de test

```python
def test_nb_occupants_restants():
    p1 = Piece(5, 7)
    # Pièce vide
    assert p1.nb_occupants_restants() == 0
    # Ajout de valeurs connues
    from random import randint
    n1 = randint(1, 5)
    cases_occupees = {(0, 3): 4, (0, 1): 2, (3, 4): 3, (4, 0): n1, (4, 3): 2}
    for c in cases_occupees:
        p1.ajouter_occupants(c[0], c[1], cases_occupees[c])
    assert p1.nb_occupants_restants() == 11 + n1
    print("Les tests sont validés.")

test_nb_occupants_restants()
```

---

## Question 2 — `evacuation`

### Énoncé

Écrire la fonction `evacuation(p, silencieux=True)` qui simule l'évacuation complète et renvoie le nombre de tours. Elle doit appeler `p.alerter(silencieux)` à chaque tour, et afficher l'état si `silencieux=False`.

### Ce que fait `alerter()`

- Simule **un tour** : chaque occupant avance d'une case vers sa sortie la plus proche.
- Renvoie `True` si au moins un déplacement a eu lieu, `False` si personne n'a pu bouger.
- Quand la pièce est vide, renvoie `False`.
- On compte le nombre d'appels à `alerter()` = le nombre de tours.

### Solution

```python
def evacuation(p: Piece, silencieux: bool = True) -> int:
    """Simule l'évacuation complète et renvoie le nombre de tours."""
    tours = 0
    while p.alerter(silencieux):   # alerter() est appelé ET son résultat testé
        tours += 1
        if not silencieux:
            print(p)               # affichage de l'état à chaque tour
    return tours
```

### Points clés

- `alerter()` est appelé dans la condition du `while` : il s'exécute ET son résultat est testé en même temps.
- On incrémente `tours` *après* chaque tour réussi.
- Quand `alerter()` renvoie `False`, la boucle s'arrête sans incrémenter.

### Fonction de test

```python
def test_evacuation(silencieux=True):
    p1 = Piece(5, 7)
    p1.ajouter_sortie("N", 5)
    situations = [
        {"cases": {(0,3):3, (1,1):1, (3,2):5}, "attendu": 11},
        {"cases": {(0,3):4, (0,1):2, (3,4):3, (4,0):1, (4,3):2}, "attendu": 14},
        {"cases": {(0,3):1, (0,1):2, (3,4):1, (4,0):3, (4,3):5}, "attendu": 15},
    ]
    for s in situations:
        for c, nb in s["cases"].items():
            p1.ajouter_occupants(c[0], c[1], nb)
        nbT = evacuation(p1, silencieux)
        assert nbT == s["attendu"]
    print("Les tests sont validés.")
```

### Trace d'exécution sur un exemple simple

Pièce 1×2, 1 occupant en (0,0), sortie en (0,1) :

| Tour | Avant alerter() | alerter() renvoie | Après |
|---|---|---|---|
| 1 | [1, 0] | True (déplacement) | [0, 0] |
| — | [0, 0] | False (rien à déplacer) | Fin |

Résultat : `tours = 1`

---

## Question 3 — Compléter `ajouter_sortie`

### Énoncé

Modifier `ajouter_sortie(direction, position)` pour prendre en compte les directions `"S"` (sud) et `"E"` (est) en plus des directions existantes `"N"` et `"O"`.

### Code actuel (partiel)

```python
def ajouter_sortie(self, direction: str, position: int):
    if direction == "N":
        self.sorties.append((0, position))      # ligne 0, colonne = position
    elif direction == "O":
        self.sorties.append((position, 0))      # colonne 0, ligne = position
    # "S" et "E" non traités → à compléter
```

### Solution complète

```python
def ajouter_sortie(self, direction: str, position: int):
    """Ajoute une sortie dans la direction donnée à la position donnée."""
    if direction == "N":
        self.sorties.append((0, position))               # ligne 0, colonne = position
    elif direction == "O":
        self.sorties.append((position, 0))               # colonne 0, ligne = position
    elif direction == "S":
        self.sorties.append((self.i_max, position))      # ← AJOUT : dernière ligne
    elif direction == "E":
        self.sorties.append((position, self.j_max))      # ← AJOUT : dernière colonne
```

### Fonction de test

```python
def test_ajouter_sortie():
    p1 = Piece(5, 7)    # i_max=4, j_max=6
    p1.ajouter_sortie("N", 5)   # → (0, 5)
    n1 = randint(1, 5)
    p1.ajouter_sortie("S", n1)  # → (4, n1)
    n2 = randint(1, 5)
    p1.ajouter_sortie("E", n2)  # → (n2, 6)
    p1.ajouter_sortie("O", 1)   # → (1, 0)
    assert p1.sorties == [(0, 5), (4, n1), (n2, 6), (1, 0)]
    print("Les tests sont validés.")
```

---

## Question 4 — Corriger les bugs de `choix_sortie`

### Énoncé

Identifier l'erreur logique et la variable non définie dans `choix_sortie`, puis corriger pour qu'elle renvoie la sortie la plus proche.

### Code fourni (bugué)

```python
def choix_sortie(self, i: int, j: int) -> tuple:
    def distance_de_manhattan(destination):
        return abs(i - destination[0]) + abs(j - destination[1])
    assert len(self.sorties) > 0, "Aucune sortie"
    choix    = self.sorties[0]
    distance = distance_de_manhattan(choix)
    for k in range(1, len(self.sorties)):
        autre_sortie = self.sorties[k]
        if k < 0:              # ← BUG 1 : condition toujours fausse
            choix    = autre_sortie
            distance = d2      # ← BUG 2 : d2 non définie
    return choix
```

### Analyse du Bug 1 — Condition logiquement impossible

`for k in range(1, len(self.sorties))` fait varier `k` de **1** jusqu'à la longueur de la liste moins 1. `k` est donc toujours **≥ 1**. La condition `if k < 0` est *toujours fausse* — le corps du `if` ne s'exécute jamais. La boucle tourne mais ne fait rien d'utile.

**Conséquence :** la méthode renvoie toujours `self.sorties[0]`, quelle que soit la position. Tous les occupants se dirigent vers la première sortie uniquement.

**Correction :** remplacer `if k < 0` par une comparaison de distances : `if d2 < distance`

### Analyse du Bug 2 — Variable non définie

`distance = d2` utilise `d2` qui n'a jamais été initialisée. Si le `if` avait pu s'exécuter, Python aurait levé une `NameError: name 'd2' is not defined`.

**Correction :** calculer `d2 = distance_de_manhattan(autre_sortie)` avant le test.

### Code corrigé complet

```python
def choix_sortie(self, i: int, j: int) -> tuple:
    """Renvoie la sortie la plus proche de (i, j) selon la distance de Manhattan."""
    def distance_de_manhattan(destination):
        return abs(i - destination[0]) + abs(j - destination[1])

    assert len(self.sorties) > 0, "Aucune sortie"
    choix    = self.sorties[0]              # meilleur choix actuel
    distance = distance_de_manhattan(choix) # distance correspondante

    for k in range(1, len(self.sorties)):
        autre_sortie = self.sorties[k]
        d2 = distance_de_manhattan(autre_sortie)  # ← CORRECTION BUG 2
        if d2 < distance:                          # ← CORRECTION BUG 1
            choix    = autre_sortie
            distance = d2

    return choix
```

### Vérification manuelle des 6 cas de test

Sorties : `[(0,5), (4,1), (3,6), (1,0)]` dans une pièce 5×7

| Position | d→(0,5) | d→(4,1) | d→(3,6) | d→(1,0) | Sortie choisie |
|---|---|---|---|---|---|
| (0,3) | **2** | 6 | 6 | 4 | (0,5) ✓ |
| (0,1) | 4 | 4 | 8 | **2** | (1,0) ✓ |
| (1,2) | 4 | 4 | 6 | **2** | (1,0) ✓ |
| (3,4) | 4 | 4 | **2** | 6 | (3,6) ✓ |
| (4,0) | 9 | **1** | 7 | 3 | (4,1) ✓ |
| (4,3) | 6 | **2** | 4 | 6 | (4,1) ✓ |

**Note :** en cas d'égalité, la première sortie dans l'ordre de la liste est renvoyée (condition `<` strictement inférieur, pas `<=`).

### Fonction de test

```python
def test_choix_sortie():
    p1 = Piece(5, 7)
    p1.sorties = [(0, 5), (4, 1), (3, 6), (1, 0)]
    assert p1.choix_sortie(0, 3) == (0, 5)
    assert p1.choix_sortie(0, 1) == (1, 0)
    assert p1.choix_sortie(1, 2) == (1, 0)
    assert p1.choix_sortie(3, 4) == (3, 6)
    assert p1.choix_sortie(4, 0) == (4, 1)
    assert p1.choix_sortie(4, 3) == (4, 1)
    print("Les tests sont validés.")
```

---

## Pièges fréquents

### Piège 1 — Confondre (ligne, colonne) et (x, y)

Toutes les positions sont des tuples `(i, j)` où `i` est la **ligne** (vertical) et `j` est la **colonne** (horizontal). Pour une sortie au Sud d'une pièce de profondeur 5 : la ligne est `i_max = 4`, pas `j_max`. Inverser les deux fait placer les sorties sur le mauvais mur.

### Piège 2 — Double appel à alerter()

`while p.alerter(silencieux):` appelle `alerter()` *et* teste son résultat en même temps. Si on écrit `p.alerter()` dans le corps de la boucle ET dans la condition, on perd un tour à chaque itération.

### Piège 3 — Ne pas voir que le bug ne plante pas

Le code bugué de `choix_sortie` s'exécute sans erreur (la condition `if k < 0` est juste toujours fausse). Il faut **lire et analyser** le code, pas seulement l'exécuter. La pièce semble s'évacuer, mais vers la première sortie uniquement.

### Piège 4 — Identifier un seul bug au lieu de deux

L'énoncé demande explicitement d'identifier *l'erreur logique* **et** la *variable non définie*. Ce sont deux bugs distincts. À l'examen, mentionner les deux est indispensable pour obtenir tous les points.

---

## Stratégie de performance le jour J

**Ordre d'attaque recommandé :**

1. **Q1 en 3 minutes** — Une ligne : `return sum(sum(l) for l in self.grille)`. Tester immédiatement.
2. **Q2 en 5 minutes** — Trois lignes avec `while/alerter`. Tester avec `test_evacuation()`.
3. **Q3 en 5 minutes** — Deux `elif` supplémentaires. Tester avec `test_ajouter_sortie()`.
4. **Q4 en 10 minutes** — Lire ligne par ligne, identifier `k < 0` (Bug 1) et `d2` (Bug 2), corriger les deux. Tester avec `test_choix_sortie()`.
5. **Tester l'IHM** — Lancer `IHM_evacuation.py` et vérifier visuellement que tout fonctionne.

---

## Mini-exercices de vérification

### Exercice A — Distance de Manhattan

Calculer les distances depuis (2, 3) vers `[(0,5), (4,1), (3,6), (1,0)]` :

- (0,5) : |2−0| + |3−5| = 2+2 = **4**
- (4,1) : |2−4| + |3−1| = 2+2 = **4**
- (3,6) : |2−3| + |3−6| = 1+3 = **4**
- (1,0) : |2−1| + |3−0| = 1+3 = **4**

Toutes égales → `choix_sortie` renvoie la première : `(0, 5)`.

### Exercice B — Analyser une condition de boucle

Dans `for k in range(1, 4)`, `k` prend les valeurs 1, 2, 3. La condition `if k < 0` est toujours fausse → Bug 1.

### Exercice C — Coordonnées de sortie

Pour `Piece(8, 10)` → `i_max = 7`, `j_max = 9` :
- Sud, position 4 → `(7, 4)`
- Est, position 3 → `(3, 9)`

---

## Code complet corrigé — `simulation_evacuation.py`

```python
from random import randint, shuffle
from copy import deepcopy


class Piece:

    def __init__(self, profondeur: int, largeur: int):
        self.grille = [[0 for _ in range(largeur)] for _ in range(profondeur)]
        self.i_max = profondeur - 1
        self.j_max = largeur - 1
        self.capacite = profondeur * largeur * 5
        self.sorties = []

    def ajouter_occupants(self, i: int, j: int, nb: int):
        nb_add = min(nb, 5 - self.grille[i][j])
        if nb_add > 0:
            self.grille[i][j] = self.grille[i][j] + nb_add
        return nb_add

    def nb_occupants_restants(self) -> int:
        """Renvoie le nombre d'occupants restants dans la pièce."""
        return sum(sum(ligne) for ligne in self.grille)          # ← Q1

    def ajouter_sortie(self, direction: str, position: int):
        """Ajoute une sortie dans la direction donnée."""
        if direction == "N":
            self.sorties.append((0, position))
        elif direction == "O":
            self.sorties.append((position, 0))
        elif direction == "S":                                    # ← Q3
            self.sorties.append((self.i_max, position))
        elif direction == "E":                                    # ← Q3
            self.sorties.append((position, self.j_max))

    def choix_sortie(self, i: int, j: int) -> tuple:
        """Renvoie la sortie la plus proche de (i, j)."""
        def distance_de_manhattan(destination):
            return abs(i - destination[0]) + abs(j - destination[1])
        assert len(self.sorties) > 0, "Aucune sortie"
        choix    = self.sorties[0]
        distance = distance_de_manhattan(choix)
        for k in range(1, len(self.sorties)):
            autre_sortie = self.sorties[k]
            d2 = distance_de_manhattan(autre_sortie)             # ← Q4 : correction Bug 2
            if d2 < distance:                                    # ← Q4 : correction Bug 1
                choix    = autre_sortie
                distance = d2
        return choix

    def deplacer(self, i: int, j: int, nb: int, direction: str, silencieux: bool = True) -> int:
        d = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        nv_i, nv_j = i + d[direction][0], j + d[direction][1]
        nb_dep = min(nb, 5 - self.grille[nv_i][nv_j], self.grille[i][j])
        if nb_dep > 0:
            if not silencieux:
                print("déplacement de", nb_dep, "occupant(s) (", i, ",", j, ") vers", direction)
            self.grille[i][j] = self.grille[i][j] - nb_dep
            self.grille[nv_i][nv_j] = self.grille[nv_i][nv_j] + nb_dep
        return nb_dep

    def alerter(self, silencieux: bool = True) -> bool:
        old_grille = deepcopy(self.grille)
        modif = False
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if old_grille[i][j] > 0:
                    sortie_i, sortie_j = self.choix_sortie(i, j)
                    dx, dy = sortie_j - j, sortie_i - i
                    if dx == 0 and dy == 0:
                        if not silencieux:
                            print("évacuation d'un occupant (", i, ",", j, ")")
                        self.grille[i][j] = self.grille[i][j] - 1
                        nb_dep = 1
                    else:
                        mvt_possibles = []
                        if dx > 0:
                            mvt_possibles.append("E")
                        elif dx < 0 and j > 0:
                            mvt_possibles.append("O")
                        if dy > 0:
                            mvt_possibles.append("S")
                        elif dy < 0 and i > 0:
                            mvt_possibles.append("N")
                        shuffle(mvt_possibles)
                        nb_dep = self.deplacer(i, j, old_grille[i][j], mvt_possibles[0], silencieux)
                        if nb_dep == 0 and len(mvt_possibles) > 1:
                            nb_dep = self.deplacer(i, j, old_grille[i][j], mvt_possibles[1], silencieux)
                    if nb_dep > 0:
                        modif = True
        return modif

    def __str__(self) -> str:
        s = "  "
        for j in range(self.j_max + 1):
            s = s + ("P  " if (0, j) in self.sorties else "   ")
        s = s + "\n"
        for i in range(len(self.grille)):
            s = s + ("P" if (i, 0) in self.sorties else " ")
            s = s + str(self.grille[i])
            if i != 0 and i != self.i_max and (i, self.j_max) in self.sorties:
                s = s + "P\n"
            else:
                s = s + "\n"
        s = s + "  "
        for j in range(self.j_max + 1):
            s = s + ("P  " if (self.i_max, j) in self.sorties else "   ")
        return s + "\n"


def evacuation(p: Piece, silencieux: bool = True) -> int:
    """Simule l'évacuation complète et renvoie le nombre de tours."""
    tours = 0
    while p.alerter(silencieux):    # ← Q2
        tours += 1
        if not silencieux:
            print(p)
    return tours
```

## Récapitulatif — Les 4 réponses en un coup d'œil

```python
# Q1 — nb_occupants_restants (1 ligne)
return sum(sum(ligne) for ligne in self.grille)

# Q2 — evacuation (4 lignes)
tours = 0
while p.alerter(silencieux):
    tours += 1
    if not silencieux: print(p)
return tours

# Q3 — ajouter_sortie (2 elif à ajouter)
elif direction == "S":
    self.sorties.append((self.i_max, position))
elif direction == "E":
    self.sorties.append((position, self.j_max))

# Q4 — choix_sortie (2 corrections dans la boucle)
d2 = distance_de_manhattan(autre_sortie)   # ← AJOUTER cette ligne
if d2 < distance:                           # ← REMPLACER if k < 0
```
