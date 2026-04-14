#############################################################################
# Jeux de données fournis                                                   #
#############################################################################
from plantes import plantes
from mesures import mesures

#############################################################################
# Écrire le code de la fonction croissance_moyenne de la question 1         #
#############################################################################
def croissance_moyenne(plantes):
    if not plantes: #plantes == [] ou len(plantes) == 0
        return None
    croissance_somme = 0
    for plante in plantes:
        croissance_somme += plante.croissance
    return croissance_somme/len(plantes)

def test_croissance_moyenne():
    assert croissance_moyenne([]) == None
    assert croissance_moyenne(plantes) == 79.0

#############################################################################
# Écrire le code de la fonction dictionnaire_mesure de la question 2      #
#############################################################################
def dictionnaire_mesure(plantes, mesures):
    dictionnaire_mesures = {}
    for plante in plantes:
        dictionnaire_mesures[plante.nom] = []
    for mesure in mesures:
        if mesure['plante'] in dictionnaire_mesures:
            dictionnaire_mesures[mesure['plante']].append(mesure)
    return dictionnaire_mesures

mesures_test= [
    {'jour': 1, 'plante': 'Basilic', 'hauteur': 0.85, 'temperature': 29.3, 'humidite': 50.89} ,
    {'jour': 1, 'plante': 'Tomate', 'hauteur': 1.27, 'temperature': 21.51, 'humidite': 47.19} ,
    {'jour': 1, 'plante': 'Menthe', 'hauteur': 0.67, 'temperature': 27.75, 'humidite': 61.14} ,
    {'jour': 1, 'plante': 'Tournesol', 'hauteur': 2.29, 'temperature': 18.42, 'humidite': 49.3} ,
    {'jour': 2, 'plante': 'Basilic', 'hauteur': 1.7, 'temperature': 17.44, 'humidite': 78.99} ,
    {'jour': 2, 'plante': 'Tomate', 'hauteur': 2.4, 'temperature': 18.98, 'humidite': 41.78} ,
    {'jour': 2, 'plante': 'Menthe', 'hauteur': 1.25, 'temperature': 15.15, 'humidite': 67.99} ,
    {'jour': 2, 'plante': 'Tournesol', 'hauteur': 4.44, 'temperature': 23.82, 'humidite': 77.61} ,
    {'jour': 3, 'plante': 'Basilic', 'hauteur': 2.49, 'temperature': 20.03, 'humidite': 66.27} ,
    {'jour': 3, 'plante': 'Tomate', 'hauteur': 3.68, 'temperature': 22.42, 'humidite': 54.39} ,
    {'jour': 3, 'plante': 'Menthe', 'hauteur': 1.84, 'temperature': 25.24, 'humidite': 57.66}]

def test_dictionnaire_mesure():
    dictionnaire = dictionnaire_mesure(plantes, mesures_test)
    assert 'Basilic' in dictionnaire
    assert 'Tomate' in dictionnaire.keys()
    assert 'Menthe' in dictionnaire
    assert 'Tournesol' in dictionnaire
    assert 'Fougère' in dictionnaire
    assert len(dictionnaire['Basilic']) == 3
    assert dictionnaire['Fougère'] == []
#############################################################################
# Fonction défaillante à analyser et corriger pour les questions 3 et 4     #
#############################################################################

def purger_mesures_extremes(liste_mesures):
    """
    Supprime de la liste toutes les mesures dont la température 
    n'est pas comprise entre 20 et 25°C inclus.
    """
    #     for mesure in liste_mesures[:]:
    #         if mesure['temperature'] < 20 or mesure['temperature'] > 25:
    #             liste_mesures.remove(mesure)
    #     return liste_mesures
    
    #     valide = [mesure for mesure in liste_mesures if 20 <= mesure['temperature'] <= 25]
    #     liste_mesures.clear()
    #     liste_mesures.extend(valide)
    
    for i in range(len(liste_mesures)-1, -1, -1):
        if liste_mesures[i]['temperature'] < 20 or liste_mesures[i]['temperature'] > 25:
                 liste_mesures.remove(liste_mesures[i])
    return liste_mesures


    
def test_purger():
    mesures_test = [
         {'jour': 1, 'plante': 'Basilic', 'temperature': 18.0},
         {'jour': 2, 'plante': 'Basilic', 'temperature': 19.0},
         {'jour': 3, 'plante': 'Basilic', 'temperature': 22.0},
         {'jour': 4, 'plante': 'Basilic', 'temperature': 28.0},
         {'jour': 5, 'plante': 'Basilic', 'temperature': 29.0}
    ]

    purger_mesures_extremes(mesures_test)

    print("Résultat après la purge :")
    for m in mesures_test:
        print(f"Jour {m['jour']} : {m['temperature']}°C")

test_purger()