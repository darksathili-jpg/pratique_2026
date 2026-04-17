# Fiche de révision — BAC NSI 2026 — Sujet n°19 : Gestion de l'eau en Polynésie

**Niveau :** Terminale NSI  
**Thèmes :** Dictionnaires · Filtrage · Agrégation par clé · Débogage · Analyse par district  
**Source :** Épreuve pratique BAC NSI 2026, sujet n°19  
**Lycée Antoine Watteau — DarkSATHI Li**

---

## Analyse critique — Bug identifié dans le code fourni

La fonction `volume_moyen` divise par `len(reservoirs) - 1` au lieu de `len(reservoirs)` :

```python
moyenne = somme_totale / (len(reservoirs)-1)   # ← BUG : diviseur trop petit
```

| Cas | Résultat bugué | Résultat attendu | Problème |
|---|---|---|---|
| 1 réservoir (vol. 42 000) | **ZeroDivisionError** | 42 000 | Division par zéro ! |
| 2 réservoirs (1 000 L chacun) | **2 000** | 1 000 | Double du réel |
| 10 réservoirs (total 470 000) | **52 222 L** | 47 000 L | +11,1 % de surestimation |

**Correction :** remplacer `(len(reservoirs)-1)` par `len(reservoirs)`.

---

## Contexte du sujet

Dans une commune d'une île polynésienne, les services communaux gèrent plusieurs réservoirs d'eau alimentant différents districts. L'eau provient de précipitations ou de captages naturels. Un programme Python doit aider à analyser les volumes disponibles, détecter les pénuries et identifier les districts vulnérables.

---

## Rappels de cours indispensables

### Représentation d'un réservoir

```python
{"nom": "Nuiavai", "capacite": 100000, "volume": 55000, "district": "Tepua"}
# Accès : reservoir["nom"], reservoir["volume"], etc.
```

### Patron 1 — Recherche par nom dans une liste de dictionnaires

```python
def trouver_par_nom(reservoirs, nom):
    for r in reservoirs:
        if r["nom"] == nom:
            return r      # trouvé → on renvoie le dictionnaire
    return None           # pas trouvé
```

### Patron 2 — Agrégation par clé (volume par district)

```python
resultat = {}                        # dictionnaire résultat
for r in reservoirs:
    cle = r["district"]              # clé d'agrégation
    if cle not in resultat:
        resultat[cle] = 0            # initialiser si première rencontre
    resultat[cle] += r["volume"]     # accumuler
```

### Formule du taux de remplissage

$$\text{taux} = \frac{\text{volume}}{\text{capacité}} \times 100$$

Un réservoir est en **pénurie** si ce taux est *strictement inférieur* à 20 % : `volume / capacite * 100 < 20`.

### La moyenne — erreur classique de diviseur

```python
# CORRECT : diviser par le nombre d'éléments
moyenne = somme / len(liste)

# INCORRECT (bug du sujet) : divise par n-1 → résultat trop grand
# et ZeroDivisionError si la liste contient un seul élément
moyenne = somme / (len(liste) - 1)
```

La formule de la moyenne est \(\bar{x} = \frac{\sum x_i}{n}\). Le diviseur \(n-1\) est utilisé en statistiques pour la variance corrigée — notion sans rapport ici.

---

## Les données du sujet

### Les 10 réservoirs

| nom | capacite | volume | district | taux |
|---|---|---|---|---|
| Nuiavai | 100 000 | 55 000 | Tepua | 55,0 % |
| Farepape | 120 000 | 45 000 | Fare | 37,5 % |
| Vaipuna | 80 000 | 60 000 | Hiva Oro | 75,0 % |
| Vaihere | 95 000 | 20 000 | Fare | 21,1 % |
| Teanavai | 110 000 | 90 000 | Avera | 81,8 % |
| Matavai | 70 000 | 25 000 | Tepua | 35,7 % |
| Ana'itea | 85 000 | 30 000 | Hiva Oro | 35,3 % |
| Faaroa | 60 000 | 40 000 | Avera | 66,7 % |
| Vaitiare | 105 000 | 95 000 | Fare | 90,5 % |
| **Motuavai** | 90 000 | **10 000** | Tepua | **11,1 % ⚠ PÉNURIE** |

### Chiffres clés à mémoriser

- **1 seul réservoir en pénurie :** Motuavai (11,1 % < 20 %)
- **Volume total :** 470 000 L — **Volume moyen correct :** 47 000 L
- **Volume moyen bugué :** 52 222 L (diviseur = 9 au lieu de 10)
- **Seuil vulnérabilité (80 %) :** 47 000 × 0,80 = **37 600 L**
- **District vulnérable :** Tepua (vol. moyen 30 000 L < 37 600 L)

### Analyse par district

| District | Réservoirs | Vol. total | Vol. moyen | Statut |
|---|---|---|---|---|
| Avera | Teanavai, Faaroa | 130 000 L | 65 000 L | ✓ OK |
| Fare | Farepape, Vaihere, Vaitiare | 160 000 L | 53 333 L | ✓ OK |
| Hiva Oro | Vaipuna, Ana'itea | 90 000 L | 45 000 L | ✓ OK |
| **Tepua** | Nuiavai, Matavai, Motuavai | 90 000 L | **30 000 L** | **⚠ VULNÉRABLE** |

### Fonctions fournies (à ne pas réécrire)

```python
def taux_remplissage(reservoir, changement=0):
    """Renvoie le taux de remplissage (en %), avec changement hypothétique optionnel."""
    volume_modifie = reservoir["volume"] + changement
    capacite = reservoir["capacite"]
    if volume_modifie < 0: volume_modifie = 0
    if volume_modifie > capacite: volume_modifie = capacite
    return volume_modifie * 100 / capacite

def liste_districts(reservoirs):
    """Renvoie la liste des districts présents."""
    liste = []
    for r in reservoirs:
        if r["district"] not in liste:
            liste.append(r["district"])
    return liste

def reservoirs_par_district(reservoirs):
    """Renvoie {district: [liste des réservoirs du district]}."""
    rpd = {}
    for r in reservoirs:
        d = r["district"]
        if d not in rpd: rpd[d] = []
        rpd[d].append(r)
    return rpd
```

---

## Question 1 — `est_en_penurie`

### Énoncé

Écrire `est_en_penurie(reservoirs, nom)` qui prend une liste et un nom, et renvoie `True` si le taux de remplissage est strictement inférieur à 20 %, `False` sinon.

### Solution

```python
def est_en_penurie(reservoirs, nom):
    """Renvoie True si le réservoir nommé nom est en pénurie (taux < 20%)."""
    for r in reservoirs:
        if r["nom"] == nom:
            taux = r["volume"] / r["capacite"] * 100
            return taux < 20   # True si pénurie, False sinon
```

### Fonction de test

```python
def test_est_en_penurie():
    # Seul réservoir en pénurie : Motuavai (10000/90000 = 11.1%)
    assert est_en_penurie(reservoirs, "Motuavai") == True
    # Vaihere : 20000/95000 = 21.05% → pas en pénurie (strictement < 20 !)
    assert est_en_penurie(reservoirs, "Vaihere")  == False
    assert est_en_penurie(reservoirs, "Nuiavai")  == False   # 55.0%
    assert est_en_penurie(reservoirs, "Vaitiare") == False   # 90.5%
    print("Les tests sont validés.")

test_est_en_penurie()
```

### Points clés

- Condition **strictement** inférieure : `taux < 20`, pas `taux <= 20`.
- Vaihere à 21,05 % → **pas** en pénurie (piège classique de ce sujet).
- On peut aussi utiliser `taux_remplissage(r) < 20` qui est déjà fournie.

---

## Question 2 — `volume_par_district`

### Énoncé

Écrire `volume_par_district(reservoirs)` qui renvoie un dictionnaire `{district: volume_total}` pour chaque district.

### Solution

```python
def volume_par_district(reservoirs):
    """Renvoie {district: volume_total} pour chaque district."""
    volumes = {}
    for r in reservoirs:
        d = r["district"]
        if d not in volumes:
            volumes[d] = 0          # initialiser si première rencontre
        volumes[d] += r["volume"]   # accumuler
    return volumes
```

### Fonction de test

```python
def test_volume_par_district():
    vpd = volume_par_district(reservoirs)
    assert len(vpd)            == 4
    assert vpd["Fare"]         == 160000   # 45000 + 20000 + 95000
    assert vpd["Avera"]        == 130000   # 90000 + 40000
    assert vpd["Hiva Oro"]     == 90000    # 60000 + 30000
    assert vpd["Tepua"]        == 90000    # 55000 + 25000 + 10000
    assert sum(vpd.values())   == 470000
    print("Les tests sont validés.")
```

### Points clés

- L'initialisation `if d not in volumes: volumes[d] = 0` est **obligatoire** — sans elle, la première rencontre d'un district lève une `KeyError`.
- La somme de tous les volumes doit donner 470 000 L — c'est un bon test global.

---

## Question 3 — Tester et corriger `volume_moyen`

### Énoncé

Proposer des assertions qui mettent le bug en évidence, puis proposer une version corrigée.

### Code fourni (bugué)

```python
def volume_moyen(reservoirs):
    somme_totale = 0
    for r in reservoirs:
        somme_totale += r["volume"]
    moyenne = somme_totale / (len(reservoirs)-1)   # ← BUG : diviseur n-1
    return moyenne
```

### Les 3 assertions demandées

```python
# Assertion 1 : 2 réservoirs de même volume → moyenne = ce volume
r2 = [{"volume": 1000, "capacite": 5000, "nom":"A", "district":"X"},
      {"volume": 1000, "capacite": 5000, "nom":"B", "district":"X"}]
assert volume_moyen(r2) == 1000
# Avec le bug : 2000/1 = 2000 ≠ 1000 → ÉCHOUE ✗

# Assertion 2 : moyenne ≤ volume maximal de la liste
max_vol = max(r["volume"] for r in reservoirs)
assert volume_moyen(reservoirs) <= max_vol
# Avec le bug : 52222 > 95000 ? Non, passe... mais trompe le développeur

# Assertion 3 : valeur exacte connue (470000 / 10 = 47000)
assert volume_moyen(reservoirs) == 47000.0
# Avec le bug : 52222.22 ≠ 47000 → ÉCHOUE ✗
```

### Version corrigée

```python
def volume_moyen(reservoirs):
    """Renvoie le volume moyen d'eau disponible sur tous les réservoirs."""
    somme_totale = 0
    for r in reservoirs:
        somme_totale += r["volume"]
    return somme_totale / len(reservoirs)   # ← CORRECTION : len(reservoirs)
```

### Vérification

- Sur les 10 réservoirs : 470 000 / 10 = **47 000 L** ✓
- Avec 2 réservoirs de 1 000 L : 2 000 / 2 = **1 000 L** ✓
- Avec 1 réservoir de 42 000 L : 42 000 / 1 = **42 000 L** ✓ (plus de ZeroDivisionError)

---

## Question 4 — Districts vulnérables

### Énoncé

Proposer une fonction identifiant les districts vulnérables (volume moyen < seuil_relatif × volume moyen global), puis proposer une stratégie de gestion.

### Solution

```python
def districts_vulnerables(reservoirs, seuil_relatif=0.80):
    """Renvoie la liste des districts dont le vol. moyen < seuil_relatif × vol. moyen global."""
    vol_moy_global = volume_moyen(reservoirs)
    seuil          = vol_moy_global * seuil_relatif
    rpd = reservoirs_par_district(reservoirs)   # fonction fournie → réutiliser !
    vulnerables = []
    for district, ress in rpd.items():
        vol_moy_district = volume_moyen(ress)
        if vol_moy_district < seuil:
            vulnerables.append(district)
    return vulnerables
```

### Résultats

- Vol. moyen global : **47 000 L**
- Seuil (80 %) : **37 600 L**

| District | Vol. moyen | Statut |
|---|---|---|
| Avera | 65 000 L | ✓ OK |
| Fare | 53 333 L | ✓ OK |
| Hiva Oro | 45 000 L | ✓ OK |
| **Tepua** | **30 000 L** | **⚠ VULNÉRABLE** |

### Fonction de test

```python
def test_districts_vulnerables():
    # Avec seuil 80% : seul Tepua vulnérable
    assert districts_vulnerables(reservoirs) == ["Tepua"]
    # Avec seuil 100% : Tepua et Hiva Oro (< 47000)
    vuln_100 = districts_vulnerables(reservoirs, seuil_relatif=1.0)
    assert "Tepua"    in vuln_100
    assert "Hiva Oro" in vuln_100
    # Avec seuil 0% : aucun vulnérable
    assert districts_vulnerables(reservoirs, seuil_relatif=0.0) == []
    print("Les tests sont validés.")
```

### Stratégie de gestion pour le district Tepua

Le district Tepua est vulnérable à cause principalement de Motuavai (11,1 % — pénurie) et de Matavai (35,7 %). Quatre leviers d'action :

1. **Transfert d'eau prioritaire :** Teanavai (Avera, 81,8 %) et Vaitiare (Fare, 90,5 %) peuvent céder de l'eau via camion-citerne vers Motuavai. Utiliser `taux_remplissage` avec un `changement` négatif pour simuler l'impact d'un prélèvement.

2. **Restriction temporaire de consommation :** réduire la consommation dans Tepua jusqu'à rétablissement des niveaux.

3. **Alertes automatiques :** tableau de bord appelant `est_en_penurie` et `districts_vulnerables` à intervalles réguliers pour déclencher des alertes préventives.

4. **Priorisation des captages :** orienter les prochaines pluies/captages naturels vers les réservoirs de Tepua.

---

## Pièges fréquents

### Piège 1 — Diviser par n-1 au lieu de n pour la moyenne

La moyenne de \(n\) valeurs = somme / \(n\). Le diviseur \(n-1\) est pour la variance corrigée (statistiques). Avec `len == 1`, `len - 1 == 0` → `ZeroDivisionError`.

### Piège 2 — Condition stricte vs non stricte

La pénurie est « strictement inférieure à 20 % » → `taux < 20`. Vaihere à 21,05 % n'est pas en pénurie. Toujours tester les cas limites.

### Piège 3 — Oublier d'initialiser la clé du dictionnaire

Sans `if d not in volumes: volumes[d] = 0`, Python lève `KeyError` à la première tentative de `volumes[d] += ...`. L'initialisation est indispensable.

### Piège 4 — Réécrire les fonctions fournies

Le code fourni contient déjà `reservoirs_par_district`, `liste_districts`, `taux_remplissage`. Il faut **réutiliser** ces fonctions plutôt que les réécrire. Lire tout le code avant de commencer.

---

## Stratégie optimale le jour J

| Question | Temps | Ce qu'il faut faire |
|---|---|---|
| Q1 | 8 min | boucle + filtre par nom + taux &lt; 20. Tester Motuavai=True, Vaihere=False |
| Q2 | 8 min | patron agrégation par clé. Vérifier Fare=160 000, total=470 000 |
| Q3 | 10 min | repérer `len-1`, écrire 3 assertions, corriger → `len(reservoirs)` |
| Q4 | 12 min | écrire `districts_vulnerables`, résultat Tepua, proposer 3-4 mesures |

---

## Mini-exercices de vérification

### Exercice A — Taux de remplissage à la main

Motuavai : 10 000 / 90 000 × 100 = **11,11 %** < 20 % → **en pénurie** → `True`

### Exercice B — Volume total du district Fare

Farepape (45 000) + Vaihere (20 000) + Vaitiare (95 000) = **160 000 L**

### Exercice C — Bug de volume_moyen

3 réservoirs de 10, 20 et 30 : somme = 60, diviseur bugué = 2 → **30** (faux). Attendu : 60 / 3 = **20**.

---

## Code complet corrigé — `gestion_eau.py`

```python
from donnees import reservoirs


# ── Q1 ─────────────────────────────────────────────────────────────────────

def est_en_penurie(reservoirs, nom):
    """Renvoie True si le réservoir nommé nom est en pénurie (taux < 20%)."""
    for r in reservoirs:
        if r["nom"] == nom:
            taux = r["volume"] / r["capacite"] * 100
            return taux < 20


# ── Q2 ─────────────────────────────────────────────────────────────────────

def volume_par_district(reservoirs):
    """Renvoie {district: volume_total} pour chaque district."""
    volumes = {}
    for r in reservoirs:
        d = r["district"]
        if d not in volumes:
            volumes[d] = 0
        volumes[d] += r["volume"]
    return volumes


# ── Q3 — version CORRIGÉE ──────────────────────────────────────────────────

def volume_moyen(reservoirs):
    """Renvoie le volume moyen d'eau disponible sur tous les réservoirs."""
    somme_totale = 0
    for r in reservoirs:
        somme_totale += r["volume"]
    return somme_totale / len(reservoirs)   # ← CORRECTION : len(reservoirs)


def test_volume_moyen():
    r2 = [{"volume": 1000, "capacite": 5000, "nom":"A", "district":"X"},
          {"volume": 1000, "capacite": 5000, "nom":"B", "district":"X"}]
    assert volume_moyen(r2) == 1000
    max_vol = max(r["volume"] for r in reservoirs)
    assert volume_moyen(reservoirs) <= max_vol
    assert volume_moyen(reservoirs) == 47000.0
    print("Les tests sont validés.")


# ── Fonctions fournies (non modifiées) ─────────────────────────────────────

def taux_remplissage(reservoir, changement=0):
    volume_modifie = reservoir["volume"] + changement
    capacite = reservoir["capacite"]
    if volume_modifie < 0:       volume_modifie = 0
    if volume_modifie > capacite: volume_modifie = capacite
    return volume_modifie * 100 / capacite


def liste_districts(reservoirs):
    liste = []
    for r in reservoirs:
        if r["district"] not in liste:
            liste.append(r["district"])
    return liste


def reservoirs_par_district(reservoirs):
    rpd = {}
    for r in reservoirs:
        d = r["district"]
        if d not in rpd: rpd[d] = []
        rpd[d].append(r)
    return rpd


# ── Q4 ─────────────────────────────────────────────────────────────────────

def districts_vulnerables(reservoirs, seuil_relatif=0.80):
    """Renvoie les districts dont le vol. moyen < seuil_relatif × vol. moyen global."""
    vol_moy_global = volume_moyen(reservoirs)
    seuil          = vol_moy_global * seuil_relatif
    rpd = reservoirs_par_district(reservoirs)
    vulnerables = []
    for district, ress in rpd.items():
        vol_moy_district = volume_moyen(ress)
        if vol_moy_district < seuil:
            vulnerables.append(district)
    return vulnerables
```

## Récapitulatif — Les 4 réponses en un coup d'œil

```python
# Q1 (3 lignes)
for r in reservoirs:
    if r["nom"] == nom:
        return r["volume"] / r["capacite"] * 100 < 20

# Q2 (5 lignes)
volumes = {}
for r in reservoirs:
    d = r["district"]
    if d not in volumes: volumes[d] = 0
    volumes[d] += r["volume"]
return volumes

# Q3 — 1 mot supprimé : (len(reservoirs)-1) → len(reservoirs)
# Résultat : 47 000 L (au lieu de 52 222 L)

# Q4 (5 lignes + réutilisation des fonctions fournies)
seuil = volume_moyen(reservoirs) * seuil_relatif
rpd   = reservoirs_par_district(reservoirs)
return [d for d, ress in rpd.items() if volume_moyen(ress) < seuil]
# Résultat : ["Tepua"] — vol. moyen 30 000 L < seuil 37 600 L
```
