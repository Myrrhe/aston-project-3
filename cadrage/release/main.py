# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:12:19 2023

@author: baudi
"""

import queue
import subprocess
import sys
import threading
from typing import IO

# Ce programme envoi des nombre à deux autres programmes : A et B
# A et B renvoient une réponse différente selon les nombres envoyés
# Cette réponse correspond au comportement des programmes, et les nombres à
# l'état en cours. On put ettendre ce comportement pour fairs'affronter A et B
# sur un jeu comme le morpion, les dames, ou autre chose.

# Si un programme met trop de temps à renvoyer une réponse, on peut décider
# que cela le fait perdre automatiquement

# Pour exécuter ce programme, lancez 'python main.py' en ligne de commande


# Fonction pour lire la sortie du sous-programme de manière asynchrone
def read_output(output: IO[str], output_queue: queue) -> None:
    """Read the output"""
    for line in iter(output.readline, ""):
        output_queue.put(line)
    output.close()


def main() -> int:
    """The main method"""
    print("Programme principal lancé\n")

    count = 0

    # Créez une file pour stocker la sortie du sous-programme
    output_queue_a = queue.Queue()
    output_queue_b = queue.Queue()

    # Lancez les sous-programmes en tant que processus enfants
    process_a = subprocess.Popen(
        ["python", "a.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    process_b = subprocess.Popen(
        ["python", "b.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )

    # Créez des threads pour lire la sortie des sous-programmes de manière asynchrone
    output_thread_a = threading.Thread(
        target=read_output, args=(process_a.stdout, output_queue_a)
    )
    output_thread_a.daemon = True
    output_thread_a.start()

    output_thread_b = threading.Thread(
        target=read_output, args=(process_b.stdout, output_queue_b)
    )
    output_thread_b.daemon = True
    output_thread_b.start()

    res = ""

    try:
        while res != "RIGHT-DOWN-":
            count += 1

            res = ""

            inp = "0" if count < 3 else "1"

            # Envoyez des données au sous-programmes via l'entrée standard
            # On peut envoyer des mots séparés par des expaces, ou un mot unique
            process_a.stdin.write("0\n")
            process_a.stdin.flush()
            process_a.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            process_a.stdin.flush()
            process_a.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            process_a.stdin.flush()

            # Attendez une réponse du sous-programme avec un timeout
            try:
                # Définissez le timeout en secondes
                response = output_queue_a.get(timeout=10)
                print("Réponse du sous-programme A :", response)
                res += response
            except queue.Empty:
                print(
                    "Timeout : Le sous-programme A n'a pas répondu dans le délai spécifié."
                )

            process_b.stdin.write("1\n")
            process_b.stdin.flush()
            process_b.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            process_b.stdin.flush()
            process_b.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            process_b.stdin.flush()

            # Attendez une réponse du sous-programme avec un timeout
            try:
                # Définissez le timeout en secondes
                response = output_queue_b.get(timeout=10)
                print("Réponse du sous-programme B :", response)
                res += response
            except queue.Empty:
                print(
                    "Timeout : Le sous-programme B n'a pas répondu dans le délai spécifié."
                )

            res = res.replace("\n", "-")
            print(f"Réponse globale = {res}\n")
    except KeyboardInterrupt:
        pass

    process_a.stdin.close()
    process_a.wait()
    process_b.stdin.close()
    process_b.wait()
    print("Programme principal terminé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
