# Fiche de révision — BAC NSI 2026 — Sujet n°23 : Module DEMETER

**Niveau :** Terminale NSI  
**Thèmes :** POO · Encodage binaire · BCD · Parité · Robustesse  
**Source :** Épreuve pratique BAC NSI 2026, sujet n°23  
**Lycée Antoine Watteau — DarkSATHI Li**

---

## Note d'analyse critique — Corrections apportées à l'énoncé original

Après analyse rigoureuse du fichier `data.txt` et du code `analyse.py`, deux problèmes supplémentaires ont été identifiés, non mentionnés explicitement dans l'énoncé :

**Erreur 1 dans `analyse.py` (ligne 2) :**  
`from Transmission import Transmission` utilise une majuscule, alors que le fichier s'appelle `transmission.py` (minuscule). Sur Linux et macOS, cette différence de casse entraîne un `ModuleNotFoundError` immédiat. C'est la **première cause du plantage** observé en Q3.

**Erreur 2 dans `data.txt` :**  
Le fichier contient 314 trames, dont 3 de longueur incorrecte :
- Ligne 73 : 41 bits (1 bit de trop)
- Ligne 111 : 38 bits (2 bits manquants)
- Ligne 126 : 41 bits (1 bit de trop)

La trame de 38 bits provoque un `IndexError: string index out of range` dans toute implémentation naïve de `est_valide` qui accède à `trame[38]` ou `trame[39]`. C'est la **deuxième cause de plantage**.

Par ailleurs, 3 trames de 40 bits ont une parité incorrecte. Au total, **308 trames sur 314 sont valides**.

---

## Contexte du sujet

L'entreprise PlovaNuvia développe un module d'acquisition DEMETER pour la prévention de maladies dans les cultures agricoles (vignes). Plusieurs fois par heure, chaque module mesure la température et l'humidité et transmet les données par ondes radio sous forme de trames de 40 bits.

Le but du sujet est de finaliser la programmation du serveur de réception : décoder les trames, vérifier leur intégrité, et produire un graphe des températures valides.

---

## Rappels de cours — Binaire, BCD et parité

### Conversion binaire vers décimal en Python

```python
int(chaine, 2)   # convertit une chaîne binaire vers un entier décimal

int("00101010", 2)     # → 42
int("010010001100", 2) # → 1164
int("1010", 2)         # → 10
int("0110", 2)         # → 6
```

### Slicing de chaînes

Le slicing `trame[a:b]` extrait les caractères d'indice `a` (inclus) jusqu'à `b` (exclu).

```python
trame = "0010101011001000010010001100011000101101"
trame[0:8]   # → "00101010"    (ID, 8 bits)
trame[8:16]  # → "11001000"    (clé, 8 bits)
trame[16:28] # → "010010001100" (température, 12 bits)
trame[28:36] # → "01100010"    (humidité, 8 bits)
trame[36:40] # → "1101"        (contrôle, 4 bits)
```

**Attention :** si la trame fait 38 caractères, `trame[38]` lève une `IndexError`. C'est exactement le bug de ce sujet.

### Le codage BCD (Décimal Codé Binaire)

En BCD, chaque **chiffre décimal** est codé indépendamment sur 4 bits. Pour coder « 62 », on code « 6 » sur 4 bits puis « 2 » sur 4 bits.

| Groupe | Bits | Décimal |
|---|---|---|
| Dizaines | `0110` | 6 |
| Unités | `0010` | 2 |
| **Résultat** | `01100010` | **62 %** |

```python
hum_bits = "01100010"
d1 = int(hum_bits[0:4], 2)   # → 6  (dizaines)
d2 = int(hum_bits[4:8], 2)   # → 2  (unités)
humidite = d1 * 10 + d2       # → 62
```

**Cas particulier :** 100 % est codé `10100000`. Le groupe `1010` vaut 10 en décimal — ce n'est pas un chiffre BCD valide. Ce cas doit être traité séparément :

```python
if hum_bits == "10100000":
    humidite = 100
```

### La parité — détecter les erreurs de transmission

Un **bit de parité** permet au destinataire de détecter si un bit a été modifié pendant la transmission.

**Règle :** le bit de parité d'un bloc vaut **1** si le nombre de bits à 1 est *impair*, **0** si ce nombre est *pair*.

```python
def parite(bloc):
    """Renvoie le bit de parité d'un bloc binaire (sous forme de caractère)."""
    return '1' if bloc.count('1') % 2 == 1 else '0'

parite("00101010")     # 3 uns → impair → '1'
parite("11001000")     # 3 uns → impair → '1'
parite("010010001100") # 4 uns → pair   → '0'
parite("01100010")     # 3 uns → impair → '1'
# Bits de contrôle calculés : '1101' ✓
```

---

## Structure de la trame DEMETER

Une trame fait **exactement 40 bits**, découpés en 5 blocs contigus :

```
[0:8]   ID              (8 bits)  — binaire classique
[8:16]  Clé de sécurité (8 bits)  — non décodée dans ce sujet
[16:28] Température     (12 bits) — binaire avec offset 900
[28:36] Humidité        (8 bits)  — BCD (4 bits dizaines + 4 bits unités)
[36:40] Bits de contrôle(4 bits)  — parité des 4 blocs précédents
```

### Trame d'exemple complète

```
0010101011001000010010001100011000101101
│       │       │           │       │
│       │       │           │       └── Contrôle  : 1101
│       │       │           └────────── Humidité  : 01100010 → 62%
│       │       └────────────────────── Température: 010010001100 → 26,4°C
│       └────────────────────────────── Clé        : 11001000
└────────────────────────────────────── ID         : 00101010 → 42
```

### Décodage de la température

Bits `[16:28]` = `010010001100`

Valeur binaire → décimal : `int("010010001100", 2)` = **1164**

Température en °C : (1164 − 900) / 10 = **26,4 °C**

La valeur 900 est un décalage (*offset*) qui permet de représenter des températures négatives. La valeur minimale codée est (0 − 900)/10 = −90 °C, la maximale est (4095 − 900)/10 = 319,5 °C.

### Vérification des bits de contrôle

| Bloc | Bits | Nombre de 1 | Parité |
|---|---|---|---|
| ID | `00101010` | 3 (impair) | **1** |
| Clé | `11001000` | 3 (impair) | **1** |
| Température | `010010001100` | 4 (pair) | **0** |
| Humidité | `01100010` | 3 (impair) | **1** |
| **Contrôle calculé** | | | **1101** ✓ |

Les bits de contrôle calculés `1101` sont identiques aux bits `trame[36:40]` → trame valide.

---

## La classe `Transmission` — Architecture

```python
class Transmission:
    def __init__(self, trame):
        self._id          = None
        self._temperature = None
        self._humidite    = None
        self._trame       = trame
        self.decoder()        # décode tout à la construction

    def decoder(self):
        self.decoder_id()
        self.decoder_temperature()   # À COMPLÉTER (Q1)
        self.decoder_humidite()      # À COMPLÉTER (Q1)

    def decoder_id(self):
        self._id = int(self._trame[0:8], 2)

    def est_valide(self):
        return False  # À COMPLÉTER (Q2)

    # Getters
    def get_id(self):          return self._id
    def get_temperature(self): return self._temperature
    def get_humidite(self):    return self._humidite
```

---

## Question 1 — Décoder la température et l'humidité

### Énoncé

Écrire les méthodes `decoder_temperature(self)` et `decoder_humidite(self)`. Vérifier avec la trame d'exemple que les résultats sont bien 26,4 °C et 62 %.

### Solution

```python
def decoder_temperature(self):
    """Décode la température en °C (flottant)."""
    valeur = int(self._trame[16:28], 2)
    self._temperature = (valeur - 900) / 10

def decoder_humidite(self):
    """Décode l'humidité en % (entier) en BCD."""
    hum_bits = self._trame[28:36]
    if hum_bits == "10100000":        # cas spécial : 100 %
        self._humidite = 100
    else:
        d1 = int(hum_bits[0:4], 2)   # dizaines
        d2 = int(hum_bits[4:8], 2)   # unités
        self._humidite = d1 * 10 + d2
```

### Fonction de test

```python
TRAME_EXEMPLE = "0010101011001000010010001100011000101101"

def test_decodage():
    t = Transmission(TRAME_EXEMPLE)
    assert t.get_temperature() == 26.4
    assert t.get_humidite()    == 62
    assert t.get_id()          == 42
    # Cas spécial 100 %
    trame_100 = "00101010" + "11001000" + "010010001100" + "10100000" + "1001"
    t2 = Transmission(trame_100)
    assert t2.get_humidite() == 100
    print("Les tests sont validés.")

test_decodage()
```

### Points clés

- La division par 10 produit automatiquement un `float` en Python 3.
- Le cas `10100000` pour 100 % doit être testé **avant** le décodage BCD.
- La valeur 900 est un offset permettant de représenter des températures négatives jusqu'à −90 °C.

---

## Question 2 — Valider une trame par contrôle de parité

### Énoncé

Écrire la méthode `est_valide(self)` qui renvoie `True` si les 4 bits de contrôle `trame[36:40]` correspondent aux bits de parité des 4 blocs de données, `False` sinon.

### Correspondance blocs / bits de contrôle

| Bloc | Indices données | Indice bit de contrôle |
|---|---|---|
| ID | `[0:8]` | `trame[36]` |
| Clé | `[8:16]` | `trame[37]` |
| Température | `[16:28]` | `trame[38]` |
| Humidité | `[28:36]` | `trame[39]` |

### Solution

```python
def est_valide(self):
    """Vérifie l'intégrité de la trame par contrôle de parité."""
    blocs = [
        self._trame[0:8],    # ID
        self._trame[8:16],   # Clé
        self._trame[16:28],  # Température
        self._trame[28:36],  # Humidité
    ]
    for i, bloc in enumerate(blocs):
        bit_attendu = '1' if bloc.count('1') % 2 == 1 else '0'
        if self._trame[36 + i] != bit_attendu:
            return False
    return True
```

### Fonction de test

```python
TRAME_EXEMPLE = "0010101011001000010010001100011000101101"

def test_est_valide():
    # Trame valide de l'énoncé
    assert Transmission(TRAME_EXEMPLE).est_valide() == True
    # Trame avec dernier bit de contrôle corrompu
    trame_ko = TRAME_EXEMPLE[:-1] + ('0' if TRAME_EXEMPLE[-1] == '1' else '1')
    assert Transmission(trame_ko).est_valide() == False
    # Trame avec un bit de données corrompu
    t_list = list(TRAME_EXEMPLE)
    t_list[0] = '1' if t_list[0] == '0' else '0'
    assert Transmission("".join(t_list)).est_valide() == False
    print("Les tests sont validés.")

test_est_valide()
```

### Points clés

- `self._trame[36 + i]` renvoie un **caractère** (`'0'` ou `'1'`), pas un entier. Toujours comparer avec des chaînes.
- Cette version plantera sur une trame de 38 bits à `i = 2` : `trame[38]` → `IndexError`. C'est précisément ce qui sera corrigé en Q4.

---

## Question 3 — Analyser le plantage de `analyse.py`

### Énoncé

Exécuter `analyse.py` et analyser le message d'erreur. Identifier la cause en observant notamment `data.txt`.

### Contenu de `analyse.py`

```python
import matplotlib.pyplot as plt
from Transmission import Transmission   # ← ERREUR : majuscule

with open("data.txt", "r") as f:
    trames = f.read().split("\n")
    trames.pop()   # supprime la ligne vide finale

transmissions = [Transmission(t) for t in trames]
temperatures  = [t.get_temperature() for t in transmissions if t.est_valide()]

plt.plot(temperatures)
plt.show()
```

### Bug n°1 — Import avec mauvaise casse

```
from Transmission import Transmission   # 'T' majuscule
```

Le fichier s'appelle `transmission.py` (minuscule).

- **Sur Windows :** fonctionne (système de fichiers insensible à la casse)
- **Sur Linux / macOS :** `ModuleNotFoundError: No module named 'Transmission'`

**Correction :** `from transmission import Transmission`

### Bug n°2 — Trames de longueur incorrecte dans `data.txt`

Le fichier contient 314 trames. Trois ont une longueur incorrecte :

| Ligne | Longueur | Anomalie |
|---|---|---|
| 73 | 41 bits | 1 bit de trop |
| 111 | 38 bits | 2 bits manquants |
| 126 | 41 bits | 1 bit de trop |

La trame de **38 bits** provoque une `IndexError` dans `est_valide` à l'itération `i = 2` :

```
self._trame[36 + 2]   →   self._trame[38]   →   IndexError: string index out of range
```

### Résumé des anomalies

| Catégorie | Nombre | Cause |
|---|---|---|
| Trames valides | 308 | Longueur 40 bits + parité correcte |
| Longueur incorrecte | 3 | Corruption lors de la transmission radio |
| Parité incorrecte | 3 | Bit(s) flippé(s) pendant la transmission |
| **Total** | **314** | |

---

## Question 4 — Rendre la classe robuste

### Énoncé

Proposer des corrections de la classe `Transmission` et du fichier `analyse.py` permettant de les rendre robustes et d'analyser les 308 trames valides.

### Stratégie

Deux corrections sont nécessaires :

1. **`analyse.py` :** corriger la casse de l'import.
2. **`Transmission` :** vérifier `len(self._trame) == 40` avant tout décodage et dans `est_valide`.

La vérification explicite est préférable à `try/except` car elle indique précisément la raison du rejet sans masquer d'éventuelles autres erreurs.

### Correction 1 — `analyse.py`

```python
# AVANT (bugué sur Linux/macOS) :
from Transmission import Transmission

# APRÈS (correct) :
from transmission import Transmission   # 't' minuscule
```

### Correction 2 — `transmission.py` (version robuste complète)

```python
class Transmission:
    def __init__(self, trame):
        self._id          = None
        self._temperature = None
        self._humidite    = None
        self._trame       = trame
        if len(trame) == 40:        # AJOUT : garde sur la longueur
            self.decoder()          # ne décode que les trames complètes

    def decoder(self):
        self.decoder_id()
        self.decoder_temperature()
        self.decoder_humidite()

    def decoder_id(self):
        self._id = int(self._trame[0:8], 2)

    def decoder_temperature(self):
        self._temperature = (int(self._trame[16:28], 2) - 900) / 10

    def decoder_humidite(self):
        hum_bits = self._trame[28:36]
        if hum_bits == "10100000":
            self._humidite = 100
        else:
            self._humidite = int(hum_bits[0:4], 2) * 10 + int(hum_bits[4:8], 2)

    def est_valide(self):
        """Vérifie l'intégrité de la trame par contrôle de parité."""
        if len(self._trame) != 40:  # AJOUT : trame de longueur incorrecte → invalide
            return False
        blocs = [self._trame[0:8], self._trame[8:16],
                 self._trame[16:28], self._trame[28:36]]
        for i, bloc in enumerate(blocs):
            bit_attendu = '1' if bloc.count('1') % 2 == 1 else '0'
            if self._trame[36 + i] != bit_attendu:
                return False
        return True

    def get_id(self):          return self._id
    def get_temperature(self): return self._temperature
    def get_humidite(self):    return self._humidite

    def __repr__(self):
        return f"ID:{self._id} / Temp:{self._temperature}°C / Hum:{self._humidite}%"
```

### Fonction de test de robustesse

```python
def test_robustesse():
    TRAME_EX = "0010101011001000010010001100011000101101"

    # Trame normale → valide
    assert Transmission(TRAME_EX).est_valide() == True

    # Trame de 38 bits → ne plante pas, renvoie False
    trame_38 = "00101010100000100100101101110110001010"
    assert len(trame_38) == 38
    assert Transmission(trame_38).est_valide() == False

    # Trame de 41 bits → ne plante pas, renvoie False
    trame_41 = "00101010000110010100111100110101100011111"
    assert len(trame_41) == 41
    assert Transmission(trame_41).est_valide() == False

    # Trame avec parité incorrecte → False
    trame_ko = TRAME_EX[:-1] + ('0' if TRAME_EX[-1] == '1' else '1')
    assert Transmission(trame_ko).est_valide() == False

    # Trame de longueur incorrecte : attributs restent None
    t = Transmission(trame_38)
    assert t.get_temperature() is None
    assert t.get_humidite()    is None

    print("Les tests sont validés.")

test_robustesse()
```

### Pourquoi ne pas utiliser `try/except` ?

Le `try/except` masque **toutes** les exceptions, y compris les erreurs de logique non anticipées. La vérification explicite de longueur est plus précise et plus lisible : elle dit exactement *pourquoi* la trame est rejetée.

### Résultat final attendu

Avec `data.txt` et la classe robuste : **308 températures valides** extraites sur 314 trames (3 de longueur incorrecte + 3 de parité incorrecte rejetées), disponibles pour le tracé `matplotlib`.

---

## Pièges fréquents

### Piège 1 — Comparer un caractère avec un entier

`self._trame[36]` renvoie le *caractère* `'1'` ou `'0'`, pas l'entier 1 ou 0. Il faut comparer avec des chaînes :

```python
# INCORRECT :
if self._trame[36 + i] != 1:   # compare toujours True → trame toujours invalide

# CORRECT :
if self._trame[36 + i] != '1':
# ou :
bit_attendu = '1' if condition else '0'
if self._trame[36 + i] != bit_attendu:
```

### Piège 2 — Oublier le cas spécial 100 % en BCD

`10100000` doit être traité explicitement. Sans cela, `int("1010", 2)` = 10 — ce qui donnerait par hasard 100 en calculant `10 * 10 + 0`, mais ce comportement accidentel ne doit pas être assumé.

### Piège 3 — Ne pas filtrer par `est_valide()` avant `get_temperature()`

Pour une trame corrompue, `get_temperature()` renvoie `None`. Si on ne filtre pas, les `None` font planter `matplotlib` :

```python
# INCORRECT :
temperatures = [t.get_temperature() for t in transmissions]

# CORRECT :
temperatures = [t.get_temperature() for t in transmissions if t.est_valide()]
```

### Piège 4 — La casse des imports Python sur Linux/macOS

`from Transmission import Transmission` et `from transmission import Transmission` sont identiques sur Windows mais différents sur Linux/macOS. Toujours faire correspondre **exactement** la casse du nom du fichier.

---

## Mini-exercices de vérification

### Exercice A — Décodage manuel

Décoder la trame : `0010101010011111010010001010011000011001`

**Réponse :**
- Bits température `[16:28]` = `010010001010` → `int("010010001010", 2)` = 1162 → (1162 − 900) / 10 = **26,2 °C**
- Bits humidité `[28:36]` = `01100001` → BCD : `0110` = 6, `0001` = 1 → **61 %**
- Bits contrôle `[36:40]` = `1001`

### Exercice B — Calcul de parité

Calculer le bit de parité du bloc température `010010001010`.

**Réponse :**  
Nombre de 1 : positions 1, 4, 8, 10 → **4 uns** (pair) → bit de parité = **0**.

### Exercice C — Identifier l'anomalie

La trame `00101010100000100100101101110110001010` a-t-elle une longueur correcte ? Est-elle valide ?

**Réponse :**  
Longueur : 38 caractères → **incorrecte** (devrait être 40). C'est la trame corrompue de la ligne 111 de `data.txt`. Grâce à la garde `if len(self._trame) != 40: return False`, elle est rejetée sans provoquer d'`IndexError`.

---

## Récapitulatif des points essentiels

1. `int(chaine, 2)` convertit du binaire vers décimal — indispensable pour décoder les trames.
2. Le slicing `trame[a:b]` extrait les caractères d'indice `a` à `b-1` inclus.
3. En **BCD**, chaque chiffre décimal est codé indépendamment sur 4 bits — ne pas traiter les 8 bits comme un seul nombre binaire.
4. Le **bit de parité** est `'1'` si le bloc contient un nombre impair de 1, `'0'` sinon — comparer des caractères, pas des entiers.
5. Toujours vérifier `len(trame) == 40` avant d'accéder aux indices — sinon `IndexError` sur les trames corrompues.
6. Sur Linux/macOS, la casse des noms de modules Python est signifiante — `Transmission` ≠ `transmission`.
7. Le filtrage `if t.est_valide()` dans la compréhension de liste élimine proprement les données corrompues sans planter.

---

## Code complet corrigé — `transmission.py`

```python
class Transmission:
    def __init__(self, trame):
        self._id          = None
        self._temperature = None
        self._humidite    = None
        self._trame       = trame
        if len(trame) == 40:
            self.decoder()

    def __repr__(self):
        return f"ID : {self._id} / Temp. : {self._temperature}°C / Hum. : {self._humidite}%"

    def decoder(self):
        self.decoder_id()
        self.decoder_temperature()
        self.decoder_humidite()

    def decoder_id(self):
        self._id = int(self._trame[0:8], 2)

    def decoder_temperature(self):
        self._temperature = (int(self._trame[16:28], 2) - 900) / 10

    def decoder_humidite(self):
        hum_bits = self._trame[28:36]
        if hum_bits == "10100000":
            self._humidite = 100
        else:
            self._humidite = int(hum_bits[0:4], 2) * 10 + int(hum_bits[4:8], 2)

    def est_valide(self):
        if len(self._trame) != 40:
            return False
        blocs = [self._trame[0:8], self._trame[8:16],
                 self._trame[16:28], self._trame[28:36]]
        for i, bloc in enumerate(blocs):
            bit_attendu = '1' if bloc.count('1') % 2 == 1 else '0'
            if self._trame[36 + i] != bit_attendu:
                return False
        return True

    def get_id(self):          return self._id
    def get_temperature(self): return self._temperature
    def get_humidite(self):    return self._humidite
```

## Code complet corrigé — `analyse.py`

```python
import matplotlib.pyplot as plt
from transmission import Transmission   # correction : 't' minuscule

with open("data.txt", "r") as f:
    trames = f.read().split("\n")
    trames.pop()   # supprime la ligne vide finale

transmissions = [Transmission(t) for t in trames]
temperatures  = [t.get_temperature() for t in transmissions if t.est_valide()]

print(f"{len(temperatures)} températures valides extraites sur {len(transmissions)} trames.")

plt.plot(temperatures)
plt.xlabel("Indice de mesure")
plt.ylabel("Température (°C)")
plt.title("Températures valides — Module DEMETER")
plt.show()
```
