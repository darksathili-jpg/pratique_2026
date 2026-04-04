# NSI Terminale – Sujet pratique n°11 – BAC 2026
## Prédiction d'habitats de renards par l'algorithme des k plus proches voisins (k-NN)

---

## MÉTADONNÉES DU DOCUMENT

- **Matière** : Numérique et Sciences Informatiques (NSI)
- **Niveau** : Terminale générale
- **Type d'épreuve** : Partie pratique du baccalauréat — durée 1 heure
- **Session** : 2026 — Sujet n°11
- **Thème du programme** : Algorithmique — traitement de données, algorithme des k plus proches voisins
- **Langage** : Python 3
- **Fichiers fournis à l'examen** : `prediction_habitat.py`, `donnees_habitats.py`

---

## PARTIE 1 — CONTEXTE ET PROBLÉMATIQUE

### Contexte réglementaire

Le renard est un animal capable de vivre dans des environnements très variés : plaines, montagnes, zones rurales, périurbaines et urbaines. La loi Biodiversité 2016 et l'arrêté du 3 août 2023 ont retiré le renard de la liste des animaux « nuisibles » pour le classer « susceptible d'être nuisible ». Malgré cette évolution juridique, le renard reste souvent chassé hors de zones où il pourrait naturellement réguler la faune. Il est donc recommandé de surveiller les populations de renards et de prédire si un renard peut habiter une zone donnée.

### Objectif informatique

L'objectif est d'implémenter et corriger un programme Python qui prédit, à partir de caractéristiques mesurables d'une zone géographique, si un renard est susceptible d'y vivre. La méthode utilisée est l'algorithme des **k plus proches voisins** (k-NN).

---

## PARTIE 2 — STRUCTURE DES DONNÉES

### Description d'un habitat

Chaque zone géographique est représentée par un **dictionnaire Python** à cinq clés :

```python
zone = {
    'vegetation':            9,   # entier de 0 à 10 (densité de végétation)
    'proximite_eau':         6,   # entier de 0 à 10 (proximité d'une source d'eau)
    'densite_urbaine':       0,   # entier de 0 à 10 (présence humaine/urbaine)
    'disponibilite_proies':  4,   # entier de 0 à 10 (nourriture disponible)
    'presence_renard':       1    # 1 si le renard est présent, 0 sinon
}
```

**Remarque importante** : la clé `'presence_renard'` est un entier (0 ou 1), pas un booléen Python. La comparaison correcte est `zone['presence_renard'] == 1`.

### Le jeu de données

Le fichier `donnees_habitats.py` contient une liste Python nommée `zones_connues` comprenant 1002 dictionnaires (zones déjà étudiées avec présence ou absence de renard connue). Extrait des premières zones :

```python
zones_connues = [
    {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0, 'disponibilite_proies': 4, 'presence_renard': 1},
    {'vegetation': 10, 'proximite_eau': 5, 'densite_urbaine': 9, 'disponibilite_proies': 10, 'presence_renard': 0},
    {'vegetation': 8, 'proximite_eau': 5, 'densite_urbaine': 1, 'disponibilite_proies': 6, 'presence_renard': 0},
    {'vegetation': 8, 'proximite_eau': 5, 'densite_urbaine': 7, 'disponibilite_proies': 6, 'presence_renard': 1},
    {'vegetation': 6, 'proximite_eau': 9, 'densite_urbaine': 9, 'disponibilite_proies': 6, 'presence_renard': 1},
    # ... (1002 entrées au total)
]
```

### Le nouvel habitat à évaluer

```python
nouveau = {
    'vegetation': 5,
    'proximite_eau': 2,
    'densite_urbaine': 4,
    'disponibilite_proies': 6,
    'presence_renard': 0   # inconnu — on veut prédire si un renard y vivrait
}
```

---

## PARTIE 3 — L'ALGORITHME DES K PLUS PROCHES VOISINS (k-NN)

### Principe intuitif

Pour prédire si un renard peut habiter une nouvelle zone, on cherche les zones déjà connues qui lui ressemblent le plus. Si la majorité de ces zones proches accueillent des renards, on prédit que la nouvelle zone en accueil probablement aussi.

### Les 4 étapes de l'algorithme

1. **Calculer** la distance entre le nouvel habitat et chacun des habitats connus.
2. **Trier** ces distances de la plus petite à la plus grande.
3. **Garder** les k premiers résultats (les k plus proches voisins).
4. **Voter** : si strictement plus de k/2 voisins ont un renard → présence probable (True), sinon False.

### La formule de distance euclidienne

Pour deux habitats ha = (va, pa, dea, dia, pra) et hb = (vb, pb, deb, dib, prb) :

```
d = sqrt( (va-vb)² + (pa-pb)² + (dea-deb)² + (dia-dib)² + (pra-prb)² )
```

**Attention** : la distance inclut **les 5 clés**, y compris `presence_renard`. C'est la formule exacte donnée par l'énoncé.

En Python : `from math import sqrt` est nécessaire.

### Structure des résultats intermédiaires

Les fonctions de calcul de distance retournent des **listes de tuples**. Chaque tuple a la forme :

```python
(distance_euclidienne, dictionnaire_habitat)
# Exemple :
(7.211102550927978, {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0, 'disponibilite_proies': 4, 'presence_renard': 1})
```

- `tuple[0]` → float (la distance)
- `tuple[1]` → dict (les caractéristiques de la zone)

---

## PARTIE 4 — FICHIER DE DÉPART `prediction_habitat.py`

Voici le contenu intégral du fichier fourni aux candidats à l'examen :

```python
from math import sqrt
from donnees_habitats import zones_connues

nouveau = {'vegetation': 5, 'proximite_eau': 2, 'densite_urbaine': 4, 'disponibilite_proies': 6}


def distance(habitat_1, habitat_2):
    '''
    Calcule la distance euclidienne entre deux habitats.
    entrée :
        - habitat_1 : dictionnaire représentant un habitat.
        - habitat_2 : dictionnaire représentant un autre habitat.
    sortie :
        - float : distance euclidienne entre habitat_1 et habitat_2.
    '''
    pass  # à remplacer par votre code


def distance_d_un_habitat(habitat, habitats):
    '''
    Calcule la distance entre un habitat et chaque habitat de la liste.
    entrée :
        - habitat : dictionnaire représentant un habitat.
        - habitats : liste de dictionnaires représentant des habitats.
    sortie :
        - list[tuple] : liste de tuples (distance, habitat) où distance est
          la distance entre habitat et chaque habitat de la liste.
    '''
    pass  # à remplacer par votre code


def k_plus_proches(k, habitat, habitats):
    '''
    Calcule les k habitats les plus proches de l'habitat donné.
    entrée :
        - k : entier représentant le nombre d'habitats à retourner.
        - habitat : dictionnaire représentant un habitat.
        - habitats : liste de dictionnaires représentant des habitats.
    sortie :
        - list[tuple] : liste de tuples (distance, habitat)
    '''
    distances = distance_d_un_habitat(habitat, habitats)
    distances.sort(key=lambda x: x[0])
    return distances[:k]


def presence_renard(k, habitat, habitats):
    '''
    Vérifie si l'habitat donné a plus de k/2 voisins avec des renards.
    entrée :
        - k : entier représentant le nombre d'habitats à considérer.
        - habitat : dictionnaire représentant un habitat.
        - habitats : liste de dictionnaires représentant des habitats.
    sortie :
        - bool : True si l'habitat a plus de k/2 voisins avec des renards, False sinon.
    '''
    habitats = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for habitat in habitats:
        distance = habitat[0]
        caracteristiques = habitat[1]
        if distance['presence_renard'] == 1:   # ← LIGNE BUGUÉE
            n_renards += 1
    return n_renards > k / 2
```

---

## PARTIE 5 — QUESTIONS DE L'EXAMEN ET CORRECTIONS COMPLÈTES

---

### QUESTION 1 — Écrire la fonction `distance`

**Énoncé** : Écrire le code de la fonction `distance` qui prend en paramètres deux habitats sous la forme de dictionnaires et renvoie la valeur « distance » entre ces deux habitats définie par la formule euclidienne. On rappelle que la racine carrée se calcule avec la fonction `sqrt` du module `math`.

**Démarche** :
1. Identifier les 5 clés à utiliser : `'vegetation'`, `'proximite_eau'`, `'densite_urbaine'`, `'disponibilite_proies'`, `'presence_renard'`.
2. Pour chaque clé, calculer `(habitat_1[cle] - habitat_2[cle]) ** 2`.
3. Sommer les 5 termes.
4. Retourner `sqrt(somme)`.

**Correction — version avec boucle (recommandée à l'examen)** :

```python
def distance(habitat_1, habitat_2):
    cles = ['vegetation', 'proximite_eau', 'densite_urbaine',
            'disponibilite_proies', 'presence_renard']
    somme = 0
    for cle in cles:
        diff = habitat_1[cle] - habitat_2[cle]
        somme += diff ** 2
    return sqrt(somme)
```

**Correction — version dépliée (aussi acceptée)** :

```python
def distance(habitat_1, habitat_2):
    somme = (habitat_1['vegetation']           - habitat_2['vegetation'])**2 \
          + (habitat_1['proximite_eau']         - habitat_2['proximite_eau'])**2 \
          + (habitat_1['densite_urbaine']        - habitat_2['densite_urbaine'])**2 \
          + (habitat_1['disponibilite_proies']   - habitat_2['disponibilite_proies'])**2 \
          + (habitat_1['presence_renard']        - habitat_2['presence_renard'])**2
    return sqrt(somme)
```

**Correction — version compréhension (concise)** :

```python
def distance(habitat_1, habitat_2):
    cles = ['vegetation', 'proximite_eau', 'densite_urbaine',
            'disponibilite_proies', 'presence_renard']
    return sqrt(sum((habitat_1[c] - habitat_2[c])**2 for c in cles))
```

**Vérifications numériques attendues** :

| habitat_1 | habitat_2 | distance attendue |
|-----------|-----------|-------------------|
| zones_connues[0] (veg=9,eau=6,dens=0,proies=4,renard=1) | nouveau (veg=5,eau=2,dens=4,proies=6,renard=0) | 7.211102550927978 |
| zones_connues[1] (veg=10,eau=5,dens=9,proies=10,renard=0) | nouveau | 8.660254037844387 |
| zones_connues[2] (veg=8,eau=5,dens=1,proies=6,renard=0) | nouveau | 5.196152422706632 |
| une zone avec elle-même | elle-même | 0.0 |

**Calcul détaillé pour zones_connues[0] vs nouveau** :
- (9-5)² = 16
- (6-2)² = 16
- (0-4)² = 16
- (4-6)² = 4
- (1-0)² = 1
- Somme = 53
- sqrt(53) ≈ 7.211102550927978 ✓

**Fonction de test** :

```python
def test_distance():
    h_a = {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0,
            'disponibilite_proies': 4, 'presence_renard': 1}
    h_b = {'vegetation': 5, 'proximite_eau': 2, 'densite_urbaine': 4,
            'disponibilite_proies': 6, 'presence_renard': 0}
    h_identique = {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0,
                   'disponibilite_proies': 4, 'presence_renard': 1}

    assert abs(distance(h_a, h_b) - 7.211102550927978) < 1e-6
    assert distance(h_a, h_identique) == 0.0
    assert isinstance(distance(h_a, h_b), float)
    print("Les tests sont validés.")

test_distance()
```

---

### QUESTION 2 — Écrire la fonction `distance_d_un_habitat`

**Énoncé** : Écrire le code de la fonction `distance_d_un_habitat` qui prend en paramètres un habitat (dictionnaire) et une liste d'habitats (liste de dictionnaires). La fonction doit renvoyer une **liste de tuples** où chaque tuple contient : la distance entre l'habitat fourni et un habitat de la liste ; puis le dictionnaire représentant cet habitat.

**Démarche** :
1. Créer une liste vide `resultats = []`.
2. Parcourir chaque zone de la liste `habitats` avec une boucle `for`.
3. Calculer `d = distance(habitat, zone)`.
4. Ajouter le tuple `(d, zone)` à la liste avec `.append()`.
5. Retourner la liste.

**Correction** :

```python
def distance_d_un_habitat(habitat, habitats):
    resultats = []
    for zone in habitats:
        d = distance(habitat, zone)
        resultats.append((d, zone))
    return resultats
```

**Structure exacte du résultat** : la fonction retourne une liste de tuples non triés, dans l'ordre des habitats fournis en entrée. Exemple avec les 3 premières zones :

```python
[
    (7.211102550927978, {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0, 'disponibilite_proies': 4, 'presence_renard': 1}),
    (8.660254037844387, {'vegetation': 10, 'proximite_eau': 5, 'densite_urbaine': 9, 'disponibilite_proies': 10, 'presence_renard': 0}),
    (5.196152422706632, {'vegetation': 8, 'proximite_eau': 5, 'densite_urbaine': 1, 'disponibilite_proies': 6, 'presence_renard': 0}),
]
```

**Fonction de test** :

```python
def test_distance_d_un_habitat():
    mini = [
        {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0,
         'disponibilite_proies': 4, 'presence_renard': 1},
        {'vegetation': 10, 'proximite_eau': 5, 'densite_urbaine': 9,
         'disponibilite_proies': 10, 'presence_renard': 0},
        {'vegetation': 8, 'proximite_eau': 5, 'densite_urbaine': 1,
         'disponibilite_proies': 6, 'presence_renard': 0},
    ]
    resultats = distance_d_un_habitat(nouveau, mini)
    assert isinstance(resultats, list)
    assert len(resultats) == 3
    assert isinstance(resultats[0], tuple)
    assert isinstance(resultats[0][0], float)
    assert isinstance(resultats[0][1], dict)
    assert abs(resultats[0][0] - 7.211102550927978) < 1e-6
    assert abs(resultats[1][0] - 8.660254037844387) < 1e-6
    assert abs(resultats[2][0] - 5.196152422706632) < 1e-6
    print("Les tests sont validés.")

test_distance_d_un_habitat()
```

---

### QUESTION 3 — Tester la fonction et afficher les 3 premiers tuples

**Énoncé** : Tester la fonction `distance_d_un_habitat` avec l'habitat `nouveau` et la liste d'habitats fournis, en affichant les 3 premiers tuples de la liste.

**Point de vigilance** : les « 3 premiers tuples » correspondent aux 3 premières zones de `zones_connues` dans leur ordre d'apparition, pas aux 3 zones les plus proches. La liste n'est pas triée ici.

**Correction** :

```python
resultats = distance_d_un_habitat(nouveau, zones_connues)
for t in resultats[:3]:
    print(t)
```

**Résultat attendu exactement** :

```
(7.211102550927978, {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0, 'disponibilite_proies': 4, 'presence_renard': 1})
(8.660254037844387, {'vegetation': 10, 'proximite_eau': 5, 'densite_urbaine': 9, 'disponibilite_proies': 10, 'presence_renard': 0})
(5.196152422706632, {'vegetation': 8, 'proximite_eau': 5, 'densite_urbaine': 1, 'disponibilite_proies': 6, 'presence_renard': 0})
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question. L'élève doit montrer son programme tournant et produisant exactement ces 3 lignes.

---

### QUESTION 4 — Identifier et corriger le bug de `presence_renard`

**Énoncé** : La fonction `presence_renard` contient une erreur de traitement des tuples. Corriger la fonction `presence_renard`.

**Analyse du bug** :

La ligne buguée est :
```python
if distance['presence_renard'] == 1:
```

Analyse :
- `habitat` dans la boucle est un tuple de la forme `(float, dict)`.
- `distance = habitat[0]` → c'est un **float** (la distance euclidienne).
- `caracteristiques = habitat[1]` → c'est le **dict** avec les données de la zone.
- Or le code tente `distance['presence_renard']` — indexer un float avec une clé de dictionnaire.
- Cela lève une `TypeError: 'float' object is not subscriptable`.
- La vérification doit se faire sur `caracteristiques`, pas sur `distance`.

**Autres problèmes de style dans la fonction originale** :
- La variable de boucle `habitat` écrase le paramètre `habitat` de la fonction.
- La variable `habitats` est réassignée au début de la fonction, écrasant le paramètre.
- La variable `distance` dans la boucle masque la fonction `distance` importée.

**Correction minimale (une seule ligne change)** :

```python
def presence_renard(k, habitat, habitats):
    habitats = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for habitat in habitats:
        distance = habitat[0]
        caracteristiques = habitat[1]
        if caracteristiques['presence_renard'] == 1:   # ← CORRIGÉ
            n_renards += 1
    return n_renards > k / 2
```

**Correction améliorée (nommage clair)** :

```python
def presence_renard(k, habitat, habitats):
    voisins = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for voisin in voisins:
        distance_val = voisin[0]          # float : la distance euclidienne
        caracteristiques = voisin[1]      # dict  : les données de la zone
        if caracteristiques['presence_renard'] == 1:
            n_renards += 1
    return n_renards > k / 2
```

**Fonction de test** :

```python
def test_presence_renard():
    mini = [
        {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0,
         'disponibilite_proies': 4, 'presence_renard': 1},
        {'vegetation': 10, 'proximite_eau': 5, 'densite_urbaine': 9,
         'disponibilite_proies': 10, 'presence_renard': 0},
        {'vegetation': 8, 'proximite_eau': 5, 'densite_urbaine': 1,
         'disponibilite_proies': 6, 'presence_renard': 0},
    ]
    assert isinstance(presence_renard(1, nouveau, mini), bool)
    assert presence_renard(1, nouveau, mini) == False  # voisin le plus proche : renard=0
    z_renard = mini[0]  # presence_renard = 1
    assert presence_renard(1, z_renard, mini) == True   # lui-même distance 0, renard=1
    print("Les tests sont validés.")

test_presence_renard()
```

---

### QUESTION 5 — Conclusion : le nouvel habitat est-il habitable par un renard ?

**Énoncé** : L'habitat `zones_connues` proposé est-il susceptible ou non de contenir une population de renards ? Expliquer en utilisant la fonction précédente avec plusieurs valeurs pour k.

**Note** : l'énoncé parle de l'habitat `nouveau` à évaluer (valeurs : végétation=5, eau=2, densité=4, proies=6).

**Code de test** :

```python
for k in [1, 3, 5, 7, 9]:
    resultat = presence_renard(k, nouveau, zones_connues)
    print(f"k = {k} → presence_renard = {resultat}")
```

**Résultats typiques** (dépendent du jeu de données complet) :

```
k = 1 → presence_renard = False
k = 3 → presence_renard = False
k = 5 → presence_renard = False
k = 7 → presence_renard = True
k = 9 → presence_renard = True
```

**Réponse rédigée attendue par l'examinateur** :

Pour les petites valeurs de k (1, 3, 5), la majorité des voisins les plus proches n'accueillent pas de renard : la fonction retourne `False`. Pour k=7 et au-delà, la conclusion s'inverse. Les résultats varient selon le nombre de voisins considérés, ce qui indique que le nouvel habitat se situe dans une zone ambiguë. Avec un k modéré (3 à 5), la prédiction suggère une **absence probable de renard**. Il serait prudent de collecter davantage de données pour conclure avec certitude.

**Appel professeur** : l'énoncé précise un appel professeur après cette question. L'élève montre et commente ses résultats pour plusieurs valeurs de k.

---

## PARTIE 6 — CODE COMPLET ET FONCTIONNEL (SOLUTION DE RÉFÉRENCE)

```python
from math import sqrt
from donnees_habitats import zones_connues

nouveau = {'vegetation': 5, 'proximite_eau': 2, 'densite_urbaine': 4,
           'disponibilite_proies': 6, 'presence_renard': 0}


def distance(habitat_1, habitat_2):
    """Calcule la distance euclidienne entre deux habitats (5 dimensions)."""
    cles = ['vegetation', 'proximite_eau', 'densite_urbaine',
            'disponibilite_proies', 'presence_renard']
    somme = 0
    for cle in cles:
        diff = habitat_1[cle] - habitat_2[cle]
        somme += diff ** 2
    return sqrt(somme)


def distance_d_un_habitat(habitat, habitats):
    """Retourne la liste de tuples (distance, zone) pour toutes les zones connues."""
    resultats = []
    for zone in habitats:
        d = distance(habitat, zone)
        resultats.append((d, zone))
    return resultats


def k_plus_proches(k, habitat, habitats):
    """Retourne les k zones les plus proches, triées par distance croissante."""
    distances = distance_d_un_habitat(habitat, habitats)
    distances.sort(key=lambda x: x[0])
    return distances[:k]


def presence_renard(k, habitat, habitats):
    """Retourne True si plus de k/2 des k voisins les plus proches ont un renard."""
    voisins = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for voisin in voisins:
        caracteristiques = voisin[1]
        if caracteristiques['presence_renard'] == 1:
            n_renards += 1
    return n_renards > k / 2


# Question 3 : afficher les 3 premiers tuples
resultats = distance_d_un_habitat(nouveau, zones_connues)
for t in resultats[:3]:
    print(t)

# Question 5 : tester avec plusieurs valeurs de k
for k in [1, 3, 5, 7, 9]:
    print(f"k = {k} → presence_renard = {presence_renard(k, nouveau, zones_connues)}")
```

---

## PARTIE 7 — ERREURS FRÉQUENTES ET PIÈGES

### Piège 1 — Confondre les indices d'un tuple

Un tuple résultat est `(float, dict)`. L'indice `[0]` est le float (distance), l'indice `[1]` est le dict.

```python
# ERREUR : distance est un float, pas un dict
if distance['presence_renard'] == 1:   # TypeError !

# CORRECT : caracteristiques est le dict
if caracteristiques['presence_renard'] == 1:
```

### Piège 2 — Oublier d'importer `sqrt`

Sans `from math import sqrt`, Python lève `NameError: name 'sqrt' is not defined`. Cette ligne doit être en tête de fichier.

### Piège 3 — Omettre `'presence_renard'` dans la formule de distance

La formule du sujet utilise les **5 clés**, dont `'presence_renard'`. Utiliser seulement 4 clés produit des distances incorrectes et un résultat faux à Q3.

### Piège 4 — Écraser les variables de paramètre dans une boucle

Dans le code original, la boucle utilise `for habitat in habitats:` alors que `habitat` et `habitats` sont déjà des noms de paramètres. Cela écrase les paramètres dans la portée locale. Utiliser `voisin` et `voisins` évite ce problème.

### Piège 5 — Mal comprendre la condition `n_renards > k/2`

C'est une comparaison **strictement supérieure**. Pour k=4 : il faut au moins 3 renards (pas 2) pour que la condition soit vraie. Pour k=5 : il faut au moins 3 renards.

### Piège 6 — Confondre liste triée et liste dans l'ordre d'entrée

`distance_d_un_habitat` renvoie les résultats **dans l'ordre des données d'entrée**, pas triés. C'est `k_plus_proches` qui trie. À la Question 3, les 3 premiers éléments correspondent aux 3 premières zones du fichier, pas aux 3 plus proches.

### Piège 7 — Utiliser k pair

Avec k pair, la condition `n_renards > k/2` peut être ambiguë. Exemple : k=4, n_renards=2 → `2 > 2.0` est `False`. Pour éviter les ex-æquo, préférer des valeurs impaires de k (1, 3, 5, 7…).

---

## PARTIE 8 — POINTS CLÉS À RETENIR POUR L'EXAMEN

### Syntaxe Python à maîtriser absolument

| Opération | Syntaxe Python |
|-----------|---------------|
| Accéder à une valeur dans un dict | `dico['cle']` |
| Accéder à l'élément 0 d'un tuple | `tuple[0]` |
| Accéder à l'élément 1 d'un tuple | `tuple[1]` |
| Ajouter un élément à une liste | `liste.append(element)` |
| Créer un tuple | `(valeur1, valeur2)` |
| Trier une liste par un critère | `liste.sort(key=lambda x: x[0])` |
| Garder les k premiers éléments | `liste[:k]` |
| Racine carrée | `from math import sqrt` puis `sqrt(valeur)` |
| Mettre au carré | `valeur ** 2` |

### Checklist avant de rendre le code

- [ ] `from math import sqrt` est présent en haut du fichier
- [ ] La fonction `distance` utilise bien les **5 clés** (dont `'presence_renard'`)
- [ ] `distance_d_un_habitat` retourne bien une **liste de tuples**
- [ ] Dans `presence_renard` corrigée, on accède à `voisin[1]['presence_renard']` (le dict), pas à `voisin[0]['presence_renard']` (le float)
- [ ] La condition de vote est `n_renards > k / 2` (strictement supérieur)
- [ ] Les résultats Q3 correspondent exactement aux valeurs attendues dans l'énoncé

### Structure des fonctions et leur rôle

```
distance(h1, h2)
    → float
    → calcule la "ressemblance" entre deux zones

distance_d_un_habitat(habitat, habitats)
    → list of (float, dict)   [non triée]
    → applique distance() à chaque zone connue

k_plus_proches(k, habitat, habitats)     [déjà fournie, ne pas modifier]
    → list of (float, dict)   [triée, longueur k]
    → garde les k zones les plus ressemblantes

presence_renard(k, habitat, habitats)    [à corriger]
    → bool
    → vote majoritaire parmi les k voisins
```

---

## PARTIE 9 — GLOSSAIRE

**Algorithme des k plus proches voisins (k-NN)** : méthode de classification qui prédit la catégorie d'un nouvel élément en regardant les k éléments les plus proches dans les données d'entraînement.

**Distance euclidienne** : mesure de la "distance" entre deux points dans un espace multidimensionnel, généralisée du théorème de Pythagore. Plus la distance est petite, plus deux habitats se ressemblent.

**Dictionnaire Python** : structure de données qui associe des clés à des valeurs. Accès par `dico['cle']`.

**Tuple Python** : séquence ordonnée et immuable. Accès par indice : `t[0]`, `t[1]`.

**Liste de tuples** : structure de données utilisée ici pour stocker les paires (distance, habitat). Chaque élément est un tuple à deux composantes.

**k** : paramètre de l'algorithme k-NN. Nombre de voisins à considérer pour le vote. Plus k est grand, plus la prédiction est "lissée" mais potentiellement moins précise localement.

**Vote majoritaire** : règle de décision qui retourne True si strictement plus de la moitié des k voisins appartiennent à la classe recherchée (ici : présence de renard).

**`presence_renard`** : valeur entière (0 ou 1) dans le dictionnaire d'un habitat. 1 = renard présent, 0 = renard absent. Ne pas confondre avec la fonction Python du même nom.

**`TypeError: 'float' object is not subscriptable`** : erreur Python obtenue quand on tente d'indexer un nombre avec `[]`, comme si c'était un dictionnaire ou une liste.

---

*Document produit pour une utilisation pédagogique dans NotebookLM. Lycée Antoine Watteau — DarkSATHI Li*
