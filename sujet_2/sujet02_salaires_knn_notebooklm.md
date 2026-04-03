# Sujet 02 — Écarts de salaires femmes/hommes & algorithme k-NN
**NSI Terminale · BAC 2026 · Partie pratique**
Thèmes : traitement de données, listes de dictionnaires, algorithme k plus proches voisins, éthique algorithmique

---

## Vue d'ensemble du sujet

Ce sujet porte sur l'analyse de données salariales d'une entreprise fictive. À partir d'une liste de 2 000 employés décrits par leur expérience, leur niveau d'études, leur sexe et leur salaire, on écrit des fonctions Python pour mesurer les inégalités salariales entre femmes et hommes, puis on étudie et corrige un algorithme de recommandation de salaire basé sur la méthode des k plus proches voisins.

**Les 4 questions du sujet :**
- Question 1 : écrire `salaire_moyen_condition` — calculer une moyenne conditionnelle
- Question 2 : écrire `effectif_par_sexe` — compter les effectifs par sexe
- Question 3 : déboguer `calcul_ecart_sexe` — identifier et corriger deux bugs
- Question 4 : tester et corriger un algorithme k-NN biaisé

---

## 1. Rappels — Les listes de dictionnaires en Python

### Définition

Une liste de dictionnaires est une liste Python dont chaque élément est un dictionnaire. Tous les dictionnaires partagent les mêmes clés — comme les colonnes d'un tableau. Chaque dictionnaire représente une ligne de ce tableau.

```python
annuaire = [
    {'prenom': 'Alice', 'maths': 17, 'nsi': 18},
    {'prenom': 'Bob',   'maths': 12, 'nsi': 15},
    {'prenom': 'Carla', 'maths': 14, 'nsi': 16}
]
```

Pour accéder à la note NSI d'Alice : `annuaire[0]['nsi']`

Pour parcourir tous les éléments :
```python
for eleve in annuaire:
    print(eleve['prenom'])
```

### Filtrer une liste avec une compréhension

```python
bons_en_nsi = [e for e in annuaire if e['nsi'] > 15]
# résultat : les élèves ayant plus de 15 en NSI
```

### Calculer une moyenne

```python
# Approche boucle
total = 0
for e in annuaire:
    total = total + e['nsi']
moyenne = total / len(annuaire)

# Approche compacte avec sum()
moyenne = sum(e['nsi'] for e in annuaire) / len(annuaire)
```

### Renvoyer None pour une liste vide

Toujours tester si la liste est vide avant de diviser (éviter la ZeroDivisionError) :
```python
if len(liste) == 0:
    return None
# ou plus pythonique :
if not liste:
    return None
```

---

## 2. Contexte — Structure des données

### Structure d'un employé

Chaque employé est un dictionnaire avec quatre champs :

| Champ | Type | Description | Exemple |
|---|---|---|---|
| `'experience'` | int | Années d'expérience professionnelle | 5 |
| `'etudes'` | int | Années d'études après le bac | 3 |
| `'sexe'` | str | Sexe ('F' ou 'M') | 'F' |
| `'salaire'` | int | Salaire mensuel en euros | 2400 |

### Jeu de données de test (6 employés)

```python
employes_test = [
    {'experience': 5, 'etudes': 3, 'sexe': 'F', 'salaire': 2400},
    {'experience': 3, 'etudes': 3, 'sexe': 'M', 'salaire': 2550},
    {'experience': 5, 'etudes': 5, 'sexe': 'F', 'salaire': 2500},
    {'experience': 3, 'etudes': 5, 'sexe': 'M', 'salaire': 2800},
    {'experience': 2, 'etudes': 5, 'sexe': 'F', 'salaire': 2300},
    {'experience': 2, 'etudes': 3, 'sexe': 'M', 'salaire': 2700}
]
```

Sur ce jeu de test :
- Salaire moyen des femmes : (2400 + 2500 + 2300) / 3 = **2400 €**
- Salaire moyen des hommes : (2550 + 2800 + 2700) / 3 ≈ **2683 €**

Un jeu complet de 2 000 employés est aussi fourni (`donnees_completes.py`).

### Contexte statistique

En France, selon l'INSEE, l'écart de salaire moyen entre les femmes et les hommes est d'environ 15 % en 2023. L'objectif du sujet est d'observer et mesurer cet écart sur un jeu de données simulé, puis d'étudier comment un algorithme peut le reproduire ou le corriger.

---

## 3. Question 1 — Salaire moyen conditionnel

### Énoncé

Écrire la fonction `salaire_moyen_condition(employes, champ, valeur)` qui renvoie le salaire moyen des employés dont la valeur associée au champ `champ` est égale à `valeur`. La fonction renvoie `None` si aucun employé ne correspond.

**Exemple :** `salaire_moyen_condition(employes, 'sexe', 'F')` renvoie `2400.0`

### Méthode — 3 étapes

1. **Filtrer** : garder uniquement les employés dont `emp[champ] == valeur`
2. **Vérifier** : si la liste filtrée est vide, renvoyer `None`
3. **Calculer** : renvoyer `sum(...) / len(...)` sur les salaires filtrés

### Correction complète

```python
def salaire_moyen_condition(employes, champ, valeur):
    '''Renvoie le salaire moyen des employes dont la valeur du champ
    correspond a la valeur donnee. Renvoie None si aucun employe.'''
    # Etape 1 : filtrer les salaires correspondant au critère
    salaires_filtres = [emp['salaire'] for emp in employes if emp[champ] == valeur]
    # Etape 2 : cas vide -> None
    if len(salaires_filtres) == 0:
        return None
    # Etape 3 : calcul de la moyenne
    return sum(salaires_filtres) / len(salaires_filtres)
```

### Tests de validation

```python
def test_salaire_moyen_condition():
    e = employes_test
    assert salaire_moyen_condition([], 'sexe', 'F') == None      # liste vide
    assert salaire_moyen_condition(e, 'sexe', 'F') == 2400.0     # 3 femmes
    assert salaire_moyen_condition(e, 'etudes', 3) == 2550.0     # études = 3
    assert salaire_moyen_condition(e, 'etudes', 12) == None      # valeur absente
    print("Les tests sont valides.")
```

### Résultats sur les 2 000 employés

- Salaire moyen des femmes ≈ **2 229 €**
- Salaire moyen des hommes ≈ **2 438 €**
- Écart brut ≈ 209 €, soit environ **8,6 %**

### Point clé de cette question

L'argument `champ` est une **variable**, pas une chaîne en dur. Écrire `emp[champ]` (pas `emp['sexe']`) rend la fonction générique et réutilisable pour filtrer sur n'importe quel champ.

---

## 4. Question 2 — Effectifs par sexe

### Énoncé

Écrire la fonction `effectif_par_sexe(employes)` qui prend en paramètre un tableau non vide d'employés et qui renvoie un dictionnaire ayant deux clés `'F'` et `'M'` associées respectivement au nombre de femmes et au nombre d'hommes.

**Exemple :** `effectif_par_sexe(employes_test)` renvoie `{'F': 3, 'M': 3}`

### Deux approches valides

**Approche A — Compteur explicite :**
```python
def effectif_par_sexe(employes):
    nb_f = 0
    nb_m = 0
    for emp in employes:
        if emp['sexe'] == 'F':
            nb_f += 1
        else:
            nb_m += 1
    return {'F': nb_f, 'M': nb_m}
```

**Approche B — Avec sum() et compréhension :**
```python
def effectif_par_sexe(employes):
    nb_f = sum(1 for emp in employes if emp['sexe'] == 'F')
    nb_m = sum(1 for emp in employes if emp['sexe'] == 'M')
    return {'F': nb_f, 'M': nb_m}
```

### Tests de validation

```python
def test_effectif_par_sexe():
    e = employes_test
    assert effectif_par_sexe(e) == {'F': 3, 'M': 3}
    assert effectif_par_sexe([e[0], e[2]]) == {'F': 2, 'M': 0}  # clé M présente même si 0
    assert effectif_par_sexe([e[1]]) == {'F': 0, 'M': 1}
    print("Les tests sont valides.")
```

### Point clé

La fonction renvoie toujours les deux clés `'F'` et `'M'`, même si l'une vaut 0. Ne pas renvoyer `{'M': 1}` quand il n'y a que des hommes — les deux clés doivent toujours être présentes.

---

## 5. Question 3 — Déboguer `calcul_ecart_sexe`

### Énoncé

La fonction `calcul_ecart_sexe` est incorrecte. Expliquer pourquoi, proposer des assertions pour mettre les erreurs en évidence, puis écrire une version corrigée nommée `ecart_salaire`.

### Code bugué original

```python
def calcul_ecart_sexe(employes):
    '''Renvoie l'écart de salaire en pourcentage pour les femmes
    par rapport aux hommes'''
    moy_h = salaire_moyen_condition(employes, 'sexe', 'M')
    moy_f = salaire_moyen_condition('employes', 'sexe', 'F')  # BUG 1 : guillemets
    return moy_h - moy_f                                       # BUG 2 : différence, pas pourcentage
```

### Bug 1 — Chaîne de caractères au lieu de la variable

`salaire_moyen_condition('employes', ...)` passe la **chaîne** `'employes'` (avec guillemets) au lieu de la **variable** `employes` (sans guillemets).

Python va itérer sur les caractères de la chaîne `'employes'` : `'e'`, `'m'`, `'p'`, `'l'`, `'o'`, `'y'`, `'e'`, `'s'`. Aucun caractère n'a le champ `'sexe'`, donc la fonction renvoie `None`. La soustraction `moy_h - None` lève alors une `TypeError`.

**Réflexe :** si une fonction renvoie `None` de façon inattendue, vérifier l'absence de guillemets autour d'un nom de variable.

### Bug 2 — Différence en euros au lieu d'un pourcentage

La formule correcte de l'écart en pourcentage est :

```
écart = (salaire_moyen_hommes - salaire_moyen_femmes) / salaire_moyen_hommes × 100
```

Or la fonction renvoie `moy_h - moy_f`, qui est une différence en euros (environ 283 € sur le jeu de test), pas un pourcentage.

### Assertions pour mettre en évidence les bugs

```python
employes_only_f = [e for e in employes_test if e['sexe'] == 'F']
# Si un seul sexe est présent, ecart_salaire doit renvoyer None
assert ecart_salaire(employes_only_f) == None

# L'écart en pourcentage doit être compris entre 0 et 100
assert 0 <= ecart_salaire(employes_test) <= 100
```

### Correction complète

```python
def ecart_salaire(employes):
    '''Renvoie l'ecart de salaire en pourcentage (femmes vs hommes).
    Renvoie None si un seul sexe est present.'''
    # Correction bug 1 : variable sans guillemets
    moy_h = salaire_moyen_condition(employes, 'sexe', 'M')
    moy_f = salaire_moyen_condition(employes, 'sexe', 'F')
    # Correction bug 2 : cas None et formule correcte
    if moy_h is None or moy_f is None:
        return None
    return (moy_h - moy_f) / moy_h * 100
```

### Résultats

- Sur le jeu de test (6 employés) : écart ≈ **10,6 %**
- Sur les 2 000 employés : écart ≈ **8,6 %**
- INSEE France (2023) : ≈ 15 % (le jeu simulé ne reflète pas tous les facteurs réels : secteur, temps partiel, progression de carrière)

### Tests de validation

```python
def test_ecart_salaire():
    e = employes_test
    employes_only_f = [emp for emp in e if emp['sexe'] == 'F']
    assert ecart_salaire(employes_only_f) == None
    assert ecart_salaire([]) == None
    ecart = ecart_salaire(e)
    assert ecart is not None
    assert 0 <= ecart <= 100
    print("Les tests sont valides.")
```

---

## 6. Question 4 — Algorithme k-NN et biais algorithmique

### Énoncé

L'entreprise utilise l'algorithme des k plus proches voisins pour proposer un salaire d'embauche. Tester `salaire_par_proximite` sur deux profils identiques (même expérience, mêmes études) mais de sexe différent. Identifier la source de l'écart et corriger le programme.

### Principe de l'algorithme k-NN

L'analogie : pour estimer le loyer d'un appartement, on cherche les 3 appartements les plus similaires (même surface, même quartier) et on fait la moyenne de leurs loyers. C'est la méthode des k plus proches voisins.

**Étapes de l'algorithme :**
1. Définir une **distance** entre deux individus
2. Calculer la distance entre le nouvel individu et **tous** les individus connus
3. Garder les **k plus proches** (les k distances les plus faibles)
4. Renvoyer la **moyenne** des valeurs cibles de ces k voisins (ici : leurs salaires)

### Fonction de distance fournie dans le sujet (version buguée)

```python
def sexe_vers_entier(e):
    if e['sexe'] == 'F':
        return 1
    else:
        return -1

def distance(e1, e2):
    s = (sexe_vers_entier(e1) - sexe_vers_entier(e2))**2   # différence sexe
    s = s + (e1['experience'] - e2['experience'])**2        # différence expérience
    s = s + (e1['etudes'] - e2['etudes'])**2                # différence études
    return sqrt(s)
```

La distance est la **distance euclidienne généralisée** à 3 dimensions : sqrt((Δsexe)² + (Δexp)² + (Δetu)²). C'est la généralisation du théorème de Pythagore.

### Mise en évidence du biais — calcul manuel

Pour `profil_f = {'experience': 3, 'etudes': 3, 'sexe': 'F'}` :

| Employé | sexe (entier) | Δsexe | Δexp | Δetu | Distance |
|---|---|---|---|---|---|
| 1 — F, 5, 3, 2400€ | F→1 | 0 | 2 | 0 | sqrt(0+4+0) = 2 |
| 2 — M, 3, 3, 2550€ | M→-1 | 2 | 0 | 0 | sqrt(4+0+0) = 2 |
| 3 — F, 5, 5, 2500€ | F→1 | 0 | 2 | 2 | sqrt(0+4+4) ≈ 2,83 |
| 4 — M, 3, 5, 2800€ | M→-1 | 2 | 0 | 2 | sqrt(4+0+4) ≈ 2,83 |
| 5 — F, 2, 5, 2300€ | F→1 | 0 | 1 | 2 | sqrt(0+1+4) ≈ 2,24 |
| 6 — M, 2, 3, 2700€ | M→-1 | 2 | 1 | 0 | sqrt(4+1+0) ≈ 2,24 |

Pour `profil_f`, les 3 plus proches sont l'employé 1 (F, 2400€), l'employé 2 (M, 2550€) et selon le tri l'employé 5 (F, 2300€) → salaire proposé ≈ **2 417 €**

Pour `profil_m` (même profil mais sexe M), le tri favorise les hommes → salaire proposé ≈ **2 683 €**

**Résultat choquant :** deux profils identiques (expérience 3, études 3) reçoivent des salaires proposés différents uniquement à cause de leur sexe.

### Pourquoi c'est un biais algorithmique

En incluant le sexe dans la distance, on fait en sorte que les voisins des femmes sont principalement des femmes (qui ont historiquement des salaires plus bas), et inversement pour les hommes. L'algorithme **reproduit et perpétue** le biais salarial existant dans les données d'entraînement. C'est un problème éthique majeur en apprentissage automatique : un algorithme peut sembler objectif tout en étant discriminatoire si ses données ou sa conception intègrent des caractéristiques sensibles.

### Correction — Exclure le sexe de la distance

```python
def distance_sans_sexe(e1, e2):
    '''Distance basée uniquement sur l'expérience et les études.'''
    s = (e1['experience'] - e2['experience'])**2
    s += (e1['etudes'] - e2['etudes'])**2
    return sqrt(s)
```

### Fonctions k-NN complètes

```python
from math import sqrt

def k_plus_proches(k, employes, e, dist_fn):
    '''Renvoie les k employés les plus proches de e selon dist_fn.'''
    e_d = [(dist_fn(e, employes[i]), i) for i in range(len(employes))]
    e_d.sort()
    return [employes[e_d[i][1]] for i in range(k)]

def salaire_moyen(employes):
    if len(employes) == 0:
        return None
    return sum(emp['salaire'] for emp in employes) / len(employes)

def salaire_par_proximite_corrige(employes, e):
    '''Version corrigée : le sexe n'intervient pas dans la distance.'''
    voisins = k_plus_proches(3, employes, e, distance_sans_sexe)
    return salaire_moyen(voisins)
```

### Résultats comparatifs

| Version | Profil F (exp=3, etu=3) | Profil M (exp=3, etu=3) |
|---|---|---|
| **Avec sexe dans distance (buguée)** | ~2 417 € | ~2 683 € |
| **Sans sexe dans distance (corrigée)** | 2 550 € | 2 550 € |

Après correction, deux profils identiques obtiennent le même salaire proposé : **2 550 €**.

### Tests de validation

```python
def test_knn_corrige():
    e = employes_test
    profil_f = {'experience': 3, 'etudes': 3, 'sexe': 'F'}
    profil_m = {'experience': 3, 'etudes': 3, 'sexe': 'M'}
    voisins_f = k_plus_proches(3, e, profil_f, distance_sans_sexe)
    voisins_m = k_plus_proches(3, e, profil_m, distance_sans_sexe)
    sal_f = salaire_moyen(voisins_f)
    sal_m = salaire_moyen(voisins_m)
    assert sal_f == sal_m, f"Encore un biais : {sal_f} != {sal_m}"
    assert sal_f == 2550.0
    print("Les tests sont valides.")
```

---

## 7. Pièges fréquents

### Piège 1 — Variable vs chaîne de caractères

C'est le bug central de Q3 : `'employes'` avec guillemets itère sur les caractères de la chaîne au lieu de parcourir la liste. Python ne lève pas d'erreur immédiatement, ce qui rend le bug difficile à repérer.

**Réflexe :** si une fonction renvoie `None` de façon inattendue, vérifier l'absence de guillemets autour d'un nom de variable.

### Piège 2 — Oublier le cas « aucun employé »

Toute fonction calculant une moyenne doit gérer la liste vide (ZeroDivisionError). Toujours tester : `assert salaire_moyen_condition([], 'sexe', 'F') == None`

### Piège 3 — Différence vs pourcentage

L'écart en euros (`moy_h - moy_f`) et l'écart en pourcentage (`(moy_h - moy_f) / moy_h * 100`) sont deux choses très différentes. Sur le jeu de test : différence ≈ 283 €, pourcentage ≈ 10,6 %. L'énoncé demande toujours le pourcentage.

### Piège 4 — Biais dans la distance k-NN

Intégrer une caractéristique sensible (sexe, origine…) dans le calcul de distance revient à regrouper les individus par cette caractéristique et à reproduire les inégalités des données d'entraînement. C'est un problème éthique majeur en apprentissage automatique.

### Piège 5 — `is None` vs `== None`

En Python, la bonne pratique est d'écrire `if x is None` (et non `if x == None`). Les deux fonctionnent pour `None`, mais `is None` est plus idiomatique et plus sûr avec des objets personnalisés.

---

## 8. Mini-exercices de vérification

### Mini-exercice A — Jeu de données à 20 % d'écart

Inventer un jeu de 4 employés (2F, 2M) où l'écart de salaire est exactement 20 %. 

**Exemple :** femmes à 2 000 €, hommes à 2 500 €
→ Écart = (2500 - 2000) / 2500 × 100 = 500/2500 × 100 = **20 %** ✓

### Mini-exercice B — Interpréter l'écart de 8,6 %

Sur 2 000 employés, l'écart calculé est d'environ 8,6 %, alors que l'INSEE annonce 15 %. Le jeu de données simulé ne reflète pas tous les facteurs réels : secteur d'activité, temps partiel (souvent subi par les femmes), progression de carrière différente. L'écart brut de 8,6 % reste significatif car il est mesuré sur des profils comparables (même expérience, mêmes études).

### Mini-exercice C — Assertions supplémentaires

```python
employes_h = [e for e in employes_test if e['sexe'] == 'M']
assert ecart_salaire(employes_h) == None          # un seul sexe → None
assert ecart_salaire(employes_test) > 0           # écart positif sur jeu complet
```

---

## 9. Récapitulatif — Ce qu'il faut retenir

1. **Listes de dictionnaires :** se parcourt avec `for emp in employes`, on accède aux champs avec `emp['champ']`.
2. **Moyenne conditionnelle :** filtrer d'abord, vérifier que la liste n'est pas vide, puis diviser.
3. **Guillemets = piège :** `'employes'` ≠ `employes`. Les guillemets transforment une variable en chaîne de caractères.
4. **Formule de l'écart :** `(moy_H - moy_F) / moy_H × 100`, pas une simple soustraction.
5. **Biais k-NN :** inclure une caractéristique sensible dans la distance reproduit les inégalités des données d'entraînement.
6. **Tests :** toujours écrire au moins 3 assertions par fonction pour détecter les bugs rapidement.

---

## 10. Code complet du sujet (synthèse)

```python
from math import sqrt

# --- Données de test ---
employes_test = [
    {'experience': 5, 'etudes': 3, 'sexe': 'F', 'salaire': 2400},
    {'experience': 3, 'etudes': 3, 'sexe': 'M', 'salaire': 2550},
    {'experience': 5, 'etudes': 5, 'sexe': 'F', 'salaire': 2500},
    {'experience': 3, 'etudes': 5, 'sexe': 'M', 'salaire': 2800},
    {'experience': 2, 'etudes': 5, 'sexe': 'F', 'salaire': 2300},
    {'experience': 2, 'etudes': 3, 'sexe': 'M', 'salaire': 2700}
]

# --- Q1 ---
def salaire_moyen_condition(employes, champ, valeur):
    salaires = [emp['salaire'] for emp in employes if emp[champ] == valeur]
    if len(salaires) == 0:
        return None
    return sum(salaires) / len(salaires)

# --- Q2 ---
def effectif_par_sexe(employes):
    nb_f = sum(1 for emp in employes if emp['sexe'] == 'F')
    nb_m = sum(1 for emp in employes if emp['sexe'] == 'M')
    return {'F': nb_f, 'M': nb_m}

# --- Q3 ---
def ecart_salaire(employes):
    moy_h = salaire_moyen_condition(employes, 'sexe', 'M')
    moy_f = salaire_moyen_condition(employes, 'sexe', 'F')
    if moy_h is None or moy_f is None:
        return None
    return (moy_h - moy_f) / moy_h * 100

# --- Q4 ---
def distance_sans_sexe(e1, e2):
    s = (e1['experience'] - e2['experience'])**2
    s += (e1['etudes'] - e2['etudes'])**2
    return sqrt(s)

def k_plus_proches(k, employes, e, dist_fn):
    e_d = [(dist_fn(e, employes[i]), i) for i in range(len(employes))]
    e_d.sort()
    return [employes[e_d[i][1]] for i in range(k)]

def salaire_moyen(employes):
    if len(employes) == 0:
        return None
    return sum(emp['salaire'] for emp in employes) / len(employes)
```

---

*Sujet 02 · NSI Terminale · BAC 2026 · DarkSATHI Li*
