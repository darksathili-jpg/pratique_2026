# Fiche NSI Terminale — Modélisation 3D et Programmation Orientée Objet
## BAC 2026 — Sujet n°9 — Partie pratique

**Matière :** Numérique et Sciences Informatiques (NSI)  
**Niveau :** Terminale — voie générale  
**Thème du programme :** Programmation orientée objet — classes, instances, méthodes  
**Durée de l'épreuve :** 1 heure  
**Fichiers fournis :** `Sommet.py`, `Face.py`, `Objet3D.py`, `main.py`

---

## Contexte général du sujet

Le sujet porte sur la manipulation d'objets 3D au format **OBJ**, un format de fichier texte très utilisé en modélisation 3D. Un fichier OBJ décrit une forme géométrique en listant ses sommets (points dans l'espace) et ses faces (surfaces reliant ces points).

Le sujet comporte cinq questions progressives :

1. Écrire la méthode `distance` dans la classe `Sommet`
2. Écrire la méthode `trouver_sommets_adjacents` dans la classe `Objet3D`
3. Écrire la fonction `estimation_impression` pour calculer un temps d'impression 3D
4. Construire et afficher une pyramide dans `main.py`
5. Analyser, corriger et améliorer la méthode `transformer`

---

## Partie 1 — Rappels : Programmation Orientée Objet

### Vocabulaire essentiel

| Terme | Définition |
|-------|-----------|
| **Classe** | Modèle (gabarit) décrivant la structure et les comportements d'un type d'objet |
| **Instance** | Un objet concret créé à partir d'une classe |
| **Attribut** | Variable appartenant à une instance (stockée via `self`) |
| **Méthode** | Fonction définie dans une classe, agissant sur l'instance via `self` |
| `__init__` | Constructeur — appelé automatiquement à la création d'une instance |
| `self` | Référence à l'instance courante — toujours premier paramètre d'une méthode |

### Principe fondamental de l'appel de méthode

```python
p.decrire()
# est équivalent à :
Point2D.decrire(p)
```

`self` reçoit automatiquement l'instance `p`. On ne passe jamais `self` explicitement lors de l'appel.

### Méthode recevant une autre instance en paramètre

```python
s1.est_adjacent(s2)
# Dans la méthode : self = s1, sommet = s2
```

Ce mécanisme est utilisé dans tout le sujet : une méthode de `Sommet` reçoit un autre `Sommet` en paramètre, et accède à ses coordonnées via `sommet.x`, `sommet.y`, `sommet.z`.

---

## Partie 2 — Les trois classes du sujet

### Classe Sommet (fichier Sommet.py)

**Attributs :** `x`, `y`, `z` (coordonnées entières du point dans l'espace 3D)

**Méthodes fournies :**

```python
def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

def est_adjacent(self, sommet):
    """
    Deux sommets sont adjacents si leurs coordonnées ne diffèrent
    que sur UN SEUL axe (ils sont reliés par une arête).
    """
    nb_changement = 0
    if self.x != sommet.x: nb_changement += 1
    if self.y != sommet.y: nb_changement += 1
    if self.z != sommet.z: nb_changement += 1
    return nb_changement == 1
```

**Méthode à écrire :** `distance(self, sommet)` → Q1

### Classe Face (fichier Face.py)

**Attributs :** `sommets` (liste d'entiers — indices des sommets formant la face, 1-indexés)

```python
class Face:
    def __init__(self, sommets):
        self.sommets = sommets
```

### Classe Objet3D (fichier Objet3D.py)

**Attributs :** `sommets` (liste d'objets `Sommet`), `faces` (liste d'objets `Face`), `nom` (chaîne)

**Méthodes fournies :**
- `ajouter_sommet(x, y, z)` : crée un `Sommet` et l'ajoute à `self.sommets`
- `ajouter_face(liste_sommets)` : crée une `Face` et l'ajoute à `self.faces`
- `afficher()` : affiche l'objet avec matplotlib (utilise `self.sommets[s-1]` car OBJ est 1-indexé)
- `__str__()` : représentation textuelle

**Méthodes à écrire / corriger :** `trouver_sommets_adjacents` (Q2), `transformer` (Q5 — buguée)

### Le format OBJ — structure d'un fichier

```
o cube            ← nom de l'objet
v 0.0 0.0 0.0    ← sommet 1 : coordonnées x y z
v 0.0 1.0 0.0    ← sommet 2
v 1.0 1.0 0.0    ← sommet 3
v 1.0 0.0 0.0    ← sommet 4
f 1 2 3 4        ← face reliant les sommets 1, 2, 3, 4
```

**Point critique :** Les indices dans les lignes `f` commencent à **1** (convention OBJ). Les listes Python commencent à **0**. D'où le `self.sommets[s-1]` dans `afficher()`.

---

## Question 1 — Méthode distance dans Sommet

### Énoncé

Écrire la méthode `distance(self, sommet)` dans la classe `Sommet`. Elle prend un objet `Sommet` en paramètre et renvoie la distance euclidienne entre les deux points (type `float`).

Formule :
$$d(A, B) = \sqrt{(x_A - x_B)^2 + (y_A - y_B)^2 + (z_A - z_B)^2}$$

Utiliser `math.sqrt` du module `math`.

### Démarche

1. `self` représente le point A, `sommet` représente le point B
2. Calculer `dx = self.x - sommet.x`, `dy = self.y - sommet.y`, `dz = self.z - sommet.z`
3. Calculer `dx**2 + dy**2 + dz**2`
4. Appliquer `math.sqrt(...)` et retourner le résultat

### Solution

```python
import math

def distance(self, sommet):
    dx = self.x - sommet.x
    dy = self.y - sommet.y
    dz = self.z - sommet.z
    return math.sqrt(dx**2 + dy**2 + dz**2)
```

### Fonction de test

```python
def test_distance():
    s1 = Sommet(0, 0, 0)
    s2 = Sommet(3, 4, 0)
    assert s1.distance(s2) == 5.0          # triangle 3-4-5 classique
    s3 = Sommet(1, 1, 1)
    s4 = Sommet(1, 1, 1)
    assert s3.distance(s4) == 0.0          # distance d'un point à lui-même
    s5 = Sommet(0, 0, 0)
    s6 = Sommet(1, 0, 0)
    assert s5.distance(s6) == 1.0          # arête unitaire
    print("Les tests sont validés.")

test_distance()
```

**Vérification mentale :** `Sommet(0,0,0)` et `Sommet(3,4,0)` → `√(9+16+0) = √25 = 5`. Le triangle 3-4-5 est le cas de vérification idéal.

---

## Question 2 — Méthode trouver_sommets_adjacents dans Objet3D

### Énoncé

Écrire la méthode `trouver_sommets_adjacents(self)` dans `Objet3D`. Elle renvoie un tuple `(sommet_a, sommet_b)` pour le premier couple adjacent trouvé, ou `None` si aucun couple n'est adjacent.

### Démarche — Parcourir tous les couples sans doublon

Pour parcourir tous les couples `(i, j)` avec `i < j` (évite les doublons et le couple `(i, i)`) :

```python
for i in range(len(self.sommets)):
    for j in range(i + 1, len(self.sommets)):
        # tester self.sommets[i] et self.sommets[j]
```

Dès qu'un couple adjacent est trouvé, le renvoyer immédiatement avec `return`. Si la double boucle se termine sans rien trouver, renvoyer `None`.

**Pourquoi `j = i + 1` et pas `j = 0` ?**
- `j = 0` testerait `(i, i)` : un sommet n'est pas adjacent à lui-même (0 changement)
- `j = 0` testerait `(0,1)` et `(1,0)` en doublon

### Solution

```python
def trouver_sommets_adjacents(self):
    for i in range(len(self.sommets)):
        for j in range(i + 1, len(self.sommets)):
            if self.sommets[i].est_adjacent(self.sommets[j]):
                return (self.sommets[i], self.sommets[j])
    return None
```

### Fonction de test

```python
def test_trouver_sommets_adjacents():
    objet = Objet3D()
    objet.ajouter_sommet(0, 0, 0)   # s1
    objet.ajouter_sommet(1, 0, 0)   # s2 — adjacent à s1 (seul x change)
    objet.ajouter_sommet(0, 1, 0)   # s3 — adjacent à s1 (seul y change)
    objet.ajouter_sommet(0, 0, 1)   # s4 — adjacent à s1 (seul z change)
    resultat = objet.trouver_sommets_adjacents()
    assert resultat is not None, "Devrait trouver un couple adjacent"
    assert len(resultat) == 2, "Doit renvoyer un tuple de 2 sommets"
    s_a, s_b = resultat
    assert s_a.est_adjacent(s_b), "Les sommets renvoyés doivent être adjacents"
    # Test cas sans adjacent
    objet2 = Objet3D()
    objet2.ajouter_sommet(0, 0, 0)
    objet2.ajouter_sommet(1, 1, 1)   # 2 différences → pas adjacent
    assert objet2.trouver_sommets_adjacents() is None
    print("Les tests sont validés.")

test_trouver_sommets_adjacents()
```

---

## Question 3 — Fonction estimation_impression

### Énoncé

Écrire la fonction `estimation_impression(volume, parametres)` dans `main.py`. Elle prend le volume réel d'un objet 3D (entier, en mm³) et un dictionnaire de paramètres d'imprimante. Elle renvoie le temps d'impression en secondes (float).

### Paramètres de l'imprimante

```python
parametres_imprimante = {
    'remplissage': 20,           # taux de remplissage en pourcentage (20 %)
    'vitesse_extrusion': 8       # vitesse d'impression en mm³/s
}
```

### Calcul en deux étapes

**Étape 1 — Volume d'impression :**
```
volume_impression = volume_réel × (taux_remplissage / 100)
```

**Étape 2 — Temps d'impression :**
```
temps = volume_impression / vitesse_extrusion
```

**Exemple chiffré :** cube de côté 10 mm → volume = 1000 mm³
- Volume d'impression = 1000 × 20 / 100 = **200 mm³**
- Temps = 200 / 8 = **25 secondes**

### Solution

```python
def estimation_impression(volume, parametres):
    volume_impression = volume * parametres['remplissage'] / 100
    temps = volume_impression / parametres['vitesse_extrusion']
    return temps
```

### Fonction de test

```python
def test_estimation_impression():
    params = {'remplissage': 20, 'vitesse_extrusion': 8}
    assert estimation_impression(1000, params) == 25.0
    assert estimation_impression(0, params) == 0.0
    params2 = {'remplissage': 100, 'vitesse_extrusion': 10}
    assert estimation_impression(500, params2) == 50.0
    print("Les tests sont validés.")

test_estimation_impression()
```

**Piège fréquent :** oublier de diviser par 100. Sans cela, le volume d'impression est 100× trop grand et le temps est absurde.

---

## Question 4 — Construire et afficher une pyramide

### Énoncé

Modifier `main.py` pour instancier et afficher la pyramide dont les coordonnées sont données dans la Figure 2 du sujet.

### Analyse de la figure

La pyramide a une **base carrée** et un **apex** au-dessus du centre :

| Indice OBJ | Coordonnées | Rôle |
|------------|-------------|------|
| 1 | (0, 0, 0) | Base — coin |
| 2 | (2, 0, 0) | Base — coin |
| 3 | (0, 2, 0) | Base — coin |
| 4 | (2, 2, 0) | Base — coin |
| 5 | (1, 1, 2) | Apex (sommet de la pyramide) |

**Structure :** 5 sommets + 5 faces (1 base carrée + 4 faces triangulaires).

### Solution complète — main.py

```python
from Objet3D import Objet3D

objet = Objet3D()

# 5 sommets : base carrée + apex
objet.ajouter_sommet(0, 0, 0)   # sommet 1
objet.ajouter_sommet(2, 0, 0)   # sommet 2
objet.ajouter_sommet(0, 2, 0)   # sommet 3
objet.ajouter_sommet(2, 2, 0)   # sommet 4
objet.ajouter_sommet(1, 1, 2)   # sommet 5 — apex

# 5 faces : 1 base carrée + 4 triangles latéraux
objet.ajouter_face([1, 2, 4, 3])   # base carrée
objet.ajouter_face([1, 2, 5])      # face avant
objet.ajouter_face([2, 4, 5])      # face droite
objet.ajouter_face([4, 3, 5])      # face arrière
objet.ajouter_face([3, 1, 5])      # face gauche

objet.afficher()
```

### Logique de construction des faces

Chaque face triangulaire latérale relie deux sommets consécutifs de la base à l'apex (indice 5). Les 4 faces triangulaires tournent autour de la base :
- Avant : 1-2-5 (bord avant de la base → apex)
- Droite : 2-4-5 (bord droit → apex)
- Arrière : 4-3-5 (bord arrière → apex)
- Gauche : 3-1-5 (bord gauche → apex)

---

## Question 5 — Corriger et améliorer transformer

### Code fourni (bugué)

```python
def transformer(self, rapport):
    sommets = []
    for sommet in self.sommets:
        sommets.append(
            Sommet(sommet.x*rapport, sommet.y*rapport, sommet.z*rapport))
    self.sommet = sommets   # ← BUG : "sommet" sans "s"
```

### Identification du bug

La ligne `self.sommet = sommets` crée un **nouvel attribut** `sommet` (sans **s**) au lieu de modifier l'attribut existant `self.sommets` (avec **s**).

Conséquences :
- L'attribut `self.sommets` **reste inchangé** — la transformation n'est pas appliquée
- Un attribut fantôme `self.sommet` est créé inutilement
- Python ne lève aucune erreur — le bug est silencieux

**Détection :** `print(vars(objet))` après appel révèle les deux attributs coexistants.

### Amélioration demandée

Au-delà de la correction de la faute de frappe, le sujet demande de changer le comportement : la méthode doit **renvoyer un nouvel objet** sans modifier l'instance d'origine.

Ce patron de conception (créer un objet transformé au lieu de muter l'existant) est appelé **objet immuable** en POO. Il facilite le débogage et permet d'appliquer plusieurs transformations indépendantes.

### Solution corrigée et améliorée

```python
def transformer(self, rapport):
    """
    Renvoie un nouvel Objet3D dont tous les sommets sont multipliés par rapport.
    L'objet courant (self) n'est PAS modifié.
    """
    nouvel_objet = Objet3D()
    for sommet in self.sommets:
        nouvel_objet.ajouter_sommet(
            sommet.x * rapport,
            sommet.y * rapport,
            sommet.z * rapport)
    for face in self.faces:
        nouvel_objet.ajouter_face(face.sommets)
    return nouvel_objet
```

**Pourquoi copier les faces ?** Les indices dans les faces restent valides car les sommets sont dans le même ordre dans les deux objets. Seules les coordonnées changent, pas les relations entre sommets.

### Fonction de test

```python
def test_transformer():
    # Construction de la pyramide
    pyramide = Objet3D()
    pyramide.ajouter_sommet(0, 0, 0); pyramide.ajouter_sommet(2, 0, 0)
    pyramide.ajouter_sommet(0, 2, 0); pyramide.ajouter_sommet(2, 2, 0)
    pyramide.ajouter_sommet(1, 1, 2)
    pyramide.ajouter_face([1, 2, 4, 3]); pyramide.ajouter_face([1, 2, 5])
    pyramide.ajouter_face([2, 4, 5]); pyramide.ajouter_face([4, 3, 5])
    pyramide.ajouter_face([3, 1, 5])

    grande = pyramide.transformer(2)

    # L'original ne doit pas être modifié
    assert pyramide.sommets[0].x == 0
    assert pyramide.sommets[1].x == 2

    # Le nouvel objet doit avoir les coordonnées doublées
    assert grande.sommets[0].x == 0    # 0 × 2 = 0
    assert grande.sommets[1].x == 4    # 2 × 2 = 4
    assert grande.sommets[4].z == 4    # 2 × 2 = 4 (apex)

    # Le nombre de faces doit être conservé
    assert len(grande.faces) == len(pyramide.faces)
    print("Les tests sont validés.")

test_transformer()
```

---

## Code complet corrigé — Sommet.py

```python
import math

class Sommet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def est_adjacent(self, sommet):
        nb_changement = 0
        if self.x != sommet.x: nb_changement += 1
        if self.y != sommet.y: nb_changement += 1
        if self.z != sommet.z: nb_changement += 1
        return nb_changement == 1

    def distance(self, sommet):        # Q1 — ajoutée
        dx = self.x - sommet.x
        dy = self.y - sommet.y
        dz = self.z - sommet.z
        return math.sqrt(dx**2 + dy**2 + dz**2)


# Test Q1
s1 = Sommet(0, 0, 0)
s2 = Sommet(3, 4, 0)
assert s1.distance(s2) == 5.0
```

## Code complet corrigé — Objet3D.py (extraits modifiés)

```python
def trouver_sommets_adjacents(self):    # Q2 — ajoutée
    for i in range(len(self.sommets)):
        for j in range(i + 1, len(self.sommets)):
            if self.sommets[i].est_adjacent(self.sommets[j]):
                return (self.sommets[i], self.sommets[j])
    return None

def transformer(self, rapport):          # Q5 — corrigée
    nouvel_objet = Objet3D()
    for sommet in self.sommets:
        nouvel_objet.ajouter_sommet(
            sommet.x * rapport,
            sommet.y * rapport,
            sommet.z * rapport)
    for face in self.faces:
        nouvel_objet.ajouter_face(face.sommets)
    return nouvel_objet
```

## Code complet corrigé — main.py

```python
from Objet3D import Objet3D

parametres_imprimante = {'remplissage': 20, 'vitesse_extrusion': 8}

def volume_cube(cube):
    a, b = cube.trouver_sommets_adjacents()
    taille_cote = a.distance(b)
    return taille_cote ** 3

def estimation_impression(volume, parametres):  # Q3
    volume_impression = volume * parametres['remplissage'] / 100
    return volume_impression / parametres['vitesse_extrusion']

# Q4 — pyramide
objet = Objet3D()
objet.ajouter_sommet(0, 0, 0); objet.ajouter_sommet(2, 0, 0)
objet.ajouter_sommet(0, 2, 0); objet.ajouter_sommet(2, 2, 0)
objet.ajouter_sommet(1, 1, 2)
objet.ajouter_face([1, 2, 4, 3])
objet.ajouter_face([1, 2, 5]); objet.ajouter_face([2, 4, 5])
objet.ajouter_face([4, 3, 5]); objet.ajouter_face([3, 1, 5])
objet.afficher()

# Q5 — transformation
grande_pyramide = objet.transformer(2)
grande_pyramide.afficher()
```

---

## Pièges fréquents

### Piège 1 — self.sommet vs self.sommets (une lettre, tout change)

```python
# FAUX — crée un attribut fantôme "sommet" (sans s)
self.sommet = sommets

# JUSTE — modifie l'attribut existant "sommets" (avec s)
self.sommets = sommets
```

Python ne lève aucune erreur dans les deux cas. Pour détecter ce type de bug : `print(vars(objet))`.

### Piège 2 — Indices OBJ commencent à 1, Python à 0

```python
# Dans afficher() — le "-1" est indispensable
self.sommets[s - 1].x    # OBJ : indice 1 → Python : indice 0
```

Oublier le `-1` produit soit un rendu incorrect, soit une `IndexError` sur le dernier sommet.

### Piège 3 — Boucle imbriquée : j doit partir de i+1

```python
# FAUX — teste (i, i) et les doublons
for j in range(len(self.sommets)):

# JUSTE — n² paires uniques, pas de doublon
for j in range(i + 1, len(self.sommets)):
```

### Piège 4 — Taux de remplissage en pourcentage, pas en coefficient

```python
# FAUX — multiplie par 20 au lieu de 0.20
volume_impression = volume * parametres['remplissage']

# JUSTE — divise par 100 pour obtenir le coefficient
volume_impression = volume * parametres['remplissage'] / 100
```

### Piège 5 — transformer sans return renvoie None

```python
# FAUX — modifie self, ne renvoie rien (None)
self.sommets = nouveaux_sommets

# JUSTE — crée un nouvel objet et le renvoie
return nouvel_objet
```

Si `transformer` ne contient pas `return nouvel_objet`, alors `grande = objet.transformer(2)` attribue `None` à `grande`. Toute tentative d'accès à `grande.sommets` provoquera une `AttributeError`.

---

## Astuces de vérification

### Inspecter les attributs d'une instance

```python
print(vars(objet))
# Affiche : {'sommets': [...], 'faces': [...], 'nom': ''}
# Permet de détecter un attribut fantôme comme 'sommet'
```

### Cas de test essentiels pour distance

```python
# Triangle 3-4-5 (Pythagore)
assert Sommet(0,0,0).distance(Sommet(3,4,0)) == 5.0

# Distance nulle
assert Sommet(1,1,1).distance(Sommet(1,1,1)) == 0.0

# Arête unitaire
assert Sommet(0,0,0).distance(Sommet(1,0,0)) == 1.0
```

### Cas de test pour est_adjacent

| Couple | Résultat | Raison |
|--------|----------|--------|
| (0,0,0) et (1,0,0) | `True` | 1 différence (x) |
| (0,0,0) et (1,1,0) | `False` | 2 différences (x, y) |
| (2,3,4) et (2,3,5) | `True` | 1 différence (z) |
| (0,0,0) et (0,0,0) | `False` | 0 différence |

### Vérifier que transformer ne modifie pas l'original

```python
x_avant = pyramide.sommets[1].x      # mémoriser une valeur
grande = pyramide.transformer(2)
assert pyramide.sommets[1].x == x_avant   # l'original est intact
assert grande.sommets[1].x == x_avant * 2  # le nouvel objet est transformé
```

---

## Mini-exercices de calcul mental

### Exercice A — Distance 3D

Sans Python, calculer la distance entre ces couples :

| Couple | Calcul | Résultat |
|--------|--------|----------|
| (0,0,0) et (0,0,5) | √(0+0+25) | **5.0** |
| (1,1,1) et (4,5,1) | √(9+16+0) | **5.0** |
| (0,0,0) et (1,1,1) | √(1+1+1) | **√3 ≈ 1.732** |

### Exercice B — Adjacence

| Couple | Adjacents ? |
|--------|-------------|
| (0,0,0) et (1,0,0) | ✅ Oui — seul x change |
| (0,0,0) et (1,1,0) | ❌ Non — x et y changent |
| (2,3,4) et (2,3,5) | ✅ Oui — seul z change |
| (0,0,0) et (0,0,0) | ❌ Non — 0 différence |

### Exercice C — temps d'impression mental

Cube de côté 5 mm, remplissage 40 %, vitesse 8 mm³/s. Combien de secondes ?
- Volume réel = 5³ = **125 mm³**
- Volume d'impression = 125 × 40 / 100 = **50 mm³**
- Temps = 50 / 8 = **6.25 secondes**

---

## Récapitulatif — Points clés à retenir

| Notion | Retenir |
|--------|---------|
| Format OBJ | Indices des faces commencent à 1 → `sommets[s-1]` en Python |
| `distance` | Formule euclidienne 3D avec `math.sqrt` — vérifier avec le 3-4-5 |
| `est_adjacent` | 1 seule coordonnée différente → adjacent ; 0 ou 2+ → non adjacent |
| Boucles imbriquées | Boucle interne de `i+1` à la fin pour éviter doublons et auto-comparaison |
| `estimation_impression` | Remplissage en % → diviser par 100 ; temps = volume / vitesse |
| Pyramide | 5 sommets + 5 faces (1 base carrée + 4 triangles latéraux) |
| Bug `transformer` | `self.sommet` ≠ `self.sommets` — faute de frappe silencieuse |
| `transformer` corrigée | Créer un `Objet3D` vide, peupler, **`return`** — ne jamais modifier `self` |

---

*Lycée Antoine Watteau — DarkSATHI Li — BAC NSI 2026 — Sujet n°9*
