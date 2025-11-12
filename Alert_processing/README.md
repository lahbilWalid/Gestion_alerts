## Comment déclencher une alerte depuis un autre programme ?
Par exemple, pour l’intégrer dans le module de path-planning :

 1 - Ouvrir le fichier print_map.py.

 2 - Importer les modules Alert_App et time.

 3 - Instancier la classe AlertManager.

 4 - Appeler la méthode declencher_alerte().
````python
from Alert_App import AlertManager

import time

manager = AlertManager()

#Exemple pour déclencher l'alerte "Obstacle détecté" :
manager.declencher_alerte("Obstacle détecté")

# Un délai est nécessaire ici pour éviter que le fichier ne se ferme immédiatement.
# Si le script Python s'exécute pendant toute la durée de l'alerte sonore,
# il n'est pas nécessaire d'ajouter un time.sleep.
time.sleep(2)

````
