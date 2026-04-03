# Codage RLE — Fiche de révision guidée
*BAC NSI 2026 — Sujet n°1 — Partie pratique*  
*Terminale NSI · Algorithmique · Traitement de données*

---

## Sommaire

1. [Rappels de cours – images en niveaux de gris](#1--rappels--les-images-en-niveaux-de-gris)
2. [Le codage RLE – principe et vocabulaire](#2--le-codage-rle--principe)
3. [Question 1 – Longueur du code RLE](#question-1--longueur-du-code-rle)
4. [Question 2 – Écrire `decodage_rle`](#question-2--écrire-decodage_rle)
5. [Question 3 – Tester sur de vraies images](#question-3--tester-sur-de-vraies-images)
6. [Question 4 – Dépasser la limite de 255](#question-4--dépasser-la-limite-de-255)
7. [Pièges fréquents & astuces de vérification](#pièges-fréquents--astuces-de-vérification)

---

## 1 — Rappels : les images en niveaux de gris

Imagine que tu regardes une photo en noir et blanc. Chaque point de cette image — appelé **pixel** — possède une teinte de gris, que l'ordinateur encode par un entier entre `0` (noir absolu) et `255` (blanc pur). Entre les deux, `128` correspond à un gris moyen.

> **Définition – Pixel et niveau de gris**  
> Un **pixel** (*picture element*) est la plus petite unité d'une image numérique.  
> Dans une image en niveaux de gris, chaque pixel est codé par un **octet** (valeur entre 0 et 255).  
> La valeur `0` correspond au noir, la valeur `255` au blanc.

Pour stocker toute une image, on la « lit » ligne par ligne, de gauche à droite et de haut en bas, et on mémorise les valeurs de tous les pixels dans une simple liste Python. En connaissant la largeur de l'image, on peut reconstruire chaque ligne.

**Exemple concret — mini-image 5 × 4 pixels :**

| ligne | col 1 | col 2 | col 3 | col 4 | col 5 |
|-------|-------|-------|-------|-------|-------|
| 1     | 0     | 128   | 128   | 255   | 64    |
| 2     | 255   | 128   | 128   | 255   | 255   |
| 3     | 128   | 128   | 0     | 0     | 64    |
| 4     | 255   | 0     | 0     | 0     | 0     |

Aplatie en liste Python :
```
[0, 128, 128, 255, 64, 255, 128, 128, 255, 255, 128, 128, 0, 0, 64, 255, 0, 0, 0, 0]
```
Avec la largeur `5`, on peut retrouver l'image : ligne 1 = indices 0 à 4, ligne 2 = indices 5 à 9, etc.

Les images du sujet sont des dessins en niveaux de gris avec de grandes zones uniformes (fond noir `0`, texte blanc `255`). C'est exactement cette régularité que le codage RLE va exploiter.

---

## 2 — Le codage RLE : principe

Imagine que tu dois dicter cette liste : `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255]`. Tu pourrais dire « douze zéros, puis trois deux-cent-cinquante-cinq » — c'est beaucoup plus rapide. C'est exactement l'idée du codage RLE.

> **Définition – Codage RLE**  
> **RLE** signifie *Run-Length Encoding* (codage par plages).  
> Une *plage* (*run*) est une suite de valeurs identiques consécutives.  
> Chaque plage est remplacée par le couple `(compte, valeur)`, où `compte` est le nombre d'occurrences.  
> L'ensemble des couples est aplati en une seule liste :  
> `[compte1, valeur1, compte2, valeur2, ...]`

**Exemple pas à pas :**

Liste de départ : `[4, 4, 4, 0, 5, 5]`
- La valeur `4` apparaît **3 fois** → couple `(3, 4)`
- La valeur `0` apparaît **1 fois** → couple `(1, 0)`
- La valeur `5` apparaît **2 fois** → couple `(2, 5)`

Liste RLE obtenue : `[3, 4, 1, 0, 2, 5]`  
(mais pour `[0, 0, 0, 0, 0]` on obtient `[5, 0]` — bien plus courte !)

### Architecture du code fourni

| Fonction | Rôle |
|---|---|
| `codage_rle(liste_octets)` | Compresse une liste d'octets en liste RLE |
| `decodage_rle(liste_rle)` | **À compléter** — décompresse une liste RLE |
| `enregistrer_octets(nom, liste)` | Écrit une liste d'octets dans un fichier binaire |
| `charger_octets(nom)` | Lit un fichier binaire et renvoie la liste d'octets |
| `enregistrer_image(nom, largeur, liste)` | Enregistre une liste de pixels comme image PNG |
| `charger_image(nom)` | Charge un PNG et renvoie `(largeur, liste_pixels)` |
| `encoder_decoder_image(nom)` | Encode puis décode une image pour tester le cycle complet |

### Code de `codage_rle` (fourni — à étudier)

```python
def codage_rle(liste_octets):
    '''Renvoie une liste d'octets obtenue par compression RLE'''
    liste_rle = []
    i = 0
    while i < len(liste_octets):
        c = liste_octets[i]   # valeur courante
        k = 1                  # compteur d'occurrences
        # tant que le pixel suivant est identique, on continue
        while i + k < len(liste_octets) and liste_octets[i + k] == c:
            k += 1
        liste_rle.append(k)   # on ajoute le compte
        liste_rle.append(c)   # on ajoute la valeur
        i += k                 # on saute toute la plage
    return liste_rle
```

> **Astuce de lecture :** La boucle extérieure parcourt chaque *début de plage*. La boucle intérieure compte combien de fois la même valeur se répète. À la fin, `k` contient le nombre exact d'occurrences de `c` à partir de la position `i`. Le saut `i += k` permet de passer directement à la plage suivante.

---

## Question 1 — Longueur du code RLE

**Énoncé :** Déterminer si la liste obtenue par codage RLE est **forcément** de longueur inférieure ou égale à la liste de départ. Justifier avec un contre-exemple si ce n'est pas le cas.

> 💡 **Indice 1 — Réfléchis au pire des cas**  
> Que se passe-t-il si **aucune valeur ne se répète** dans la liste ?  
> Par exemple : `[1, 2, 3, 4, 5]`. Quelle est la longueur de la liste RLE produite ?

> 💡 **Indice 2 — Calcule la longueur**  
> Chaque plage, même de longueur 1, génère **deux éléments** dans la liste RLE (le compte et la valeur).  
> Donc si une liste de longueur n est composée de n valeurs toutes différentes, chaque valeur forme une plage de longueur 1. Combien d'éléments contient la liste RLE correspondante ?

### ✅ Correction — Question 1

**Non, la liste RLE n'est pas forcément plus courte.**

Contre-exemple : la liste `[1, 2, 3, 4, 5]` (5 valeurs toutes différentes). Chaque valeur forme une plage de longueur 1, ce qui génère les couples `(1,1), (1,2), (1,3), (1,4), (1,5)`, soit la liste RLE `[1, 1, 1, 2, 1, 3, 1, 4, 1, 5]` — de longueur **10**, le double de la liste initiale !

**Règle générale :** si une liste de longueur *n* est constituée de *p* plages, alors la liste RLE a pour longueur *2p*. La liste RLE est plus courte si et seulement si *2p ≤ n*, c'est-à-dire si les plages sont assez longues (en moyenne au moins 2 éléments chacune).

**Conclusion :** le codage RLE est efficace sur des images avec de larges zones uniformes (comme `bac_nsi_256.png`), mais il peut *alourdir* une image dont chaque pixel est différent.

---

## Question 2 — Écrire `decodage_rle`

**Énoncé :** En étudiant bien la fonction `codage_rle`, écrire le corps de la fonction `decodage_rle` qui réalise le **décodage** d'une liste RLE et renvoie la liste d'octets originale.

```python
def decodage_rle(liste_rle):
    '''Renvoie la liste d'octets obtenue à partir de la liste RLE.'''
    # À toi de compléter !
    pass


def test_decodage_rle():
    assert decodage_rle([2, 255, 1, 0, 3, 255]) == [255, 255, 0, 255, 255, 255]
    assert decodage_rle([5, 0]) == [0, 0, 0, 0, 0]
    assert decodage_rle([1, 128, 1, 64, 1, 0]) == [128, 64, 0]
    assert decodage_rle([3, 4, 1, 0, 2, 5]) == [4, 4, 4, 0, 5, 5]
    print("Les tests sont validés.")

test_decodage_rle()
```

> 💡 **Indice 1 — Structure des données**  
> La liste RLE est de la forme `[compte1, valeur1, compte2, valeur2, ...]`.  
> Les éléments sont par paires : l'élément à l'indice `i` est un compte, celui à l'indice `i+1` est la valeur correspondante.  
> Comment parcourir une liste deux éléments par deux éléments en Python ?

> 💡 **Indice 2 — Répéter une valeur**  
> Pour ajouter `k` fois la valeur `v` à une liste `resultat`, deux approches :
> ```python
> # Approche 1 : boucle for
> for _ in range(k):
>     resultat.append(v)
>
> # Approche 2 : extension de liste (plus lisible)
> resultat.extend([v] * k)
> ```

### ✅ Correction — Question 2

```python
def decodage_rle(liste_rle):
    '''Renvoie la liste d'octets obtenue à partir de la liste RLE.'''
    liste_octets = []
    i = 0
    while i < len(liste_rle):
        k = liste_rle[i]       # nombre de répétitions
        c = liste_rle[i + 1]   # valeur à répéter
        liste_octets.extend([c] * k)
        i += 2                 # on avance de 2 (compte + valeur)
    return liste_octets
```

La structure est le symétrique exact de `codage_rle` : on parcourt la liste RLE deux éléments par deux (un couple compte/valeur à chaque itération), et on étend la liste résultat avec `k` copies de `c`.

**Vérification :** `decodage_rle(codage_rle(liste_octets))` doit renvoyer `liste_octets` — les deux fonctions sont bien inverses l'une de l'autre.

---

## Question 3 — Tester sur de vraies images

**Énoncé :** Utilise la fonction `encoder_decoder_image` sur les deux images `bac_nsi_32.png` et `bac_nsi_256.png`. Observe et explique la différence de comportement entre les deux images.

*La fonction encode l'image, enregistre le résultat dans un fichier `.rle`, puis décode ce fichier et enregistre l'image reconstruite dans un fichier `.dec.png`.*

**Rappel — Les deux images du sujet :**  
Les deux images représentent le même texte « BAC NSI » en blanc sur fond noir.
- `bac_nsi_32.png` — version **32 × 32 pixels** (très petite)
- `bac_nsi_256.png` — version **256 × 256 pixels** (grande)

La grande image a de très longues lignes de pixels noirs consécutifs — des plages bien plus longues que 255 éléments. C'est là que le problème va apparaître.

> 💡 **Indice 1 — Rappel sur les octets**  
> La liste RLE est enregistrée dans un fichier binaire via `enregistrer_octets`. Chaque élément de la liste est écrit comme un octet. Or un octet ne peut contenir qu'une valeur entre 0 et 255. Que se passe-t-il si le *compte* d'une plage dépasse 255 ?

> 💡 **Indice 2 — Effet sur l'image reconstruite**  
> ```python
> fichier.write(bytes([max(0, min(255, b)) for b in liste_octets]))
> ```
> Toute valeur supérieure à 255 est tronquée à 255. Un compte de 300 sera donc stocké comme 255. Lors du décodage, on lira 255 répétitions au lieu de 300 — l'image reconstruite sera **incorrecte**.

### ✅ Correction — Question 3

**Sur `bac_nsi_32.png` :** l'image est 32 × 32 = 1 024 pixels. Chaque ligne ne fait que 32 pixels. Les plages de pixels noirs consécutifs ne dépassent jamais 255 éléments. L'encodage et le décodage fonctionnent correctement — l'image reconstruite est identique à l'originale.

**Sur `bac_nsi_256.png` :** l'image est 256 × 256 = 65 536 pixels. Dans une image de 256 pixels de large avec un fond majoritairement noir, certaines lignes peuvent contenir plus de 255 pixels noirs consécutifs (par exemple toute la première ligne du fond est exactement 256 pixels noirs). Or, le compte est stocké comme un octet, donc limité à 255. Lors de l'enregistrement, un compte de 256 est tronqué à 255. Le décodage restitue alors 255 pixels au lieu de 256, et la liste est trop courte pour reconstruire l'image : celle-ci apparaît **corrompue ou décalée**.

**Conclusion :** le problème vient du fait que le *compte* d'une plage peut dépasser 255, valeur maximale d'un octet. C'est exactement ce que résout la Question 4.

---

## Question 4 — Dépasser la limite de 255

**Énoncé :** Proposer une démarche de résolution du problème identifié en Question 3 (compte pouvant dépasser 255), puis l'implémenter en modifiant `codage_rle` et `decodage_rle`.

**Rappel du problème :** lorsqu'une plage contient plus de 255 éléments identiques, le compte ne tient pas dans un seul octet. Il faut trouver une façon de représenter ce grand compte en utilisant uniquement des valeurs entre 0 et 255.

```python
def codage_rle_v2(liste_octets):
    '''Codage RLE gérant les comptes supérieurs à 255.'''
    # À toi de compléter !
    pass


def decodage_rle_v2(liste_rle):
    '''Décodage RLE — identique à decodage_rle si le codage est correct.'''
    # À toi de compléter !
    pass


def test_codage_rle_v2():
    assert codage_rle_v2([255, 255, 0, 255, 255, 255]) == [2, 255, 1, 0, 3, 255]
    assert codage_rle_v2([0] * 256) == [255, 0, 1, 0]   # plage de 256 → (255,0) + (1,0)
    assert codage_rle_v2([128] * 300) == [255, 128, 45, 128]
    print("Les tests sont validés.")


def test_decodage_rle_v2():
    assert decodage_rle_v2([255, 0, 1, 0]) == [0] * 256
    assert decodage_rle_v2([255, 128, 45, 128]) == [128] * 300
    assert decodage_rle_v2([2, 255, 1, 0, 3, 255]) == [255, 255, 0, 255, 255, 255]
    print("Les tests sont validés.")
```

> 💡 **Indice 1 — Découper les grandes plages**  
> L'idée la plus simple : si une plage a un compte supérieur à 255, on la **découpe** en plusieurs sous-plages de taille maximale 255.  
> Exemple : une plage de 300 pixels noirs devient deux couples consécutifs : `(255, 0)` puis `(45, 0)`. Le décodage lit les deux couples et ajoute `255 + 45 = 300` pixels noirs.

> 💡 **Indice 2 — Modifier codage_rle**  
> Dans `codage_rle`, une fois que tu connais `k` (le compte total), au lieu d'ajouter directement `k`, utilise une boucle :
> ```python
> while k > 255:
>     liste_rle.append(255)
>     liste_rle.append(c)
>     k -= 255
> liste_rle.append(k)
> liste_rle.append(c)
> ```
> `decodage_rle` n'a alors **pas besoin d'être modifié** — il lit simplement plusieurs couples `(255, valeur)` consécutifs et les reconstruit normalement.

### ✅ Correction — Question 4

```python
def codage_rle_v2(liste_octets):
    '''Codage RLE gérant les comptes supérieurs à 255.
    Les grandes plages sont découpées en sous-plages de 255 maximum.'''
    liste_rle = []
    i = 0
    while i < len(liste_octets):
        c = liste_octets[i]
        k = 1
        while i + k < len(liste_octets) and liste_octets[i + k] == c:
            k += 1
        nb_pleins = k // 255   # nombre de morceaux de 255
        reste     = k % 255    # ce qui reste
        for _ in range(nb_pleins):
            liste_rle.append(255)
            liste_rle.append(c)
        if reste > 0:
            liste_rle.append(reste)
            liste_rle.append(c)
        i += k
    return liste_rle


def decodage_rle_v2(liste_rle):
    '''Décodage RLE — identique à la version de base.
    Le découpage est transparent au décodeur.'''
    liste_octets = []
    i = 0
    while i < len(liste_rle):
        k = liste_rle[i]
        c = liste_rle[i + 1]
        liste_octets.extend([c] * k)
        i += 2
    return liste_octets
```

**Démarche :** plutôt que de changer le format de stockage, on garde des comptes sur un seul octet en découpant les grandes plages. Une plage de *k* pixels identiques devient ⌊k/255⌋ couples `(255, valeur)` suivis d'un couple `(k mod 255, valeur)` si le reste est non nul.

**Avantage :** le décodeur n'a pas besoin d'être modifié — il lit simplement plusieurs couples consécutifs avec la même valeur et les empile.

**Cas particulier :** si *k* est un multiple exact de 255 (ex : k = 510), on n'ajoute que les 2 couples pleins, sans couple résiduel. La condition `if reste > 0` gère ce cas.

---

## Pièges fréquents & astuces de vérification

### ⚠️ Piège 1 — Confondre compte et valeur

Dans la liste RLE, l'ordre est toujours **compte d'abord, valeur ensuite**. Inverser les deux produit une liste incorrecte. Pour vérifier : `[2, 255]` signifie « deux fois 255 », pas « deux-cent-cinquante-cinq fois 2 ».

### ⚠️ Piège 2 — Oublier le pas de 2 dans `decodage_rle`

La liste RLE se lit **deux éléments par deux**. Si tu fais `i += 1` au lieu de `i += 2`, tu vas lire les valeurs comme des comptes et les comptes comme des valeurs. Le résultat sera complètement erroné, souvent très long ou avec une erreur d'index.

### ⚠️ Piège 3 — Liste RLE de longueur impaire

Une liste RLE valide a toujours un nombre **pair** d'éléments. Si ton décodeur reçoit une liste de longueur impaire, il va provoquer une `IndexError` à la dernière itération (`liste_rle[i + 1]` hors bornes). Pense à vérifier cette propriété dans tes tests.

### ⚠️ Piège 4 — Ne pas traiter le cas du compte nul

Dans la version v2 (Question 4), si `k` est un multiple exact de 255, le reste vaut 0. Il ne faut **pas** ajouter le couple `(0, valeur)` — cela produirait un zéro dans la liste RLE, interprété comme « répéter 0 fois ». La condition `if reste > 0` est donc indispensable.

### ✅ Astuces de vérification

- **Aller-retour :** `decodage_rle(codage_rle(liste)) == liste` doit toujours être vrai. C'est le test ultime.
- **Liste vide :** `codage_rle([]) == []` et `decodage_rle([]) == []` doivent renvoyer une liste vide sans erreur.
- **Liste d'un seul élément :** `codage_rle([42]) == [1, 42]`.
- **Taille du fichier :** après `encoder_decoder_image`, compare la taille du fichier `.rle` avec l'original — sur `bac_nsi_256.png`, le fichier RLE doit être nettement plus petit si la version v2 est utilisée.

---

### Mini-exercice A — Calcul mental RLE

Sans ordinateur, donne le codage RLE des listes suivantes :
1. `[7, 7, 7, 7, 3, 3]`
2. `[0, 255, 0, 255, 0]`
3. `[128]`

**Réponses :**
1. `[4, 7, 2, 3]`
2. `[1, 0, 1, 255, 1, 0, 1, 255, 1, 0]` — liste plus longue que l'originale !
3. `[1, 128]`

---

### Mini-exercice B — Décodage mental

Sans ordinateur, décode les listes RLE suivantes :
1. `[4, 0, 2, 255]`
2. `[1, 64, 3, 128, 1, 64]`
3. `[255, 0, 1, 0]` — comment interprètes-tu deux couples avec la même valeur ?

**Réponses :**
1. `[0, 0, 0, 0, 255, 255]`
2. `[64, 128, 128, 128, 64]`
3. `[0] * 256` — 255 zéros puis 1 zéro = 256 zéros au total. C'est la technique de la Question 4 !

---

## Récapitulatif — Ce que tu dois retenir

- Le codage RLE remplace chaque suite de valeurs identiques par le couple `(compte, valeur)`.
- La liste RLE **n'est pas toujours plus courte** — elle peut être deux fois plus longue dans le pire cas.
- Le décodage est l'opération inverse : pour chaque couple, on ajoute `compte` fois la `valeur`.
- La limite de 255 vient du stockage des comptes sur un seul octet.
- La solution : découper les grandes plages en sous-plages de taille maximale 255.
- Le décodeur n'a pas besoin d'être modifié — il lit les couples consécutifs normalement.

---

*DarkSATHI Li — NSI Terminale BAC 2026*
