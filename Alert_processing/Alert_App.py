import os
import json
import time
import random
import tkinter as tk
from tkinter import ttk
from pygame import mixer
from queue import PriorityQueue
import logging

# Charger la configuration
with open("Alerts_config.json", "r", encoding="utf-8") as Al:
    Alerts = json.load(Al)

Alert_priority = Alerts["ALERTS"]
Alert_icon = Alerts["ICONS"]
Alert_son = Alerts["SONS"]
Alert_sensor = Alerts["SENSORS"]

# Configurer le logging
logging.basicConfig(filename="alerts.log", level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s", encoding="utf-8")

# Classe Alerte (données)
class Alerte:
    def __init__(self, nom, priority, horodatage, icon, son):
        self.nom = nom
        self.priority = priority
        self.horodatage = horodatage
        self.icon = icon
        self.son = son

    def __lt__(self, other):
        return self.priority < other.priority

# Classe AlertManager (logique métier)
class AlertManager:
    def __init__(self):
        mixer.init()
        self.alertQueue = PriorityQueue()
        self.current_alert = None
        self.current_channel = None

    def declencher_alerte(self, nom):
        if nom not in Alert_priority:
            print(f"[!] Alerte inconnue : {nom}")
            return

        priority = Alert_priority[nom]
        horodatage = time.strftime("%Y-%m-%d %H:%M:%S")
        icon = Alert_icon[nom]
        son = Alert_son[nom]

        alerte = Alerte(nom, priority, horodatage, icon, son)
        self.alertQueue.put(alerte)
        self._traiter_alert()

    def _traiter_alert(self):
        if not self.alertQueue.empty():
            new_alerte = self.alertQueue.get()
            print(f"[ALERTE] {new_alerte.nom} (Priorité {new_alerte.priority})")

            chemin = os.path.join("waves", new_alerte.son)
            notif_path = os.path.join("waves", "notif.wav")
            sound = mixer.Sound(chemin)

            self._journaliser(new_alerte)

            if self.current_alert:
                if new_alerte.priority < self.current_alert.priority:
                    if self.current_channel and self.current_channel.get_busy():
                        self.current_channel.stop()
                        print(f"{self.current_alert.nom} est interrompue (moins prioritaire)")
                        print("///")
                elif new_alerte.priority >= self.current_alert.priority:
                    if self.current_channel and self.current_channel.get_busy():
                        notif_sound = mixer.Sound(notif_path)
                        channel = mixer.find_channel()
                        if channel:
                            channel.play(notif_sound)
                            print(f"{self.current_alert.nom} continue de jouer (plus prioritaire ou avec la même priorité)")
                            print("///")
                        return

            self.current_alert = new_alerte
            self.current_channel = mixer.find_channel()
            if self.current_channel:
                self.current_channel.play(sound)

    def _journaliser(self, alerte):
        if alerte.priority == 1:
            logging.critical(f"Alerte : {alerte.nom} | Priorité : {alerte.priority} | Icon : {alerte.icon} | Son : {alerte.son}")
        elif alerte.priority == 2:
            logging.warning(f"Alerte : {alerte.nom} | Priorité : {alerte.priority} | Icon : {alerte.icon} | Son : {alerte.son}")
        else:
            logging.info(f"Alerte : {alerte.nom} | Priorité : {alerte.priority} | Icon : {alerte.icon} | Son : {alerte.son}")

# Classe AlertApp (UI)
class AlertApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("Simulation des alertes du smart car Ecockpit")

        # Interface graphique
        self.tree = ttk.Treeview(root, columns=("Horodatage","Alert", "Priorité", "Icône", "Son"), show="headings")
        for col in ["Horodatage", "Alert", "Priorité", "Icône", "Son"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.all_alerts = []

        # Filtrage
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Filtrer par alerte :").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var)
        self.filter_combo['values'] = ['Tous'] + list(Alert_priority.keys())
        self.filter_combo.current(0)
        self.filter_combo.pack(side=tk.LEFT)
        self.filter_combo.bind('<<ComboboxSelected>>', self.filtrer_alertes)

        # Couleurs par priorité
        self.tree.tag_configure("priorite1", background="#ffcccc")
        self.tree.tag_configure("priorite2", background="#ffe5b4")
        self.tree.tag_configure("priorite3", background="#ccffcc")

        # Bouton pour générer une alerte
        tk.Button(root, text="Générer une alerte aléatoire", command=self.genererAlert).pack(pady=10)

        # Capteurs
        sensor_frame = tk.Frame(root)
        sensor_frame.pack(pady=10)
        for sensor, alert_name in Alert_sensor.items():
            btn = tk.Button(sensor_frame, text=sensor, command=lambda a=alert_name: self.genererAlert(a))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def genererAlert(self, alert=None):
        nom = alert if alert else random.choice(list(Alert_priority.keys()))
        priority = Alert_priority[nom]
        horodatage = time.strftime("%Y-%m-%d %H:%M:%S")
        icon = Alert_icon[nom]
        son = Alert_son[nom]

        alerte = Alerte(nom, priority, horodatage, icon, son)
        self.all_alerts.append(alerte)
        self.tree.insert("", "end", values=(alerte.horodatage, alerte.nom, alerte.priority, alerte.icon, alerte.son), tags=(f"priorite{alerte.priority}",))

        # Déclencher via AlertManager
        self.manager.declencher_alerte(nom)

    def filtrer_alertes(self, event=None):
        filtre = self.filter_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for alerte in self.all_alerts:
            if filtre == 'Tous' or filtre == alerte.nom:
                self.tree.insert("", "end", values=(alerte.horodatage, alerte.nom, alerte.priority, alerte.icon, alerte.son), tags=(f"priorite{alerte.priority}",))

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    manager = AlertManager()
    app = AlertApp(root, manager)
    root.mainloop()