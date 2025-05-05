# IHM Contrôle mission temps réel

## Description générale
Cette IHM permet d'afficher sur une interface graphique en temps réel les mesures télémétriques reçues par la Kikiwi.
De manière chronologique :
* Réception des télémesures du port série externe (Arduino->Kikiwi)
* Réception des télémétrie via le Kikiwi Soft (Kikiwi->Kikiwi Soft)
* Écriture des données du port série dans un fichier .dat dès leur réception (Kikiwi Soft->Fichier .dat)
* Lecture en temps réel du fichier .dat trames par trames par un script python (Fichier .dat->Python)
* Envoie des trames complètes via un port série virtuel null-modem com0com (Python->com0com)
* Réception des trames sur l'IHM MATLAB APP (com0com->MATLAB)
  
## Prérequis
Le script Python nécéssite les bibliothèques : 

```
import re
import time
import os
import serial
```
La création du port série virtuel null-modem peut utiliser [com0com](https://com0com.sourceforge.net/)

L'IHM utilise MATLAB APP

## Précisions sur le script Python
Les trames suivent le format suivant : 
```
00h00m32s,96.17,8.67,0,0,786.11,23.81,2090.36,10165.12,-9.83,-1.57,0.08,-53.20,15.65,-0.12,-0.00,0.03,-0.07,36.54,96.25,8.36,0,0,833.12,22.81,1620.93,96.24,8.49,0,0,833.53,24.21,1616.91;
00h01m02s,96.18,8.68,26342,0,1001.90,7.60,94.94,9695.22,-9.81,-1.58,0.04,-53.05,14.40,2.94,-0.00,0.01,-0.06,25.57,96.26,8.29,27844,0,1001.23,8.01,100.54,96.23,8.48,28099,0,1001.53,8.44,98.08;
00h01m32s,96.18,8.65,26739,0,1001.90,7.58,94.91,11672.03,-9.81,-1.60,0.06,-52.95,15.81,2.51,-0.00,0.02,-0.06,25.75,96.25,8.33,28744,0,1001.24,7.99,100.51,96.22,8.46,29005,0,1001.52,8.47,98.13;
...
```
Le débit de données de la Kikiwi étant imposés (1 émissions toutes les 3 secondes), et au vu de la longeur des trames, il est nécessaire d'attendre 3 à 4 émissions pour réceptionner une trame complète.
Le script python détecte les délimiteurs afin de reconstruire une trame complète, et supprimeles valeurs aberrantes qui pourraient être dûe à une perte de donnée et/ ou de trames en cours de route.

## Protocole de mise en route
Respectez l'ordre suivant pour la mise en place de la chaîne de liaison :
* Lancer le [Kikiwi Soft](https://kikiwi.fr/), établir la connection avec la Kikiwi
* Lancer l'enregistrement des mesures avec sauvegarde des données du port série externe sur un fichier externe
* Trouver l'emplacement du fichier .dat contenant les logs (généralement dans le dossier de Kikiwi)
* Initialiser les ports COM null-modem
* Remplacer le chemin absolu du .dat dans le script Python, ainsi que le nom du port COM d'entrée
* Lancer le script Python
* Remplacer le nom du port COM de sortie dans le code .mlapp
* Exécuter le code .mlapp

## Polyvalence à d'autres jeux de capteurs
Si ce code est utilisé pour d'autres jeux de capteurs (nombres différents d'entrés), il suffit de suivre ce même protocole en modifiant les éléments lu par MATLAB et en associant chaque éléments des trames reçues au bon cadran/jauge.

## Note de l'éditeur
Le Kikiwi Soft propose "en théorie" une redirection via un port COM des données séries externes, mais est (très) difficile à mettre en place en réalité. Cette alternative, très alambiqués et très peu optimisée, est une alternative complexe mais viable.
