# Fiche de révision — BAC NSI 2026 — Sujet n°17 : Budget Club de Handball

**Niveau :** Terminale NSI  
**Thèmes :** Fichiers CSV · Filtrage de listes · Fonctions de test · Débogage · `range()`  
**Source :** Épreuve pratique BAC NSI 2026, sujet n°17  
**Lycée Antoine Watteau — DarkSATHI Li**

---

## Analyse critique — Bug identifié dans le code fourni

La fonction `solde_annuel` contient une erreur classique sur `range()` :

```python
def solde_annuel(mouvements):
    total = 0
    for m in range(1, 12):   # ← BUG : range(1, 12) génère 1 à 11 seulement
        total = total + solde_mensuel(mouvements, m)
    return total
```

`range(1, 12)` génère `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]`. **Le mois 12 (décembre) est silencieusement ignoré.**

| Jeu de données | Résultat bugué | Résultat correct | Écart |
|---|---|---|---|
| mouvements_test | 1 050,0 € | **150,0 €** | −900,0 € |
| budget_complet.csv | ~14 315 € | **−3 423,17 €** | −17 738,54 € |

**Correction :** remplacer `range(1, 12)` par `range(1, 13)`.

---

## Contexte du sujet

Un club de handball souhaite analyser ses dépenses et recettes annuelles. Les données sont stockées dans des fichiers CSV représentant des mouvements budgétaires. Le programme `analyse_budget.py` contient des fonctions à compléter et une fonction buguée à corriger.

---

## Rappels de cours indispensables

### Filtrer une liste de dictionnaires

```python
# Calculer la somme des montants de type 'recette'
total = 0.0
for m in mouvements:
    if m['type'] == 'recette':     # filtre sur la clé 'type'
        total += m['montant']

# Version compacte avec sum() et expression génératrice
total = sum(m['montant'] for m in mouvements if m['type'] == 'recette')
```

### Le piège fondamental de `range(debut, fin)`

`range(debut, fin)` génère les entiers de `debut` jusqu'à `fin - 1` inclus. La borne `fin` est **exclue**.

```python
list(range(1, 12))   # → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  ← 12 absent !
list(range(1, 13))   # → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  ← correct
```

**Règle :** pour parcourir les mois 1 à 12 inclus, il faut `range(1, 13)`.

### Écrire une fonction de test avec `assert`

```python
def test_ma_fonction():
    assert ma_fonction(args1) == résultat_attendu_1, "Message d'erreur"
    assert ma_fonction(args2) == résultat_attendu_2
    print("Les tests sont validés.")

test_ma_fonction()  # appel immédiat
```

Si une assertion est fausse, Python lève une `AssertionError` avec le message. C'est exactement ce qui se passe en Q2 : le test révèle que `solde_annuel` est bugué.

---

## Structure des données

### Format d'un mouvement (dictionnaire)

| Clé | Type | Valeurs possibles |
|---|---|---|
| `'type'` | str | `'recette'` ou `'dépense'` |
| `'catégorie'` | str | 8 catégories : subventions, sponsoring, billetterie, marketing, salaires, déplacements, fonctionnement, cotisations, autres_charges |
| `'montant'` | float | Nombre positif en € |
| `'mois'` | int | 1 à 12 |

### Le jeu de test `mouvements_test`

```python
mouvements_test = [
    {'type': 'recette',  'catégorie': 'cotisations',    'montant': 1200.0, 'mois': 1},
    {'type': 'recette',  'catégorie': 'billetterie',    'montant':  300.0, 'mois': 6},
    {'type': 'dépense',  'catégorie': 'fonctionnement', 'montant':  450.0, 'mois': 6},
    {'type': 'dépense',  'catégorie': 'déplacements',   'montant':  200.0, 'mois': 12},
    {'type': 'dépense',  'catégorie': 'salaires',       'montant': 1500.0, 'mois': 12},
    {'type': 'recette',  'catégorie': 'subventions',    'montant':  800.0, 'mois': 12},
]
```

**Données clés à mémoriser :**
- Total recettes = 1200 + 300 + 800 = **2 300,0 €**
- Total dépenses = 450 + 200 + 1500 = **2 150,0 €**
- Solde annuel RÉEL = 2300 − 2150 = **150,0 €** (bénéfice)
- Solde annuel BUGUÉ = **1 050,0 €** (mois 12 ignoré)

### Fonctions fournies

**`solde_mensuel(mouvements, mois)` — CORRECTE ✓**

```python
def solde_mensuel(mouvements, mois):
    """Calcule recettes - dépenses pour un mois donné."""
    total_recettes = 0
    total_depenses = 0
    for m in mouvements:
        if m['mois'] == mois:
            if m['type'] == 'recette':
                total_recettes += m['montant']
            else:
                total_depenses += m['montant']
    return total_recettes - total_depenses
```

**`solde_annuel(mouvements)` — BUGUÉE ✗**

```python
def solde_annuel(mouvements):
    total = 0
    for m in range(1, 12):   # ← BUG : oublie décembre
        total = total + solde_mensuel(mouvements, m)
    return total
```

---

## Question 1 — `total_par_type` et ses tests

### Énoncé

Écrire `total_par_type(mouvements, type_mouvement)` qui renvoie la somme des montants du type donné. Si aucun mouvement ne correspond, renvoyer 0.  
Créer `test_total()` avec au moins deux assertions sur `mouvements_test`.

### Solution

```python
def total_par_type(mouvements, type_mouvement):
    """Renvoie la somme des montants du type donné, 0 si aucun."""
    total = 0.0
    for m in mouvements:
        if m['type'] == type_mouvement:
            total += m['montant']
    return total

# Version compacte équivalente :
# return sum(m['montant'] for m in mouvements if m['type'] == type_mouvement)
```

### Fonction de test

```python
def test_total():
    assert total_par_type(mouvements_test, 'recette') == 2300.0
    assert total_par_type(mouvements_test, 'dépense') == 2150.0
    assert total_par_type(mouvements_test, 'autre')   == 0     # type inexistant → 0
    print("Les tests sont validés.")

test_total()
```

### Points clés

- Initialiser à `0.0` (float) garantit que le résultat est toujours un flottant.
- Le cas type inexistant → 0 est imposé par l'énoncé : l'assertion sur `'autre'` le vérifie.
- La boucle + filtre est le patron fondamental de filtrage sur une liste de dictionnaires.

---

## Question 2 — Calcul manuel et test d'assertion

### Énoncé

Calculer manuellement le solde annuel de `mouvements_test`. Écrire `test_solde_annuel()` avec une assertion. Exécuter — le test lève une erreur.

### Calcul manuel étape par étape

`solde_annuel` additionne les `solde_mensuel` de chaque mois.

| Mois | Recettes | Dépenses | Solde mensuel |
|---|---|---|---|
| 1 | +1 200,0 € | 0 € | **+1 200,0 €** |
| 2 à 5, 7 à 11 | 0 € | 0 € | 0 € (aucun mouvement) |
| 6 | +300,0 € | −450,0 € | **−150,0 €** |
| 12 | +800,0 € | −1 700,0 € (200+1500) | **−900,0 €** |
| **Total annuel** | | | **+150,0 €** |

$$1200 + (-150) + (-900) = \mathbf{150{,}0\ \text{€}}$$

### Fonction de test

```python
def test_solde_annuel():
    # Le solde réel est 150.0 €
    assert solde_annuel(mouvements_test) == 150.0, \
        f"Résultat obtenu : {solde_annuel(mouvements_test)}, attendu : 150.0"
    print("Les tests sont validés.")

test_solde_annuel()
# → AssertionError : 1050.0 != 150.0
# C'est normal ! Le bug est révélé.
```

**Ce que l'exécution produit :** une `AssertionError` car `solde_annuel(mouvements_test)` renvoie `1050.0` au lieu de `150.0`. C'est l'objectif : le test révèle le bug à corriger en Q3.

---

## Question 3 — Identifier et corriger le bug

### Énoncé

Analyser `solde_annuel`, identifier l'erreur logique, expliquer pourquoi certains mouvements ont été ignorés, corriger. Appliquer sur `budget_complet.csv`.

### Explication détaillée du bug

```python
for m in range(1, 12):   # génère 1, 2, 3, ..., 11
```

`range(1, 12)` ne génère **jamais** le nombre 12. Le mois 12 (décembre) est silencieusement ignoré.

`solde_mensuel(mouvements_test, 12)` = 800 − 200 − 1500 = **−900,0 €**. Ce montant n'est jamais additionné.

La version buguée calcule : `1200 + (−150) = 1050,0 €` au lieu de `1200 + (−150) + (−900) = 150,0 €`.

### Correction — une seule modification

```python
def solde_annuel(mouvements):
    """Version CORRIGÉE."""
    total = 0
    for m in range(1, 13):   # ← CORRECTION : 13 au lieu de 12, pour inclure décembre
        total = total + solde_mensuel(mouvements, m)
    return total
```

### Vérification

```python
def test_solde_annuel():
    assert solde_annuel(mouvements_test) == 150.0
    print("Les tests sont validés.")

test_solde_annuel()  # → "Les tests sont validés."
```

### Résultats sur `budget_complet.csv` (2026 mouvements)

```python
import csv

mouvements_complets = []
with open("budget_complet.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f):
        ligne['montant'] = float(ligne['montant'])
        ligne['mois']    = int(ligne['mois'])
        mouvements_complets.append(ligne)

print(solde_annuel(mouvements_complets))   # → -3423.17
```

**Résultats réels vérifiés :**

| Indicateur | Valeur |
|---|---|
| Total recettes | 796 580,58 € |
| Total dépenses | 800 003,75 € |
| **Solde annuel corrigé** | **−3 423,17 €** |
| Conclusion | Le club est en **DÉFICIT** |

### Soldes mensuels (budget_complet.csv)

| Mois | Solde | Tendance |
|---|---|---|
| Janvier | +21 945,15 € | Positif |
| Février | −41 052,69 € | Déficit |
| Mars | −50 751,88 € | Déficit |
| Avril | −27 063,55 € | Déficit |
| Mai | +47 532,14 € | Positif |
| Juin | −37 103,20 € | Déficit |
| Juillet | −18 479,03 € | Déficit |
| Août | −25 960,85 € | Déficit |
| Septembre | −26 139,40 € | Déficit |
| Octobre | +1 875,27 € | Légèrement positif |
| Novembre | **+169 513,41 €** | **Meilleur mois** |
| **Décembre** | **−17 738,54 €** | **Le mois ignoré par le bug** |

Novembre est exceptionnel (probablement les subventions annuelles). Décembre est le mois ignoré par le bug — son omission faussait le résultat de 17 738,54 €, transformant un déficit réel en bénéfice fictif.

---

## Pièges fréquents

### Piège 1 — `range(1, 12)` vs `range(1, 13)`

`range(a, b)` génère les entiers de `a` à `b-1` inclus. La borne droite est **exclue**. Pour parcourir les mois 1 à 12, il faut `range(1, 13)`. C'est l'erreur la plus fréquente avec `range` en Python.

### Piège 2 — Initialiser le total à `0` vs `0.0`

Initialiser à `0.0` (float) garantit que la fonction renvoie toujours un flottant, même quand la liste est vide. Avec `0` (int), `0 == 0.0` est vrai en Python mais le type diffère — ce qui peut causer des surprises dans des comparaisons strictes de type.

### Piège 3 — Ne pas tester le cas « type inexistant »

L'énoncé impose que `total_par_type` renvoie `0` si aucun mouvement ne correspond. Sans assertion sur un type inexistant (`'autre'`), un bug retournant `None` passerait inaperçu.

### Piège 4 — Corriger `solde_mensuel` au lieu de `solde_annuel`

`solde_mensuel` est correcte. Le bug est uniquement dans `solde_annuel`, dans la borne de `range`. Modifier `solde_mensuel` serait hors sujet et casserait le fonctionnement global.

---

## Stratégie optimale le jour J

**Ordre d'attaque recommandé (3 questions, 1 heure) :**

1. **Q1 — 8 minutes :** écrire `total_par_type` (boucle + filtre + accumulation), puis `test_total()` avec 3 assertions (recettes=2300, dépenses=2150, autre=0). Appeler le professeur.

2. **Q2 — 5 minutes :** calcul manuel sur papier (mois 1 +1200, mois 6 −150, mois 12 −900 → total 150 €). Écrire `test_solde_annuel()`. Observer l'`AssertionError` (attendue).

3. **Q3 — 10 minutes :** lire `solde_annuel` ligne par ligne. Repérer `range(1, 12)`. Comprendre que 12 est exclu. Corriger → `range(1, 13)`. Relancer le test → succès. Décommenter les deux dernières lignes pour afficher le solde du fichier complet. Annoncer **−3 423,17 €** (déficit).

---

## Mini-exercices de vérification

### Exercice A — range() dans tous les sens

Sans Python, écrire les listes :

1. `list(range(1, 12))` → `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]` — **12 absent !**
2. `list(range(1, 13))` → `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]` — correct ✓
3. `list(range(0, 6))` → `[0, 1, 2, 3, 4, 5]`

### Exercice B — total_par_type à la main

`total_par_type(mouvements_test, 'dépense')` = 450,0 + 200,0 + 1 500,0 = **2 150,0 €**

### Exercice C — Résultat de la version buguée

La version buguée appelle `solde_mensuel` pour les mois 1 à 11. Seuls les mois 1 et 6 ont des mouvements dans cette plage : mois 1 = +1200, mois 6 = −150 → **1 050,0 €**. Le mois 12 (−900) est ignoré.

---

## Code complet corrigé — `analyse_budget.py`

```python
import csv


def lire_mouvements_depuis_csv(nom_fichier_csv):
    """Lit le CSV et retourne une liste de dictionnaires avec types convertis."""
    mouvements_csv = []
    try:
        with open(nom_fichier_csv, mode='r', newline='', encoding='utf-8') as f:
            lecteur_csv = csv.DictReader(f)
            for ligne in lecteur_csv:
                ligne['montant'] = float(ligne['montant'])
                ligne['mois']    = int(ligne['mois'])
                mouvements_csv.append(ligne)
        return mouvements_csv
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier_csv}' est introuvable.")
        return []


mouvements_test = [
    {'type': 'recette',  'catégorie': 'cotisations',    'montant': 1200.0, 'mois': 1},
    {'type': 'recette',  'catégorie': 'billetterie',    'montant':  300.0, 'mois': 6},
    {'type': 'dépense',  'catégorie': 'fonctionnement', 'montant':  450.0, 'mois': 6},
    {'type': 'dépense',  'catégorie': 'déplacements',   'montant':  200.0, 'mois': 12},
    {'type': 'dépense',  'catégorie': 'salaires',       'montant': 1500.0, 'mois': 12},
    {'type': 'recette',  'catégorie': 'subventions',    'montant':  800.0, 'mois': 12},
]


# ── Q1 ─────────────────────────────────────────────────────────────────────

def total_par_type(mouvements, type_mouvement):
    """Renvoie la somme des montants du type donné, 0.0 si aucun."""
    total = 0.0
    for m in mouvements:
        if m['type'] == type_mouvement:
            total += m['montant']
    return total


def test_total():
    assert total_par_type(mouvements_test, 'recette') == 2300.0
    assert total_par_type(mouvements_test, 'dépense') == 2150.0
    assert total_par_type(mouvements_test, 'autre')   == 0
    print("Les tests sont validés.")

test_total()


# ── Fonctions de calcul du solde ───────────────────────────────────────────

def solde_mensuel(mouvements, mois):
    """Calcule le solde pour un mois donné (recettes - dépenses)."""
    total_recettes = 0
    total_depenses = 0
    for m in mouvements:
        if m['mois'] == mois:
            if m['type'] == 'recette':
                total_recettes += m['montant']
            else:
                total_depenses += m['montant']
    return total_recettes - total_depenses


def solde_annuel(mouvements):
    """Calcule le solde annuel — version CORRIGÉE."""
    total = 0
    for m in range(1, 13):   # ← CORRECTION : inclut décembre (mois 12)
        total = total + solde_mensuel(mouvements, m)
    return total


# ── Q2 ─────────────────────────────────────────────────────────────────────

def test_solde_annuel():
    # Calcul manuel : mois 1 (+1200) + mois 6 (−150) + mois 12 (−900) = 150.0
    assert solde_annuel(mouvements_test) == 150.0, \
        f"Obtenu {solde_annuel(mouvements_test)}, attendu 150.0"
    print("Les tests sont validés.")

test_solde_annuel()


# ── Programme principal ────────────────────────────────────────────────────

mouvements_complets = lire_mouvements_depuis_csv("budget_complet.csv")
print("Le solde annuel sur le fichier complet est de :", solde_annuel(mouvements_complets))
# → -3423.17 (DÉFICIT)
```

## Récapitulatif — Les 3 réponses en un coup d'œil

```python
# Q1 — total_par_type (5 lignes)
def total_par_type(mouvements, type_mouvement):
    total = 0.0
    for m in mouvements:
        if m['type'] == type_mouvement:
            total += m['montant']
    return total

# Q1 — test_total (3 assertions)
assert total_par_type(mouvements_test, 'recette') == 2300.0
assert total_par_type(mouvements_test, 'dépense') == 2150.0
assert total_par_type(mouvements_test, 'autre')   == 0

# Q2 — Solde annuel théorique
# 1200 + (300−450) + (800−200−1500) = 1200 − 150 − 900 = 150.0 €
assert solde_annuel(mouvements_test) == 150.0

# Q3 — Correction du bug (1 mot changé)
for m in range(1, 13):   # ← 13 au lieu de 12

# Q3 — Résultat sur budget_complet.csv
# Solde = −3 423,17 € → DÉFICIT
```
