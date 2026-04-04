# Simulation Coccinelles — Fiche de révision guidée

**BAC NSI 2026 — Sujet n°7 — Partie pratique**  
Terminale NSI · Programmation Orientée Objet · Simulation d'écosystème  
*Lycée Antoine Watteau — DarkSATHI Li*

---

## Sommaire

1. [Introduction & Rappels — POO, attributs, méthodes](#1--introduction--rappels-de-cours)
2. [Question 1 — Créer la population initiale et simuler 5 jours](#question-1--population-initiale--5-jours-de-simulation)
3. [Question 2 — Écrire `simulation_simple`](#question-2--la-fonction-simulation_simple)
4. [Question 3 — Documenter `chasser`](#question-3--documenter-la-méthode-chasser)
5. [Question 4 — Améliorer le modèle biologique](#question-4--améliorer-le-modèle-biologique)
6. [Pièges fréquents](#pièges-fréquents--points-de-vigilance)
7. [Ce que tu dois retenir](#ce-que-tu-dois-retenir)

---

## 1 — Introduction & Rappels de cours

### Le contexte : une serre sous attaque

Un producteur de tomates sous serre fait face à une invasion de pucerons. Pour éviter les pesticides, il lâche des coccinelles — leurs prédatrices naturelles. Ton rôle : **modéliser cet écosystème en Python** pour prédire ce qui va se passer.

**🐞 Coccinelles** → *mangent* → **🦟 Pucerons**

- Les coccinelles chassent, vieillissent et se reproduisent.
- Les pucerons prolifèrent de **+20 % par jour** s'ils ne sont pas mangés.

Chaque journée, la simulation effectue dans cet ordre :
1. La **chasse** (les coccinelles mangent des pucerons)
2. La **reproduction** (les femelles bien nourries pondent)
3. Le **vieillissement** (certaines coccinelles meurent)
4. La **croissance des pucerons** (+20 %)

---

### Rappel — La Programmation Orientée Objet (POO)

Imagine que chaque coccinelle est une **fiche individuelle** qui contient ses informations personnelles et ses actions possibles. En Python, on appelle ça un **objet**. Le modèle de cette fiche (ce qu'elle contient) est défini par une **classe**.

#### Vocabulaire POO essentiel

| Terme | Définition | Exemple dans ce sujet |
|---|---|---|
| `classe` | Le modèle (le plan de construction) | `class Coccinelle` |
| `objet` / instance | Un exemplaire concret de la classe | `c = Coccinelle("femelle", 10, 2)` |
| `attribut` | Une donnée propre à chaque objet | `c.age`, `c.sexe`, `c.niv_nutrition` |
| `méthode` | Une fonction appartenant à la classe | `c.chasser(200, 3)`, `c.reproduction()` |
| `__init__` | Le constructeur (appelé à la création) | `Coccinelle("femelle", 10, 2)` |

---

### La classe `Coccinelle` en détail

Chaque coccinelle possède quatre attributs définis dans `__init__` :

- `age` — âge en jours. Une coccinelle meurt quand `age >= esperance_de_vie`.
- `esperance_de_vie` — durée de vie maximale, tirée aléatoirement entre 200 et 350 jours.
- `sexe` — `"male"` ou `"femelle"`.
- `niv_nutrition` — nombre de jours consécutifs bien nourris. Monte si elle mange ≥ 10 proies, descend sinon (minimum 0).

---

### Les méthodes à connaître

| Méthode | Rôle |
|---|---|
| `Coccinelle.__init__(sexe, age, niv_nutrition)` | Crée une coccinelle avec ses attributs de départ |
| `chasser(nb_proies, nb_coccinelles)` | Chasse et renvoie le nouveau nombre de proies. Met à jour `niv_nutrition`. |
| `reproduction()` | Renvoie une liste de 2 descendants si femelle bien nourrie, sinon liste vide |
| `a_survecu()` | Incrémente l'âge et renvoie `True` si elle est encore en vie |
| `evolution(population, nb_proies)` | Simule **une journée** complète et renvoie `(population_suivante, nouveau_nb_proies)` |

#### Exemple — Créer un objet Coccinelle

```python
# Syntaxe : Coccinelle(sexe, age, niv_nutrition)
c1 = Coccinelle("femelle", 10, 2)
c2 = Coccinelle("male", 10, 2)
print(c1.age)    # affiche 10
print(c1.sexe)   # affiche "femelle"

# La méthode __repr__ permet un affichage lisible :
print(c1)
# → Coccinelle femelle, âge: 10/274, niv_nutrition: 2
```

> **Remarque :** L'espérance de vie (`274` dans l'exemple) est **aléatoire** à chaque création — donc tes résultats numériques varieront d'une exécution à l'autre. C'est tout à fait normal pour un modèle de simulation.

---

## Question 1 — Population initiale & 5 jours de simulation

### Énoncé

Créer une population initiale contenant **3 coccinelles** (2 femelles et 1 mâle), toutes âgées de 10 jours et ayant un niveau de nutrition de 2. Le nombre initial de pucerons est fixé à **200**.

Écrire une séquence d'instructions (utilisant une boucle) permettant de simuler l'évolution de ce petit écosystème sur **5 jours consécutifs**, en appelant la fonction `evolution`. Afficher le nombre de coccinelles et de pucerons à la fin de chaque journée.

✋ *Appel professeur — présente ta réponse ou sollicite de l'aide.*

---

### Comment lire les résultats d'`evolution` ?

La fonction `evolution` renvoie un **tuple à deux éléments** : la nouvelle liste de coccinelles et le nouveau nombre de pucerons. Pour récupérer les deux valeurs, on peut utiliser le *déballage* :

```python
population, nb_proies = evolution(population, nb_proies)
# Maintenant population et nb_proies sont mis à jour
```

### Indice 1 — Créer la liste initiale

```python
population = [
    Coccinelle("femelle", 10, 2),
    Coccinelle("femelle", 10, 2),
    Coccinelle("male", 10, 2)
]
nb_proies = 200
```

### Indice 2 — Structure de la boucle

```python
for jour in range(1, 6):   # 5 jours : jour 1, 2, 3, 4, 5
    population, nb_proies = evolution(population, nb_proies)
    print(f"Jour {jour} : {len(population)} coccinelles, {nb_proies} pucerons")
```

---

### Correction — Question 1

```python
# Création de la population initiale
population = [
    Coccinelle("femelle", 10, 2),
    Coccinelle("femelle", 10, 2),
    Coccinelle("male", 10, 2)
]
nb_proies = 200

# Boucle sur 5 jours
for jour in range(1, 6):
    population, nb_proies = evolution(population, nb_proies)
    print(f"Jour {jour} : {len(population)} coccinelle(s), {nb_proies} puceron(s)")
```

> Les résultats sont **aléatoires** (car `random.randint` est utilisé dans `chasser` et `__init__`). Plusieurs exécutions donneront des valeurs différentes. C'est le propre d'un modèle de simulation.

---

## Question 2 — La fonction `simulation_simple`

### Énoncé

Écrire une fonction `simulation_simple(population, nb_proies)` qui automatise ce processus sur une **durée maximale de 30 jours**.

Cette fonction doit s'interrompre prématurément si la population de coccinelles ou de pucerons **tombe à zéro**.

Elle doit renvoyer un **triplet (tuple)** contenant : le nombre final de coccinelles, le nombre final de pucerons, et le nombre de jours effectivement simulés. Tester avec la même population initiale face à **1 000 pucerons**.

✋ *Appel professeur — présente ta réponse ou sollicite de l'aide.*

---

### Comment structurer cette fonction ?

Il faut une boucle qui tourne **au maximum 30 fois**, mais qui peut s'arrêter avant si une condition de fin est atteinte. La boucle `while` est parfaite pour ça.

#### Structure générale

```python
def simulation_simple(population, nb_proies):
    jour = 0
    while jour < 30 and len(population) > 0 and nb_proies > 0:
        population, nb_proies = evolution(population, nb_proies)
        jour += 1
    return (len(population), nb_proies, jour)
```

### Indice — Pourquoi un tuple en retour ?

Renvoyer plusieurs valeurs à la fois se fait naturellement avec un tuple en Python. L'appelant peut ensuite déballer :

```python
nb_cocci, nb_pucerons, nb_jours = simulation_simple(...)

resultat = simulation_simple(population, nb_proies)
print(f"Résultat : {resultat[0]} coccinelles, {resultat[1]} pucerons après {resultat[2]} jours")
```

---

### Correction — Question 2

```python
def simulation_simple(population, nb_proies):
    """
    Simule l'écosystème sur au maximum 30 jours.
    S'arrête si la population de coccinelles ou le nombre de pucerons
    tombe à zéro.
    Renvoie un triplet (nb_coccinelles, nb_pucerons, nb_jours_simules).
    """
    jour = 0
    while jour < 30 and len(population) > 0 and nb_proies > 0:
        population, nb_proies = evolution(population, nb_proies)
        jour += 1
    return (len(population), nb_proies, jour)

# Test avec 1000 pucerons
population = [
    Coccinelle("femelle", 10, 2),
    Coccinelle("femelle", 10, 2),
    Coccinelle("male", 10, 2)
]
nb_cocci, nb_puce, nb_jours = simulation_simple(population, 1000)
print(f"Fin après {nb_jours} jour(s) : {nb_cocci} coccinelle(s), {nb_puce} puceron(s)")
```

#### Tests

```python
def test_simulation_simple():
    # Test 1 : ne dépasse pas 30 jours, valeurs positives
    pop = [Coccinelle("femelle", 10, 2), Coccinelle("femelle", 10, 2), Coccinelle("male", 10, 2)]
    nb_cocci, nb_puce, nb_jours = simulation_simple(pop, 5)
    assert nb_jours <= 30, "La simulation ne doit pas dépasser 30 jours"
    assert nb_cocci >= 0 and nb_puce >= 0, "Les valeurs sont positives"

    # Test 2 : les trois valeurs sont bien des entiers
    pop2 = [Coccinelle("femelle", 10, 2), Coccinelle("femelle", 10, 2), Coccinelle("male", 10, 2)]
    nb_cocci2, nb_puce2, nb_jours2 = simulation_simple(pop2, 1000)
    assert isinstance(nb_cocci2, int) and isinstance(nb_puce2, int) and isinstance(nb_jours2, int)

    # Test 3 : la fonction renvoie bien un triplet
    pop3 = [Coccinelle("femelle", 10, 2)]
    resultat = simulation_simple(pop3, 1000)
    assert len(resultat) == 3, "Le retour doit être un triplet"

    print("Les tests sont validés.")
```

> La condition de la boucle `while` cumule trois gardes : ne pas dépasser 30 jours, avoir encore des coccinelles, avoir encore des pucerons. Dès qu'une condition est fausse, la simulation s'arrête et renvoie l'état courant.

---

## Question 3 — Documenter la méthode `chasser`

### Énoncé

Écrire la **documentation** (docstring) et les **commentaires** de la méthode `chasser`. La documentation doit expliquer ce que fait la méthode, ses paramètres, et ce qu'elle renvoie. Les commentaires inline doivent expliquer les parties non évidentes du code.

---

### Qu'est-ce qu'une docstring ?

Une **docstring** est une chaîne de caractères placée juste après l'en-tête d'une fonction ou méthode, entre triples guillemets. Elle décrit le contrat de la fonction : ce qu'elle fait, ce qu'elle attend, ce qu'elle renvoie.

#### Structure d'une bonne docstring

```python
def ma_fonction(param1, param2):
    """
    Description générale en une phrase.

    param1 : type et rôle du premier paramètre
    param2 : type et rôle du second paramètre

    Renvoie : type et signification de la valeur renvoyée
    """
    ...
```

---

### Le code de `chasser` à documenter

```python
def chasser(self, nb_proies, nb_coccinelles):
    if nb_coccinelles == 0:
        return nb_proies

    proies_par_cocci = nb_proies / nb_coccinelles

    if proies_par_cocci > 20:
        consomme = random.randint(12, 20)
    elif proies_par_cocci > 10:
        consomme = random.randint(8, 15)
    else:
        consomme = random.randint(3, 8)

    consomme = min(consomme, nb_proies)

    if consomme >= 10:
        self.niv_nutrition += 1
    else:
        self.niv_nutrition = max(0, self.niv_nutrition - 1)

    return nb_proies - consomme
```

### Indice — Analyse bloc par bloc

- **Bloc 1** (`if nb_coccinelles == 0`) : cas de sécurité pour éviter une division par zéro.
- **Bloc 2** (`proies_par_cocci`) : calcule la disponibilité en nourriture par coccinelle.
- **Bloc 3** (les trois `if/elif/else`) : plus il y a de proies par coccinelle, plus elle mange.
- **Bloc 4** (`min(consomme, nb_proies)`) : on ne peut pas manger plus qu'il n'en reste.
- **Bloc 5** (mise à jour de `niv_nutrition`) : bon repas → monte, mauvais repas → descend (plancher à 0).
- **Bloc 6** (`return`) : renvoie le nombre de proies restantes après la chasse.

---

### Correction — Question 3

```python
def chasser(self, nb_proies, nb_coccinelles):
    """
    Simule la chasse d'une coccinelle pour la journée.

    La quantité de proies consommées dépend de la densité de nourriture
    disponible par coccinelle. Un bon repas (>= 10 proies) améliore le
    niveau de nutrition ; un mauvais repas le diminue (plancher à 0).

    nb_proies      : int — nombre de proies disponibles dans la serre
    nb_coccinelles : int — nombre de coccinelles présentes (pour partager)

    Renvoie : int — nombre de proies restantes après la chasse de cette coccinelle
    """
    # Cas de sécurité : évite une division par zéro si la population est vide
    if nb_coccinelles == 0:
        return nb_proies

    # Densité de nourriture disponible par coccinelle
    proies_par_cocci = nb_proies / nb_coccinelles

    # Plus la densité est élevée, plus la coccinelle mange
    if proies_par_cocci > 20:
        consomme = random.randint(12, 20)   # abondance : repas copieux
    elif proies_par_cocci > 10:
        consomme = random.randint(8, 15)    # nourriture suffisante
    else:
        consomme = random.randint(3, 8)     # pénurie : repas maigre

    # Garde-fou : on ne peut pas manger plus qu'il n'en reste
    consomme = min(consomme, nb_proies)

    # Mise à jour du niveau de nutrition
    if consomme >= 10:
        self.niv_nutrition += 1                          # bon repas → niveau monte
    else:
        self.niv_nutrition = max(0, self.niv_nutrition - 1)  # mauvais repas → descend (min. 0)

    return nb_proies - consomme    # proies restantes après la chasse
```

---

## Question 4 — Améliorer le modèle biologique

### Énoncé

Le producteur constate deux limites biologiques dans le modèle actuel :

1. **Maturité sexuelle absente :** le modèle permet la reproduction dès la naissance, alors qu'en réalité elle n'est possible qu'**à partir de 20 jours de vie**.
2. **Impact du manque de nourriture sous-estimé :** quand `niv_nutrition == 0`, la coccinelle a en réalité **1 chance sur 3 (environ 33 %)** de ne pas survivre à la journée.

Modifier les méthodes `reproduction` et `a_survecu` pour intégrer ces deux nouvelles règles biologiques. Tester à nouveau la simulation pour observer les changements.

✋ *Appel professeur — présente ta réponse ou sollicite de l'aide.*

---

### Modification 1 — La maturité sexuelle dans `reproduction`

#### Code actuel

```python
def reproduction(self):
    descendants = []
    if self.sexe == "femelle" and self.niv_nutrition >= 2:
        descendants.append(Coccinelle("male", 0, 0))
        descendants.append(Coccinelle("femelle", 0, 0))
        self.niv_nutrition = 0
    return descendants
```

#### Indice — Quelle ligne modifier ?

Il suffit d'ajouter `and self.age >= 20` dans la condition du `if` :

```python
if self.sexe == "femelle" and self.niv_nutrition >= 2 and self.age >= 20:
```

---

### Modification 2 — Le risque de mort par faim dans `a_survecu`

#### Code actuel

```python
def a_survecu(self):
    self.age = self.age + 1
    return self.age < self.esperance_de_vie
```

#### Indice — Simuler une probabilité avec `random.random()`

`random.random()` renvoie un flottant entre 0 inclus et 1 exclu. La probabilité que ce flottant soit strictement inférieur à `1/3` est exactement 33 %.

```python
if self.niv_nutrition == 0 and random.random() < 1/3:
    return False   # meurt de faim
```

Ce bloc doit être placé **après** la mise à jour de l'âge, mais **avant** le `return` final.

---

### Correction — Question 4

```python
def reproduction(self):
    """
    Une femelle d'au moins 20 jours avec un niveau de nutrition >= 2
    engendre exactement deux descendants : un mâle et une femelle.
    La maturité sexuelle (age >= 20) est désormais requise.
    """
    descendants = []
    if self.sexe == "femelle" and self.niv_nutrition >= 2 and self.age >= 20:
        descendants.append(Coccinelle("male", 0, 0))
        descendants.append(Coccinelle("femelle", 0, 0))
        self.niv_nutrition = 0
    return descendants


def a_survecu(self):
    """
    Met à jour l'âge de la coccinelle et indique si elle est encore en vie.
    Si niv_nutrition == 0, la coccinelle a 1 chance sur 3 de mourir de faim.
    """
    self.age = self.age + 1
    # Risque de mort par sous-nutrition (probabilité 1/3)
    if self.niv_nutrition == 0 and random.random() < 1/3:
        return False
    return self.age < self.esperance_de_vie


def test_ameliorations():
    # Test 1 : femelle trop jeune → pas de reproduction
    c_jeune = Coccinelle("femelle", 5, 3)
    assert c_jeune.reproduction() == []

    # Test 2 : femelle mature et bien nourrie → 2 descendants
    c_mature = Coccinelle("femelle", 20, 2)
    assert len(c_mature.reproduction()) == 2

    # Test 3 : après reproduction, niv_nutrition est remis à 0
    c_mature2 = Coccinelle("femelle", 25, 3)
    c_mature2.reproduction()
    assert c_mature2.niv_nutrition == 0

    print("Les tests sont validés.")
```

> **Effet attendu sur la simulation :** avec la maturité sexuelle, les nouveau-nés ne se reproduisent pas avant 20 jours — la croissance de la population est donc plus lente. Avec le risque de mort par faim, les périodes de pénurie de pucerons causent davantage de mortalité. Le modèle devient plus réaliste biologiquement.

---

## Pièges fréquents & points de vigilance

### ⚠️ Piège 1 — Oublier `self` dans les méthodes

Chaque méthode d'une classe doit avoir `self` comme premier paramètre. Si tu écris `def reproduction()` au lieu de `def reproduction(self)`, Python lèvera une `TypeError` dès que tu appelleras `c.reproduction()`. Le `self` représente l'objet lui-même — c'est lui qui permet d'accéder à `self.age`, etc.

### ⚠️ Piège 2 — Modifier la liste pendant qu'on la parcourt

Dans la fonction `evolution`, on construit une `population_suivante` distincte au lieu de modifier `population` directement. C'est indispensable : supprimer des éléments d'une liste pendant un `for … in liste` saute des éléments et produit des résultats incorrects.

### ⚠️ Piège 3 — Confondre `len(population)` et `nb_coccinelles`

Dans `evolution`, `nb_coccinelles` est capturé *avant* la boucle de chasse — c'est le nombre de coccinelles au *début* de la journée. Si tu utilisais `len(population_suivante)` à la place, tu diviserais par un nombre qui change en cours de boucle, faussant le calcul de `proies_par_cocci`.

### ⚠️ Piège 4 — Oublier la condition d'arrêt dans `simulation_simple`

La boucle `while` doit tester simultanément trois conditions : `jour < 30`, `len(population) > 0` et `nb_proies > 0`. Oublier l'une d'elles peut mener à une division par zéro dans `chasser` (si `nb_coccinelles` vaut 0 mais que la boucle continue) ou à une boucle infinie si le critère de temps n'est pas vérifié.

### ⚠️ Piège 5 — Les résultats aléatoires ne sont pas reproductibles

Les fonctions `random.randint` et `random.random` produisent des résultats différents à chaque exécution. Les tests portant sur les *valeurs numériques* exactes (nombre de pucerons, de coccinelles) ne peuvent donc pas utiliser des valeurs littérales. Teste plutôt des *propriétés* : la valeur est positive, le tuple a 3 éléments, le nombre de jours est ≤ 30, etc.

---

### Astuces de vérification

- **Tester `reproduction` directement :** crée une femelle avec `niv_nutrition = 2` et `age = 20`, appelle `reproduction()` — tu dois obtenir une liste de 2 éléments.
- **Tester le garde-fou de `chasser` :** appelle `c.chasser(100, 0)` — la méthode doit renvoyer `100` sans erreur.
- **Valider le retour de `simulation_simple` :** vérifie toujours que c'est bien un tuple et que `nb_jours <= 30`.
- **Fixer la graine aléatoire pour des tests reproductibles :** `random.seed(42)` avant ton test garantit que `random.randint` produira toujours la même séquence — utile pour comparer deux versions du code.

---

## Ce que tu dois retenir

- Une **classe** définit un modèle d'objet avec des attributs (`self.age`) et des méthodes (`self.chasser()`).
- Le constructeur `__init__` initialise les attributs à la création de l'objet.
- On ne modifie pas une liste pendant qu'on la parcourt — on en construit une nouvelle.
- Un `while` avec plusieurs conditions garde est la bonne structure pour une simulation bornée.
- `random.random() < p` simule un événement aléatoire de probabilité `p`.
- Les tests sur code aléatoire portent sur des *propriétés structurelles*, pas sur des valeurs exactes.

---

*Lycée Antoine Watteau — DarkSATHI Li · NSI Terminale · Session Pratique 2026 · Sujet n°7*
