# aston-project-3

Le troisième projet de la promo CDNT21.

> Vous pouvez consulter le Wiki du projet [ici][1].

[1]: <https://github.com/Myrrhe/aston-project-3/wiki>

## Installation

### 1. Python3

Lancez la commande `python3 --version` OU `python --version` (la commande pour invoquer Python est en général **python3** sous Linux et **python** ou **py** sous Windows) pour vérifier si Python3 est installé. S'il n'est pas installé, téléchargez le [ici][2] pour pouvoir l'installer.

[2]: https://www.python.org/downloads/

### 2. pip

[pip][3] est le gestionnaire de package pour Python. Il sert donc à installer et mettre à jour toutes les bibliothèque pouvant être utilises par Python dans ce projet.

[3]: https://pypi.org/project/pip/

Dans un terminal, exécutez la commande :

`python -m ensurepip --upgrade`

### 3. venv

[venv][4] est un outil permettant de créer un environnement Python isolé.

[4]: https://docs.python.org/3/library/venv.html

L'idée est d'avoir un espace 'stérile', avec ses propres installations, bibliothèques et dépendances qui n'iront pas gêner les autres environnements virtuels (par exemple si 2 applications ont besoins d'avoir des versions différentes de la même bibliothèque).

- À la racine du projet, dans une console *PowerShell*, lancez :

`python -m venv venv`

Ici, *venv* est le nom de l'environnement virtuel créé.

- Lancez l'environnement virtual avec :

`.\venv\Scripts\Activate.ps1`

Le terminal devrait à présent avoir sa ligne d'entrée préfixée par **(venv)**

- Vérifiez la version de Python avec : `python3 --version`

- Vérifiez la création de pip avec : `pip list`

Il y a un fichier 'requirements.txt' dans le projet. Ce fichier contient toute les dépendances nécessaires au fonctionnement du projet.

- Pour installer ces dépendances, lancez :

`pip install -r requirements.txt`

### 4. Lancement du projet

Pour lancer le projet, exécutez simplement :

`python manage.py runserver`
