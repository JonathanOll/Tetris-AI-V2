# Tetris_AI
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

[Deuxième version](https://github.com/JonathanOll/Tetris_AI/) d'un programme d'intelligence artificielle pour le jeu du Tetris

## Fonctionnement

Une intelligence artificielle capable de jouer au Tetris toute seule, fonctionnant sur la base des algorithmes génétiques, l'IA utilise des indicateurs comme la différence de hauteur entre chaque colonne ou encore le nombre de trous présents dans le jeu pour juger de si un état du jeu est plus ou moins bon, en essayant toutes les actions possibles, l'IA selectionne celle qui maximise ses chances de réaliser une bonne partie. 

À la première génération, les IA sont plutôt mauvaise, mais l'algorithme génétique leur permet d'optimiser leurs paramètres, et de sélectionner les meilleurs individus à chaque génération pour se reproduire.

## Performances

![image](https://user-images.githubusercontent.com/70845195/177747996-590c1c2f-5bb2-4426-9e77-a75c64c8cf8b.png)

## Installation

- Installer une version de [python](https://www.python.org/) supérieure ou égale à 3.7
- Installer pygame (éxécuter la commande `pip install pygame`)
- Télécharger le code et lancer le fichier main.py

