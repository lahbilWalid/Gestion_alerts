from Alert_App import AlertManager
import time
from flask import Flask, request
from pygame import mixer
import os

manager = AlertManager()
app = Flask(__name__)
mixer.init()

@app.route("/play", methods=["POST"])
def play_sound():
    data = request.json
    nom = data.get("nom")
    if nom:
        manager.declencher_alerte(nom)
        print("je joue depuis test_sound")
        time.sleep(0.1)
    else:
        print("son introuvable")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)