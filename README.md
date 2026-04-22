# Prédicteur de score exact de football

Petit script Python pour prédire un score exact de football à partir des 5 derniers résultats.

## Description

Le projet propose deux façons d'utiliser le prédicteur :
- en ligne de commande
- via une interface graphique simple (Tkinter)

Le script utilise :
- la détection d'un score répété
- une moyenne pondérée des buts pour donner plus de poids aux derniers matchs

## Prérequis

- Python 3.8+

## Installation

Aucune dépendance externe n'est requise : Tkinter est inclus dans la majorité des distributions Python.

## Utilisation

### Interface graphique

```bash
python predict_score.py --gui
```

### En ligne de commande

```bash
python predict_score.py 1-0 2-1 1-1 2-0 1-2
```

### Exemple de données fictives

```bash
python predict_score.py --example
```

## Résultat

Le script affiche ou affiche dans l'interface graphique la prédiction du score exact basée sur les 5 derniers résultats.

## Structure du dépôt

- `predict_score.py` : script principal avec interface CLI et GUI
- `README.md` : documentation
- `.gitignore` : fichiers à ignorer pour Git
