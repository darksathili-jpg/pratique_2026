# Fiche NSI Terminale — Analyse de consommation d'eau
## BAC 2026 — Sujet n°10 — Partie pratique

**Matière :** Numérique et Sciences Informatiques (NSI)  
**Niveau :** Terminale — voie générale  
**Thème du programme :** Traitement de données — listes de dictionnaires, débogage, cas limites  
**Durée de l'épreuve :** 1 heure  
**Fichier fourni :** `analyse_eau.py`

---

## Contexte général du sujet

Des compteurs d'eau intelligents enregistrent, chaque heure, la consommation d'eau chaude et d'eau froide d'un foyer. Les données sont stockées sous forme d'une **liste de dictionnaires**, triée par jour et heure croissants.

Le sujet comporte quatre questions :

1. Calculer la consommation totale d'un jour donné (`total_conso`)
2. Détecter une fuite nocturne par séquence consécutive (`fuite_possible`)
3. Identifier et corriger le bug dans `lissage_conso` (mauvais diviseur)
4. Identifier un cas limite supplémentaire non géré par `lissage_conso` (liste à un seul élément)

---

## Partie 1 — Structure des données

### Format d'une mesure

Chaque mesure est un dictionnaire Python à quatre clés :

```python
{"jour": "2025-02-04", "heure": "08:00", "chaude": 5, "froide": 8}
```

| Clé | Type | Exemple | Signification |
|-----|------|---------|---------------|
| `"jour"` | str | `"2025-02-04"` | Date au format AAAA-MM-JJ |
| `"heure"` | str | `"08:00"` | Heure au format HH:MM |
| `"chaude"` | int | `5` | Litres d'eau chaude depuis la mesure précédente |
| `"froide"` | int | `8` | Litres d'eau froide depuis la mesure précédente |

La **consommation totale** d'une mesure = `m["chaude"] + m["froide"]`.

### Données fournies dans analyse_eau.py

**Jour 2025-02-04 (8 mesures) :**

| Heure | Chaude | Froide | Total |
|-------|--------|--------|-------|
| 00:00 | 2 | 3 | **5** |
| 01:00 | 1 | 2 | **3** |
| 02:00 | 0 | 0 | 0 |
| 03:00 | 0 | 0 | 0 |
| 04:00 | 0 | 1 | **1** |
| 05:00 | 0 | 0 | 0 |
| 06:00 | 4 | 6 | **10** |
| 07:00 | 6 | 8 | **14** |

Total du jour : 5+3+0+0+1+0+10+14 = **33 litres**

**Jour 2025-02-05 (6 mesures) :**

| Heure | Chaude | Froide | Total | Note |
|-------|--------|--------|-------|------|
| 00:00 | 0 | 0 | 0 | |
| 01:00 | 1 | 1 | **2** | ← 3 mesures |
| 02:00 | 1 | 1 | **2** | ← consécutives |
| 03:00 | 1 | 1 | **2** | ← non nulles |
| 04:00 | 0 | 0 | 0 | |
| 05:00 | 0 | 0 | 0 | |

Total du jour : 0+2+2+2+0+0 = **6 litres**. Fuite possible : **True**.

---

## Partie 2 — Patrons algorithmiques du sujet

### Patron 1 — Somme conditionnelle avec drapeau None

```python
total = 0
trouve = False
for m in donnees:
    if m["jour"] == jour:
        total += m["chaude"] + m["froide"]
        trouve = True
if not trouve:
    return None
return total
```

**Pourquoi un drapeau et pas `total == 0` ?**  
Un jour avec zéro consommation donne `total = 0` mais est un jour *connu*. Un jour inexistant est *inconnu*. Ces deux cas sont différents et ne doivent pas retourner la même valeur.

### Patron 2 — Compteur de séquence consécutive

Pour détecter N occurrences consécutives d'une condition :

```python
compteur = 0
for valeur in liste:
    if condition(valeur):
        compteur += 1
        if compteur >= N:
            return True    # seuil atteint
    else:
        compteur = 0       # réinitialisation obligatoire
return False
```

**Point critique :** la réinitialisation `compteur = 0` dans le `else` est indispensable. Sans elle, on compterait des occurrences non-consécutives.

### Patron 3 — Gardes en entrée de fonction (early returns)

Pour gérer les cas limites avant la logique principale :

```python
def ma_fonction(liste):
    if len(liste) == 0:
        return []          # cas limite : liste vide
    if len(liste) == 1:
        return [traiter(liste[0])]  # cas limite : singleton
    # ... logique principale inchangée ...
```

---

## Question 1 — total_conso

### Énoncé

Écrire `total_conso(donnees, jour)` qui renvoie la consommation totale (chaude + froide) pour toutes les mesures du jour donné. Renvoyer `None` si aucune mesure n'existe pour ce jour.

```python
>>> total_conso(donnees, "2025-02-04")
33
>>> total_conso(donnees, "2025-12-25")
>>>     # renvoie None (rien affiché)
```

### Démarche

1. Initialiser `total = 0` et `trouve = False`
2. Parcourir `donnees` avec `for m in donnees`
3. Si `m["jour"] == jour` : ajouter `m["chaude"] + m["froide"]` à `total`, mettre `trouve = True`
4. Après la boucle : si `not trouve`, renvoyer `None` ; sinon renvoyer `total`

### Solution

```python
def total_conso(donnees, jour):
    total = 0
    trouve = False
    for m in donnees:
        if m["jour"] == jour:
            total += m["chaude"] + m["froide"]
            trouve = True
    if not trouve:
        return None
    return total
```

### Fonction de test

```python
def test_total_conso():
    assert total_conso(donnees, "2025-02-04") == 33
    assert total_conso(donnees, "2025-02-05") == 6
    assert total_conso(donnees, "2025-12-25") is None
    print("Les tests sont validés.")

test_total_conso()
```

**Vérification manuelle 04/02 :**  
(2+3) + (1+2) + 0 + 0 + (0+1) + 0 + (4+6) + (6+8) = 5+3+0+0+1+0+10+14 = **33** ✓

**Vérification manuelle 05/02 :**  
0 + (1+1) + (1+1) + (1+1) + 0 + 0 = 0+2+2+2+0+0 = **6** ✓

---

## Question 2 — fuite_possible

### Énoncé

Écrire `fuite_possible(donnees, jour)` qui renvoie `True` si au moins 3 mesures consécutives entre `"00:00"` et `"05:00"` **inclus** ont une consommation totale strictement positive, `False` sinon.

### Exemples de l'énoncé

| Séquence nocturne | 3 consécutifs ? | Résultat |
|-------------------|-----------------|----------|
| 5, 3, **0**, 3 | Non (brisé par 0) | `False` |
| **2, 1, 1**, 0 | Oui (dès le début) | `True` |

### Démarche

1. Initialiser `consec = 0`
2. Boucler sur les mesures avec double filtre : `m["jour"] == jour` **ET** `m["heure"] <= "05:00"`
3. Pour chaque mesure filtrée, calculer `conso = m["chaude"] + m["froide"]`
4. Si `conso > 0` : incrémenter `consec`, tester `consec >= 3` → `return True`
5. Sinon : `consec = 0` (réinitialisation)
6. Après la boucle : `return False`

**Pourquoi comparer les heures comme des chaînes ?**  
Le format `"HH:MM"` garantit que l'ordre alphabétique = ordre chronologique (toutes les heures sont sur 2 chiffres). `"05:00" < "06:00"` est vrai en Python — propriété du format ISO 8601.

### Solution

```python
def fuite_possible(donnees, jour):
    consec = 0
    for m in donnees:
        if m["jour"] == jour and m["heure"] <= "05:00":
            conso = m["chaude"] + m["froide"]
            if conso > 0:
                consec += 1
                if consec >= 3:
                    return True
            else:
                consec = 0    # réinitialisation indispensable
    return False
```

### Fonction de test

```python
def test_fuite_possible():
    # 04/02 : séquence nocturne 5,3,0,0,1,0 → pas 3 consécutifs → False
    assert fuite_possible(donnees, "2025-02-04") == False
    # 05/02 : séquence nocturne 0,2,2,2,0,0 → 3 consécutifs (01h→03h) → True
    assert fuite_possible(donnees, "2025-02-05") == True
    # Jour inexistant → aucune mesure → False
    assert fuite_possible(donnees, "2025-12-25") == False
    print("Les tests sont validés.")

test_fuite_possible()
```

**Trace détaillée pour 05/02 :**

| Heure | Conso | consec | Action |
|-------|-------|--------|--------|
| 00:00 | 0 | 0 | réinit → 0 |
| 01:00 | 2 | 1 | +1 → 1 |
| 02:00 | 2 | 2 | +1 → 2 |
| 03:00 | 2 | 3 | +1 → **3 ≥ 3 → True** |

---

## Question 3 — Analyser et corriger lissage_conso

### Code fourni (bugué)

```python
def lissage_conso(valeurs):
    lisse = []
    for i in range(len(valeurs)):
        if i == 0:
            m = (valeurs[i] + valeurs[i+1]) / 2
        elif i == len(valeurs)-1:
            m = (valeurs[i-1] + valeurs[i]) / 2
        else:
            m = (valeurs[i-1] + valeurs[i] + valeurs[i+1]) / 2   # ← BUG
        lisse.append(m)
    return lisse
```

### Identification du bug

Le cas intermédiaire (`else`) additionne **3 valeurs** (précédente, actuelle, suivante) mais divise par **2** au lieu de **3**.

**Exemple avec `i = 2` sur `[10, 20, 30, 40, 50]` :**

```
Code bugué  : (20 + 30 + 40) / 2 = 45.0   ← FAUX
Valeur juste: (20 + 30 + 40) / 3 = 30.0   ← ATTENDU
```

### Résultats attendus vs obtenus sur [10, 20, 30, 40, 50]

| Index | Calcul | Attendu | Obtenu (bugué) |
|-------|--------|---------|----------------|
| 0 (bord) | (10+20)/2 | **15.0** | 15.0 ✓ |
| 1 (inter.) | (10+20+30)/3 | **20.0** | 30.0 ❌ |
| 2 (inter.) | (20+30+40)/3 | **30.0** | 45.0 ❌ |
| 3 (inter.) | (30+40+50)/3 | **40.0** | 60.0 ❌ |
| 4 (bord) | (40+50)/2 | **45.0** | 45.0 ✓ |

Résultat attendu : `[15.0, 20.0, 30.0, 40.0, 45.0]`  
Résultat bugué : `[15.0, 30.0, 45.0, 60.0, 45.0]`

### Correction

Une seule modification : changer `/2` en `/3` dans le bloc `else`.

```python
else:
    m = (valeurs[i-1] + valeurs[i] + valeurs[i+1]) / 3   # /2 → /3
```

### Stratégie de test — 3 tests révélant l'erreur

```python
def test_lissage():
    # Test 1 : valeur intermédiaire — révèle directement le /2 vs /3
    assert lissage_conso([10, 20, 30, 40, 50]) == [15.0, 20.0, 30.0, 40.0, 45.0]
    # Test 2 : valeurs identiques → lissage transparent (invariant)
    assert lissage_conso([5, 5, 5, 5]) == [5.0, 5.0, 5.0, 5.0]
    # Test 3 : deux valeurs → teste uniquement les bords (correct même dans la version buguée)
    assert lissage_conso([4, 8]) == [6.0, 6.0]
    print("Les tests sont validés.")

test_lissage()
```

**Pourquoi le test `[5, 5, 5, 5]` est-il particulièrement fort ?**  
La moyenne de valeurs identiques est toujours la même valeur, quel que soit le diviseur utilisé. Ce test ne révèle donc *pas* le bug de diviseur — c'est le test 1 qui le révèle. En revanche, le test des valeurs identiques vérifie la *stabilité* du lissage : un signal constant ne doit pas être modifié.

---

## Question 4 — Cas limite oublié

### Cas déjà géré : liste de deux valeurs

Avec `[a, b]` :
- Index 0 → `i == 0` → `(a + b) / 2` ✓
- Index 1 → `i == len(valeurs)-1` (car `len == 2`) → `(a + b) / 2` ✓

Pas de problème.

### Cas limite oublié : liste à un seul élément `[x]`

Avec `[42]`, l'index 0 déclenche `i == 0`, qui calcule :
```python
m = (valeurs[0] + valeurs[1]) / 2
#                   ↑
#          IndexError ! len([42]) == 1, valeurs[1] n'existe pas.
```

**Conséquence :** `lissage_conso([42])` lève une `IndexError` sans prévenir.

### Cas limite bonus : liste vide `[]`

Avec `[]`, `range(len([]))` = `range(0)` → la boucle ne s'exécute pas → renvoie `[]` silencieusement. Ce n'est pas une erreur Python, mais le comportement n'est pas documenté.

### Solution — gardes en entrée de fonction

```python
def lissage_conso(valeurs):
    if len(valeurs) == 0:          # cas limite : liste vide
        return []
    if len(valeurs) == 1:          # cas limite : singleton → la moyenne d'un seul élément, c'est lui-même
        return [float(valeurs[0])]

    lisse = []
    for i in range(len(valeurs)):
        if i == 0:
            m = (valeurs[i] + valeurs[i+1]) / 2
        elif i == len(valeurs)-1:
            m = (valeurs[i-1] + valeurs[i]) / 2
        else:
            m = (valeurs[i-1] + valeurs[i] + valeurs[i+1]) / 3   # corrigé
        lisse.append(m)
    return lisse
```

### Fonction de test complète (Q3 + Q4 combinés)

```python
def test_lissage_complet():
    # Cas normaux (Q3)
    assert lissage_conso([10, 20, 30, 40, 50]) == [15.0, 20.0, 30.0, 40.0, 45.0]
    assert lissage_conso([5, 5, 5, 5]) == [5.0, 5.0, 5.0, 5.0]
    assert lissage_conso([4, 8]) == [6.0, 6.0]
    # Cas limites (Q4)
    assert lissage_conso([]) == []
    assert lissage_conso([42]) == [42.0]
    # Test de taille : toujours conservée
    for n in range(6):
        v = list(range(n))
        assert len(lissage_conso(v)) == n
    print("Les tests sont validés.")

test_lissage_complet()
```

---

## Code complet corrigé — analyse_eau.py

```python
donnees = [
    {"jour": "2025-02-04", "heure": "00:00", "chaude": 2, "froide": 3},
    {"jour": "2025-02-04", "heure": "01:00", "chaude": 1, "froide": 2},
    {"jour": "2025-02-04", "heure": "02:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "03:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "04:00", "chaude": 0, "froide": 1},
    {"jour": "2025-02-04", "heure": "05:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "06:00", "chaude": 4, "froide": 6},
    {"jour": "2025-02-04", "heure": "07:00", "chaude": 6, "froide": 8},
    {"jour": "2025-02-05", "heure": "00:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-05", "heure": "01:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "02:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "03:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "04:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-05", "heure": "05:00", "chaude": 0, "froide": 0},
]


def total_conso(donnees, jour):                          # Q1
    total = 0
    trouve = False
    for m in donnees:
        if m["jour"] == jour:
            total += m["chaude"] + m["froide"]
            trouve = True
    if not trouve:
        return None
    return total


def fuite_possible(donnees, jour):                       # Q2
    consec = 0
    for m in donnees:
        if m["jour"] == jour and m["heure"] <= "05:00":
            conso = m["chaude"] + m["froide"]
            if conso > 0:
                consec += 1
                if consec >= 3:
                    return True
            else:
                consec = 0
    return False


def lissage_conso(valeurs):                              # Q3 + Q4
    if len(valeurs) == 0:
        return []
    if len(valeurs) == 1:
        return [float(valeurs[0])]
    lisse = []
    for i in range(len(valeurs)):
        if i == 0:
            m = (valeurs[i] + valeurs[i+1]) / 2
        elif i == len(valeurs)-1:
            m = (valeurs[i-1] + valeurs[i]) / 2
        else:
            m = (valeurs[i-1] + valeurs[i] + valeurs[i+1]) / 3   # corrigé : /3
        lisse.append(m)
    return lisse


def test_lissage():                                      # tests demandés en Q3
    assert lissage_conso([10, 20, 30, 40, 50]) == [15.0, 20.0, 30.0, 40.0, 45.0]
    assert lissage_conso([5, 5, 5, 5]) == [5.0, 5.0, 5.0, 5.0]
    assert lissage_conso([4, 8]) == [6.0, 6.0]
    assert lissage_conso([]) == []
    assert lissage_conso([42]) == [42.0]
    print("Les tests sont validés.")

test_lissage()
```

---

## Pièges fréquents

### Piège 1 — Renvoyer 0 au lieu de None

```python
# FAUX — confond "pas de données" avec "zéro litre consommé"
if total == 0:
    return None   # un jour avec conso nulle existerait aussi !

# JUSTE — utiliser un drapeau booléen
if not trouve:
    return None
```

### Piège 2 — Oublier la réinitialisation du compteur

```python
# FAUX — compte des occurrences non-consécutives
if conso > 0:
    consec += 1

# JUSTE — remettre à zéro dès qu'on voit un 0
if conso > 0:
    consec += 1
else:
    consec = 0   # indispensable !
```

**Impact :** sur `[5, 3, 0, 0, 1, 0]` (données du 04/02), sans réinitialisation, `consec` atteindrait 3 après les positions 0, 1, 4 — résultat `True` à tort.

### Piège 3 — Ne pas filtrer sur l'heure dans fuite_possible

Les données du 04/02 ont des consommations élevées à 06:00 et 07:00. Sans `m["heure"] <= "05:00"`, ces mesures matinales entrent dans le compteur et peuvent déclencher un faux positif.

### Piège 4 — Bug de lissage : diviseur 2 vs 3 (discret mais systématique)

Le code bugué donne des résultats numériquement plausibles (juste trop grands), ce qui le rend difficile à détecter sans test rigoureux. Les bords (index 0 et dernier) sont **corrects**, seuls les éléments intermédiaires sont faux. Un test portant uniquement sur les bords passerait sans révéler le bug.

**Règle :** toujours tester au moins une valeur intermédiaire pour les fonctions de lissage.

### Piège 5 — Oublier le cas limite singleton dans lissage_conso

```python
lissage_conso([42])
# Sans garde : IndexError (valeurs[1] n'existe pas)
# Avec garde  : [42.0]
```

Python ne lève pas d'avertissement avant l'erreur. La seule protection est le test explicite.

---

## Astuces de vérification

### Invariant de taille pour lissage

```python
# La liste résultat doit toujours avoir la même longueur que l'entrée
for n in [0, 1, 2, 3, 10]:
    v = list(range(n))
    assert len(lissage_conso(v)) == n
```

### Invariant de stabilité pour lissage

```python
# Un signal constant ne doit pas être modifié par le lissage
for k in [0, 1, 5, 100]:
    v = [k] * 10
    assert lissage_conso(v) == [float(k)] * 10
```

### Test de l'heure limite 05:00

```python
# Vérifier que 05:00 est INCLUS (l'énoncé dit "inclus")
donnees_test = [
    {"jour": "2026-01-01", "heure": "03:00", "chaude": 1, "froide": 0},
    {"jour": "2026-01-01", "heure": "04:00", "chaude": 1, "froide": 0},
    {"jour": "2026-01-01", "heure": "05:00", "chaude": 1, "froide": 0},   # doit être compté
    {"jour": "2026-01-01", "heure": "06:00", "chaude": 1, "froide": 0},   # ne doit pas l'être
]
assert fuite_possible(donnees_test, "2026-01-01") == True
```

### Vérification manuelle de total_conso

Pour le 04/02 :  
(2+3) + (1+2) + (0+0) + (0+0) + (0+1) + (0+0) + (4+6) + (6+8) = **5 + 3 + 0 + 0 + 1 + 0 + 10 + 14 = 33** ✓

---

## Mini-exercices

### Exercice A — Tracer la détection de fuite

Pour chaque séquence de consommations nocturnes, donner le résultat de `fuite_possible` et tracer l'évolution du compteur :

| Séquence | Trace du compteur | Résultat |
|----------|-------------------|----------|
| `[0, 1, 2, 0, 3, 4, 5]` | 0→0, 1→1, 2→2, 0→0, 3→1, 4→2, 5→3 ≥ 3 | **True** |
| `[1, 2, 3, 0, 0, 0]` | 1→1, 2→2, 3→3 ≥ 3 | **True** |
| `[0, 0, 0, 1, 2, 3]` | 0→0, 0→0, 0→0, 1→1, 2→2, 3→3 ≥ 3 | **True** |
| `[1, 2, 0, 1, 2, 0]` | 1→1, 2→2, 0→0, 1→1, 2→2, 0→0 | **False** |

### Exercice B — Lissage mental

Calculer `lissage_conso([0, 6, 0])` (version corrigée) :

- Index 0 (bord) : (0 + 6) / 2 = **3.0**
- Index 1 (inter.) : (0 + 6 + 0) / 3 = **2.0**
- Index 2 (bord) : (6 + 0) / 2 = **3.0**

Résultat : `[3.0, 2.0, 3.0]` — le pic à 6 est atténué à 3 aux bords et 2 au centre.

### Exercice C — Chasse aux cas limites

Pour chacune de ces fonctions, donner le cas limite le plus dangereux et sa correction :

| Fonction | Cas limite dangereux | Correction |
|----------|---------------------|------------|
| `total_conso` | Jour inexistant → renvoie 0 au lieu de None | Utiliser un drapeau booléen |
| `fuite_possible` | Réinitialisation oubliée → faux positifs | Ajouter `consec = 0` dans le `else` |
| `lissage_conso` | Liste à un élément → `IndexError` | Ajouter garde `if len == 1` |

---

## Récapitulatif — Points clés à retenir

| Notion | Retenir |
|--------|---------|
| Accès dictionnaire | `m["clé"]` — guillemets obligatoires, casse exacte, pas d'espace |
| Valeur manquante | Renvoyer `None` (et non `0`) quand le jour n'existe pas dans les données |
| Séquence consécutive | Compteur + réinitialisation dans le `else` — patron universel |
| Comparaison heure | Format `"HH:MM"` → ordre alphabétique = ordre chronologique |
| Bug lissage Q3 | Cas `else` divise par `2` au lieu de `3` — somme de 3 termes |
| Cas limite Q4 | `[x]` (singleton) → `IndexError` sur `valeurs[1]` — ajouter une garde |
| Gardes (early return) | Traiter les cas limites *avant* la boucle principale, pas dedans |
| Non-régression | Après correction, relancer les tests existants pour ne rien avoir cassé |

---

*Lycée Antoine Watteau — DarkSATHI Li — BAC NSI 2026 — Sujet n°10*
