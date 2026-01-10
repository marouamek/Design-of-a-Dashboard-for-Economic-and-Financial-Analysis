# Projet PRAVAN : Construire un tableau de bord Web pour l’analyse économique et financière.

## Cadre du projet
Ce projet s'inscrit dans le cadre d'une analyse approfondie des données de l'Indice des Prix à la Consommation (IPC) pour la période 2015-2024 à Alger. Il vise à fournir une visualisation interactive et des outils d'exportation pour explorer les variations de l'IPC par groupe et sous-groupe, ainsi que les tendances générales.

## Module concerné
Le projet est développé dans le cadre du module **Programmation Avancée**.

Qui permet de se familiariser avec les nouvelles technologies du Web, notamment le langage Python, le Web multimédia et les Services web.


## Noms des étudiants
- **Étudiant 1** : BOUGHERARA Sarah | 222231520408
- **Étudiant 2** : GHERBI Redha     | 212131056673
- **Étudiant 3** : IZRARENE Sabrina | 222231520520
- **Étudiant 4** : MEKIMENE Maroua  | 222231377003

## Concepts clés utilisés
- **Backend avec Flask** :
  - Création d'API REST pour récupérer les données de la base de données MySQL.
  - Génération de fichiers CSV et Excel pour l'exportation des données.
- **Frontend avec JavaScript** :
  - Utilisation de Chart.js pour afficher des graphiques interactifs (barres, lignes, camemberts, donuts).
  - Gestion des événements utilisateur (boutons toggle, sliders, filtres dynamiques).
- **Utilisation de Jinja** :
  - Intégration de Jinja pour générer dynamiquement les templates HTML.
  - Réutilisation des composants (comme l'aside) pour éviter la duplication de code et garantir une structure cohérente.
- **Base de données relationnelle** :
  - Modélisation des données avec des tables dimensionnelles (`Dim_Annee`, `Dim_Groupe`, `Dim_Sous_Groupe`) et une table de faits (`Fact_IPC`).
  - Requêtes SQL pour calculer les variations, les contributions et les tendances.
- **Visualisation des données** :
  - Affichage des données sous forme de graphiques interactifs pour une meilleure compréhension des tendances.
- **Exportation des données** :
  - Génération de fichiers CSV et Excel pour permettre une analyse hors ligne.

## Questions d’analyse posées
- **Vue d’Ensemble Synthétique**
1. Quelle est l’année la plus inflationniste à Alger entre 2015 et 2024 ?
2. Quel a été le groupe qui a contribué le plus à la hausse de l’IPC en 2024 ?
3. Existe-t-il une anomalie de prix spécifique sur un produit précis du panier ?
4. Quelle a été la variation annuelle de l’IPC à Alger en 2024 par rapport à 2023 ?
- **Analyse Approfondie**
5. Comment l’IPC a-t-il évolué à Alger de 2015 à 2024 ?
6. Le rythme de l’inflation est-il en train de s’accélérer ou de ralentir ?
7. Quelles ont été les variations de prix d’un mois à l’autre au cours de l’année 2024 ?
8. Comment chaque groupe contribue-t-il à l’évolution de l’IPC depuis 2015 ?
- **Analyse Granulaire** (ex : Le groupe Alimentation)
9. Quels sont les trois sous-groupes alimentaires ayant enregistré les taux d'inflation les plus critiques en 2024 ?
10. Comment le groupe alimentation a-t-il contribué à la hausse de l’IPS en 2024 par rapport aux autres groupes ?
11. Pour un sous-groupe donné (ex: céréales), la hausse des prix est-elle une accélération soudaine ou une tendance stable sur l'année ?

## Ce que nous avons appris à travers ce projet
Nous avons compris que les données brutes ne suffisent pas pour réaliser une analyse pertinente. Pour leur donner un sens, il faut les nettoyer, les structurer et les mettre en contexte. 

Ce projet nous a permis de mettre en pratique le processus ETL (Extract, Transform, Load) :

- **Extract (Extraction)** : Récupération des données hétérogènes issues des rapports de l'ONS.

- **Transform (Transformation)** : Nettoyage des données, calcul des variations annuelles et mensuelles, et normalisation des formats.

- **Load (Chargement)** : Structuration et stockage dans un schéma en étoile (tables de faits et dimensions) pour optimiser les performances des requêtes.


### Compétences techniques
- **Développement backend** :
  - Création d'API REST avec Flask pour interagir avec une base de données.
  - Gestion des connexions à une base de données MySQL et optimisation des requêtes SQL.
- **Développement frontend** :
  - Intégration de bibliothèques de visualisation comme Chart.js.
  - Gestion des événements utilisateur et mise à jour dynamique des éléments HTML.
- **Analyse des données** :
  - Modélisation des données pour répondre à des questions analytiques spécifiques.
  - Calcul des variations et des contributions à partir de données brutes.


### Compétences transversales
Au-delà de la maîtrise technique, ce projet nous a permis de :

1. Interpréter des indicateurs macroéconomiques complexes (IPC, glissement annuel, pondérations).

2. Traduire des concepts économiques réels en modèles de données techniques (passage du document à une base de données relationnelle).

3. Apprendre la scénarisation des données : choisir le bon graphique (courbe de tendance vs diagramme en secteurs) pour rendre l'information immédiatement actionnable par un décideur.

4. Développement d'un esprit critique face aux chiffres : identification des anomalies, détection des saisonnalités et compréhension des causes de l'inflation.

5. Expérience du travail collaboratif en équipe pluridisciplinaire.


---
Ce projet a permis de combiner des compétences techniques et analytiques pour répondre à des problématiques concrètes liées à l'analyse des données économiques.