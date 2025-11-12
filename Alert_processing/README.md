## Comment utiliser ou déclecher une alerte dans un autre programme ?
Par exemple pour l'integrer dans le path-planning

1 - Ouvrer le fichier print_map.py

2 - Importer Alert_App  

3- Créer une instance de la classe AlertManager 

4 - Appeler la fonction declencher_alerte 
````python
from Alert_App import AlertManager

manager = AlertManager()

#Exemple pour déclencher l'alerte "Obstacle détecté" :
manager.declencher_alerte("Obstacle détecté")
````
