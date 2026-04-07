# Fiche NSI Terminale — Températures en Polynésie française
## BAC 2026 — Sujet n°18 — Partie pratique

**Matière :** Numérique et Sciences Informatiques (NSI)  
**Niveau :** Terminale — voie générale  
**Thème du programme :** Traitement de données — listes de dictionnaires, anomalies, division entière, tests unitaires  
**Durée de l'épreuve :** 1 heure  
**Fichier fourni :** `analyse_temperatures_polynesie.py`

---

## Contexte général du sujet

Un réseau de bouées océanographiques mesure quotidiennement la température de surface de l'océan en Polynésie française dans quatre archipels : Société, Tuamotu, Marquises, Australes. L'objectif est d'analyser ces relevés pour documenter le réchauffement climatique.

Le sujet comporte quatre questions :

1. Écrire `temperature_moyenne(zone, donnees)` — moyenne ou `None`
2. Écrire `detecter_anomalies(zone, seuil, donnees)` — liste de dates déviantes
3. Écrire trois fonctions de test pour `evolution_par_decennie` qui **révèlent le bug**
4. Identifier et corriger le bug (`annee // 10` au lieu de `(annee // 10) * 10`)

---

## Partie 1 — Structure des données

### Format d'un relevé

```python
{'date': '2020-08-22', 'zone': 'Societe', 'temperature': 28.5}
```

Chaque relevé est un dictionnaire à trois clés :

| Clé | Type | Exemple | Signification |
|-----|------|---------|---------------|
| `'date'` | str | `'2020-08-22'` | Format AAAA-MM-JJ |
| `'zone'` | str | `'Societe'` | Nom de l'archipel |
| `'temperature'` | float | `28.5` | Température en °C |

### Jeu de données de test — donnees_test

| Zone | Date | Température (°C) | Décennie correcte |
|------|------|------------------|-------------------|
| Société | 2010-01-15 | 27.0 | 2010 |
| Société | 2010-06-20 | 26.5 | 2010 |
| Société | 2011-03-10 | 27.5 | 2010 |
| Société | 2020-02-14 | 28.0 | 2020 |
| Société | 2020-08-22 | 28.5 | 2020 |
| Société | 2021-05-30 | 29.0 | 2020 |
| Tuamotu | 2015-04-10 | 26.8 | 2010 |
| Tuamotu | 2020-07-15 | 27.5 | 2020 |
| Tuamotu | 2021-09-20 | 28.0 | 2020 |
| Marquises | 2020-03-15 | 25.5 | 2020 |
| Marquises | 2021-07-10 | 26.0 | 2020 |
| Marquises | 2022-11-25 | 26.5 | 2020 |

**Note :** la zone Australes n'a aucun relevé dans ce jeu de données — elle sert uniquement à tester le cas d'une zone inexistante.

### Valeurs calculées — à mémoriser pour les tests

| Zone | Moy. globale | Moy. décennie 2010 | Moy. décennie 2020 |
|------|--------------|--------------------|-------------------|
| Société | **(27.0+26.5+27.5+28.0+28.5+29.0)/6 = 27.75** | (27.0+26.5+27.5)/3 = **27.0** | (28.0+28.5+29.0)/3 = **28.5** |
| Tuamotu | (26.8+27.5+28.0)/3 ≈ **27.43** | 26.8/1 = **26.8** | (27.5+28.0)/2 = **27.75** |
| Marquises | (25.5+26.0+26.5)/3 = **26.0** | — | (25.5+26.0+26.5)/3 = **26.0** |
| Australes | **None** | — | — |

---

## Partie 2 — Rappels techniques

### Filtrer et calculer sur une liste de dictionnaires

```python
# Filtrer les relevés d'une zone
releves_zone = [r for r in donnees if r['zone'] == zone]

# Vérifier qu'il y a des données
if not releves_zone:    # liste vide → falsy en Python
    return None

# Extraire les températures
temperatures = [r['temperature'] for r in releves_zone]

# Calculer la moyenne
moyenne = sum(temperatures) / len(temperatures)
```

### Valeur absolue et détection d'anomalie

```python
ecart = abs(temperature - moyenne)
if ecart > seuil:                    # strictement supérieur
    anomalies.append(r['date'])
```

### Extraire l'année d'une date et calculer la décennie

```python
date = "2020-08-22"
annee = int(date.split('-')[0])      # → 2020  (int obligatoire !)

# Calcul de décennie — FORMULE CORRECTE :
decennie = (annee // 10) * 10        # → 2020

# FORMULE BUGUÉE (sujet) :
decennie = (annee // 10)             # → 202  (oubli du * 10)
```

### Table de vérification de la division entière

| Année | `annee // 10` | `(annee // 10) * 10` |
|-------|---------------|----------------------|
| 2010 | 201 ❌ | **2010** ✓ |
| 2015 | 201 ❌ | **2010** ✓ |
| 2019 | 201 ❌ | **2010** ✓ |
| 2020 | 202 ❌ | **2020** ✓ |
| 2023 | 202 ❌ | **2020** ✓ |

---

## Question 1 — temperature_moyenne

### Énoncé

Écrire `temperature_moyenne(zone, donnees)` qui renvoie la température moyenne (float) pour la zone, ou `None` si aucun relevé n'existe.

```python
>>> temperature_moyenne('Societe', donnees_test)
27.75
>>> temperature_moyenne('Australes', donnees_test)
>>>    # renvoie None
```

### Démarche

1. Filtrer : `temperatures = [r['temperature'] for r in donnees if r['zone'] == zone]`
2. Si `not temperatures` → `return None`
3. Renvoyer `sum(temperatures) / len(temperatures)`

### Solution

```python
def temperature_moyenne(zone, donnees):
    """Renvoie la moyenne des températures pour la zone, None si absente."""
    temperatures = [r['temperature'] for r in donnees if r['zone'] == zone]
    if not temperatures:
        return None
    return sum(temperatures) / len(temperatures)
```

### Fonction de test

```python
def test_temperature_moyenne():
    assert temperature_moyenne('Societe',   donnees_test) == 27.75
    assert temperature_moyenne('Marquises', donnees_test) == 26.0
    assert abs(temperature_moyenne('Tuamotu', donnees_test) - 27.4333) < 0.001
    assert temperature_moyenne('Australes', donnees_test) is None
    print("Les tests sont validés.")

test_temperature_moyenne()
```

**Note sur les comparaisons flottantes :**  
- `27.75` = (27.0+26.5+27.5+28.0+28.5+29.0)/6 → représentable exactement → `== 27.75` OK
- `27.433...` = 82.3/3 → non-entier → utiliser `abs(résultat - 27.4333) < 0.001`

---

## Question 2 — detecter_anomalies

### Énoncé

Écrire `detecter_anomalies(zone, seuil, donnees)` qui renvoie la liste des dates dont `abs(température - moyenne) > seuil`. Renvoyer `[]` si la zone n'existe pas.

### Démarche

1. Calculer `moyenne = temperature_moyenne(zone, donnees)` (réutiliser Q1)
2. Si `moyenne is None` → `return []`
3. Parcourir les relevés de la zone, tester `abs(r['temperature'] - moyenne) > seuil`
4. Accumuler les `r['date']` correspondantes

### Anomalies Société, seuil = 1.0 (moy = 27.75)

| Date | Temp. | Écart | Anomalie ? |
|------|-------|-------|-----------|
| 2010-01-15 | 27.0 | 0.75 | Non |
| 2010-06-20 | 26.5 | **1.25** | **Oui** |
| 2011-03-10 | 27.5 | 0.25 | Non |
| 2020-02-14 | 28.0 | 0.25 | Non |
| 2020-08-22 | 28.5 | 0.75 | Non |
| 2021-05-30 | 29.0 | **1.25** | **Oui** |

Résultat : `['2010-06-20', '2021-05-30']`

### Anomalies Marquises, seuil = 0.4 (moy = 26.0)

| Date | Temp. | Écart | Anomalie ? |
|------|-------|-------|-----------|
| 2020-03-15 | 25.5 | **0.5** | **Oui** |
| 2021-07-10 | 26.0 | 0.0 | Non |
| 2022-11-25 | 26.5 | **0.5** | **Oui** |

Résultat : `['2020-03-15', '2022-11-25']`

### Solution

```python
def detecter_anomalies(zone, seuil, donnees):
    moyenne = temperature_moyenne(zone, donnees)
    if moyenne is None:
        return []
    anomalies = []
    for r in donnees:
        if r['zone'] == zone:
            if abs(r['temperature'] - moyenne) > seuil:
                anomalies.append(r['date'])
    return anomalies
```

### Fonction de test

```python
def test_detecter_anomalies():
    assert detecter_anomalies('Societe', 1.0, donnees_test) == ['2010-06-20', '2021-05-30']
    assert detecter_anomalies('Marquises', 0.4, donnees_test) == ['2020-03-15', '2022-11-25']
    assert detecter_anomalies('Australes', 1.0, donnees_test) == []
    assert detecter_anomalies('Societe', 100.0, donnees_test) == []  # seuil infini → vide
    print("Les tests sont validés.")

test_detecter_anomalies()
```

---

## Question 3 — Les trois fonctions de test

### Énoncé

Compléter les trois fonctions de test pour `evolution_par_decennie`. Les tests **doivent révéler le bug** présent dans le code.

### Rappel — code bugué fourni

```python
def evolution_par_decennie(zone, donnees):
    releves_zone = [r for r in donnees if r['zone'] == zone]
    if not releves_zone: return {}
    temperatures_par_decennie = {}
    for releve in releves_zone:
        annee = int(releve['date'].split('-')[0])
        decennie = (annee // 10)          # ← BUG : manque * 10
        if decennie not in temperatures_par_decennie:
            temperatures_par_decennie[decennie] = []
        temperatures_par_decennie[decennie].append(releve['temperature'])
    moyennes = {}
    for decennie, temperatures in temperatures_par_decennie.items():
        moyennes[decennie] = round(sum(temperatures) / len(temperatures), 2)
    return moyennes
```

**Ce que renvoie le code bugué :**
- `evolution_par_decennie('Societe', donnees_test)` → `{201: 27.0, 202: 28.5}` ❌
- `evolution_par_decennie('Marquises', donnees_test)` → `{202: 26.0}` ❌

**Ce qu'il devrait renvoyer :**
- `evolution_par_decennie('Societe', donnees_test)` → `{2010: 27.0, 2020: 28.5}` ✓
- `evolution_par_decennie('Marquises', donnees_test)` → `{2020: 26.0}` ✓

### Stratégie — pourquoi le test 3 révèle le bug, pas le test 1

**Test 1 (zone inexistante)** ne révèle pas le bug : la zone Australes renvoie `{}` bugué ou non.  
**Test 2 (une seule décennie)** révèle le bug : `2020 in resultat` échoue car la clé est `202`.  
**Test 3 (plusieurs décennies)** révèle le bug le plus clairement : les clés `2010` et `2020` sont absentes, remplacées par `201` et `202`.

**Observation clé :** les *valeurs* des moyennes (27.0, 28.5) sont identiques dans les deux versions — seules les *clés* diffèrent. Un test qui ne vérifie pas les clés du dictionnaire ne détecterait pas ce bug.

### Solution — trois fonctions de test

```python
def test_zone_inexistante():
    """Test 1 : zone sans données → dictionnaire vide."""
    resultat = evolution_par_decennie('Australes', donnees_test)
    assert resultat == {}
    print("Test 1 (zone inexistante) : OK")


def test_une_seule_decennie():
    """Test 2 : Marquises → une seule décennie 2020 (pas 202 !), moy = 26.0."""
    resultat = evolution_par_decennie('Marquises', donnees_test)
    assert len(resultat) == 1, f"Attendu 1 décennie, obtenu {len(resultat)}"
    assert 2020 in resultat, \
        f"Clé 2020 absente (clés présentes : {list(resultat.keys())})"
    assert resultat[2020] == 26.0
    print("Test 2 (une seule décennie) : OK")


def test_plusieurs_decennies():
    """Test 3 : Société → décennies 2010 et 2020 (pas 201 et 202 !), moy 27.0 et 28.5."""
    resultat = evolution_par_decennie('Societe', donnees_test)
    assert len(resultat) == 2, f"Attendu 2 décennies, obtenu {len(resultat)}"
    assert 2010 in resultat, \
        f"Clé 2010 absente (clés présentes : {list(resultat.keys())})"
    assert 2020 in resultat, \
        f"Clé 2020 absente (clés présentes : {list(resultat.keys())})"
    assert resultat[2010] == 27.0
    assert resultat[2020] == 28.5
    print("Test 3 (plusieurs décennies) : OK")
```

**Pourquoi les messages d'assertion sont importants :**  
`assert 2010 in resultat, f"Clé 2010 absente (clés présentes : {list(resultat.keys())})"` affiche `"Clé 2010 absente (clés présentes : [201, 202])"` — ce qui pointe directement vers le bug du `* 10` manquant.

---

## Question 4 — Identifier et corriger le bug

### Identification précise

**Ligne buguée (ligne du calcul de décennie) :**

```python
decennie = (annee // 10)       # FAUX — donne le quotient (201, 202)
```

**Explication :**
- `//` est la division entière euclidienne
- `2010 // 10 = 201` : nombre de décennies depuis l'an 0
- Pour retrouver l'année de début de la décennie, il faut *remettre à l'échelle* : `201 × 10 = 2010`

### Correction — une seule ligne à modifier

```python
# AVANT (bugué) :
decennie = (annee // 10)

# APRÈS (corrigé) :
decennie = (annee // 10) * 10
```

### Vérification de la correction

```python
# Toutes les années de la décennie 2010 → clé 2010
(2010 // 10) * 10 = 201 * 10 = 2010  ✓
(2015 // 10) * 10 = 201 * 10 = 2010  ✓
(2019 // 10) * 10 = 201 * 10 = 2010  ✓

# Toutes les années de la décennie 2020 → clé 2020
(2020 // 10) * 10 = 202 * 10 = 2020  ✓
(2021 // 10) * 10 = 202 * 10 = 2020  ✓
(2022 // 10) * 10 = 202 * 10 = 2020  ✓
```

### Résultats avant/après correction

| Zone | Version buguée | Version corrigée |
|------|----------------|-----------------|
| Société | `{201: 27.0, 202: 28.5}` ❌ | `{2010: 27.0, 2020: 28.5}` ✓ |
| Tuamotu | `{201: 26.8, 202: 27.75}` ❌ | `{2010: 26.8, 2020: 27.75}` ✓ |
| Marquises | `{202: 26.0}` ❌ | `{2020: 26.0}` ✓ |
| Australes | `{}` | `{}` (identique) |

**Observation importante :** les valeurs (moyennes) sont identiques dans les deux versions. Seules les clés changent. C'est pourquoi un test qui ne vérifie que les valeurs ne détecte pas ce bug.

### Propriété générale — arrondi à une granularité quelconque

```python
# Arrondir à la décennie :
(annee // 10) * 10

# Arrondir au siècle :
(annee // 100) * 100

# Arrondir à 5 unités près :
(valeur // 5) * 5

# Principe : (valeur // granularité) * granularité
```

### Code complet corrigé — evolution_par_decennie

```python
def evolution_par_decennie(zone, donnees):
    """
    Calcule l'évolution des températures moyennes par décennie pour une zone.
    Renvoie {décennie: température_moyenne} ou {} si la zone est absente.
    """
    releves_zone = [r for r in donnees if r['zone'] == zone]

    if not releves_zone:
        return {}

    temperatures_par_decennie = {}

    for releve in releves_zone:
        annee = int(releve['date'].split('-')[0])
        decennie = (annee // 10) * 10    # CORRIGÉ : * 10 ajouté

        if decennie not in temperatures_par_decennie:
            temperatures_par_decennie[decennie] = []

        temperatures_par_decennie[decennie].append(releve['temperature'])

    moyennes = {}
    for decennie, temperatures in temperatures_par_decennie.items():
        moyennes[decennie] = round(sum(temperatures) / len(temperatures), 2)

    return moyennes
```

---

## Code complet corrigé — analyse_temperatures_polynesie.py

```python
donnees_test = [
    {'date': '2010-01-15', 'zone': 'Societe',   'temperature': 27.0},
    {'date': '2010-06-20', 'zone': 'Societe',   'temperature': 26.5},
    {'date': '2011-03-10', 'zone': 'Societe',   'temperature': 27.5},
    {'date': '2020-02-14', 'zone': 'Societe',   'temperature': 28.0},
    {'date': '2020-08-22', 'zone': 'Societe',   'temperature': 28.5},
    {'date': '2021-05-30', 'zone': 'Societe',   'temperature': 29.0},
    {'date': '2015-04-10', 'zone': 'Tuamotu',   'temperature': 26.8},
    {'date': '2020-07-15', 'zone': 'Tuamotu',   'temperature': 27.5},
    {'date': '2021-09-20', 'zone': 'Tuamotu',   'temperature': 28.0},
    {'date': '2020-03-15', 'zone': 'Marquises', 'temperature': 25.5},
    {'date': '2021-07-10', 'zone': 'Marquises', 'temperature': 26.0},
    {'date': '2022-11-25', 'zone': 'Marquises', 'temperature': 26.5},
]


def temperature_moyenne(zone, donnees):                       # Q1
    temperatures = [r['temperature'] for r in donnees if r['zone'] == zone]
    if not temperatures:
        return None
    return sum(temperatures) / len(temperatures)


def detecter_anomalies(zone, seuil, donnees):                 # Q2
    moyenne = temperature_moyenne(zone, donnees)
    if moyenne is None:
        return []
    anomalies = []
    for r in donnees:
        if r['zone'] == zone:
            if abs(r['temperature'] - moyenne) > seuil:
                anomalies.append(r['date'])
    return anomalies


def evolution_par_decennie(zone, donnees):                    # Q4 corrigée
    releves_zone = [r for r in donnees if r['zone'] == zone]
    if not releves_zone:
        return {}
    temperatures_par_decennie = {}
    for releve in releves_zone:
        annee = int(releve['date'].split('-')[0])
        decennie = (annee // 10) * 10    # corrigé
        if decennie not in temperatures_par_decennie:
            temperatures_par_decennie[decennie] = []
        temperatures_par_decennie[decennie].append(releve['temperature'])
    moyennes = {}
    for decennie, temperatures in temperatures_par_decennie.items():
        moyennes[decennie] = round(sum(temperatures) / len(temperatures), 2)
    return moyennes


def test_zone_inexistante():                                  # Q3 — Test 1
    resultat = evolution_par_decennie('Australes', donnees_test)
    assert resultat == {}
    print("Test 1 (zone inexistante) : OK")


def test_une_seule_decennie():                                # Q3 — Test 2
    resultat = evolution_par_decennie('Marquises', donnees_test)
    assert len(resultat) == 1
    assert 2020 in resultat
    assert resultat[2020] == 26.0
    print("Test 2 (une seule décennie) : OK")


def test_plusieurs_decennies():                               # Q3 — Test 3
    resultat = evolution_par_decennie('Societe', donnees_test)
    assert len(resultat) == 2
    assert 2010 in resultat
    assert 2020 in resultat
    assert resultat[2010] == 27.0
    assert resultat[2020] == 28.5
    print("Test 3 (plusieurs décennies) : OK")


test_zone_inexistante()
test_une_seule_decennie()
test_plusieurs_decennies()
```

---

## Pièges fréquents

### Piège 1 — Oublier * 10 dans le calcul de décennie

```python
# FAUX — donne 201, 202 (quotient de la division)
decennie = annee // 10

# JUSTE — donne 2010, 2020 (début de la décennie)
decennie = (annee // 10) * 10
```

Ce bug est particulièrement traître : aucune erreur Python, les moyennes sont correctes, seules les clés sont fausses.

### Piège 2 — Tester les valeurs mais pas les clés

```python
# INSUFFISANT — passe même avec le bug car les valeurs sont identiques
assert list(resultat.values()) == [27.0, 28.5]

# NÉCESSAIRE — échoue avec le bug car les clés sont fausses
assert 2010 in resultat
assert 2020 in resultat
```

### Piège 3 — Utiliser == None au lieu de is None

```python
# DÉCONSEILLÉ
if moyenne == None:

# IDIOMATIQUE
if moyenne is None:
```

### Piège 4 — Oublier int() sur le résultat de split

```python
# FAUX — TypeError : can't divide str by int
annee = date.split('-')[0]    # "2020" (chaîne)
decennie = annee // 10        # TypeError !

# JUSTE
annee = int(date.split('-')[0])   # 2020 (entier)
decennie = (annee // 10) * 10     # 2020
```

### Piège 5 — Comparer des flottants non-entiers avec ==

```python
# DANGEREUX pour les fractions (ex: 82.3/3 = 27.433...)
assert temperature_moyenne('Tuamotu', donnees_test) == 27.43   # peut échouer

# ROBUSTE
assert abs(temperature_moyenne('Tuamotu', donnees_test) - 27.43) < 0.01

# SAFE pour les entiers exacts (27.0, 28.5, 26.0...)
assert temperature_moyenne('Societe', donnees_test) == 27.75   # OK
```

---

## Astuces de vérification

### Invariants à tester pour detecter_anomalies

```python
# Seuil infini → aucune anomalie
assert detecter_anomalies(zone, 1000.0, donnees) == []

# Zone inexistante → liste vide (pas None, pas d'exception)
assert detecter_anomalies('ZoneInexistante', 1.0, donnees) == []

# La liste résultat a au plus autant d'éléments que de relevés dans la zone
assert len(detecter_anomalies(zone, seuil, donnees)) <= len([r for r in donnees if r['zone'] == zone])
```

### Invariants à tester pour evolution_par_decennie

```python
# Toutes les clés doivent être multiples de 10
resultat = evolution_par_decennie(zone, donnees)
for cle in resultat:
    assert cle % 10 == 0, f"Clé {cle} n'est pas un multiple de 10 !"

# Toutes les valeurs doivent être entre les températures min et max de la zone
```

### Calcul manuel de vérification rapide

Pour vérifier une moyenne à la main sans additionner tous les nombres :
- Société décennie 2010 : (27.0 + 26.5 + 27.5) / 3 = 81.0 / 3 = **27.0** ✓
- Société décennie 2020 : (28.0 + 28.5 + 29.0) / 3 = 85.5 / 3 = **28.5** ✓
- Marquises décennie 2020 : (25.5 + 26.0 + 26.5) / 3 = 78.0 / 3 = **26.0** ✓

---

## Mini-exercices

### Exercice A — Calcul mental de décennie

Calculer `(annee // 10) * 10` pour chaque année :

| Année | Calcul | Décennie |
|-------|--------|---------|
| 1999 | (199) × 10 | **1990** |
| 2000 | (200) × 10 | **2000** |
| 2009 | (200) × 10 | **2000** |
| 2024 | (202) × 10 | **2020** |
| 2030 | (203) × 10 | **2030** |

### Exercice B — Anomalies Tuamotu, seuil 0.5 (moy ≈ 27.43)

| Date | Temp. | Écart = |t – 27.43| | Anomalie ? |
|------|-------|----------------------|-----------|
| 2015-04-10 | 26.8 | 0.63 | **Oui** |
| 2020-07-15 | 27.5 | 0.07 | Non |
| 2021-09-20 | 28.0 | 0.57 | **Oui** |

Résultat : `['2015-04-10', '2021-09-20']`

### Exercice C — Que révèle chaque test ?

| Test | Zone testée | Révèle le bug ? | Pourquoi |
|------|-------------|-----------------|---------|
| `test_zone_inexistante` | Australes | Non | `{}` bugué ou non |
| `test_une_seule_decennie` | Marquises | **Oui** | `2020 in resultat` échoue (clé = 202) |
| `test_plusieurs_decennies` | Société | **Oui** | `2010 in resultat` et `2020 in resultat` échouent |

---

## Récapitulatif — Points clés à retenir

| Notion | Retenir |
|--------|---------|
| Filtrer une liste de dicts | `[r for r in donnees if r['zone'] == zone]` |
| Zone absente → None | Tester `if not liste_filtree: return None` |
| Vérifier None | `is None` (pas `== None`) |
| Valeur absolue | `abs(temperature - moyenne) > seuil` |
| Extraire l'année | `int(date.split('-')[0])` — le `int()` est obligatoire |
| Calcul de décennie | `(annee // 10) * 10` — ne jamais oublier `* 10` |
| Bug du sujet | `annee // 10` seul → clés `201`/`202` au lieu de `2010`/`2020` |
| Ce que révèle les tests | Tester les **clés** du dictionnaire, pas seulement les valeurs |
| Flottants non-entiers | Éviter `==` → utiliser `abs(a - b) < ε` |

---

*Lycée Antoine Watteau — DarkSATHI Li — BAC NSI 2026 — Sujet n°18*
