# 🎓 NSI Terminale — Fiches BAC 2026

[![NSI](https://img.shields.io/badge/Discipline-NSI-blue.svg)](https://eduscol.education.fr/1715/numerique-et-sciences-informatiques-bac-general)
[![Session](https://img.shields.io/badge/Session-2026-orange.svg)](#)
[![Status](https://img.shields.io/badge/Statut-En_cours-green.svg)](#)

Cette application web est un **hub de révision centralisé** conçu pour accompagner les élèves de Terminale dans la préparation de l'épreuve pratique de **Numérique et Sciences Informatiques (NSI)**.

Elle regroupe les **23 sujets officiels** de la banque nationale avec un suivi de progression en temps réel.

---

## 🚀 Fonctionnalités

* **Tableau de bord interactif** : Visualisation claire des 23 sujets de l'épreuve pratique.
* **Suivi de progression** : Une barre de progression dynamique calcule automatiquement le pourcentage de fiches complétées.
* **Système de filtrage** : Filtrez les sujets par statut (`À créer`, `Fiche prête`) pour mieux organiser vos révisions.
* **Design Responsive** : Interface optimisée pour ordinateur et tablette (basée sur Bootstrap 5.3).
* **Typographie Soignée** : Utilisation de polices spécifiques (`Rubik Dirt` pour le titre, `JetBrains Mono` pour l'aspect technique) pour un confort de lecture optimal.

---

## 📂 Structure du Projet

L'architecture est pensée pour être simple et évolutive :

```bash
.
├── index.html          # Page d'accueil (le dashboard)
├── sujet_01/           # Dossier par sujet (ex: Traitement d'images)
│   └── fiche_rle.html  # Fiche de révision détaillée
├── sujet_02/
│   └── ...
└── assets/             # (Optionnel) Images et ressources communes
```

---

## 🛠️ Stack Technique

* **HTML5 / CSS3** : Structure et mise en forme (Variables CSS pour le thème).
* **Bootstrap 5.3** : Système de grille et composants.
* **JavaScript (Vanilla)** : Logique de filtrage, animation d'entrée (staggered) et calcul de la progression.
* **Google Fonts** : Intégration de polices web modernes.

---

## 📝 Comment utiliser ou contribuer ?

### Pour un élève :
1.  Ouvrez `index.html` dans votre navigateur.
2.  Consultez les cartes marquées **"✓ Fiche prête"**.
3.  Utilisez les filtres pour voir ce qu'il vous reste à bosser.

### Pour ajouter une fiche (Mode Édition) :
1.  Créez un nouveau dossier pour le sujet correspondant (ex: `sujet_02/`).
2.  Dans `index.html`, repérez la carte du sujet.
3.  Modifiez l'attribut `data-status="todo"` en `data-status="done"`.
4.  Remplacez `href="#"` par le lien vers votre nouvelle page HTML.
5.  Actualisez : la barre de progression se mettra à jour automatiquement !

---

## ⚖️ Licence

Contenu pédagogique destiné à la préparation du Baccalauréat NSI 2026. Les sujets sont issus de la **Banque Nationale des Sujets**.

---

**Développé avec passion par DarkSATHI Li** *Maintenez le code propre, et que le `return` soit avec vous !*
