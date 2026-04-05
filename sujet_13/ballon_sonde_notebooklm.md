# NSI Terminale – Sujet pratique n°13 – BAC 2026
## Étude climatique par ballon sonde — Traitement CSV, fonctions, assertions, KML

---

## MÉTADONNÉES DU DOCUMENT

- **Matière** : Numérique et Sciences Informatiques (NSI)
- **Niveau** : Terminale générale
- **Type d'épreuve** : Partie pratique du baccalauréat — durée 1 heure
- **Session** : 2026 — Sujet n°13
- **Thème du programme** : Traitement de données, algorithmique, assertions, fichiers
- **Langage** : Python 3
- **Fichiers fournis à l'examen** : `etude_climatique.py`, `releves_ballon_sonde.csv`
- **Modules Python requis** : aucun (lecture manuelle du CSV)

---

## PARTIE 1 — CONTEXTE ET PROBLÉMATIQUE

### Contexte scientifique

Un ballon sonde est gonflé à l'hélium et équipé d'instruments de mesure. Lâché au sol, il s'élève et collecte des données tout au long de sa montée (température en kelvins, altitude en mètres, géolocalisation), puis éclate entre 20 et 30 km d'altitude et redescend par parachute. Ces données sont essentielles pour les prévisions météorologiques. Ce sujet n'exploite que les données de la montée.

### Objectifs du script Python à compléter

1. Récupérer les 4 listes de données depuis le fichier CSV.
2. Convertir les températures de kelvins en degrés Celsius, arrondies à 1 décimale.
3. Trouver la température minimale et les altitudes correspondantes.
4. Sécuriser et corriger la fonction de génération du fichier KML.

---

## PARTIE 2 — DONNÉES DU FICHIER `releves_ballon_sonde.csv`

### Structure du fichier

Séparateur : point-virgule (`;`). Première ligne : en-têtes `Altitude_m;Temperature_K;Longitude;Latitude`. La fonction `recupere_donnees_fichier_csv` supprime automatiquement cette ligne d'en-têtes.

### Contenu intégral du fichier (20 relevés)

```
Altitude_m;Temperature_K;Longitude;Latitude
0;288.15;4.760467;45.602117
200;286.85;4.760467;45.602167
500;284.85;4.761183;45.60125
1100;281.05;4.766717;45.600117
1800;276.55;4.765183;45.60085
2250;273.65;4.766633;45.601017
2680;270.85;4.770567;45.605383
5070;255.45;4.800883;45.602433
6800;244.25;4.819033;45.608467
8900;230.65;4.850517;45.608551
9800;224.85;4.892783;45.601533
11000;217.15;4.963467;45.596267
13500;216.95;5.155833;45.586467
15120;216.65;5.298383;45.591167
17210;216.65;5.444417;45.595083
19500;217.15;5.578417;45.597952
20100;217.05;5.6044;45.605617
21250;220.15;5.662033;45.611053
23620;223.05;5.747867;45.62555
24865;225.15;5.766817;45.616383
```

### Tableau complet avec températures converties en °C

| Altitude (m) | Temp. (K) | Temp. (°C) | Longitude | Latitude |
|-------------|-----------|-----------|-----------|---------|
| 0 | 288.15 | 15.0 | 4.760467 | 45.602117 |
| 200 | 286.85 | 13.7 | 4.760467 | 45.602167 |
| 500 | 284.85 | 11.7 | 4.761183 | 45.60125 |
| 1100 | 281.05 | 7.9 | 4.766717 | 45.600117 |
| 1800 | 276.55 | 3.4 | 4.765183 | 45.60085 |
| 2250 | 273.65 | 0.5 | 4.766633 | 45.601017 |
| 2680 | 270.85 | -2.3 | 4.770567 | 45.605383 |
| 5070 | 255.45 | -17.7 | 4.800883 | 45.602433 |
| 6800 | 244.25 | -28.9 | 4.819033 | 45.608467 |
| 8900 | 230.65 | -42.5 | 4.850517 | 45.608551 |
| 9800 | 224.85 | -48.3 | 4.892783 | 45.601533 |
| 11000 | 217.15 | -56.0 | 4.963467 | 45.596267 |
| 13500 | 216.95 | -56.2 | 5.155833 | 45.586467 |
| **15120** | **216.65** | **-56.5 ❄** | 5.298383 | 45.591167 |
| **17210** | **216.65** | **-56.5 ❄** | 5.444417 | 45.595083 |
| 19500 | 217.15 | -56.0 | 5.578417 | 45.597952 |
| 20100 | 217.05 | -56.1 | 5.6044 | 45.605617 |
| 21250 | 220.15 | -53.0 | 5.662033 | 45.611053 |
| 23620 | 223.05 | -50.1 | 5.747867 | 45.62555 |
| 24865 | 225.15 | -48.0 | 5.766817 | 45.616383 |

### Statistiques clés

- **Nombre de relevés** : 20
- **Altitude minimale** : 0 m (sol)
- **Altitude maximale** : 24 865 m
- **Température au sol** : 15.0 °C (288.15 K)
- **Température au sommet** : -48.0 °C (225.15 K)
- **Température minimale** : **-56.5 °C** (216.65 K)
- **Altitudes à -56.5 °C** : **[15120, 17210]** (deux altitudes à égalité)

---

## PARTIE 3 — FICHIER DE DÉPART `etude_climatique.py`

### Fonctions déjà fournies

#### Fonction 1 — `recupere_donnees_fichier_csv(nom_fichier)`

```python
def recupere_donnees_fichier_csv(nom_fichier):
    """ Fonction qui récupère les données relevées du ballon sonde sans les en-têtes """
    altitudes    = []
    temperatures = []
    longitudes   = []
    latitudes    = []
    contenu_fichier = open(nom_fichier, 'r')
    contenu_fichier.readline()           # supprime la 1ère ligne (en-têtes)
    for ligne in contenu_fichier.readlines():
        ligne = ligne.rstrip()           # supprime \n et espaces en fin de ligne
        listeValeurs = ligne.split(";")  # sépare les colonnes par ;
        altitudes.append(int(listeValeurs[0]))        # int
        temperatures.append(float(listeValeurs[1]))   # float
        longitudes.append(float(listeValeurs[2]))     # float
        latitudes.append(float(listeValeurs[3]))      # float
    return altitudes, temperatures, longitudes, latitudes
```

**Ce que renvoie cette fonction** : un tuple de 4 listes, dans cet ordre exact :
1. `altitudes` — liste d'entiers (mètres)
2. `temperatures` — liste de flottants (kelvins, pas encore convertis !)
3. `longitudes` — liste de flottants
4. `latitudes` — liste de flottants

#### Fonction 2 — `genere_kml(liste_longitudes, liste_latitudes)` — version buguée fournie

```python
def genere_kml(liste_longitudes, liste_latitudes):
    fichier_kml = open('ballon sonde.kml', 'w')
    entete_fichier  = '<?xml version="1.0" encoding="UTF-8"?>\n'
    entete_fichier += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    entete_fichier += '<Document>\n'
    entete_fichier += '<name>Trajectoire ballon sonde</name>\n'
    fichier_kml.write(entete_fichier)
    for i in range(len(liste_longitudes)):
        corps_fichier  = '<Placemark>\n'
        corps_fichier += f'<name>Point {i}</name>\n'
        corps_fichier += '<Point>\n'
        corps_fichier += f'<coordinates>{liste_longitudes[i]},{liste_latitudes[i]}</coordinates>\n'
        corps_fichier += '</Point>\n'
        corps_fichier += '</Placemark>\n'
        fichier_kml.write(corps_fichier)
    bas_fichier = '</Document>\n'
    fichier_kml.write(bas_fichier)
    fichier_kml.close()
    # BUG : </kml> est absent — le fichier KML n'est pas valide !
```

### Squelette à compléter

```python
# QUESTION 1
# Compléter ici

# QUESTION 2
def conversion_K_en_C(liste_temperatures):
    pass  # Ajuster la fonction

# QUESTION 3
def altitude_la_plus_froide(liste_altitudes, liste_temperatures):
    pass  # Ajuster la fonction
```

---

## PARTIE 4 — QUESTIONS ET CORRECTIONS COMPLÈTES

---

### QUESTION 1 — Appeler `recupere_donnees_fichier_csv` et récupérer les 4 listes

**Énoncé** : En utilisant cette fonction, écrire la ou les lignes de code qui récupèrent les données relevées par le ballon sonde dans 4 listes différentes (altitudes, temperatures, longitudes et latitudes).

**Concept clé** : dépackage de retour multiple. Une fonction peut retourner plusieurs valeurs séparées par des virgules. À l'appel, on les récupère dans autant de variables.

**Correction** :

```python
altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv('releves_ballon_sonde.csv')
```

**C'est une seule ligne.** L'ordre des 4 variables doit être identique à l'ordre du `return` de la fonction.

**Vérifications après l'appel** :
- `len(altitudes)` → 20
- `len(temperatures)` → 20
- `altitudes[0]` → 0 (sol)
- `altitudes[-1]` → 24865 (sommet)
- `temperatures[0]` → 288.15 (en kelvins, pas encore converti)
- `temperatures` contient des kelvins — il faudra appeler `conversion_K_en_C` ensuite

**Fonction de test** :

```python
def test_recuperation():
    alt, temp, lon, lat = recupere_donnees_fichier_csv('releves_ballon_sonde.csv')
    assert len(alt)  == 20
    assert len(temp) == 20
    assert len(lon)  == 20
    assert len(lat)  == 20
    assert alt[0]    == 0
    assert alt[-1]   == 24865
    assert temp[0]   == 288.15
    print("Les tests sont validés.")

test_recuperation()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 2 — Écrire la fonction `conversion_K_en_C`

**Énoncé** : Écrire une fonction `conversion_K_en_C` qui prend en paramètre une liste de températures en kelvins et retourne cette même liste convertie en degrés Celsius, avec les valeurs arrondies à 1 chiffre après la virgule.

**Formule** : T°C = TK − 273,15

**Pourquoi arrondir ?** En Python, `288.15 - 273.15` peut donner `14.999999999999972` à cause des erreurs d'arrondi des nombres flottants. `round(14.999999999999972, 1)` → `15.0`.

**Valeurs de conversion exactes pour les données du ballon** :

| Kelvin | Calcul | °C (arrondi) |
|--------|--------|-------------|
| 288.15 | 288.15 − 273.15 | 15.0 |
| 273.65 | 273.65 − 273.15 | 0.5 |
| 255.45 | 255.45 − 273.15 | -17.7 |
| 216.65 | 216.65 − 273.15 | -56.5 |
| 225.15 | 225.15 − 273.15 | -48.0 |

**Correction — version boucle** :

```python
def conversion_K_en_C(liste_temperatures):
    resultat = []
    for temp_k in liste_temperatures:
        temp_c = round(temp_k - 273.15, 1)
        resultat.append(temp_c)
    return resultat
```

**Correction — version compréhension de liste** :

```python
def conversion_K_en_C(liste_temperatures):
    return [round(t - 273.15, 1) for t in liste_temperatures]
```

**Ligne de test demandée par l'énoncé** :

```python
print(conversion_K_en_C([288.15, 273.65, 255.45, 216.65]))
# → [15.0, 0.5, -17.7, -56.5]
```

**Fonction de test** :

```python
def test_conversion_K_en_C():
    assert conversion_K_en_C([288.15]) == [15.0]
    assert conversion_K_en_C([273.65]) == [0.5]
    assert conversion_K_en_C([216.65]) == [-56.5]
    assert conversion_K_en_C([288.15, 273.65, 255.45, 216.65]) == [15.0, 0.5, -17.7, -56.5]
    print("Les tests sont validés.")

test_conversion_K_en_C()
```

**Usage dans le script complet** :

```python
altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv('releves_ballon_sonde.csv')
temperatures_celsius = conversion_K_en_C(temperatures)
# temperatures_celsius[0]  → 15.0
# temperatures_celsius[-1] → -48.0
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 3 — Écrire la fonction `altitude_la_plus_froide`

**Énoncé** : Proposer une écriture de la fonction `altitude_la_plus_froide` qui prend en paramètres une liste d'altitudes et une liste de températures en °C, et renvoie la température la plus froide ainsi qu'une liste contenant la ou les altitudes correspondantes.

**Exemples de l'énoncé** :

```python
>>> altitude_la_plus_froide([7000, 10125, 13896, 14211], [-35.2, -52.1, -57.4, -57.4])
(-57.4, [13896, 14211])

>>> altitude_la_plus_froide([6000, 7250, 11542, 15214, 17300], [-33.7, -45, -53, -58.5, -60.1])
(-60.1, [17300])
```

**Résultat avec les vraies données du ballon** :

```python
altitude_la_plus_froide(altitudes, temperatures_celsius)
→ (-56.5, [15120, 17210])
```

Les altitudes 15 120 m et 17 210 m ont toutes deux la même température de -56.5 °C (216.65 K). La fonction doit renvoyer les **deux** altitudes dans la liste.

**Correction** :

```python
def altitude_la_plus_froide(liste_altitudes, liste_temperatures):
    t_min    = min(liste_temperatures)
    alts_min = []
    for alt, temp in zip(liste_altitudes, liste_temperatures):
        if temp == t_min:
            alts_min.append(alt)
    return (t_min, alts_min)
```

**Correction — version avec indice** :

```python
def altitude_la_plus_froide(liste_altitudes, liste_temperatures):
    t_min    = min(liste_temperatures)
    alts_min = []
    for i in range(len(liste_altitudes)):
        if liste_temperatures[i] == t_min:
            alts_min.append(liste_altitudes[i])
    return (t_min, alts_min)
```

**Fonction de test** :

```python
def test_altitude_la_plus_froide():
    # Exemple 1 de l'énoncé
    assert altitude_la_plus_froide([7000, 10125, 13896, 14211],
                                   [-35.2, -52.1, -57.4, -57.4]) == (-57.4, [13896, 14211])
    # Exemple 2 de l'énoncé
    assert altitude_la_plus_froide([6000, 7250, 11542, 15214, 17300],
                                   [-33.7, -45, -53, -58.5, -60.1]) == (-60.1, [17300])
    # Données réelles
    alt_b  = [15120, 17210, 19500]
    temp_b = [-56.5, -56.5, -56.0]
    assert altitude_la_plus_froide(alt_b, temp_b) == (-56.5, [15120, 17210])
    print("Les tests sont validés.")

test_altitude_la_plus_froide()
```

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

### QUESTION 4 — Ajouter une assertion dans `genere_kml`

**Énoncé** : Observer le corps de la fonction `genere_kml`, puis, à l'aide d'une assertion, insérer une ligne de code qui garantit que les deux listes `liste_longitudes` et `liste_latitudes` sont de même longueur.

**Pourquoi cette assertion ?** La boucle `for i in range(len(liste_longitudes))` utilise `i` pour accéder aux deux listes simultanément avec `liste_longitudes[i]` et `liste_latitudes[i]`. Si les deux listes ont des longueurs différentes, un `IndexError` se produit en cours de boucle. L'assertion, placée en début de fonction, détecte le problème avant tout traitement.

**Correction** :

```python
def genere_kml(liste_longitudes, liste_latitudes):
    assert len(liste_longitudes) == len(liste_latitudes), \
           "Erreur : les listes longitude et latitude n'ont pas la même longueur"
    fichier_kml = open('ballon sonde.kml', 'w')
    ...
```

**Comportement avec l'assertion** :
- `genere_kml([4.76, 5.15], [45.60, 45.59])` → fonctionne normalement (2 == 2)
- `genere_kml([4.76, 5.15, 5.44], [45.60])` → lève `AssertionError` immédiatement

**Avec les données du ballon** : `len(longitudes) == len(latitudes) == 20` → assertion toujours satisfaite.

---

### QUESTION 5 — Appeler `genere_kml`

**Énoncé** : Écrire une ligne de code qui appelle la fonction `genere_kml` avec les deux listes de longitudes et latitudes obtenues à la question 1.

**Correction** :

```python
genere_kml(longitudes, latitudes)
```

**Ordre des arguments** : la signature est `genere_kml(liste_longitudes, liste_latitudes)`. L'ordre doit être `longitudes` en premier, `latitudes` en second.

**Effet** : crée le fichier `ballon sonde.kml` dans le répertoire courant, avec 20 balises `<Placemark>` (une par relevé GPS du ballon).

---

### QUESTION 6 — Corriger le bug de la balise `</kml>`

**Énoncé** : La balise `</kml>` est absente en toute fin de fichier, ce qui cause des problèmes de compatibilité. Proposer une amélioration du code.

**Structure d'un fichier KML valide** :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">    ← balise ouvrante
<Document>
  ...20 Placemark...
</Document>
</kml>                                           ← balise FERMANTE — MANQUANTE
```

**Analyse du bug** : la fonction fournie écrit `</Document>` puis ferme le fichier, sans écrire `</kml>`. Le fichier XML n'est donc pas valide selon la norme KML.

**Correction — Solution A (modifier `bas_fichier`)** :

```python
# Remplacer :
bas_fichier = '</Document>\n'
fichier_kml.write(bas_fichier)
fichier_kml.close()

# Par :
bas_fichier  = '</Document>\n'
bas_fichier += '</kml>\n'          # ← correction : ajout de la balise fermante
fichier_kml.write(bas_fichier)
fichier_kml.close()
```

**Correction — Solution B (écriture séparée)** :

```python
bas_fichier = '</Document>\n'
fichier_kml.write(bas_fichier)
fichier_kml.write('</kml>\n')     # ← correction : ligne supplémentaire
fichier_kml.close()
```

**Vérification** : ouvrir le fichier `ballon sonde.kml` dans un éditeur texte et confirmer que la dernière ligne est `</kml>`.

**Appel professeur** : l'énoncé précise un appel professeur après cette question.

---

## PARTIE 5 — CODE COMPLET ET FONCTIONNEL (SOLUTION DE RÉFÉRENCE)

```python
def recupere_donnees_fichier_csv(nom_fichier):
    altitudes = []; temperatures = []; longitudes = []; latitudes = []
    contenu_fichier = open(nom_fichier, 'r')
    contenu_fichier.readline()
    for ligne in contenu_fichier.readlines():
        ligne = ligne.rstrip()
        listeValeurs = ligne.split(";")
        altitudes.append(int(listeValeurs[0]))
        temperatures.append(float(listeValeurs[1]))
        longitudes.append(float(listeValeurs[2]))
        latitudes.append(float(listeValeurs[3]))
    return altitudes, temperatures, longitudes, latitudes


def genere_kml(liste_longitudes, liste_latitudes):
    assert len(liste_longitudes) == len(liste_latitudes), \
           "Les listes longitudes et latitudes doivent avoir la même longueur"
    fichier_kml = open('ballon sonde.kml', 'w')
    entete_fichier  = '<?xml version="1.0" encoding="UTF-8"?>\n'
    entete_fichier += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    entete_fichier += '<Document>\n'
    entete_fichier += '<name>Trajectoire ballon sonde</name>\n'
    fichier_kml.write(entete_fichier)
    for i in range(len(liste_longitudes)):
        corps_fichier  = '<Placemark>\n'
        corps_fichier += f'<name>Point {i}</name>\n'
        corps_fichier += '<Point>\n'
        corps_fichier += f'<coordinates>{liste_longitudes[i]},{liste_latitudes[i]}</coordinates>\n'
        corps_fichier += '</Point>\n'
        corps_fichier += '</Placemark>\n'
        fichier_kml.write(corps_fichier)
    bas_fichier  = '</Document>\n'
    bas_fichier += '</kml>\n'          # ← correction Q6
    fichier_kml.write(bas_fichier)
    fichier_kml.close()


# QUESTION 1
altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv('releves_ballon_sonde.csv')


# QUESTION 2
def conversion_K_en_C(liste_temperatures):
    resultat = []
    for temp_k in liste_temperatures:
        temp_c = round(temp_k - 273.15, 1)
        resultat.append(temp_c)
    return resultat

temperatures_celsius = conversion_K_en_C(temperatures)
print(conversion_K_en_C([288.15, 273.65, 255.45, 216.65]))
# → [15.0, 0.5, -17.7, -56.5]


# QUESTION 3
def altitude_la_plus_froide(liste_altitudes, liste_temperatures):
    t_min    = min(liste_temperatures)
    alts_min = []
    for alt, temp in zip(liste_altitudes, liste_temperatures):
        if temp == t_min:
            alts_min.append(alt)
    return (t_min, alts_min)

print(altitude_la_plus_froide(altitudes, temperatures_celsius))
# → (-56.5, [15120, 17210])


# QUESTION 5
genere_kml(longitudes, latitudes)
```

---

## PARTIE 6 — ERREURS FRÉQUENTES ET PIÈGES

### Piège 1 — Inverser l'ordre des 4 listes au dépackage (Q1)

La fonction retourne dans l'ordre : `altitudes, temperatures, longitudes, latitudes`. Si l'ordre est inversé, aucune erreur Python n'est levée mais les données sont mélangées silencieusement.

```python
# ERREUR : ordre incorrect
longitudes, latitudes, altitudes, temperatures = recupere_donnees_fichier_csv(...)

# CORRECT
altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv(...)
```

### Piège 2 — Oublier `round()` dans `conversion_K_en_C` (Q2)

Sans `round(..., 1)`, Python peut retourner `14.999999999999972` au lieu de `15.0` à cause de l'arithmétique flottante. Les assertions échoueront.

```python
# ERREUR : sans arrondi
[t - 273.15 for t in liste]   # peut donner 14.999999...

# CORRECT
[round(t - 273.15, 1) for t in liste]   # donne 15.0
```

### Piège 3 — Sortir de la boucle à la première occurrence (Q3)

Si on utilise `return` à l'intérieur de la boucle, on manque les altitudes suivantes qui partagent la même température minimale. La boucle doit parcourir toute la liste.

```python
# ERREUR : s'arrête à la première altitude
for alt, temp in zip(liste_altitudes, liste_temperatures):
    if temp == t_min:
        return (t_min, [alt])   # manque les suivantes !

# CORRECT : collecte toutes les altitudes
alts_min = []
for alt, temp in zip(liste_altitudes, liste_temperatures):
    if temp == t_min:
        alts_min.append(alt)
return (t_min, alts_min)
```

### Piège 4 — Placer l'assertion après des opérations irréversibles (Q4)

L'assertion doit être la première instruction de `genere_kml`, avant l'ouverture du fichier. Si elle est placée au milieu, le fichier peut être partiellement créé avant que l'erreur soit détectée.

### Piège 5 — Inverser longitudes et latitudes dans l'appel (Q5)

La signature est `genere_kml(liste_longitudes, liste_latitudes)`. Appeler `genere_kml(latitudes, longitudes)` génère un fichier KML avec des coordonnées inversées — les points seront positionnés dans l'océan ou en dehors de la zone attendue.

### Piège 6 — Oublier l'ordre dans le fichier KML (Q6)

La balise `</kml>` doit être après `</Document>`. L'ordre est imposé par la norme XML/KML. Écrire `</kml>` avant `</Document>` génère un fichier invalide.

```
</Document>
</kml>      ← APRÈS </Document>, jamais avant
```

---

## PARTIE 7 — RAPPELS DE COURS

### Dépackage de retour multiple

```python
def ma_fonction():
    return 10, 20, 30, 40    # retourne un tuple

a, b, c, d = ma_fonction()  # dépackage en 4 variables
```

### Assertion

```python
assert condition               # lève AssertionError si condition est False
assert condition, "message"    # avec message d'erreur personnalisé
```

### La fonction `zip`

Permet de parcourir deux listes simultanément élément par élément.

```python
for a, b in zip(liste_a, liste_b):
    print(a, b)   # a et b sont les éléments de même indice
```

### La fonction `round`

```python
round(valeur, n)   # arrondit à n chiffres après la virgule
round(14.9999, 1)  # → 15.0
round(-56.500, 1)  # → -56.5
```

### La fonction `min`

```python
min(liste)   # retourne le plus petit élément
min([-56.5, -56.0, -48.0])  # → -56.5
```

### Fichier KML — structure valide

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>Nom du document</name>
  <Placemark>
    <name>Point 0</name>
    <Point>
      <coordinates>longitude,latitude</coordinates>
    </Point>
  </Placemark>
  <!-- ... autres Placemark ... -->
</Document>
</kml>
```

---

## PARTIE 8 — CHECKLIST AVANT DE RENDRE LE CODE

- [ ] Q1 : une seule ligne avec les 4 variables dans le bon ordre
- [ ] Q1 : le nom du fichier est `'releves_ballon_sonde.csv'` (avec guillemets)
- [ ] Q2 : `round(..., 1)` est présent dans la conversion
- [ ] Q2 : la ligne de test est écrite et affiche `[15.0, 0.5, -17.7, -56.5]`
- [ ] Q3 : la boucle parcourt toute la liste (pas de `return` à l'intérieur)
- [ ] Q3 : le résultat est un tuple `(t_min, [altitudes])`
- [ ] Q3 : retourne `(-56.5, [15120, 17210])` sur les vraies données
- [ ] Q4 : l'assertion est la première ligne de `genere_kml`
- [ ] Q4 : comparaison avec `==`, pas avec `is`
- [ ] Q5 : `genere_kml(longitudes, latitudes)` dans le bon ordre
- [ ] Q6 : `</kml>\n` est ajouté avant `fichier_kml.close()`
- [ ] Q6 : `</kml>` est après `</Document>` dans le fichier

---

## PARTIE 9 — GLOSSAIRE

**Kelvin (K)** : unité de température absolue. 0 K = zéro absolu ≈ -273,15 °C. Conversion : T°C = TK − 273,15.

**Dépackage** : récupération de plusieurs valeurs renvoyées par une fonction dans plusieurs variables distinctes. `a, b, c = f()`.

**Assertion** : instruction Python qui vérifie une condition et lève `AssertionError` si elle est fausse. Utilisée pour valider les préconditions d'une fonction.

**`AssertionError`** : exception levée quand une assertion échoue.

**`IndexError`** : exception levée quand on accède à un indice hors de la plage d'une liste.

**KML (Keyhole Markup Language)** : format XML standard pour représenter des données géographiques. Compatible avec Google Earth, QGIS, et de nombreuses applications de cartographie.

**Ballon sonde** : ballon météorologique gonflé à l'hélium, équipé de capteurs, lâché dans l'atmosphère pour mesurer température, pression, humidité, et géolocalisation à différentes altitudes.

**`zip(liste_a, liste_b)`** : fonction Python qui produit des paires d'éléments de même indice à partir de deux listes. Permet de les parcourir simultanément.

**`round(valeur, n)`** : fonction Python qui arrondit un flottant à n décimales.

**`min(liste)`** : fonction Python qui renvoie la plus petite valeur d'une liste.

**Erreur d'arrondi flottant** : phénomène où `288.15 - 273.15` donne `14.999999999999972` au lieu de `15.0`. Résolu par `round(..., 1)`.

---

*Document produit pour une utilisation pédagogique dans NotebookLM. Lycée Antoine Watteau — DarkSATHI Li*
