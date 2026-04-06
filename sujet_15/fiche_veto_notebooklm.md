# Fiche NSI Terminale — Cabinet vétérinaire : chaînes, SQL, dictionnaires
## BAC 2026 — Sujet n°15 — Partie pratique

**Matière :** Numérique et Sciences Informatiques (NSI)  
**Niveau :** Terminale — voie générale  
**Thème du programme :** Traitement de chaînes, bases de données relationnelles (SQLite), dictionnaires, débogage  
**Durée de l'épreuve :** 1 heure  
**Fichiers fournis :** `veto.py`, `cabinet.sqlite`

---

## Contexte général du sujet

Un cabinet vétérinaire souhaite envoyer des SMS de rappel de vaccination aux propriétaires de chats, deux mois avant l'échéance annuelle. La plateforme d'envoi requiert des numéros au format mobile français normalisé (`06XXXXXXXX` ou `07XXXXXXXX`). Les numéros sont stockés en base de données dans des formats hétérogènes.

Le sujet comporte quatre questions :

1. Normaliser un numéro de téléphone (supprimer tous les non-chiffres)
2. Écrire un jeu de tests pour `validation_tel`
3. Écrire une requête SQL à deux jointures pour extraire les vaccinations de chats
4. Identifier et corriger un bug dans `derniere_vaccination` (opérateur `<` inversé)

---

## Partie 1 — Structure de la base de données

### Schéma des trois tables

**Table `proprietaire`** (400 lignes) :

| Colonne | Type | Rôle |
|---------|------|------|
| `id` | INTEGER (PK) | Identifiant unique |
| `nom` | TEXT | Nom de famille |
| `prenom` | TEXT | Prénom |
| `telephone` | TEXT | Numéro en format libre |

**Table `animal`** (411 lignes — 100 chats, 104 chiens, 96 lapins, 111 oiseaux) :

| Colonne | Type | Rôle |
|---------|------|------|
| `id` | INTEGER (PK) | Identifiant unique |
| `espece` | TEXT | `'chat'`, `'chien'`, `'lapin'`, `'oiseau'` |
| `nom` | TEXT | Nom de l'animal |
| `date_naissance` | TEXT | Format AAAAMMJJ |
| `id_proprietaire` | INTEGER (FK) | Clé étrangère → `proprietaire.id` |

**Table `consultation`** (4 457 lignes — 3 063 vaccinations) :

| Colonne | Type | Rôle |
|---------|------|------|
| `id` | INTEGER (PK) | Identifiant unique |
| `id_animal` | INTEGER (FK) | Clé étrangère → `animal.id` |
| `date` | TEXT | Format AAAAMMJJ |
| `motif` | TEXT | `'vaccination'`, `'bilan'`, `'chirurgie'`, `'maladie'` |

### Relations entre les tables

```
proprietaire (id) ←── animal (id_proprietaire)
animal (id)       ←── consultation (id_animal)
```

Pour obtenir le téléphone du propriétaire lors d'une consultation : **deux jointures** sont nécessaires.
`consultation → animal → proprietaire`

### Extraits réels de la base

```
proprietaire :
(1, 'Duhamel', 'François', '06-57-84-52-41')
(2, 'Dumont',  'Marcelle', '0648747223')
(3, 'Joubert', 'Anouk',    '0 4 76 33 78 15')

animal :
(1, 'oiseau', 'Flocon',    '20171111', 1)
(2, 'lapin',  'Roudoudou', '20210901', 2)
(3, 'chat',   'Mistral',   '20251206', 2)

consultation :
(1,  1, '20171229', 'vaccination')
(25, 4, '20050621', 'bilan')
(34, 5, '20131106', 'maladie')
```

---

## Partie 2 — Rappels techniques

### isdigit() et parcours de chaîne

```python
# isdigit() : True seulement pour les chiffres 0-9
'2'.isdigit()   # True
'C'.isdigit()   # False
'.'.isdigit()   # False
' '.isdigit()   # False
'('.isdigit()   # False
'-'.isdigit()   # False

# Parcourir une chaîne caractère par caractère
for c in "(0)6.12.99-90-12 gilbert":
    if c.isdigit():
        ...   # traiter le chiffre
```

### Connexion SQLite avec paramètre

```python
import sqlite3

conn = sqlite3.connect("cabinet.sqlite")
cursor = conn.cursor()

# Requête avec paramètre — le ? est remplacé par la valeur du tuple
resultats = cursor.execute(
    "SELECT nom FROM animal WHERE espece = 'chat' AND id_proprietaire = ?",
    (2,)    # tuple à un élément : virgule obligatoire !
)
rows = list(resultats)   # convertir en liste réutilisable
```

### Comparaison de dates AAAAMMJJ

Les dates au format `AAAAMMJJ` peuvent être comparées directement comme des chaînes :
```python
"20251125" > "20241024"   # True — ordre alphabétique = ordre chronologique
"20240101" < "20240102"   # True
# En SQL :
WHERE consultation.date > '20240923'
```

---

## Question 1 — normalisation_tel

### Énoncé

Écrire `normalisation_tel(tel)` qui prend un numéro de téléphone en format libre et renvoie uniquement ses chiffres, dans l'ordre.

```python
normalisation_tel("(0)2 12 99 90 12")   # → "0212999012"
normalisation_tel("0.6.12.99.90.12")    # → "0612999012"
normalisation_tel("06-12-99-90-12")     # → "0612999012"
normalisation_tel("(0)6.12.99-90-12 gilbert")  # → "0612999012"
normalisation_tel("061299901")          # → "061299901"  (9 chiffres, non tronqué)
normalisation_tel("06129990123")        # → "06129990123" (11 chiffres, non tronqué)
```

### Démarche

1. Initialiser `resultat = ""`
2. Parcourir chaque caractère `c` de `tel`
3. Si `c.isdigit()` : ajouter à `resultat`
4. Renvoyer `resultat`

### Trace sur "(0)6.12.99-90-12 gilbert"

| Caractère | `(` | `0` | `)` | `6` | `.` | `1` | `2` | … | résultat final |
|-----------|-----|-----|-----|-----|-----|-----|-----|---|----------------|
| isdigit ? | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✓ | … | `"0612999012"` |

### Solution

```python
def normalisation_tel(tel):
    """Renvoie uniquement les chiffres du numéro, dans l'ordre."""
    resultat = ""
    for c in tel:
        if c.isdigit():
            resultat += c
    return resultat

# Version équivalente, plus compacte :
def normalisation_tel(tel):
    return "".join(c for c in tel if c.isdigit())
```

### Fonction de test

```python
def test_normalisation_tel():
    assert normalisation_tel("06 12 99 90 12")        == "0612999012"
    assert normalisation_tel("02 12 99 90 12")        == "0212999012"
    assert normalisation_tel("02.12.99.90.12")        == "0212999012"
    assert normalisation_tel("0.6.12.99.90.12")       == "0612999012"
    assert normalisation_tel("06-12-99-90-12")        == "0612999012"
    assert normalisation_tel("(0)6.12.99-90-12 gilbert") == "0612999012"
    assert normalisation_tel("061299901")             == "061299901"
    assert normalisation_tel("06129990123")           == "06129990123"
    print("Les tests de la fonction normalisation_tel sont passés")

test_normalisation_tel()
```

**Points importants :**
- La fonction ne valide pas, elle ne fait que filtrer. Un numéro de 9 ou 11 chiffres est renvoyé tel quel.
- Chaîne sans chiffres → renvoie `""` (vide).
- Les lettres (`gilbert`) sont silencieusement ignorées.

---

## Question 2 — Jeu de tests de validation_tel

### Code fourni (à tester)

```python
def validation_tel(tel):
    if len(tel) != 10:              # condition 1 : longueur exacte
        return False
    if tel[0] != "0":               # condition 2 : commence par 0
        return False
    if tel[1] != "6" and tel[1] != "7":  # condition 3 : 2e chiffre = 6 ou 7
        return False
    return True
```

### Stratégie de test : couvrir chaque branche

Un bon jeu de tests doit déclencher **chaque condition de rejet** au moins une fois, en plus des cas valides.

| Cas | Entrée | Attendu | Condition déclenchée |
|-----|--------|---------|----------------------|
| 06 valide | `"0612345678"` | `True` | Aucune |
| 07 valide | `"0712345678"` | `True` | Aucune |
| Trop court (9) | `"061299901"` | `False` | len != 10 |
| Trop long (11) | `"06129990123"` | `False` | len != 10 |
| Vide | `""` | `False` | len != 10 |
| Ne commence pas par 0 | `"1612345678"` | `False` | tel[0] != '0' |
| Fixe 01 | `"0112345678"` | `False` | tel[1] ni '6' ni '7' |
| Fixe 02 | `"0212345678"` | `False` | tel[1] ni '6' ni '7' |
| Fixe 03 | `"0312345678"` | `False` | tel[1] ni '6' ni '7' |
| Fixe 04 | `"0412345678"` | `False` | tel[1] ni '6' ni '7' |
| Fixe 05 | `"0512345678"` | `False` | tel[1] ni '6' ni '7' |
| Fixe 08 | `"0812345678"` | `False` | tel[1] ni '6' ni '7' |
| Fixe 09 | `"0912345678"` | `False` | tel[1] ni '6' ni '7' |

### Solution

```python
def test_validation_tel():
    # Cas valides
    assert validation_tel("0612345678") == True
    assert validation_tel("0712345678") == True
    assert validation_tel("0699999999") == True

    # Longueur incorrecte
    assert validation_tel("061299901")   == False   # 9 chiffres
    assert validation_tel("06129990123") == False   # 11 chiffres
    assert validation_tel("")            == False   # vide

    # Ne commence pas par 0
    assert validation_tel("1612345678") == False

    # 2e chiffre invalide (numéros fixes)
    assert validation_tel("0112345678") == False   # 01
    assert validation_tel("0212345678") == False   # 02
    assert validation_tel("0312345678") == False   # 03
    assert validation_tel("0412345678") == False   # 04
    assert validation_tel("0512345678") == False   # 05
    assert validation_tel("0812345678") == False   # 08
    assert validation_tel("0912345678") == False   # 09

    print("Tests de validation_tel passés")

test_validation_tel()
```

**Pourquoi tester la chaîne vide ?**  
Sans le test de longueur en premier, accéder à `tel[0]` sur une chaîne vide lèverait une `IndexError`. Python évalue les `if` en séquence — si `len != 10` est vrai, on renvoie `False` avant d'accéder aux indices. Ce test vérifie cette protection.

---

## Question 3 — consultation_vaccination_chat

### Énoncé

Écrire `consultation_vaccination_chat(date)` qui renvoie une liste de tuples
`(id_animal, nom_animal, telephone_proprietaire, date_consultation)`
pour toutes les consultations de vaccination de chats dont la date est supérieure à `date`.
Triée par `id_animal` puis `date` croissants.

### Construction de la requête SQL étape par étape

**Étape 1 — SELECT : quels champs ?**
```sql
SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date
```

**Étape 2 — FROM : table de départ**
```sql
FROM consultation
```
(Elle contient le `motif` et la `date` de consultation — les deux filtres principaux.)

**Étape 3 — JOIN pour remonter vers animal et proprietaire**
```sql
JOIN animal ON consultation.id_animal = animal.id
JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
```

**Étape 4 — WHERE : trois conditions**
```sql
WHERE animal.espece = 'chat'
  AND consultation.motif = 'vaccination'
  AND consultation.date > ?
```

**Étape 5 — ORDER BY**
```sql
ORDER BY animal.id, consultation.date
```

### Requête complète

```sql
SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date
FROM consultation
    JOIN animal ON consultation.id_animal = animal.id
    JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
WHERE animal.espece = 'chat'
  AND consultation.motif = 'vaccination'
  AND consultation.date > ?
ORDER BY animal.id, consultation.date;
```

### Solution Python complète

```python
def consultation_vaccination_chat(date):
    """
    Renvoie les consultations de vaccination de chats dont la date > date.
    Résultat : liste de tuples (id_animal, nom_animal, telephone, date).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    resultat = cursor.execute(
        """
    SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date
    FROM consultation
        JOIN animal ON consultation.id_animal = animal.id
        JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
    WHERE animal.espece = 'chat'
      AND consultation.motif = 'vaccination'
      AND consultation.date > ?
    ORDER BY animal.id, consultation.date;
    """,
        (date,),
    )
    return list(resultat)
```

### Résultats attendus (premiers éléments pour date = "20240923")

```python
vaccinations = consultation_vaccination_chat("20240923")
len(vaccinations)   # → 118

vaccinations[0]  # → (16, 'Plume',  '0.6.36.96.89.83',  '20241024')
vaccinations[1]  # → (16, 'Plume',  '0.6.36.96.89.83',  '20251125')
vaccinations[2]  # → (17, 'Gollum', '0.6.36.96.89.83',  '20250113')
vaccinations[3]  # → (26, 'Olympe', '(0)4 73 98 01 23',  '20250109')
vaccinations[4]  # → (32, 'Chopin', '06.37.97.66.64',    '20241201')
```

**Notes importantes :**
- Les téléphones sont renvoyés en format brut (avec points, tirets, parenthèses).
- `(date,)` : virgule obligatoire pour un tuple à un seul élément.
- `list(resultat)` : obligatoire pour convertir le curseur en liste réutilisable.

---

## Question 4 — Corriger derniere_vaccination

### Code fourni (bugué)

```python
def derniere_vaccination(consultations):
    derniere = {}
    for consult in consultations:
        id_animal = consult[0]
        date = consult[3]
        if id_animal not in derniere:
            derniere[id_animal] = consult
        elif date < derniere[id_animal][3]:   # ← BUG : < au lieu de >
            derniere[id_animal] = consult
    return derniere
```

### Identification du bug

**Le bug :** la condition `date < derniere[id_animal][3]` met à jour le dictionnaire quand la date courante est **antérieure** à celle déjà stockée. On garde donc la date la plus **ancienne** au lieu de la plus **récente**.

**La correction :** remplacer `<` par `>`.

### Trace détaillée sur Plume (id=16)

```
Consultations triées :
  (16, 'Plume', ..., '20241024')   ← 1ère
  (16, 'Plume', ..., '20251125')   ← 2ème
```

| Étape | date courante | derniere[16] | Condition `<` | Action (bugué) | Condition `>` | Action (corrigé) |
|-------|---------------|-------------|----------------|----------------|---------------|-----------------|
| 1ère | `20241024` | absent | — | stocker `20241024` | — | stocker `20241024` |
| 2ème | `20251125` | `20241024` | `20251125 < 20241024` → **False** | ❌ Ne met pas à jour | `20251125 > 20241024` → **True** | ✅ Stocker `20251125` |

**Résultat bugué :** `derniere[16]` = `(16, 'Plume', ..., '20241024')` ← FAUX  
**Résultat corrigé :** `derniere[16]` = `(16, 'Plume', ..., '20251125')` ← JUSTE

### Solution corrigée

```python
def derniere_vaccination(consultations):
    """
    Renvoie {id_animal: consultation_la_plus_récente}.
    Correction : > (et non <) pour garder le maximum de date.
    """
    derniere = {}
    for consult in consultations:
        id_animal = consult[0]
        date = consult[3]
        if id_animal not in derniere:
            derniere[id_animal] = consult
        elif date > derniere[id_animal][3]:   # > et non <
            derniere[id_animal] = consult
    return derniere
```

### Règle générale pour minimum / maximum par dictionnaire

```python
# Garder le MAXIMUM (valeur la plus grande / date la plus récente)
elif nouvelle_valeur > dictionnaire[cle]:
    dictionnaire[cle] = nouvelle_valeur

# Garder le MINIMUM (valeur la plus petite / date la plus ancienne)
elif nouvelle_valeur < dictionnaire[cle]:
    dictionnaire[cle] = nouvelle_valeur
```

### Fonction de test complète

```python
def test_derniere_vaccination():
    consultations_pour_test = [
        (16, "Plume",  "0.6.36.96.89.83", "20241024"),
        (16, "Plume",  "0.6.36.96.89.83", "20251125"),
        (17, "Gollum", "0.6.36.96.89.83", "20250113"),
        (26, "Olympe", "(0)4 73 98 01 23", "20250109"),
        (32, "Chopin", "06.37.97.66.64",  "20241201"),
        (32, "Chopin", "06.37.97.66.64",  "20251119"),
        (34, "Jazz",   "0.6.37.51.65.52", "20250801"),
        (35, "Tango",  "0324182",          "20250706"),
        (38, "Loulou", "05-35-95-87-54",  "20250209"),
        (39, "Tango",  "07.45.48.02.42",  "20250329"),
        (40, "Sésame", "07.45.48.02.42",  "20250228"),
        (41, "Pixel",  "0130709285",       "20241204"),
        (41, "Pixel",  "0130709285",       "20251222"),
    ]
    resultat = derniere_vaccination(consultations_pour_test)
    assert resultat == {
        16: (16, "Plume",  "0.6.36.96.89.83", "20251125"),
        17: (17, "Gollum", "0.6.36.96.89.83", "20250113"),
        26: (26, "Olympe", "(0)4 73 98 01 23", "20250109"),
        32: (32, "Chopin", "06.37.97.66.64",  "20251119"),
        34: (34, "Jazz",   "0.6.37.51.65.52", "20250801"),
        35: (35, "Tango",  "0324182",          "20250706"),
        38: (38, "Loulou", "05-35-95-87-54",  "20250209"),
        39: (39, "Tango",  "07.45.48.02.42",  "20250329"),
        40: (40, "Sésame", "07.45.48.02.42",  "20250228"),
        41: (41, "Pixel",  "0130709285",       "20251222"),
    }
    print("Les tests de derniere_vaccination sont passés")

test_derniere_vaccination()
```

---

## Code complet corrigé — veto.py

```python
import sqlite3

DB_PATH = "cabinet.sqlite"


def normalisation_tel(tel):              # Q1
    resultat = ""
    for c in tel:
        if c.isdigit():
            resultat += c
    return resultat


def validation_tel(tel):                 # fournie — inchangée
    if len(tel) != 10:
        return False
    if tel[0] != "0":
        return False
    if tel[1] != "6" and tel[1] != "7":
        return False
    return True


def consultation_vaccination_chat(date): # Q3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    resultat = cursor.execute(
        """
    SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date
    FROM consultation
        JOIN animal ON consultation.id_animal = animal.id
        JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
    WHERE animal.espece = 'chat'
      AND consultation.motif = 'vaccination'
      AND consultation.date > ?
    ORDER BY animal.id, consultation.date;
    """,
        (date,),
    )
    return list(resultat)


def derniere_vaccination(consultations): # Q4 — corrigée
    derniere = {}
    for consult in consultations:
        id_animal = consult[0]
        date = consult[3]
        if id_animal not in derniere:
            derniere[id_animal] = consult
        elif date > derniere[id_animal][3]:   # > et non <
            derniere[id_animal] = consult
    return derniere


# Pipeline complet (exemple d'utilisation)
vaccinations = consultation_vaccination_chat("20240923")
dernieres = derniere_vaccination(vaccinations)

for id_animal, consult in dernieres.items():
    tel_brut  = consult[2]
    tel_clean = normalisation_tel(tel_brut)
    if validation_tel(tel_clean):
        print(f"SMS à envoyer : {consult[1]} ({tel_clean}), dernière vaccin le {consult[3]}")
```

---

## Pièges fréquents

### Piège 1 — Tuple à un seul paramètre SQL

```python
# FAUX — (date) n'est pas un tuple, juste des parenthèses
cursor.execute("... WHERE date > ?", (date))

# JUSTE — virgule finale obligatoire
cursor.execute("... WHERE date > ?", (date,))
```

`ProgrammingError: Binding 1 has no name` est l'erreur typique quand on oublie la virgule.

### Piège 2 — Curseur non converti en liste

```python
# FAUX — le curseur est consommé après le premier parcours
return cursor.execute("SELECT ...")

# JUSTE — liste réutilisable
return list(cursor.execute("SELECT ..."))
```

### Piège 3 — Opérateur inversé dans derniere_vaccination

```python
# Pour garder le MAXIMUM : condition >
elif date > derniere[id_animal][3]:

# Pour garder le MINIMUM : condition <
elif date < derniere[id_animal][3]:
```

Le bug `<` au lieu de `>` est silencieux : aucune erreur Python, résultats faux mais plausibles.

### Piège 4 — Ambiguïté de colonnes dans les JOIN

Sans préfixe de table, `id` ou `date` peuvent être ambigus quand plusieurs tables sont jointes :

```sql
-- FAUX : quel "id" ? lequel des trois ?
SELECT id, nom, telephone, date FROM consultation JOIN animal JOIN proprietaire ...

-- JUSTE : préfixer toutes les colonnes
SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date ...
```

### Piège 5 — Ne tester que les True dans validation_tel

Un jeu de tests qui ne contient que `assert validation_tel("0612345678") == True` ne prouve rien. La fonction pourrait renvoyer `True` pour tout et les tests passeraient. Il faut impérativement au moins un test pour chaque condition `return False`.

---

## Astuces de vérification

### Pipeline de validation complet

```python
def est_mobile_valide(tel_brut):
    """Normaliser puis valider — teste l'intégration Q1+Q2."""
    return validation_tel(normalisation_tel(tel_brut))

# Tests d'intégration
assert est_mobile_valide("06.37.97.66.64")    == True    # normalise → "0637976664" → True
assert est_mobile_valide("0.6.36.96.89.83")   == True    # normalise → "0636968983" → True
assert est_mobile_valide("(0)4 73 98 01 23")  == False   # normalise → "0473980123" → False (04)
assert est_mobile_valide("0324182")           == False   # normalise → "0324182" (7 ch.) → False
assert est_mobile_valide("05-35-95-87-54")    == False   # normalise → "0535958754" → False (05)
```

### Vérifier le nombre de résultats SQL

```python
vaccinations = consultation_vaccination_chat("20240923")
assert len(vaccinations) == 118   # test de sanité minimal
assert vaccinations[0][0] == 16   # id du premier animal
assert vaccinations[0][3] == "20241024"   # date de la première consultation
```

### Test de robustesse de normalisation_tel

```python
assert normalisation_tel("abc---///")  == ""          # aucun chiffre
assert normalisation_tel("1234")       == "1234"      # que des chiffres
assert normalisation_tel("")           == ""           # chaîne vide
```

---

## Mini-exercices

### Exercice A — Normalisation et validation à la main

Pour chaque numéro brut, donner le résultat après normalisation et si `validation_tel` renvoie `True` ou `False` :

| Numéro brut | Normalisé | Valide ? | Raison si False |
|-------------|-----------|----------|----------------|
| `"(0)4 76 33 78 15"` | `"0476337815"` | False | 2e chiffre = 4 |
| `"06-57-84-52-41"` | `"0657845241"` | True | — |
| `"0324182"` | `"0324182"` | False | 7 chiffres |
| `"05-35-95-87-54"` | `"0535958754"` | False | 2e chiffre = 5 |
| `"(0)6.12.99-90-12 gilbert"` | `"0612999012"` | True | — |

### Exercice B — Dernière vaccination à la main

Donner le résultat de `derniere_vaccination` (version corrigée) sur :

```python
[(10, "Mimi", "0600000000", "20230601"),
 (10, "Mimi", "0600000000", "20240701"),   ← la plus récente
 (10, "Mimi", "0600000000", "20220501"),
 (20, "Rex",  "0700000001", "20241201")]
```

Trace : Mimi → `20230601` stocké, puis `20240701 > 20230601` → mis à jour, puis `20220501 > 20240701` → False, non mis à jour.

**Résultat :**
```python
{
    10: (10, "Mimi", "0600000000", "20240701"),
    20: (20, "Rex",  "0700000001", "20241201")
}
```

### Exercice C — Construire la requête SQL

Écrire la requête SQL qui renvoie le nom et le téléphone du propriétaire de l'animal d'id 3 :

```sql
SELECT proprietaire.nom, proprietaire.telephone
FROM animal
JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
WHERE animal.id = 3;
-- Résultat : ('Dumont', '0648747223')
```

---

## Récapitulatif — Points clés à retenir

| Notion | Retenir |
|--------|---------|
| `isdigit()` | True pour 0-9 uniquement — ponctuation, espaces, lettres → False |
| `normalisation_tel` | Boucle `for c in tel` + `if c.isdigit()` + concaténation |
| Jeu de tests | Couvrir chaque branche `return False` séparément |
| Dates AAAAMMJJ | Comparaison directe comme chaînes — ordre alphabétique = chronologique |
| JOIN double | `consultation → animal → proprietaire` pour atteindre le téléphone |
| Tuple SQL | `(date,)` avec virgule obligatoire même pour un seul paramètre |
| Résultat SQL | Toujours envelopper dans `list(...)` avant de retourner |
| Bug Q4 | `<` au lieu de `>` — pour garder le maximum, la condition est `>` |

---

*Lycée Antoine Watteau — DarkSATHI Li — BAC NSI 2026 — Sujet n°15*
