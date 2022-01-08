[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
![forthebadge](https://img.shields.io/badge/Framework-DRF-green)

# P10_Konrath_Kevin
Créez une API sécurisée RESTful en utilisant Django REST

## 1. Récupérer le projet :


    $ git clone https://github.com/Ikeaven/P10_Konrath_Kevin

Se déplacer dans le repertoire du projet :

    $ cd P10_Konrath_Kevin

## 2. Créer et activer un environnement virtuel :

    $ python3 -m venv env


Sous macOS ou Linux :

    $ . env/bin/activate

Sous Windows :

    $ env\Scripts\activate.bat

## 3. Installer les dépendances :

    $ pip install -r requirements.txt

## 4. Créer un super user :

    $ cd SoftDesk_API/
    $ ./manage.py createsuperuser

Suivre les indications de la console.
Une fois le super user créé, vous pouvez vous connecter à l'espace d'admin du site grâce à son identifiant et mot de passe. Mais avant il faut encore démarrer le serveur de developpement.

## 5. Démarrer le serveur de developpement :

On est toujours dans le dossier du projet SoftDesk_API.

    $  ./manage.py runserver

L'API sera accéssible à l'adresse local : 127.0.0.1:8000 sur le port 8000 par défaut.
Si le port n'est pas disponible :

    $ ./manage.py runserver <your_port>

## 6. Naviguer vers l'éspace d'administration

Ouvrir un navigateur, et aller à l'adresse du site en ajouter /admin/.
ex : http://127.0.0.1:8000/admin/

Vous retrouverez la documentation de l'API à l'adresse suivante :
https://documenter.getpostman.com/view/11117999/UVRBn6ni
