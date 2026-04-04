# NSI Terminale – Sujet pratique n°12 – BAC 2026
## Gestion d'un refuge pour renards — Programmation Orientée Objet & fichiers CSV

---

## MÉTADONNÉES DU DOCUMENT

- **Matière** : Numérique et Sciences Informatiques (NSI)
- **Niveau** : Terminale générale
- **Type d'épreuve** : Partie pratique du baccalauréat — durée 1 heure
- **Session** : 2026 — Sujet n°12
- **Thème du programme** : Programmation orientée objet (POO), traitement de données CSV
- **Langage** : Python 3
- **Fichiers fournis à l'examen** : `gestion_refuge.py`, `donnees_renards.csv`
- **Modules Python requis** : `csv`

---

## PARTIE 1 — CONTEXTE ET PROBLÉMATIQUE

### Contexte

Le renard, longtemps considéré comme nuisible, est aujourd'hui de plus en plus protégé pour son rôle dans la régulation de la biodiversité. Un refuge de protection a été construit pour réhabiliter les individus blessés ou orphelins. La personne en charge souhaite réaliser une base de données en CSV et Python pour stocker les informations essentielles sur les renards pris en charge.

### Les deux entités du sujet

**Entité 1 — Renard** : défini par un identifiant (entier), un nom (chaîne), un poids en kg (flottant), une date d'arrivée (chaîne au format AAAA-MM-JJ).

**Entité 2 — Refuge** : défini par son nom (chaîne), son adresse postale (chaîne), et une liste d'objets `Renard`.

---

## PARTIE 2 — DONNÉES DU FICHIER `donnees_renards.csv`

### Structure du fichier

Le fichier utilise le point-virgule (`;`) comme séparateur. La première ligne est l'en-tête.

### Contenu intégral du fichier (30 renards)

```
id;nom;poids;date_arrivee
101;Zorro;6.5;2023-01-15
102;Roxy;5.8;2023-02-10
103;Filou;7.2;2023-03-05
104;Kira;4.9;2024-11-20
105;Rouky;6.1;2023-05-12
106;Vixen;5.5;2023-06-01
107;Goupil;7.8;2023-07-18
108;Pipo;5.3;2023-08-22
109;Vulpec;6.9;2023-09-09
110;Foxy;4.5;2023-10-25
111;Renardeau;3.2;2024-04-01
112;Rubis;7.0;2024-03-10
113;Sacha;6.3;2024-02-05
114;Pacha;5.7;2024-01-28
115;Delta;6.6;2023-11-03
116;Écho;5.1;2023-12-19
117;Tango;7.1;2024-05-15
118;Oscar;5.9;2024-06-11
119;Lima;6.8;2024-07-07
120;Mia;4.7;2024-08-29
121;Léo;6.4;2024-09-17
122;Nina;5.6;2024-10-14
123;Max;7.3;2024-05-25
124;Bella;4.8;2024-04-18
125;Toby;6.2;2024-03-29
126;Sparky;5.0;2024-02-14
127;Shadow;7.4;2024-01-01
128;Pip;4.6;2023-11-29
129;Ziggy;6.7;2023-10-10
130;Loup;5.2;2023-09-01
```

### Statistiques du jeu de données

- **Nombre total de renards** : 30
- **Renards peu corpulents** (poids strictement < 6,0 kg) : **15**
- **Renards de poids normal** (poids ≥ 6,0 kg) : 15
- **Pourcentage peu corpulents** : **50,0 %** exactement (15/30 × 100)

### Liste complète des renards peu corpulents (poids < 6,0 kg)

| id  | nom       | poids | date_arrivee |
|-----|-----------|-------|--------------|
| 102 | Roxy      | 5.8   | 2023-02-10   |
| 104 | Kira      | 4.9   | 2024-11-20   |
| 106 | Vixen     | 5.5   | 2023-06-01   |
| 108 | Pipo      | 5.3   | 2023-08-22   |
| 110 | Foxy      | 4.5   | 2023-10-25   |
| 111 | Renardeau | 3.2   | 2024-04-01   |
| 114 | Pacha     | 5.7   | 2024-01-28   |
| 116 | Écho      | 5.1   | 2023-12-19   |
| 118 | Oscar     | 5.9   | 2024-06-11   |
| 120 | Mia       | 4.7   | 2024-08-29   |
| 122 | Nina      | 5.6   | 2024-10-14   |
| 124 | Bella     | 4.8   | 2024-04-18   |
| 126 | Sparky    | 5.0   | 2024-02-14   |
| 128 | Pip       | 4.6   | 2023-11-29   |
| 130 | Loup      | 5.2   | 2023-09-01   |

**Vérification** : 15 renards × (1/30) × 100 = 50,0 %

---

## PARTIE 3 — FICHIER DE DÉPART `gestion_refuge.py`

Voici le contenu intégral du fichier fourni aux candidats à l'examen :

```python
import csv

class Renard:
    """
    Classe représentant un renard dans le refuge.
    Attributs : identifiant, nom, poids, date_arrivee.
    """
    def __init__(self, identifiant, nom, poids, date_arrivee):
        pass  # Question 1 à compléter

    def __str__(self):
        pass  # Question 2 à compléter

class Refuge:
    """
    Classe représentant le refuge contenant la liste des renards.
    """
    def __init__(self, nom, adresse):
        self.nom = nom
        self.adresse = adresse
        self.liste_renards = []

    def recueillir(self, un_renard):
        """Méthode d'ajout d'un renard au refuge."""
        self.liste_renards.append(un_renard)

    def lister_peu_corpulents(self):
        """Méthode qui renvoie une liste des Renards dont le poids est < 6.0 kg."""
        return [renard for renard in self.liste_renards if renard.poids < 6.0]

    def pourcentage_peu_corpulents(self):
        """Méthode qui renvoie le pourcentage des renards peu corpulents."""
        if len(self.liste_renards) == 0:
            return 0.0
        return len(self.lister_peu_corpulents()) / len(self.liste_renards) * 100

    def importer_donnees(self, nom_fichier):
        """Fonction qui importe les données des renards à partir d'un fichier CSV."""
        print(f"Tentative d'importation depuis {nom_fichier}...")
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            lignes = csv.DictReader(f, delimiter=';')
            for ligne in lignes:
                renard = Renard(ligne['id'], ligne['nom'], ligne['poids'], ligne['date_arrivee'])
                # ↑ LIGNE BUGUÉE : 'id' et 'poids' sont des str, pas int/float
                self.recueillir(renard)
```

---

## PARTIE 4 — QUESTIONS ET CORRECTIONS COMPLÈTES

---

### QUESTION 1 — Écrire le constructeur `__init__` de la classe `Renard`

**Énoncé** : Écrire le code du constructeur `__init__` de la classe `Renard`.

**Rappel de syntaxe** : Le constructeur doit sauvegarder chaque paramètre dans un attribut d'instance avec `self.nom_attribut = parametre`. Sans `self.`, la valeur est perdue à la fin du constructeur.

**Correspondance paramètres → attributs** :

| Paramètre reçu | Attribut créé | Type attendu |
|----------------|---------------|--------------|
| `identifiant`  | `self.identifiant`  | `int`   |
| `nom`          | `self.nom`          | `str`   |
| `poids`        | `self.poids`        | `float` |
| `date_arrivee` | `self.date_arrivee` | `str`   |

**Correction** :

```python
def __init__(self, identifiant, nom, poids, date_arrivee):
    self.identifiant  = identifiant
    self.nom          = nom
    self.poids        = poids
    self.date_arrivee = date_arrivee
```

**Fonction de test** :

```python
def test_init_renard():
    r = Renard(101, "Zorro", 6.5, "2023-01-15")
    assert r.identifiant  == 101
    assert r.nom          == "Zorro"
    assert r.poids        == 6.5
    assert r.date_arrivee == "2023-01-15"
    r2 = Renard(104, "Kira", 4.9, "2024-11-20")
    assert r2.identifiant == 104
    assert r2.poids       == 4.9
    assert r2.nom         == "Kira"
    print("Les tests sont validés.")

test_init_renard()
```

---

### QUESTION 2 — Écrire la méthode `__str__` et tester

**Énoncé** : Écrire le code de la méthode `__str__` qui renvoie une chaîne de caractères au format précis :

```
"Renard ID [id] - [Nom] (Arrivé le [date_arrivee])"
```

Puis instancier un renard `renard1` : identifiant 200, nom Oscar, poids 5.1 kg, arrivé le 2026-01-01. Afficher ses informations.

**Format exact attendu pour `renard1`** :
```
Renard ID 200 - Oscar (Arrivé le 2026-01-01)
```

**Points de vigilance** :
- La méthode doit `return` la chaîne, jamais `print` directement.
- L'accent sur « Arrivé » est obligatoire.
- Les espaces autour du tiret sont obligatoires (` - `).
- Le `poids` n'apparaît pas dans ce format.
- La méthode `__str__` est appelée automatiquement par `print(renard)` et `str(renard)`.

**Correction** :

```python
def __str__(self):
    return f"Renard ID {self.identifiant} - {self.nom} (Arrivé le {self.date_arrivee})"

# Test de l'énoncé :
renard1 = Renard(200, "Oscar", 5.1, "2026-01-01")
print(renard1)
# Affiche : Renard ID 200 - Oscar (Arrivé le 2026-01-01)
```

**Autres exemples de sorties correctes** :

```
Renard ID 101 - Zorro (Arrivé le 2023-01-15)
Renard ID 110 - Foxy (Arrivé le 2023-10-25)
Renard ID 130 - Loup (Arrivé le 2023-09-01)
```

**Fonction de test** :

```python
def test_str_renard():
    r = Renard(200, "Oscar", 5.1, "2026-01-01")
    assert str(r) == "Renard ID 200 - Oscar (Arrivé le 2026-01-01)"
    r2 = Renard(101, "Zorro", 6.5, "2023-01-15")
    assert str(r2) == "Renard ID 101 - Zorro (Arrivé le 2023-01-15)"
    r3 = Renard(110, "Foxy", 4.5, "2023-10-25")
    assert str(r3) == "Renard ID 110 - Foxy (Arrivé le 2023-10-25)"
    print("Les tests sont validés.")

test_str_renard()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question. L'élève montre `print(renard1)` produisant exactement `Renard ID 200 - Oscar (Arrivé le 2026-01-01)`.

---

### QUESTION 3 — Identifier et corriger le bug de `importer_donnees`

**Énoncé** : L'exécution de la méthode `importer_donnees` provoque une erreur logique lors de l'utilisation ultérieure des données, notamment lors de la manipulation du poids et de l'identifiant. Identifier la source de cette erreur, proposer une correction, puis tester en instanciant le refuge « SOS Goupil ».

**Identification du bug** :

La ligne problématique est :
```python
renard = Renard(ligne['id'], ligne['nom'], ligne['poids'], ligne['date_arrivee'])
```

`csv.DictReader` lit toutes les valeurs comme des **chaînes de caractères (`str`)**, même quand elles ressemblent à des nombres. Ainsi :
- `ligne['id']` vaut `'101'` (str), alors que le constructeur attend un `int`
- `ligne['poids']` vaut `'6.5'` (str), alors que le constructeur attend un `float`

**Nature de l'erreur** : C'est une erreur **logique**, pas syntaxique. Python crée l'objet sans signaler de problème. L'erreur n'apparaît que plus tard, lorsque `lister_peu_corpulents` tente `renard.poids < 6.0` — comparer une `str` à un `float` lève une `TypeError`.

**Correction — une seule ligne à modifier** :

```python
# AVANT (buggé) :
renard = Renard(ligne['id'], ligne['nom'], ligne['poids'], ligne['date_arrivee'])

# APRÈS (corrigé) :
renard = Renard(int(ligne['id']), ligne['nom'], float(ligne['poids']), ligne['date_arrivee'])
```

**Méthode corrigée complète** :

```python
def importer_donnees(self, nom_fichier):
    print(f"Tentative d'importation depuis {nom_fichier}...")
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        lignes = csv.DictReader(f, delimiter=';')
        for ligne in lignes:
            renard = Renard(
                int(ligne['id']),          # str → int
                ligne['nom'],              # str → str (ok)
                float(ligne['poids']),     # str → float
                ligne['date_arrivee']      # str → str (ok)
            )
            self.recueillir(renard)
```

**Test de la correction** :

```python
mon_refuge = Refuge("SOS Goupil", "12 rue de la Forêt")
mon_refuge.importer_donnees("donnees_renards.csv")

# Vérifications après import
r0 = mon_refuge.liste_renards[0]
print(type(r0.identifiant))  # → <class 'int'>
print(type(r0.poids))        # → <class 'float'>
print(r0)                    # → Renard ID 101 - Zorro (Arrivé le 2023-01-15)
```

**Fonction de test** :

```python
def test_import():
    assert len(mon_refuge.liste_renards) == 30
    r0 = mon_refuge.liste_renards[0]
    assert r0.identifiant == 101      # doit être un int, pas la str '101'
    assert r0.poids       == 6.5      # doit être un float, pas la str '6.5'
    assert r0.nom         == "Zorro"
    r1 = mon_refuge.liste_renards[1]
    assert r1.poids < 6.0             # Roxy : 5.8 < 6.0 doit être True (impossible avec str)
    print("Les tests sont validés.")

test_import()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question. L'élève montre que l'import fonctionne et que les types sont corrects.

---

### QUESTION 4 — Analyser la corpulence et justifier le pourcentage

**Énoncé** : Exécuter les deux méthodes d'analyse de la corpulence sur l'instance du refuge. Justifier le pourcentage obtenu en isolant et en affichant le nombre de renards peu corpulents par rapport au nombre total.

**Définition** : un renard est peu corpulent si son poids est **strictement inférieur à 6,0 kg** (condition `poids < 6.0`, pas `<= 6.0`).

**Code à écrire** :

```python
# Lister les peu corpulents
peu_corp = mon_refuge.lister_peu_corpulents()
print(f"Renards peu corpulents ({len(peu_corp)}/{len(mon_refuge.liste_renards)}) :")
for r in peu_corp:
    print(r)

# Afficher le pourcentage
print(f"\nPourcentage : {mon_refuge.pourcentage_peu_corpulents():.1f}%")
```

**Sortie complète attendue** :

```
Renards peu corpulents (15/30) :
Renard ID 102 - Roxy (Arrivé le 2023-02-10)
Renard ID 104 - Kira (Arrivé le 2024-11-20)
Renard ID 106 - Vixen (Arrivé le 2023-06-01)
Renard ID 108 - Pipo (Arrivé le 2023-08-22)
Renard ID 110 - Foxy (Arrivé le 2023-10-25)
Renard ID 111 - Renardeau (Arrivé le 2024-04-01)
Renard ID 114 - Pacha (Arrivé le 2024-01-28)
Renard ID 116 - Écho (Arrivé le 2023-12-19)
Renard ID 118 - Oscar (Arrivé le 2024-06-11)
Renard ID 120 - Mia (Arrivé le 2024-08-29)
Renard ID 122 - Nina (Arrivé le 2024-10-14)
Renard ID 124 - Bella (Arrivé le 2024-04-18)
Renard ID 126 - Sparky (Arrivé le 2024-02-14)
Renard ID 128 - Pip (Arrivé le 2023-11-29)
Renard ID 130 - Loup (Arrivé le 2023-09-01)

Pourcentage : 50.0%
```

**Justification rédigée pour l'examinateur** : 15 renards sur 30 ont un poids strictement inférieur à 6,0 kg. Le calcul 15 ÷ 30 × 100 = 50,0 % confirme le résultat affiché par `pourcentage_peu_corpulents()`.

**Fonction de test** :

```python
def test_corpulence():
    assert len(mon_refuge.liste_renards) == 30
    assert len(mon_refuge.lister_peu_corpulents()) == 15
    assert mon_refuge.pourcentage_peu_corpulents() == 50.0
    assert mon_refuge.lister_peu_corpulents()[0].nom == "Roxy"
    print("Les tests sont validés.")

test_corpulence()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

## PARTIE 5 — CODE COMPLET ET FONCTIONNEL (SOLUTION DE RÉFÉRENCE)

```python
import csv

class Renard:
    """Classe représentant un renard dans le refuge."""

    def __init__(self, identifiant, nom, poids, date_arrivee):
        self.identifiant  = identifiant    # int
        self.nom          = nom            # str
        self.poids        = poids          # float
        self.date_arrivee = date_arrivee   # str au format AAAA-MM-JJ

    def __str__(self):
        return f"Renard ID {self.identifiant} - {self.nom} (Arrivé le {self.date_arrivee})"


class Refuge:
    """Classe représentant le refuge contenant la liste des renards."""

    def __init__(self, nom, adresse):
        self.nom           = nom
        self.adresse       = adresse
        self.liste_renards = []

    def recueillir(self, un_renard):
        """Ajoute un renard à la liste du refuge."""
        self.liste_renards.append(un_renard)

    def lister_peu_corpulents(self):
        """Renvoie la liste des Renards dont le poids est strictement < 6.0 kg."""
        return [renard for renard in self.liste_renards if renard.poids < 6.0]

    def pourcentage_peu_corpulents(self):
        """Renvoie le pourcentage de renards peu corpulents."""
        if len(self.liste_renards) == 0:
            return 0.0
        return len(self.lister_peu_corpulents()) / len(self.liste_renards) * 100

    def importer_donnees(self, nom_fichier):
        """Importe les données depuis un fichier CSV avec conversion de types."""
        print(f"Tentative d'importation depuis {nom_fichier}...")
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            lignes = csv.DictReader(f, delimiter=';')
            for ligne in lignes:
                renard = Renard(
                    int(ligne['id']),          # ← conversion str → int
                    ligne['nom'],
                    float(ligne['poids']),     # ← conversion str → float
                    ligne['date_arrivee']
                )
                self.recueillir(renard)


# ── Tests de l'énoncé ─────────────────────────────────────────────────

# Question 2 : instancier et afficher renard1
renard1 = Renard(200, "Oscar", 5.1, "2026-01-01")
print(renard1)
# → Renard ID 200 - Oscar (Arrivé le 2026-01-01)

# Questions 3 & 4 : importer et analyser
mon_refuge = Refuge("SOS Goupil", "12 rue de la Forêt")
mon_refuge.importer_donnees("donnees_renards.csv")

peu_corp = mon_refuge.lister_peu_corpulents()
print(f"Renards peu corpulents ({len(peu_corp)}/{len(mon_refuge.liste_renards)}) :")
for r in peu_corp:
    print(r)
print(f"\nPourcentage : {mon_refuge.pourcentage_peu_corpulents():.1f}%")
```

---

## PARTIE 6 — ERREURS FRÉQUENTES ET PIÈGES

### Piège 1 — Oublier `self.` devant un attribut dans `__init__`

Sans `self.`, la valeur est stockée dans une variable locale qui disparaît à la fin du constructeur.

```python
# ERREUR : identifiant est une variable locale, perdue après __init__
def __init__(self, identifiant, ...):
    identifiant = identifiant   # sans self. → perdu !

# CORRECT
def __init__(self, identifiant, ...):
    self.identifiant = identifiant
```

### Piège 2 — `__str__` qui `print` au lieu de `return`

`__str__` doit **retourner** une chaîne, jamais afficher directement. Si tu utilises `print` à l'intérieur, la méthode retourne `None` et `print(renard)` affiche `None`.

```python
# ERREUR
def __str__(self):
    print(f"Renard ID {self.identifiant} ...")   # → None retourné !

# CORRECT
def __str__(self):
    return f"Renard ID {self.identifiant} ..."   # → str retournée
```

### Piège 3 — Ne pas convertir les types lus depuis le CSV (bug principal du sujet)

Toutes les valeurs lues par `csv.DictReader` sont des `str`. Il faut convertir explicitement.

```python
# ERREUR (ligne buguée du sujet)
Renard(ligne['id'], ligne['nom'], ligne['poids'], ligne['date_arrivee'])
#       ↑ str                     ↑ str

# CORRECT
Renard(int(ligne['id']), ligne['nom'], float(ligne['poids']), ligne['date_arrivee'])
```

Sans cette correction, `renard.poids < 6.0` lève une `TypeError: '<' not supported between instances of 'str' and 'float'`.

### Piège 4 — Utiliser `<=` au lieu de `<` pour la corpulence

L'énoncé précise « **strictement** inférieur à 6,0 kg ». Un renard à exactement 6,0 kg n'est pas peu corpulent.

```python
renard.poids < 6.0   # ✓ correct (strictement inférieur)
renard.poids <= 6.0  # ✗ incorrect (inclurait 6.0)
```

### Piège 5 — Confondre définition et appel d'une méthode

Une méthode s'appelle toujours avec des parenthèses. Sans parenthèses, on obtient l'objet-méthode lui-même.

```python
mon_refuge.lister_peu_corpulents    # ✗ retourne l'objet-méthode, pas la liste
mon_refuge.lister_peu_corpulents()  # ✓ retourne la liste
```

### Piège 6 — Oublier l'accent sur « Arrivé » dans `__str__`

Le format demandé par l'énoncé contient l'accent : `(Arrivé le ...)`. Une chaîne sans accent (`Arrive le`) ne correspond pas au format attendu et peut invalider les assertions.

---

## PARTIE 7 — RAPPELS DE COURS POO

### Vocabulaire essentiel

**Classe** : modèle/moule qui définit la structure et le comportement d'un type d'objet.

**Objet (instance)** : exemplaire concret créé à partir d'une classe. `renard1 = Renard(...)` crée une instance.

**Attribut d'instance** : variable propre à chaque objet, préfixée par `self.` dans le code.

**Méthode** : fonction définie dans une classe. Son premier paramètre est toujours `self`.

**Constructeur `__init__`** : méthode spéciale appelée automatiquement à la création d'un objet. Sert à initialiser les attributs.

**`__str__`** : méthode spéciale appelée par `print(objet)` et `str(objet)`. Doit retourner une `str`.

**`self`** : référence à l'objet courant. Premier paramètre de toute méthode d'instance.

**Instanciation** : action de créer un objet à partir d'une classe. Syntaxe : `variable = NomClasse(arguments)`.

### Structure d'une classe complète

```python
class NomClasse:
    def __init__(self, param1, param2):
        self.attribut1 = param1    # toujours self.
        self.attribut2 = param2

    def __str__(self):
        return f"..."              # toujours return, jamais print

    def une_methode(self):
        # accède aux attributs avec self.attribut
        return self.attribut1
```

---

## PARTIE 8 — RAPPELS DE COURS FICHIERS CSV

### Le module `csv` et `DictReader`

```python
import csv

with open('fichier.csv', 'r', encoding='utf-8') as f:
    lignes = csv.DictReader(f, delimiter=';')
    for ligne in lignes:
        # ligne est un dict {nom_colonne: valeur_en_str}
        print(ligne['id'])     # → '101' (str !)
        print(ligne['nom'])    # → 'Zorro' (str)
        print(ligne['poids'])  # → '6.5' (str !)
```

### Conversions de types nécessaires

| Colonne CSV | Valeur brute (str) | Conversion | Résultat |
|-------------|-------------------|------------|---------|
| `id`        | `'101'`           | `int('101')` | `101` |
| `poids`     | `'6.5'`           | `float('6.5')` | `6.5` |
| `nom`       | `'Zorro'`         | aucune | `'Zorro'` |
| `date_arrivee` | `'2023-01-15'` | aucune | `'2023-01-15'` |

---

## PARTIE 9 — CHECKLIST AVANT DE RENDRE LE CODE

- [ ] `__init__` : chaque paramètre est sauvegardé avec `self.nom = valeur`
- [ ] `__init__` : la signature correspond aux 4 paramètres du sujet (identifiant, nom, poids, date_arrivee)
- [ ] `__str__` : utilise `return`, pas `print`
- [ ] `__str__` : le format correspond exactement à `"Renard ID X - Nom (Arrivé le AAAA-MM-JJ)"`
- [ ] `__str__` : l'accent sur « Arrivé » est présent
- [ ] `importer_donnees` : `int(ligne['id'])` et `float(ligne['poids'])` sont présents
- [ ] `renard1` (Q2) : identifiant=200, nom="Oscar", poids=5.1, date="2026-01-01" et affiché
- [ ] Refuge "SOS Goupil" instancié et fichier importé
- [ ] Q4 : le nombre de peu corpulents (15) et le total (30) sont affichés
- [ ] Q4 : le pourcentage affiché est 50.0 %

---

## PARTIE 10 — GLOSSAIRE

**POO (Programmation Orientée Objet)** : paradigme de programmation qui organise le code en objets regroupant données et comportements.

**`__init__`** : méthode constructeur, appelée automatiquement à la création d'un objet avec `NomClasse(...)`.

**`__str__`** : méthode spéciale qui définit la représentation textuelle d'un objet. Appelée par `print()` et `str()`.

**`self`** : référence à l'instance courante dans les méthodes. Obligatoire en premier paramètre.

**Attribut** : variable attachée à un objet, accessible via `self.nom` dans la classe ou `objet.nom` de l'extérieur.

**CSV (Comma-Separated Values)** : format de fichier texte où les données sont séparées par un délimiteur (ici le point-virgule `;`).

**`csv.DictReader`** : classe Python qui lit un fichier CSV et renvoie chaque ligne comme un dictionnaire `{colonne: valeur_str}`.

**Erreur logique** : erreur qui ne provoque pas d'exception immédiate mais produit des résultats incorrects. Opposée à une erreur de syntaxe ou de type.

**`TypeError`** : exception Python levée quand une opération est appliquée à un type incorrect. Exemple : comparer `str` et `float` avec `<`.

**`int()`** : fonction Python qui convertit une valeur en entier. `int('101')` → `101`.

**`float()`** : fonction Python qui convertit une valeur en flottant. `float('6.5')` → `6.5`.

---

*Document produit pour une utilisation pédagogique dans NotebookLM. Lycée Antoine Watteau — DarkSATHI Li*
