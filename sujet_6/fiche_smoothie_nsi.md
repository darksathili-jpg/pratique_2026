# Fiche de révision — BAC NSI 2026 — Sujet n°6 : Boutique Smoothie

**Niveau :** Terminale NSI  
**Thèmes :** Programmation Orientée Objet · Méthodes · Listes · Débogage  
**Source :** Épreuve pratique BAC NSI 2026, sujet n°6  
**Lycée Antoine Watteau — DarkSATHI Li**

---

## Contexte du sujet

La maison des lycéens (MDL) d'un lycée souhaite proposer des recettes de smoothies comme alternative aux sodas. Les fruits ne sont pas toujours tous disponibles, donc certaines recettes ne sont pas toujours réalisables. Les élèves de NSI doivent concevoir un programme Python permettant de gérer une carte dynamique de smoothies.

Le programme repose sur une classe `Boutique_smoothie` qui :
- mémorise les fruits disponibles du jour,
- connaît toutes les recettes,
- peut déterminer quels smoothies sont réalisables,
- peut proposer des alternatives proches quand une recette est impossible.

---

## Rappels de cours — Programmation Orientée Objet

### Classe, instance, attribut, méthode

Une **classe** est un modèle qui regroupe des données (attributs) et des fonctions (méthodes) qui opèrent sur ces données. Une **instance** est un objet concret créé à partir de ce modèle.

Le premier paramètre de chaque méthode est toujours `self`. Il désigne l'instance elle-même et permet d'accéder à ses attributs depuis l'intérieur de la classe.

```python
class Panier:
    def __init__(self, fruits):
        self.fruits = fruits          # attribut de l'instance

    def contient(self, fruit):        # méthode
        return fruit in self.fruits   # accès via self

p = Panier(["Mangue", "Kiwi"])
print(p.contient("Kiwi"))   # True
print(p.contient("Fraise")) # False
```

### L'opérateur `in`

Pour vérifier si un élément est présent dans une liste :

```python
fruits_dispo = ["Mangue", "Ananas", "Banane"]

"Mangue" in fruits_dispo   # True
"Kiwi"   in fruits_dispo   # False
```

Pour vérifier que **tous** les éléments d'une liste sont dans une autre, on utilise `all()` :

```python
recette = ["Mangue", "Ananas", "Banane"]
dispo   = ["Mangue", "Ananas", "Banane", "Kiwi"]

all(fruit in dispo for fruit in recette)   # True
```

### Compter les éléments communs entre deux listes

```python
def nb_communs(liste1, liste2):
    compteur = 0
    for element in liste1:
        if element in liste2:
            compteur += 1
    return compteur

# Version compacte équivalente :
sum(1 for f in liste1 if f in liste2)
```

---

## Les données du sujet

### La classe `Boutique_smoothie`

```python
class Boutique_smoothie:
    def __init__(self, liste_fruits_disponibles):
        self.liste_fruits_disponibles = liste_fruits_disponibles
        self.db_smoothies = {
            "Tropical":        ["Mangue", "Ananas", "Banane"],
            "Rouge":           ["Fraise", "Framboise", "Cerise"],
            "Vert":            ["Kiwi", "Pomme verte", "Menthe"],
            "Agrume":          ["Orange", "Citron", "Pamplemousse"],
            "Exotique":        ["Papaye", "Fruit de la passion", "Noix de coco"],
            "Tropical citron": ["Mangue", "Ananas", "Citron"],
            "Rouge kiwi":      ["Fraise", "Framboise", "Kiwi"],
            "Exotique rouge":  ["Papaye", "Fraise", "Fruit de la passion"],
            "Vert citron":     ["Kiwi", "Pomme verte", "Citron"],
            "Soleil couchant": ["Mangue", "Fraise", "Pamplemousse"],
        }
```

- `self.liste_fruits_disponibles` : liste des fruits disponibles ce jour-là.
- `self.db_smoothies` : dictionnaire dont les clés sont les noms des smoothies et les valeurs sont des listes de trois fruits.

### La carte complète des recettes

| Smoothie | Fruit 1 | Fruit 2 | Fruit 3 |
|---|---|---|---|
| Tropical | Mangue | Ananas | Banane |
| Rouge | Fraise | Framboise | Cerise |
| Vert | Kiwi | Pomme verte | Menthe |
| Agrume | Orange | Citron | Pamplemousse |
| Exotique | Papaye | Fruit de la passion | Noix de coco |
| Tropical citron | Mangue | Ananas | Citron |
| Rouge kiwi | Fraise | Framboise | Kiwi |
| Exotique rouge | Papaye | Fraise | Fruit de la passion |
| Vert citron | Kiwi | Pomme verte | Citron |
| Soleil couchant | Mangue | Fraise | Pamplemousse |

### Les méthodes de la classe

| Méthode | Rôle | Statut dans le sujet |
|---|---|---|
| `smoothie_possible(nom)` | Vérifie si un smoothie est réalisable | À compléter (Q1) |
| `liste_smoothies_possibles()` | Renvoie la liste des smoothies faisables | À compléter (Q2) |
| `score_proximite(nom1, nom2)` | Compte les fruits communs entre deux smoothies | Fournie — à tester (Q3) |
| `plus_proche_possible(nom_ref)` | Renvoie le smoothie possible le plus proche | Fournie mais buguée (Q4) |
| `affichage_possibles()` | Affiche les smoothies faisables et les alternatives | Fournie (Q5) |

---

## Question 1 — `smoothie_possible`

### Énoncé

Écrire la méthode `smoothie_possible(self, nom_smoothie)` qui prend en paramètre le nom d'un smoothie et renvoie `True` si ce smoothie peut être préparé avec les fruits disponibles, `False` sinon. Un smoothie est possible si et seulement si chacun de ses fruits figure dans `self.liste_fruits_disponibles`.

### Exemple attendu

```python
b = Boutique_smoothie(["Mangue", "Pamplemousse", "Ananas", "Banane"])
b.smoothie_possible("Tropical")       # True  — Mangue, Ananas, Banane tous présents
b.smoothie_possible("Soleil couchant") # False — Fraise absente
```

### Méthode de résolution

1. Récupérer la liste des fruits de la recette : `recette = self.db_smoothies[nom_smoothie]`
2. Pour chaque fruit de la recette, vérifier s'il est dans `self.liste_fruits_disponibles`
3. Dès qu'un fruit est absent, renvoyer `False` immédiatement (retour anticipé)
4. Si la boucle se termine sans trouver de fruit manquant, renvoyer `True`

### Solution

```python
def smoothie_possible(self, nom_smoothie):
    """Renvoie True si le smoothie peut être préparé, False sinon."""
    recette = self.db_smoothies[nom_smoothie]
    for fruit in recette:
        if fruit not in self.liste_fruits_disponibles:
            return False   # un fruit manque → impossible
    return True             # tous les fruits sont disponibles
```

### Fonction de test

```python
def test_smoothie_possible():
    b = Boutique_smoothie(["Mangue", "Ananas", "Banane", "Fraise", "Citron"])
    # Tropical = Mangue + Ananas + Banane → tous présents
    assert b.smoothie_possible("Tropical") == True
    # Rouge = Fraise + Framboise + Cerise → Framboise et Cerise absentes
    assert b.smoothie_possible("Rouge") == False
    # Tropical citron = Mangue + Ananas + Citron → tous présents
    assert b.smoothie_possible("Tropical citron") == True
    # Agrume = Orange + Citron + Pamplemousse → Orange et Pamplemousse absents
    assert b.smoothie_possible("Agrume") == False
    print("Les tests sont validés.")

test_smoothie_possible()
```

### Points clés à retenir

- Le `return True` doit se trouver **après** la boucle, pas à l'intérieur. Si on le mettait dans la boucle, la fonction renverrait `True` dès le premier fruit trouvé, sans vérifier les autres.
- Le retour anticipé `return False` à l'intérieur de la boucle est efficace : dès qu'un fruit manque, inutile de continuer.

---

## Question 2 — `liste_smoothies_possibles`

### Énoncé

Écrire la méthode `liste_smoothies_possibles(self)` qui ne prend pas de paramètre (hormis `self`) et renvoie la liste de tous les noms de smoothies réalisables avec les fruits disponibles. La méthode doit réutiliser `smoothie_possible`.

### Méthode de résolution

1. Créer une liste vide `possibles`
2. Parcourir tous les noms de smoothies avec `for nom in self.db_smoothies`
3. Pour chaque nom, appeler `self.smoothie_possible(nom)`
4. Si le résultat est `True`, ajouter le nom à `possibles`
5. Renvoyer `possibles`

### Solution

```python
def liste_smoothies_possibles(self):
    """Renvoie la liste des smoothies réalisables."""
    possibles = []
    for nom in self.db_smoothies:
        if self.smoothie_possible(nom):
            possibles.append(nom)
    return possibles

# Version compacte équivalente (compréhension de liste) :
# return [nom for nom in self.db_smoothies if self.smoothie_possible(nom)]
```

### Fonction de test

```python
def test_liste_smoothies_possibles():
    b1 = Boutique_smoothie(["Mangue", "Ananas", "Banane", "Fraise", "Citron"])
    assert b1.liste_smoothies_possibles() == ["Tropical", "Tropical citron"]

    b2 = Boutique_smoothie(["Fraise", "Framboise", "Kiwi", "Pomme verte", "Citron"])
    assert b2.liste_smoothies_possibles() == ["Rouge kiwi", "Vert citron"]

    b3 = Boutique_smoothie(["Orange", "Mangue", "Papaye"])
    assert b3.liste_smoothies_possibles() == []

    print("Les tests sont validés.")

test_liste_smoothies_possibles()
```

### Points clés à retenir

- Principe fondamental de la POO : chaque méthode a une responsabilité précise. `liste_smoothies_possibles` délègue entièrement le test à `smoothie_possible`.
- Si on corrige `smoothie_possible` plus tard, `liste_smoothies_possibles` en bénéficie automatiquement.
- L'ordre de la liste renvoyée suit l'ordre d'insertion du dictionnaire `db_smoothies`.

---

## Question 3 — Tester `score_proximite`

### Énoncé

La méthode `score_proximite(self, nom1, nom2)` est fournie. Elle renvoie le nombre de fruits communs entre deux smoothies. Compléter `test_score_proximite` avec des tests pertinents.

### Code fourni

```python
def score_proximite(self, nom1, nom2):
    """Renvoie le nombre de fruits communs entre deux smoothies."""
    nb = 0
    fruits1 = self.db_smoothies[nom1]
    fruits2 = self.db_smoothies[nom2]
    for fruit in fruits1:
        if fruit in fruits2:
            nb += 1
    return nb
```

### Calculs de scores à connaître

| Smoothie 1 | Smoothie 2 | Fruits communs | Score |
|---|---|---|---|
| Tropical (Mangue, Ananas, Banane) | Tropical citron (Mangue, Ananas, Citron) | Mangue, Ananas | **2** |
| Tropical (Mangue, Ananas, Banane) | Rouge (Fraise, Framboise, Cerise) | aucun | **0** |
| Tropical (Mangue, Ananas, Banane) | Tropical (Mangue, Ananas, Banane) | tous | **3** |
| Rouge kiwi (Fraise, Framboise, Kiwi) | Vert citron (Kiwi, Pomme verte, Citron) | Kiwi | **1** |
| Exotique (Papaye, Fruit de la passion, Noix de coco) | Exotique rouge (Papaye, Fraise, Fruit de la passion) | Papaye, Fruit de la passion | **2** |

### Fonction de test complète

```python
def test_score_proximite():
    b = Boutique_smoothie([])   # les fruits dispo n'importent pas pour ce test
    # Score = 2 : Mangue et Ananas en commun
    assert b.score_proximite("Tropical", "Tropical citron") == 2
    # Score = 0 : aucun fruit en commun
    assert b.score_proximite("Tropical", "Rouge") == 0
    # Score = 3 : smoothie identique à lui-même
    assert b.score_proximite("Tropical", "Tropical") == 3
    # Score = 1 : seul Kiwi en commun
    assert b.score_proximite("Rouge kiwi", "Vert citron") == 1
    # Score = 2 : Papaye et Fruit de la passion en commun
    assert b.score_proximite("Exotique", "Exotique rouge") == 2
    # Commutativité : score(A, B) == score(B, A)
    assert b.score_proximite("Soleil couchant", "Tropical citron") == b.score_proximite("Tropical citron", "Soleil couchant")
    print("Les tests sont validés.")

test_score_proximite()
```

### Points clés à retenir

- Le score est **commutatif** : `score(A, B) == score(B, A)`. C'est une propriété mathématique intéressante à tester.
- Le score maximum pour deux smoothies différents est 2 (ils partagent au plus 2 fruits sur 3, sinon ce serait la même recette).
- Le score d'un smoothie avec lui-même est toujours 3.

---

## Question 4 — Analyser et corriger `plus_proche_possible`

### Énoncé

Observer avec `test_plus_proche_possible` que le smoothie renvoyé n'est pas le bon. Identifier le problème, proposer une démarche de résolution et la mettre en œuvre.

### Code fourni (bugué)

```python
def plus_proche_possible(self, nom_smoothie_ref):
    max_communs = 0
    smoothie_proche = None
    for nom_smoothie in self.db_smoothies:           # ← BUG : tous les smoothies
        nb_communs = self.score_proximite(nom_smoothie_ref, nom_smoothie)
        if nb_communs > max_communs:
            max_communs = nb_communs
            smoothie_proche = nom_smoothie
    return smoothie_proche
```

### Analyse du bug

**Symptôme :** avec la boutique `["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"]`, `plus_proche_possible("Tropical")` renvoie `"Tropical"` au lieu de `"Tropical citron"`.

**Cause :** la boucle parcourt `self.db_smoothies`, c'est-à-dire **tous** les smoothies de la carte, y compris :

1. Des smoothies non réalisables (manque de fruits)
2. Le smoothie de référence lui-même

Or, `score_proximite("Tropical", "Tropical")` renvoie **3** — un smoothie partage forcément tous ses fruits avec lui-même. Ce score de 3 est imbattable, donc la fonction renvoie toujours le smoothie de référence lui-même.

### Trace d'exécution du bug

| Candidat | Score vs Tropical | Possible ? | Version buguée | Version corrigée |
|---|---|---|---|---|
| Tropical | **3** | Oui | Retenu (max = 3) | Exclu (c'est la référence) |
| Rouge | 0 | Non | Ignoré | Ignoré (non possible) |
| Tropical citron | 2 | Oui | Ignoré (3 > 2) | Retenu (max = 2) |
| Vert citron | 0 | Oui | Ignoré | Ignoré (0 < 2) |
| … | … | … | … | … |

### Les deux corrections nécessaires

1. **Remplacer `self.db_smoothies` par `self.liste_smoothies_possibles()`** — on ne propose comme alternative que des smoothies effectivement réalisables.
2. **Exclure le smoothie de référence lui-même** — on cherche une *alternative*, pas le smoothie original.

### Solution corrigée

```python
def plus_proche_possible(self, nom_smoothie_ref):
    """Version corrigée : cherche parmi les smoothies possibles,
    en excluant le smoothie de référence lui-même."""
    max_communs = 0
    smoothie_proche = None
    for nom_smoothie in self.liste_smoothies_possibles():    # correction 1
        if nom_smoothie == nom_smoothie_ref:                 # correction 2
            continue                                         # on exclut le smoothie lui-même
        nb_communs = self.score_proximite(nom_smoothie_ref, nom_smoothie)
        if nb_communs > max_communs:
            max_communs = nb_communs
            smoothie_proche = nom_smoothie
    return smoothie_proche
```

### Fonction de test

```python
def test_plus_proche_possible():
    b = Boutique_smoothie(
        ["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"])
    # Tropical → Tropical citron (2 fruits communs : Mangue, Ananas)
    assert b.plus_proche_possible("Tropical") == "Tropical citron"
    # Exotique : aucun smoothie possible ne partage de fruits avec lui
    assert b.plus_proche_possible("Exotique") is None
    # Agrume → premier smoothie avec Citron en commun
    assert b.plus_proche_possible("Agrume") in ["Vert citron", "Tropical citron"]
    print("Les tests sont validés.")

test_plus_proche_possible()
```

### Cas `None`

Quand aucun smoothie possible ne partage de fruit avec le smoothie demandé, `max_communs` reste à 0 et `smoothie_proche` reste à `None`. La fonction renvoie correctement `None`.

### Points clés à retenir

- Une fonction qui cherche un maximum dans une collection doit être précise sur **quelle collection** elle parcourt.
- Le score d'un smoothie avec lui-même est toujours maximal (3) — il faut donc toujours l'exclure explicitement.
- Il faut gérer le cas `None` dans les fonctions appelantes (ne pas afficher « essayez None »).

---

## Question 5 — Mise en situation complète

### Énoncé

Créer une boutique avec : Mangue, Ananas, Banane, Fraise, Citron, Kiwi, Pomme verte. Utiliser `affichage_possibles()` pour déterminer quel smoothie sera proposé si un client souhaite un smoothie « Agrume ».

### Analyse manuelle des smoothies possibles

| Smoothie | Vérification | Possible ? |
|---|---|---|
| Tropical | Mangue ✓, Ananas ✓, Banane ✓ | **Oui** |
| Rouge | Fraise ✓, Framboise ✗ | Non |
| Vert | Kiwi ✓, Pomme verte ✓, Menthe ✗ | Non |
| Agrume | Orange ✗ | Non |
| Exotique | Papaye ✗ | Non |
| Tropical citron | Mangue ✓, Ananas ✓, Citron ✓ | **Oui** |
| Rouge kiwi | Fraise ✓, Framboise ✗ | Non |
| Exotique rouge | Papaye ✗ | Non |
| Vert citron | Kiwi ✓, Pomme verte ✓, Citron ✓ | **Oui** |
| Soleil couchant | Mangue ✓, Fraise ✓, Pamplemousse ✗ | Non |

Smoothies possibles : **Tropical**, **Tropical citron**, **Vert citron**.

### Alternative pour « Agrume »

Agrume = Orange, Citron, Pamplemousse.

| Smoothie possible | Fruits communs avec Agrume | Score |
|---|---|---|
| Tropical | aucun | 0 |
| Tropical citron | Citron | **1** |
| Vert citron | Citron | **1** |

Deux smoothies ont le même score. L'énoncé précise : « en cas d'égalité, retourner le premier trouvé ». Le dictionnaire étant parcouru dans l'ordre d'insertion, **Tropical citron** apparaît avant **Vert citron**.

**Réponse : si un client demande un smoothie Agrume, la boutique proposera Tropical citron.**

### Code complet fonctionnel

```python
boutique = Boutique_smoothie(
    ["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"]
)
boutique.affichage_possibles()
```

**Sortie attendue :**

```
Smoothies possibles avec les fruits disponibles :
  Tropical
  Tropical citron
  Vert citron

Alternative aux autres smoothies :
  Pour le smoothie Rouge, essayez Tropical citron.
  Pour le smoothie Vert, essayez Vert citron.
  Pour le smoothie Agrume, essayez Tropical citron.
  Pour le smoothie Exotique, aucun smoothie proche disponible.
  Pour le smoothie Rouge kiwi, essayez Tropical citron.
  Pour le smoothie Exotique rouge, essayez Tropical citron.
  Pour le smoothie Soleil couchant, essayez Tropical citron.
```

---

## Pièges fréquents

### Piège 1 — Oublier `self` dans les méthodes

Toute méthode doit avoir `self` comme premier paramètre. Pour accéder aux attributs depuis l'intérieur de la classe, il faut toujours écrire `self.attribut`. Pour appeler une autre méthode : `self.smoothie_possible(nom)`, pas `smoothie_possible(nom)`.

### Piège 2 — Chercher dans tous les smoothies plutôt que dans les possibles

C'est exactement le bug de la Question 4. Si on cherche le « plus proche » parmi `self.db_smoothies`, on inclut des smoothies non réalisables — et le smoothie de référence lui-même avec un score de 3, imbattable. Il faut toujours restreindre la recherche à `self.liste_smoothies_possibles()`.

### Piège 3 — Placer `return True` à l'intérieur de la boucle dans `smoothie_possible`

Le `return True` ne doit être atteint qu'après avoir parcouru toute la recette sans trouver de fruit manquant. Le placer dans la boucle provoquerait un retour dès le premier fruit trouvé — ce qui ne garantit pas que les autres sont présents.

### Piège 4 — Ne pas gérer le cas `None`

Quand aucun smoothie possible ne partage de fruit avec un smoothie demandé, `plus_proche_possible` renvoie `None`. Il faut tester `if proche is not None:` avant d'afficher l'alternative — sinon on affiche « essayez None » au client.

---

## Mini-exercices de vérification

### Exercice A — Calcul de score à la main

Calculer `score_proximite("Soleil couchant", "Tropical citron")`.

- Soleil couchant = Mangue, Fraise, Pamplemousse
- Tropical citron = Mangue, Ananas, Citron
- Fruit commun : Mangue uniquement

**Réponse : score = 1**

### Exercice B — Smoothies possibles

Avec uniquement Fraise, Framboise, Kiwi et Citron, quels smoothies sont possibles ?

| Smoothie | Vérification | Possible ? |
|---|---|---|
| Tropical | Mangue ✗ | Non |
| Rouge | Cerise ✗ | Non |
| Vert | Pomme verte ✗ | Non |
| Agrume | Orange ✗ | Non |
| Exotique | Papaye ✗ | Non |
| Tropical citron | Mangue ✗ | Non |
| **Rouge kiwi** | Fraise ✓, Framboise ✓, Kiwi ✓ | **Oui** |
| Exotique rouge | Papaye ✗ | Non |
| Vert citron | Pomme verte ✗ | Non |
| Soleil couchant | Mangue ✗ | Non |

**Réponse : un seul smoothie possible — Rouge kiwi.**

### Exercice C — Trouver l'alternative

Avec la boutique de l'exercice B, quelle alternative pour « Vert » (Kiwi, Pomme verte, Menthe) ?

- Seul « Rouge kiwi » est possible.
- Score entre Vert et Rouge kiwi : Kiwi est commun → score = 1.

**Réponse : l'alternative proposée est Rouge kiwi.**

---

## Récapitulatif des points essentiels

1. Dans une méthode, `self` est obligatoire en premier paramètre — il donne accès aux attributs et aux autres méthodes.
2. `element in liste` renvoie `True` si l'élément est présent dans la liste.
3. `all(condition for x in liste)` teste si la condition est vraie pour tous les éléments.
4. Le bug de `plus_proche_possible` : chercher dans tous les smoothies au lieu des smoothies possibles uniquement.
5. Ne jamais oublier d'exclure le smoothie de référence lui-même de la recherche d'alternative.
6. Toujours gérer le cas `None` quand une fonction peut ne rien trouver.
7. Le score de proximité est commutatif : `score(A, B) == score(B, A)`.
8. En cas d'égalité de score, c'est le premier trouvé dans l'ordre du dictionnaire qui est retenu.

---

## Code complet corrigé — `smoothie.py`

```python
class Boutique_smoothie:
    def __init__(self, liste_fruits_disponibles):
        self.liste_fruits_disponibles = liste_fruits_disponibles
        self.db_smoothies = {
            "Tropical":        ["Mangue", "Ananas", "Banane"],
            "Rouge":           ["Fraise", "Framboise", "Cerise"],
            "Vert":            ["Kiwi", "Pomme verte", "Menthe"],
            "Agrume":          ["Orange", "Citron", "Pamplemousse"],
            "Exotique":        ["Papaye", "Fruit de la passion", "Noix de coco"],
            "Tropical citron": ["Mangue", "Ananas", "Citron"],
            "Rouge kiwi":      ["Fraise", "Framboise", "Kiwi"],
            "Exotique rouge":  ["Papaye", "Fraise", "Fruit de la passion"],
            "Vert citron":     ["Kiwi", "Pomme verte", "Citron"],
            "Soleil couchant": ["Mangue", "Fraise", "Pamplemousse"],
        }

    def smoothie_possible(self, nom_smoothie):
        """Retourne True si le smoothie peut être préparé, False sinon."""
        recette = self.db_smoothies[nom_smoothie]
        for fruit in recette:
            if fruit not in self.liste_fruits_disponibles:
                return False
        return True

    def liste_smoothies_possibles(self):
        """Retourne la liste des smoothies pouvant être préparés."""
        possibles = []
        for nom in self.db_smoothies:
            if self.smoothie_possible(nom):
                possibles.append(nom)
        return possibles

    def score_proximite(self, nom1, nom2):
        """Retourne le nombre de fruits communs entre deux smoothies."""
        nb = 0
        fruits1 = self.db_smoothies[nom1]
        fruits2 = self.db_smoothies[nom2]
        for fruit in fruits1:
            if fruit in fruits2:
                nb += 1
        return nb

    def plus_proche_possible(self, nom_smoothie_ref):
        """Retourne le smoothie possible le plus proche du smoothie de référence.
        En cas d'égalité, retourne le premier trouvé.
        Retourne None si aucun smoothie proche n'est disponible."""
        max_communs = 0
        smoothie_proche = None
        for nom_smoothie in self.liste_smoothies_possibles():
            if nom_smoothie == nom_smoothie_ref:
                continue
            nb_communs = self.score_proximite(nom_smoothie_ref, nom_smoothie)
            if nb_communs > max_communs:
                max_communs = nb_communs
                smoothie_proche = nom_smoothie
        return smoothie_proche

    def affichage_possibles(self):
        """Affiche les smoothies possibles et les alternatives."""
        smoothies = self.liste_smoothies_possibles()
        print("Smoothies possibles avec les fruits disponibles :")
        for smoothie in smoothies:
            print(" ", smoothie)
        print("Alternative aux autres smoothies :")
        for smoothie in self.db_smoothies:
            if smoothie not in smoothies:
                proche = self.plus_proche_possible(smoothie)
                if proche is not None:
                    print(f"Pour le smoothie {smoothie}, essayez {proche}.")
                else:
                    print(f"Pour le smoothie {smoothie}, aucun smoothie proche disponible.")


# ===== Tests =====

def test_smoothie_possible():
    b = Boutique_smoothie(["Mangue", "Ananas", "Banane", "Fraise", "Citron"])
    assert b.smoothie_possible("Tropical") == True
    assert b.smoothie_possible("Rouge") == False
    assert b.smoothie_possible("Tropical citron") == True
    assert b.smoothie_possible("Agrume") == False
    print("Les tests sont validés.")

def test_liste_smoothies_possibles():
    b1 = Boutique_smoothie(["Mangue", "Ananas", "Banane", "Fraise", "Citron"])
    assert b1.liste_smoothies_possibles() == ["Tropical", "Tropical citron"]
    b2 = Boutique_smoothie(["Fraise", "Framboise", "Kiwi", "Pomme verte", "Citron"])
    assert b2.liste_smoothies_possibles() == ["Rouge kiwi", "Vert citron"]
    b3 = Boutique_smoothie(["Orange", "Mangue", "Papaye"])
    assert b3.liste_smoothies_possibles() == []
    print("Les tests sont validés.")

def test_score_proximite():
    b = Boutique_smoothie([])
    assert b.score_proximite("Tropical", "Tropical citron") == 2
    assert b.score_proximite("Tropical", "Rouge") == 0
    assert b.score_proximite("Tropical", "Tropical") == 3
    assert b.score_proximite("Rouge kiwi", "Vert citron") == 1
    assert b.score_proximite("Exotique", "Exotique rouge") == 2
    print("Les tests sont validés.")

def test_plus_proche_possible():
    b = Boutique_smoothie(
        ["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"])
    assert b.plus_proche_possible("Tropical") == "Tropical citron"
    assert b.plus_proche_possible("Exotique") is None
    assert b.plus_proche_possible("Agrume") in ["Vert citron", "Tropical citron"]
    print("Les tests sont validés.")

test_smoothie_possible()
test_liste_smoothies_possibles()
test_score_proximite()
test_plus_proche_possible()

# Mise en situation complète — Question 5
boutique = Boutique_smoothie(
    ["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"])
boutique.affichage_possibles()
```
