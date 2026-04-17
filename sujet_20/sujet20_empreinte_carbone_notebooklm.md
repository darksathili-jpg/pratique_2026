# NSI Terminale – Sujet pratique n°20 – BAC 2026
## Empreinte carbone du numérique — Dictionnaires, classification, tests, ZeroDivisionError

---

## MÉTADONNÉES DU DOCUMENT

- **Matière** : Numérique et Sciences Informatiques (NSI)
- **Niveau** : Terminale générale
- **Type d'épreuve** : Partie pratique du baccalauréat — durée 1 heure
- **Session** : 2026 — Sujet n°20
- **Thème du programme** : Traitement de données, dictionnaires, assertions, gestion d'erreurs
- **Langage** : Python 3
- **Fichier fourni** : `code_empreinte.py`
- **Modules Python requis** : aucun

---

## PARTIE 1 — CONTEXTE ET PROBLÉMATIQUE

Le numérique représente environ 4 % des émissions mondiales de gaz à effet de serre — davantage que le transport aérien. L'objectif est de développer une application Python qui estime l'empreinte carbone mensuelle d'un utilisateur à partir de ses usages numériques.

Les émissions sont exprimées en **gramme de CO2 équivalent (gCO2e)**.

---

## PARTIE 2 — DONNÉES DU SUJET

### Le dictionnaire `EMISSIONS` — émissions unitaires

```python
EMISSIONS = {
    'emails_simples': 4,       # gCO2e par email
    'emails_pj': 19,           # gCO2e par email avec pièce jointe
    'streaming_sd': 36,        # gCO2e par heure
    'streaming_hd': 100,       # gCO2e par heure
    'recherches': 7,           # gCO2e par recherche
    'stockage_cloud': 10       # gCO2e par Go par mois
}
```

### Les utilisateurs fournis

```python
utilisateur1 = {'emails_simples': 150, 'emails_pj': 20, 'streaming_sd': 10,
                'streaming_hd': 25, 'recherches': 500, 'stockage_cloud': 15}

utilisateur2 = {'streaming_hd': 15, 'emails_simples': 100, 'recherches': 10}

utilisateur3 = {'emails_simples': 50, 'emails_pj': 5, 'streaming_sd': 30,
                'streaming_hd': 5, 'recherches': 200, 'stockage_cloud': 5}

utilisateur4 = {'emails_simples': 100, 'recherches': 50}

utilisateur5 = {'emails_simples': 50, 'recherches': 100}

utilisateur6 = {}   # dictionnaire vide
```

### Tableau des émissions calculées par activité et par utilisateur

| Activité | ×émission | u1 qté→gCO2e | u2 qté→gCO2e | u3 qté→gCO2e |
|----------|-----------|-------------|-------------|-------------|
| emails_simples | ×4 | 150→600 | 100→400 | 50→200 |
| emails_pj | ×19 | 20→380 | absent→0 | 5→95 |
| streaming_sd | ×36 | 10→360 | absent→0 | 30→1080 |
| streaming_hd | ×100 | 25→2500 | 15→1500 | 5→500 |
| recherches | ×7 | 500→3500 | 10→70 | 200→1400 |
| stockage_cloud | ×10 | 15→150 | absent→0 | 5→50 |
| **TOTAL** | | **7490** | **1970** | **3325** |

### Empreintes totales de tous les utilisateurs

| Utilisateur | Empreinte (gCO2e) |
|-------------|-----------------|
| utilisateur1 | **7490** (donné par l'énoncé) |
| utilisateur2 | **1970** |
| utilisateur3 | **3325** |
| utilisateur4 | **750** (100×4 + 50×7) |
| utilisateur5 | **900** (50×4 + 100×7) |
| utilisateur6 | **0** (vide) |

---

## PARTIE 3 — FICHIER DE DÉPART `code_empreinte.py`

### Fonctions à écrire (squelettes vides)

```python
# Question 1 — à écrire
def calculer_empreinte(utilisateur):
    pass

# Question 2 — à écrire
def classer_par_impact(utilisateur):
    pass
```

### Fonction fournie pour la question 3 — `comparer`

```python
def comparer(u1, u2):
    """Renvoie pour chaque activité : émission_u2 - émission_u1.
    Activité absente = émission 0."""
    differences = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        differences[activite] = emission2 - emission1
    return differences

def test_comparer():
    diff = comparer(utilisateur4, utilisateur5)
    assert diff['emails_simples'] == -200   # (50-100) × 4
    assert diff['recherches'] == 350        # (100-50) × 7
    # Ajouter vos tests ci-dessous avec justifications
```

### Fonction fournie pour la question 4 — `comparer_v2` (BUGUÉE)

```python
def comparer_v2(u1, u2):
    """Renvoie le pourcentage d'écart : (emission2 - emission1) / emission1 * 100"""
    ecarts = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        ecarts[activite] = (emission2 - emission1) / emission1 * 100   # ← BUG : ZeroDivisionError si emission1 == 0
    return ecarts
```

---

## PARTIE 4 — QUESTIONS ET CORRECTIONS COMPLÈTES

---

### QUESTION 1 — Écrire `calculer_empreinte`

**Énoncé** : Écrire la fonction `calculer_empreinte(utilisateur)` qui renvoie l'empreinte carbone totale mensuelle en gCO2e (entier). Exemple : `calculer_empreinte(utilisateur1)` → 7490.

**Démarche** :
1. Initialiser `total = 0`.
2. Parcourir `utilisateur.items()` pour obtenir chaque `(activite, quantite)`.
3. Vérifier que l'activité est dans `EMISSIONS`.
4. Ajouter `quantite * EMISSIONS[activite]` à `total`.
5. Retourner `total`.

**Correction** :

```python
def calculer_empreinte(utilisateur):
    total = 0
    for activite, quantite in utilisateur.items():
        if activite in EMISSIONS:
            total += quantite * EMISSIONS[activite]
    return total
```

**Détail du calcul pour utilisateur1** :
- emails_simples : 150 × 4 = 600
- emails_pj : 20 × 19 = 380
- streaming_sd : 10 × 36 = 360
- streaming_hd : 25 × 100 = 2500
- recherches : 500 × 7 = 3500
- stockage_cloud : 15 × 10 = 150
- **TOTAL = 7490** ✓

**Fonction de test** :

```python
def test_calculer_empreinte():
    assert calculer_empreinte(utilisateur1) == 7490
    assert calculer_empreinte(utilisateur2) == 1970   # 1500+400+70
    assert calculer_empreinte(utilisateur6) == 0      # vide
    print("Les tests sont validés.")

test_calculer_empreinte()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 2 — Écrire `classer_par_impact`

**Énoncé** : Écrire la fonction `classer_par_impact(utilisateur)` qui renvoie un dictionnaire avec les clés `'fort'`, `'moyen'`, `'faible'`, chacune associée à une liste des activités.

**Seuils** :
- `'fort'` : émissions ≥ 1000 gCO2e
- `'moyen'` : 200 ≤ émissions < 1000 gCO2e
- `'faible'` : émissions < 200 gCO2e

**Exemple de l'énoncé** : pour utilisateur2 → `{'fort': ['streaming_hd'], 'moyen': ['emails_simples'], 'faible': ['recherches']}`

**Détail utilisateur2** :
- streaming_hd : 15 × 100 = 1500 → fort (≥ 1000)
- emails_simples : 100 × 4 = 400 → moyen (200 ≤ x < 1000)
- recherches : 10 × 7 = 70 → faible (< 200)

**Correction** :

```python
def classer_par_impact(utilisateur):
    resultat = {'fort': [], 'moyen': [], 'faible': []}
    for activite, quantite in utilisateur.items():
        if activite in EMISSIONS:
            emission = quantite * EMISSIONS[activite]
            if emission >= 1000:
                resultat['fort'].append(activite)
            elif emission >= 200:
                resultat['moyen'].append(activite)
            else:
                resultat['faible'].append(activite)
    return resultat
```

**Classification complète de utilisateur1** :

| Activité | Émission | Classe |
|----------|---------|--------|
| emails_simples | 600 | moyen |
| emails_pj | 380 | moyen |
| streaming_sd | 360 | moyen |
| streaming_hd | 2500 | **fort** |
| recherches | 3500 | **fort** |
| stockage_cloud | 150 | faible |

Résultat : `{'fort': ['streaming_hd', 'recherches'], 'moyen': ['emails_simples', 'emails_pj', 'streaming_sd'], 'faible': ['stockage_cloud']}`

**Fonction de test** :

```python
def test_classer_par_impact():
    res2 = classer_par_impact(utilisateur2)
    assert res2 == {'fort': ['streaming_hd'], 'moyen': ['emails_simples'], 'faible': ['recherches']}
    res6 = classer_par_impact(utilisateur6)
    assert res6 == {'fort': [], 'moyen': [], 'faible': []}
    res1 = classer_par_impact(utilisateur1)
    assert 'streaming_hd' in res1['fort']
    assert 'recherches'   in res1['fort']
    print("Les tests sont validés.")

test_classer_par_impact()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 3 — Compléter `test_comparer` avec 2 tests justifiés

**Énoncé** : Ajouter au moins deux tests pertinents dans `test_comparer`, avec justification pour chacun.

**Valeurs exactes de `comparer(utilisateur4, utilisateur5)`** :
- emails_simples : (50-100) × 4 = **-200** (donné)
- recherches : (100-50) × 7 = **+350** (donné)
- Toutes autres activités absentes des deux → 0

**Valeurs de `comparer(utilisateur1, utilisateur2)`** :
- emails_simples : (100-150) × 4 = -200
- emails_pj : (0-20) × 19 = -380
- streaming_sd : (0-10) × 36 = -360
- streaming_hd : (15-25) × 100 = -1000
- recherches : (10-500) × 7 = -3430
- stockage_cloud : (0-15) × 10 = -150

**Cas importants à tester** :

1. **Activité absente chez u1** : vérifie que l'absence est traitée comme émission = 0 (côté u1)
2. **Utilisateurs identiques** : toutes les différences doivent être exactement 0
3. **Deux utilisateurs vides** : cas limite, toutes les différences = 0

**Correction — tests ajoutés** :

```python
def test_comparer():
    # Tests fournis
    diff = comparer(utilisateur4, utilisateur5)
    assert diff['emails_simples'] == -200   # (50-100) × 4
    assert diff['recherches'] == 350        # (100-50) × 7

    # TEST 1 : activité absente chez u1 → traitée comme 0
    ua = {'emails_simples': 0}
    ub = {'streaming_hd': 5}
    diff_ab = comparer(ua, ub)
    assert diff_ab['streaming_hd'] == 500   # (5-0) × 100
    # Justification : vérifie que l'absence d'activité chez u1 vaut bien 0,
    # comme indiqué dans la docstring de la fonction

    # TEST 2 : utilisateurs identiques → toutes différences = 0
    diff_id = comparer(utilisateur4, utilisateur4)
    for activite in EMISSIONS:
        assert diff_id[activite] == 0
    # Justification : si u1 == u2, l'écart doit être nul pour toute activité ;
    # teste la cohérence mathématique de la fonction

    print("Les tests sont validés.")
```

---

### QUESTION 4 — Identifier et corriger le bug de `comparer_v2`

**Énoncé** : Identifier dans quels cas l'erreur se produit et proposer une correction.

**Bug identifié** : `ZeroDivisionError` — division par zéro.

**Cause** : La formule `(emission2 - emission1) / emission1 * 100` divise par `emission1`. Si l'activité est absente chez l'utilisateur 1, `quantite1 = 0`, donc `emission1 = 0 × EMISSIONS[activite] = 0`. La division `/ 0` lève une `ZeroDivisionError`.

**Cas concrets qui provoquent l'erreur** : tout appel où l'utilisateur 1 n'a pas certaines activités. Exemple : `comparer_v2(utilisateur4, utilisateur5)` — utilisateur4 n'a pas `'emails_pj'`, `'streaming_sd'`, `'streaming_hd'`, `'stockage_cloud'` → 4 divisions par zéro.

**Correction** :

```python
def comparer_v2(u1, u2):
    ecarts = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        if emission1 == 0:                                         # ← AJOUTÉ
            ecarts[activite] = None                                # non calculable
        else:
            ecarts[activite] = (emission2 - emission1) / emission1 * 100
    return ecarts
```

**Résultat de `comparer_v2(utilisateur4, utilisateur5)` après correction** :

```python
{'emails_simples': -50.0,   # (50-100)/100×100×4/400 = -50%
 'emails_pj':      None,    # u4 absent → non calculable
 'streaming_sd':   None,    # u4 absent → non calculable
 'streaming_hd':   None,    # u4 absent → non calculable
 'recherches':     100.0,   # (100-50)/50×100×7/350 = +100%
 'stockage_cloud': None}    # u4 absent → non calculable
```

**Résultat de `comparer_v2(utilisateur1, utilisateur2)` (donné par l'énoncé, vérifié)** :

```python
{'emails_pj':       -100.0,
 'emails_simples':  -33.33333333333333,
 'recherches':      -98.0,
 'stockage_cloud':  -100.0,
 'streaming_hd':    -40.0,
 'streaming_sd':    -100.0}
```

**Fonction de test** :

```python
def test_comparer_v2():
    res = comparer_v2(utilisateur4, utilisateur5)
    assert abs(res['emails_simples'] - (-50.0)) < 0.001
    assert abs(res['recherches'] - 100.0) < 0.001
    assert res['streaming_hd'] is None
    print("Les tests sont validés.")

test_comparer_v2()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

## PARTIE 5 — CODE COMPLET ET FONCTIONNEL (SOLUTION DE RÉFÉRENCE)

```python
EMISSIONS = {
    'emails_simples': 4, 'emails_pj': 19,
    'streaming_sd': 36,  'streaming_hd': 100,
    'recherches': 7,     'stockage_cloud': 10
}

utilisateur1 = {'emails_simples': 150, 'emails_pj': 20, 'streaming_sd': 10,
                'streaming_hd': 25, 'recherches': 500, 'stockage_cloud': 15}
utilisateur2 = {'streaming_hd': 15, 'emails_simples': 100, 'recherches': 10}
utilisateur4 = {'emails_simples': 100, 'recherches': 50}
utilisateur5 = {'emails_simples': 50, 'recherches': 100}
utilisateur6 = {}


# QUESTION 1
def calculer_empreinte(utilisateur):
    total = 0
    for activite, quantite in utilisateur.items():
        if activite in EMISSIONS:
            total += quantite * EMISSIONS[activite]
    return total


# QUESTION 2
def classer_par_impact(utilisateur):
    resultat = {'fort': [], 'moyen': [], 'faible': []}
    for activite, quantite in utilisateur.items():
        if activite in EMISSIONS:
            emission = quantite * EMISSIONS[activite]
            if emission >= 1000:
                resultat['fort'].append(activite)
            elif emission >= 200:
                resultat['moyen'].append(activite)
            else:
                resultat['faible'].append(activite)
    return resultat


def comparer(u1, u2):
    differences = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        differences[activite] = emission2 - emission1
    return differences


# QUESTION 3
def test_comparer():
    diff = comparer(utilisateur4, utilisateur5)
    assert diff['emails_simples'] == -200
    assert diff['recherches'] == 350

    ua = {'emails_simples': 0}
    ub = {'streaming_hd': 5}
    assert comparer(ua, ub)['streaming_hd'] == 500
    # Justification : activité absente chez u1 traitée comme 0

    diff_id = comparer(utilisateur4, utilisateur4)
    for activite in EMISSIONS:
        assert diff_id[activite] == 0
    # Justification : utilisateurs identiques → différence nulle partout

    print("Les tests sont validés.")

test_comparer()


# QUESTION 4 — version corrigée
def comparer_v2(u1, u2):
    ecarts = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        if emission1 == 0:
            ecarts[activite] = None
        else:
            ecarts[activite] = (emission2 - emission1) / emission1 * 100
    return ecarts
```

---

## PARTIE 6 — ERREURS FRÉQUENTES ET PIÈGES

### Piège 1 — Parcourir EMISSIONS au lieu de l'utilisateur (Q1)

Si on parcourt `EMISSIONS` et qu'on accède à `utilisateur[activite]` directement, on obtient une `KeyError` pour les activités absentes.

```python
# ERREUR
for activite in EMISSIONS:
    total += utilisateur[activite] * EMISSIONS[activite]   # KeyError si absent

# CORRECT
for activite, quantite in utilisateur.items():
    if activite in EMISSIONS:
        total += quantite * EMISSIONS[activite]
```

### Piège 2 — Ne pas initialiser les trois listes (Q2)

```python
# RISQUE : si aucune activité faible, la clé 'faible' n'existe pas
resultat = {}
...
if emission >= 1000: resultat['fort'] = ...  # crée fort seulement si besoin

# CORRECT : toujours les trois clés
resultat = {'fort': [], 'moyen': [], 'faible': []}
```

### Piège 3 — Utiliser > 200 au lieu de >= 200 (Q2)

Les seuils sont inclusifs. Une émission de exactement 200 gCO2e est `'moyen'`, pas `'faible'`.

```python
elif emission > 200:    # FAUX : 200 exactement → faible (incorrect)
elif emission >= 200:   # CORRECT : 200 → moyen
```

### Piège 4 — Tester None avec == au lieu de is (Q4)

```python
assert res['streaming_hd'] == None   # déconseillé
assert res['streaming_hd'] is None   # correct
```

### Piège 5 — Corriger en utilisant continue (Q4)

Utiliser `continue` pour ignorer les activités à `emission1 == 0` fait que ces activités n'apparaissent pas dans le dictionnaire résultat. La fonction `comparer_v2` est censée retourner toutes les activités de `EMISSIONS` — utiliser `None` est plus correct.

---

## PARTIE 7 — RAPPELS DE COURS

### Parcours d'un dictionnaire

```python
for cle in dico:                      # clés seulement
for cle, val in dico.items():         # paires (clé, valeur)
for val in dico.values():             # valeurs seulement
```

### Accès sécurisé à une clé

```python
# Lève KeyError si absent
valeur = dico['cle_inexistante']

# Renvoie la valeur par défaut si absent
valeur = dico.get('cle_inexistante', 0)

# Test d'existence
if 'cle' in dico:
    ...
```

### Construction d'un dictionnaire avec listes

```python
resultat = {'a': [], 'b': [], 'c': []}
resultat['a'].append('valeur1')
resultat['b'].append('valeur2')
```

### ZeroDivisionError et protection

```python
# Pattern standard
if denominateur == 0:
    resultat = None    # ou 0, ou une valeur sentinelle
else:
    resultat = numerateur / denominateur
```

### Assertions dans les tests

```python
assert expression           # AssertionError si False
assert a == b, "message"    # avec message d'erreur
assert val is None          # tester None avec is, pas ==
```

---

## PARTIE 8 — CHECKLIST AVANT DE RENDRE LE CODE

- [ ] Q1 : la boucle parcourt `utilisateur.items()`, pas `EMISSIONS`
- [ ] Q1 : `if activite in EMISSIONS` est présent (sécurité)
- [ ] Q1 : retourne bien un entier (`total = 0`, accumulation entière)
- [ ] Q1 : `calculer_empreinte(utilisateur1) == 7490`
- [ ] Q1 : `calculer_empreinte(utilisateur6) == 0`
- [ ] Q2 : initialisation `{'fort': [], 'moyen': [], 'faible': []}`
- [ ] Q2 : seuils avec `>=` (pas `>`) : `>= 1000` et `>= 200`
- [ ] Q2 : résultat pour utilisateur2 = `{'fort': ['streaming_hd'], 'moyen': ['emails_simples'], 'faible': ['recherches']}`
- [ ] Q3 : au moins 2 assertions ajoutées avec justification commentée
- [ ] Q4 : identification correcte du bug (ZeroDivisionError quand emission1 == 0)
- [ ] Q4 : correction avec `if emission1 == 0: ecarts[activite] = None`
- [ ] Q4 : `comparer_v2(utilisateur4, utilisateur5)` ne lève plus d'erreur

---

## PARTIE 9 — GLOSSAIRE

**gCO2e** : gramme de CO2 équivalent. Unité de mesure des émissions de gaz à effet de serre, qui ramène tous les gaz (CO2, méthane, etc.) à une valeur équivalente en CO2.

**Empreinte carbone numérique** : quantité de CO2 équivalent émise par l'utilisation des services numériques (streaming, email, cloud, etc.).

**`dict.items()`** : méthode Python qui retourne les paires (clé, valeur) d'un dictionnaire, utilisable dans un `for`.

**`dict.get(clé, valeur_par_défaut)`** : méthode d'accès sécurisée à un dictionnaire — retourne la valeur par défaut si la clé est absente, sans lever `KeyError`.

**`ZeroDivisionError`** : exception Python levée lors d'une division par zéro.

**Assertion** : instruction Python `assert condition` qui lève `AssertionError` si la condition est fausse. Utilisée pour les tests.

**Valeur sentinelle** : valeur spéciale (souvent `None`) utilisée pour signifier « résultat non calculable » ou « donnée absente ».

**Impact carbone** : mesure de la contribution d'une activité aux émissions de gaz à effet de serre.

---

*Document produit pour une utilisation pédagogique dans NotebookLM. Lycée Antoine Watteau — DarkSATHI Li*
