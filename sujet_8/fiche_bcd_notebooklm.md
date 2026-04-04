# Fiche NSI Terminale — Codage BCD et Addition Décimale
## BAC 2026 — Sujet n°8 — Partie pratique

**Matière :** Numérique et Sciences Informatiques (NSI)  
**Niveau :** Terminale — voie générale  
**Thème du programme :** Représentation des données en machine — types et valeurs de base  
**Durée de l'épreuve :** 1 heure  
**Fichier à modifier :** `addition_BCD.py`

---

## Contexte général du sujet

Le sujet porte sur un problème concret de comptabilité informatique : les nombres flottants (type `float` en Python) génèrent des erreurs d'arrondi qui s'accumulent lors de nombreuses additions. Pour y remédier, on utilise le codage **BCD** (*Binary Coded Decimal*), une technique historique utilisée dans les calculatrices et les systèmes financiers.

Le sujet comporte quatre questions progressives :

1. Mettre en évidence l'erreur d'arrondi avec les flottants
2. Écrire une fonction de conversion BCD → décimal
3. Corriger un bug dans la fonction d'addition BCD
4. Corriger un bug d'alignement pour des nombres de longueurs différentes

---

## Partie 1 — Le problème des flottants

### Pourquoi les flottants posent problème

Les ordinateurs stockent les nombres en base 2 (binaire). Certains nombres décimaux simples, comme `0.1`, n'ont pas de représentation binaire **finie** — leur écriture en base 2 est périodique, comme `1/3 = 0.333…` en base 10.

Conséquence : l'ordinateur est forcé d'arrondir. Sur un seul calcul, l'erreur est infime (de l'ordre de 10⁻¹⁷). Mais sur des centaines de milliers d'additions, ces erreurs **s'accumulent** et finissent par fausser les totaux.

### Démonstration Python

```python
>>> 0.1 + 0.2
0.30000000000000004   # et non 0.3

>>> 2.27 + 5.19 + 1.81
9.27                  # semble juste, mais ce n'est pas exactement 9.27 en mémoire
```

### Exemple du sujet

La chaîne *RESTO NSI* a 1 000 restaurants, chacun servant 500 menus/jour.  
Un menu = entrée `2.27 €` + plat `5.19 €` + dessert `1.81 €` = `9.27 €`.  
Nombre total de menus : `1 000 × 500 = 500 000`.  
Valeur théorique exacte : `500 000 × 9.27 = 4 635 000 €`.

En additionnant avec des flottants dans une boucle, on n'obtient **pas exactement** `4 635 000`.

---

## Partie 2 — Le codage BCD

### Définition

**BCD** (*Binary Coded Decimal* — décimal codé en binaire) : chaque chiffre décimal (0 à 9) est représenté par son écriture binaire sur **4 bits**, appelée un **quartet** (ou *nibble*).

On n'utilise que 10 des 16 combinaisons possibles sur 4 bits :

| Chiffre | Quartet BCD |
|---------|-------------|
| 0       | `0000`      |
| 1       | `0001`      |
| 2       | `0010`      |
| 3       | `0011`      |
| 4       | `0100`      |
| 5       | `0101`      |
| 6       | `0110`      |
| 7       | `0111`      |
| 8       | `1000`      |
| 9       | `1001`      |

Les combinaisons `1010` à `1111` (10 à 15) sont **invalides** en BCD.

### Convention monétaire : virgule implicite

Dans ce sujet, la virgule n'est **pas codée** dans la liste. On utilise la convention :  
> Les deux derniers quartets représentent toujours les **centimes**.

Il faut donc **au minimum 3 quartets** pour représenter toute somme en euros.

### Exemples de représentation BCD

| Montant (€) | Liste de quartets BCD                        | Lecture             |
|-------------|----------------------------------------------|---------------------|
| `59.00`     | `['0101', '1001', '0000', '0000']`           | 5 — 9 — 0 — 0       |
| `1.75`      | `['0001', '0111', '0101']`                   | 1 — 7 — 5           |
| `0.23`      | `['0000', '0010', '0011']`                   | 0 — 2 — 3           |
| `13.56`     | `['0001', '0011', '0101', '0110']`           | 1 — 3 — 5 — 6       |

### Formule de conversion BCD → décimal

Pour reconstituer la valeur décimale à partir d'une liste de quartets :

```
entier = 0
Pour chaque quartet (de gauche à droite) :
    chiffre = valeur décimale du quartet (int(quartet, 2))
    entier = entier × 10 + chiffre
valeur = entier / 100
```

---

## Partie 3 — Architecture du code fourni

Le fichier `addition_BCD.py` contient les fonctions suivantes :

| Fonction | État | Rôle |
|----------|------|------|
| `convertir_dec_vers_BCD(decimal)` | Fournie ✓ | Convertit un nombre décimal (str) en liste de quartets BCD |
| `additionner_binaire_quartets(q1, q2, retenue)` | Fournie ✓ | Addition bit à bit de deux quartets, renvoie `(somme, retenue)` |
| `corriger_BCD(somme, retenue)` | Fournie ✓ | Applique la correction `+0110` si le quartet est invalide |
| `aligner_quartets(q1, q2)` | **À compléter — Q4** | Égalise les longueurs des deux listes |
| `additionner_nombres_format_BCD(a, b)` | **Buguée — Q3** | Addition complète de deux nombres BCD |
| `calcul_recettes()` | **À écrire — Q1** | Calcule les recettes avec flottants |
| `convertir_BCD_vers_decimal(liste_quartets)` | **À écrire — Q2** | Convertit BCD → float |

---

## Question 1 — calcul_recettes()

### Énoncé

Écrire la fonction `calcul_recettes()` qui additionne le prix de chaque menu vendu dans la journée en utilisant une boucle. Afficher le résultat. Justifier l'écart avec la valeur théorique `4 635 000 €`.

### Solution

```python
def calcul_recettes():
    prix_menu = 2.27 + 5.19 + 1.81  # 9.27 €, mais pas exactement en mémoire
    total = 0.0
    for _ in range(1000 * 500):     # 500 000 itérations
        total += prix_menu
    return total

print(calcul_recettes())
# Résultat observé : quelque chose comme 4634999.9999... ou 4635000.0000...x
# En tout cas différent de 4635000 exact
```

### Justification de l'écart

`2.27`, `5.19` et `1.81` ne sont pas représentables exactement en binaire IEEE 754. Leur somme est stockée avec un écart infime. Multiplié par 500 000 additions dans la boucle, cet écart devient mesurable et fausse le total comptable.

### Fonction de test

```python
def test_calcul_recettes():
    resultat = calcul_recettes()
    assert resultat != 4635000, "Étrange : le résultat est exactement juste !"
    assert abs(resultat - 4635000) < 0.01, "L'écart est trop grand !"
    assert 4634999.99 < resultat < 4635000.01
    print("Les tests sont validés.")

test_calcul_recettes()
```

---

## Question 2 — convertir_BCD_vers_decimal()

### Énoncé

Écrire la fonction `convertir_BCD_vers_decimal(liste_quartets)` qui prend une liste de chaînes de 4 bits et renvoie la valeur décimale correspondante (type `float`).  
Ajouter l'assertion : `convertir_BCD_vers_decimal(['0001', '0011', '0101', '0110'])` doit renvoyer `13.56`.

### Démarche

1. Parcourir la liste de gauche à droite.
2. Pour chaque quartet, convertir en chiffre décimal : `int(quartet, 2)`.
3. Accumuler selon le schéma `entier = entier * 10 + chiffre` (schéma de Horner).
4. Diviser le résultat final par `100` pour placer la virgule.

### Trace d'exécution sur `['0001', '0011', '0101', '0110']`

| Quartet  | Chiffre | Calcul           | Entier courant |
|----------|---------|------------------|----------------|
| `0001`   | 1       | 0 × 10 + 1       | 1              |
| `0011`   | 3       | 1 × 10 + 3       | 13             |
| `0101`   | 5       | 13 × 10 + 5      | 135            |
| `0110`   | 6       | 135 × 10 + 6     | 1356           |
| Résultat | —       | 1356 / 100       | **13.56**      |

### Solution

```python
def convertir_BCD_vers_decimal(liste_quartets):
    """
    Convertit une liste de quartets BCD en valeur décimale (float).
    Convention : virgule implicite avant les deux derniers quartets.
    """
    entier = 0
    for quartet in liste_quartets:
        chiffre = int(quartet, 2)       # quartet binaire -> chiffre 0-9
        entier = entier * 10 + chiffre  # accumulation (schéma de Horner)
    return entier / 100                 # placement de la virgule implicite
```

### Fonction de test

```python
def test_convertir_BCD_vers_decimal():
    assert convertir_BCD_vers_decimal(['0001', '0011', '0101', '0110']) == 13.56
    assert convertir_BCD_vers_decimal(['0101', '1001', '0000', '0000']) == 59.00
    assert convertir_BCD_vers_decimal(['0001', '0111', '0101']) == 1.75
    print("Les tests sont validés.")

test_convertir_BCD_vers_decimal()
```

---

## Question 3 — Corriger l'addition BCD

### Énoncé

`additionner_nombres_format_BCD('27', '35')` devrait renvoyer une liste représentant `62.00`, mais le résultat est faux. Identifier le bug et corriger en insérant un appel à `corriger_BCD` au bon endroit.

### Principe de la correction BCD

Quand on additionne deux quartets, la somme binaire peut produire un quartet **invalide** (valeur ≥ 10) ou générer une retenue. Dans ces deux cas, le format BCD est rompu.

**Règle de correction :** si le quartet résultant est ≥ `1010` (10) ou s'il y a eu une retenue, on ajoute `0110` (6 en décimal) au quartet invalide.

**Pourquoi +6 ?** Parce que BCD saute 6 combinaisons (de `1010` à `1111`). Ajouter 6 "reboucle" dans la plage valide et propage la retenue correctement.

### Illustration : 7 + 8 = 15

```
Addition binaire brute :
  0111  (7)
+ 1000  (8)
──────
  1111  ← invalide ! (valeur = 15, hors plage BCD)

Correction BCD (+ 0110) :
  1111
+ 0110
──────
1 0101  → quartet = 0101 (5), retenue = 1

Résultat : retenue 1 + quartet 5 = 15 ✓
```

### Illustration : 27 + 35 = 62

| Rang | A (27) | B (35) | Somme brute | Après corriger_BCD |
|------|--------|--------|-------------|---------------------|
| Unités | `0111` (7) | `0101` (5) | `1100` ❌ invalide | `0010`, retenue=1 |
| Dizaines | `0010` (2) | `0011` (3) | `0110` + retenue=1 → `0111` (7>9 ? non) | `0110`, retenue=0 |

Résultat : `['0110', '0010']` → 62.00 ✓

### Identification du bug

Dans `additionner_nombres_format_BCD`, la boucle appelle `additionner_binaire_quartets` mais **n'appelle jamais `corriger_BCD`**.

```python
# CODE BUGUÉ :
for i in range(longueur_max):
    index = longueur_max - i - 1
    somme, retenue = additionner_binaire_quartets(
        liste_quartets1[index], liste_quartets2[index], retenue)
    # ← manque l'appel à corriger_BCD ici !
    resultat.insert(0, somme)
```

### Correction à apporter

```python
# CODE CORRIGÉ :
for i in range(longueur_max):
    index = longueur_max - i - 1
    somme, retenue = additionner_binaire_quartets(
        liste_quartets1[index], liste_quartets2[index], retenue)
    somme, retenue = corriger_BCD(somme, retenue)   # ← ligne ajoutée
    resultat.insert(0, somme)
```

### Fonction de test

```python
def test_additionner_nombres_format_BCD():
    assert convertir_BCD_vers_decimal(additionner_nombres_format_BCD('27', '35')) == 62.00
    assert convertir_BCD_vers_decimal(additionner_nombres_format_BCD('59', '1.75')) == 60.75
    assert convertir_BCD_vers_decimal(additionner_nombres_format_BCD('0.99', '0.01')) == 1.00
    print("Les tests sont validés.")

test_additionner_nombres_format_BCD()
```

---

## Question 4 — aligner_quartets()

### Énoncé

Tester l'addition de `23` et `4`. Observer le problème. Modifier `aligner_quartets(q1, q2)` pour qu'elle ajoute des quartets `'0000'` **au début** de la liste la plus courte jusqu'à ce que les deux listes aient la même longueur.

### Pourquoi le problème apparaît

`23` est converti en 4 quartets : `['0010', '0011', '0000', '0000']`  
`4` est converti en 3 quartets : `['0000', '0100', '0000']`

La boucle d'addition parcourt les listes **par index**, de la fin vers le début. Si les listes ont des longueurs différentes, l'index `0` de chaque liste ne correspond pas au même rang décimal — on additionne des dizaines avec des centaines !

### Illustration du décalage

```
Index :        0       1       2       3
23 (4 qts) : 0010    0011    0000    0000   ← rang: cent. diz. euro cent.
 4 (3 qts) : 0000    0100    0000           ← rang:  diz. euro cent.
             ↑
             Index 0 de "4" correspond à des dizaines
             Index 0 de "23" correspond à des centaines
             → désalignement total !
```

### Après alignement correct

```
Index :        0       1       2       3
23 (4 qts) : 0010    0011    0000    0000
 4 (4 qts) : 0000    0000    0100    0000   ← '0000' ajouté en tête
             ✓ chaque colonne additionne bien le même rang
```

### Démarche

1. Calculer `diff = len(q1) - len(q2)`.
2. Si `diff > 0` : `q1` est plus longue → ajouter `diff` fois `'0000'` **en tête** de `q2`.
3. Si `diff < 0` : `q2` est plus longue → ajouter `abs(diff)` fois `'0000'` **en tête** de `q1`.
4. Retourner `(q1, q2)`.

**Point clé :** toujours ajouter à **gauche** (en tête), pas à droite. Ajouter à droite décalerait la virgule implicite.  
Syntaxe Python pour ajouter à gauche : `['0000'] * n + q`

### Solution

```python
def aligner_quartets(q1, q2):
    """
    Ajoute des quartets '0000' au début de la liste la plus courte
    pour que q1 et q2 aient la même longueur.
    """
    diff = len(q1) - len(q2)
    if diff > 0:
        q2 = ['0000'] * diff + q2
    elif diff < 0:
        q1 = ['0000'] * (-diff) + q1
    return q1, q2
```

### Fonction de test

```python
def test_aligner_quartets():
    q1, q2 = aligner_quartets(['0010', '0011', '0000', '0000'],
                               ['0000', '0100', '0000'])
    assert q1 == ['0010', '0011', '0000', '0000']
    assert q2 == ['0000', '0000', '0100', '0000']
    assert len(q1) == len(q2)
    q3, q4 = aligner_quartets(['0001'], ['0001', '0010', '0011'])
    assert len(q3) == len(q4)
    assert q3 == ['0000', '0000', '0001']
    q5, q6 = aligner_quartets(['0001', '0010'], ['0001', '0010'])
    assert q5 == q6
    print("Les tests sont validés.")

test_aligner_quartets()
```

---

## Code complet corrigé — addition_BCD.py

```python
#############################################################################
# Question 1 : Mise en évidence du problème des flottants
#############################################################################

def calcul_recettes():
    prix_menu = 2.27 + 5.19 + 1.81
    total = 0.0
    for _ in range(1000 * 500):
        total += prix_menu
    return total

print(calcul_recettes())


#############################################################################
# Question 2 : Conversion BCD vers Décimal
#############################################################################

def convertir_BCD_vers_decimal(liste_quartets):
    entier = 0
    for quartet in liste_quartets:
        chiffre = int(quartet, 2)
        entier = entier * 10 + chiffre
    return entier / 100

assert convertir_BCD_vers_decimal(['0001', '0011', '0101', '0110']) == 13.56


#############################################################################
# Fonctions fournies (inchangées)
#############################################################################

def convertir_dec_vers_BCD(decimal):
    ajouter_zero = False
    liste_quartets = []
    if '.' not in decimal:
        decimal = decimal + '.00'
    for i in range(len(decimal)):
        if decimal[i] != '.':
            quartet = bin(int(decimal[i]))[2:].zfill(4)
            liste_quartets.append(quartet)
        if decimal[i] == '.' and i == len(decimal) - 2:
            ajouter_zero = True
    if ajouter_zero:
        liste_quartets.append('0000')
    return liste_quartets


def additionner_binaire_quartets(quartet1, quartet2, retenue):
    somme = ""
    for i in range(4):
        bit1 = int(quartet1[3 - i])
        bit2 = int(quartet2[3 - i])
        total = bit1 + bit2 + retenue
        if total == 0:   somme = '0' + somme; retenue = 0
        elif total == 1: somme = '1' + somme; retenue = 0
        elif total == 2: somme = '0' + somme; retenue = 1
        elif total == 3: somme = '1' + somme; retenue = 1
    return somme, retenue


def corriger_BCD(somme, retenue):
    if somme[0] == '1' and (somme[1] == '1' or somme[2] == '1'):
        somme, retenue = additionner_binaire_quartets(somme, '0110', 0)
        return somme, retenue
    if retenue == 1:
        somme, _ = additionner_binaire_quartets(somme, '0110', 0)
        return somme, retenue
    return somme, retenue


#############################################################################
# Question 4 : aligner_quartets — CORRIGÉE
#############################################################################

def aligner_quartets(q1, q2):
    diff = len(q1) - len(q2)
    if diff > 0:
        q2 = ['0000'] * diff + q2
    elif diff < 0:
        q1 = ['0000'] * (-diff) + q1
    return q1, q2


#############################################################################
# Question 3 : additionner_nombres_format_BCD — CORRIGÉE
#############################################################################

def additionner_nombres_format_BCD(a, b):
    liste_quartets1 = convertir_dec_vers_BCD(a)
    liste_quartets2 = convertir_dec_vers_BCD(b)
    liste_quartets1, liste_quartets2 = aligner_quartets(liste_quartets1, liste_quartets2)
    retenue = 0
    resultat = []
    longueur_max = max(len(liste_quartets1), len(liste_quartets2))
    for i in range(longueur_max):
        index = longueur_max - i - 1
        somme, retenue = additionner_binaire_quartets(
            liste_quartets1[index], liste_quartets2[index], retenue)
        somme, retenue = corriger_BCD(somme, retenue)   # correction BCD ajoutée
        resultat.insert(0, somme)
    if retenue == 1:
        resultat.insert(0, '0001')
    return resultat
```

---

## Pièges fréquents

### Piège 1 — Quartet invalide non corrigé

Un quartet résultant d'une addition peut valoir entre `1010` (10) et `10010` (18 avec retenue). Toute valeur ≥ `1010` est **invalide en BCD** et doit être corrigée avec `+0110`.  
Sans correction, le résultat est incorrect mais aucune erreur Python n'est levée — le bug passe inaperçu.

### Piège 2 — Récupérer les deux valeurs de retour de corriger_BCD

`corriger_BCD` renvoie un **tuple** `(somme, retenue)`. Ne récupérer que la somme revient à perdre la nouvelle retenue éventuelle générée par la correction elle-même.

```python
# FAUX :
somme = corriger_BCD(somme, retenue)

# JUSTE :
somme, retenue = corriger_BCD(somme, retenue)
```

### Piège 3 — Ajouter les zéros d'alignement à droite

```python
# FAUX — décale la virgule vers la droite :
q2 = q2 + ['0000'] * diff

# JUSTE — ajoute des rangs de poids fort à gauche :
q2 = ['0000'] * diff + q2
```

### Piège 4 — Oublier la convention virgule implicite

La liste BCD ne code pas la virgule. La règle est toujours : les deux derniers quartets sont les centimes.  
Conséquence dans `convertir_BCD_vers_decimal` : diviser l'entier reconstitué par `100`.  
Vérification : `['0000', '0001', '0000']` doit donner `0.10`, pas `10`.

### Piège 5 — Comparer un float avec == après division par 100

La division `/100` recrée un flottant. Pour des tests robustes, préférer :
```python
assert abs(valeur - attendu) < 1e-9
# ou comparer l'entier avant division
assert entier == 1356  # plutôt que valeur == 13.56
```

---

## Astuces de vérification

### Test de cohérence aller-retour

```python
# convertir_BCD_vers_decimal(convertir_dec_vers_BCD(x)) doit redonner float(x)
assert convertir_BCD_vers_decimal(convertir_dec_vers_BCD('13.56')) == 13.56
assert convertir_BCD_vers_decimal(convertir_dec_vers_BCD('0.01')) == 0.01
assert convertir_BCD_vers_decimal(convertir_dec_vers_BCD('99.99')) == 99.99
```

### Test de commutativité de l'addition

```python
r1 = convertir_BCD_vers_decimal(additionner_nombres_format_BCD('27', '35'))
r2 = convertir_BCD_vers_decimal(additionner_nombres_format_BCD('35', '27'))
assert r1 == r2  # l'addition est commutative
```

### Cas avec retenue globale (5 quartets en sortie)

```python
# 99.99 + 0.01 = 100.00 → doit produire un cinquième quartet '0001'
resultat = additionner_nombres_format_BCD('99.99', '0.01')
assert len(resultat) == 5
assert convertir_BCD_vers_decimal(resultat) == 100.00
```

### Vérifier l'alignement

```python
q1, q2 = aligner_quartets(liste1, liste2)
assert len(q1) == len(q2)  # toujours vérifier après alignement
```

---

## Mini-exercices de calcul mental

### Exercice A — Conversion manuelle en BCD

Convertis ces montants en liste de quartets BCD (sans ordinateur) :

1. `7.50 €`
2. `12.09 €`
3. `0.01 €`

**Réponses :**
1. `['0111', '0101', '0000']` — 3 quartets : 7, 5, 0 → 7,50 €
2. `['0001', '0010', '0000', '1001']` — 4 quartets : 1, 2, 0, 9 → 12,09 €
3. `['0000', '0000', '0001']` — 3 quartets : 0, 0, 1 → 0,01 €

### Exercice B — Détection de quartet invalide

Parmi ces quartets, lesquels sont invalides en BCD ?

| Quartet  | Valeur décimale | Valide ? | Action si invalide |
|----------|-----------------|----------|--------------------|
| `1010`   | 10              | ❌ Non   | +6 → `10000` : quartet=`0000`, retenue=1 |
| `0111`   | 7               | ✅ Oui   | Rien à faire |
| `1100`   | 12              | ❌ Non   | +6 → `10010` : quartet=`0010`, retenue=1 |
| `1001`   | 9               | ✅ Oui   | Rien à faire |

### Exercice C — Tracer l'addition BCD à la main

Effectue l'addition BCD de `5.99` et `4.01` quartet par quartet.  
Quartets de `5.99` : `['0101', '1001', '1001']`  
Quartets de `4.01` : `['0100', '0000', '0001']`

| Rang     | A      | B      | Somme brute | Correction ? | Résultat |
|----------|--------|--------|-------------|--------------|----------|
| Centimes | `1001` | `0001` | `1010` ❌   | +`0110` → `10000` | `0000`, r=1 |
| Dixièmes | `1001` | `0000` + r=1 | `1010` ❌ | +`0110` → `10000` | `0000`, r=1 |
| Unités   | `0101` | `0100` + r=1 | `1010` ❌ | +`0110` → `10000` | `0000`, r=1 |
| Dizaines | —      | —      | r=1 final   | —            | `0001` |

**Résultat :** `['0001', '0000', '0000', '0000']` → 10,00 € ✓

---

## Récapitulatif — Points clés à retenir

| Notion | Retenir |
|--------|---------|
| Flottants | Accumulent des erreurs d'arrondi — impropres à la comptabilité |
| BCD | Chaque chiffre décimal (0-9) est codé sur 4 bits (quartet) |
| Quartets valides | `0000` (0) à `1001` (9) uniquement |
| Virgule implicite | Les 2 derniers quartets = centimes → division finale par 100 |
| Correction BCD | Si quartet ≥ 10 ou retenue : ajouter `0110` (6) au quartet |
| Alignement | Toujours ajouter les `'0000'` **à gauche** (poids fort) |
| Bug Q3 | Oubli de l'appel à `corriger_BCD` dans la boucle d'addition |
| Bug Q4 | `aligner_quartets` ne complétait pas les listes — `return q1, q2` sans modification |

---

*Lycée Antoine Watteau — DarkSATHI Li — BAC NSI 2026 — Sujet n°8*
