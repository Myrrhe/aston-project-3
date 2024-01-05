# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:12:19 2023

@author: baudi
"""

import queue
import subprocess
import threading
from typing import IO
from random import randint

# Ce programme envoi des nombre à deux autres programmes : A et B
# A et B renvoient une réponse différente selon les nombres envoyés
# Cette réponse correspond au comportement des programmes, et les nombres à
# l'état en cours. On peut étendre ce comportement pour faire s'affronter A et B
# sur un jeu comme le morpion, les dames, ou autre chose.

# Si un programme met trop de temps à renvoyer une réponse, on peut décider
# que cela le fait perdre automatiquement

# Pour exécuter ce programme, lancez 'python main.py' en ligne de commande

FIELD_WIDTH = 30
FIELD_HEIGHT = 20


# Fonction pour lire la sortie du sous-programme de manière asynchrone
def read_output(output: IO[str], output_queue: queue) -> None:
    """Read the output"""
    for line in iter(output.readline, ""):
        output_queue.put(line)
    output.close()


def main_fight(id1: str, id2: str) -> str:
    """The main method"""

    # Créez une file pour stocker la sortie du sous-programme
    output_queue_a = queue.Queue()
    output_queue_b = queue.Queue()

    # Lancez les sous-programmes en tant que processus enfants
    process_a = subprocess.Popen(
        ["python", f"storage/bot/{id1}.py"],
        # ["python", "../cadrage/release/a.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    process_b = subprocess.Popen(
        ["python", f"storage/bot/{id2}.py"],
        # ["python", "../cadrage/release/b.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
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

    field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]

    pos = {"init": [{
        "x": randint(0, FIELD_WIDTH - 1),
        "y": randint(0, FIELD_HEIGHT // 2 - 1),
    }]}
    pos["init"].append({
        "x": FIELD_WIDTH - 1 - pos["init"][0]["x"],
        "y": FIELD_HEIGHT - 1 - pos["init"][0]["y"],
    })
    pos["current"] = pos["init"].copy()
    pos["next"] = pos["current"].copy()
    field[pos["init"][0]["y"]][pos["init"][0]["x"]] = 1
    field[pos["init"][1]["y"]][pos["init"][1]["x"]] = 2

    res = [
        [f"{pos["init"][0]["x"]},{pos["init"][0]["y"]}"],
        [f"{pos["init"][1]["x"]},{pos["init"][1]["y"]}"],
    ]

    health = [1, 1]

    try:
        # Game loop
        while health[0] > 0 and health[1] > 0:
            # Envoyez des données au sous-programmes via l'entrée standard
            # On peut envoyer des mots séparés par des expaces, ou un mot unique
            process_a.stdin.write("0\n")
            process_a.stdin.flush()
            process_a.stdin.write(
                f"{pos["init"][0]["x"]} {pos["init"][0]["y"]} {pos["current"][0]["x"]} {pos["current"][0]["y"]}\n"
            )
            process_a.stdin.flush()
            process_a.stdin.write(
                f"{pos["init"][1]["x"]} {pos["init"][1]["y"]} {pos["current"][1]["x"]} {pos["current"][1]["y"]}\n"
            )
            process_a.stdin.flush()

            pos["next"] = pos["current"].copy()

            # Attendez une réponse du sous-programme avec un timeout
            try:
                # Définissez le timeout en secondes
                response = output_queue_a.get(timeout=10)
                match response:
                    case "LEFT\n":
                        pos["next"][0]["x"] -= 1
                    case "RIGHT\n":
                        pos["next"][0]["x"] += 1
                    case "UP\n":
                        pos["next"][0]["y"] -= 1
                    case "DOWN\n":
                        pos["next"][0]["y"] += 1
                    case _:
                        print("Error: Invalid response for A")
                        health[0] = 0
                if (
                    pos["next"][0]["x"] < 0
                    or pos["next"][0]["x"] >= FIELD_WIDTH
                    or pos["next"][0]["y"] < 0
                    or pos["next"][0]["y"] >= FIELD_HEIGHT
                    or field[pos["next"][0]["y"]][pos["next"][0]["x"]] != 0
                ):
                    health[0] = 0
                else:
                    pos["current"][0] = pos["next"][0].copy()
                    field[pos["current"][0]["y"]][pos["current"][0]["x"]] = 1
                    res[0].append(f"{pos["current"][0]["x"]},{pos["current"][0]["y"]}")
            except queue.Empty:
                print(
                    "Timeout : Le sous-programme A n'a pas répondu dans le délai spécifié."
                )

            process_b.stdin.write("1\n")
            process_b.stdin.flush()
            process_b.stdin.write(
                f"{pos["init"][0]["x"]} {pos["init"][0]["y"]} {pos["current"][0]["x"]} {pos["current"][0]["y"]}\n"
            )
            process_b.stdin.flush()
            process_b.stdin.write(
                f"{pos["init"][1]["x"]} {pos["init"][1]["y"]} {pos["current"][1]["x"]} {pos["current"][1]["y"]}\n"
            )
            process_b.stdin.flush()

            # Attendez une réponse du sous-programme avec un timeout
            try:
                # Définissez le timeout en secondes
                response = output_queue_b.get(timeout=10)
                match response:
                    case "LEFT\n":
                        pos["next"][1]["x"] -= 1
                    case "RIGHT\n":
                        pos["next"][1]["x"] += 1
                    case "UP\n":
                        pos["next"][1]["y"] -= 1
                    case "DOWN\n":
                        pos["next"][1]["y"] += 1
                    case _:
                        print("Error: Invalid response for B")
                        health[1] = 0
                if (
                    pos["next"][1]["x"] < 0
                    or pos["next"][1]["x"] >= FIELD_WIDTH
                    or pos["next"][1]["y"] < 0
                    or pos["next"][1]["y"] >= FIELD_HEIGHT
                    or field[pos["next"][1]["y"]][pos["next"][1]["x"]] != 0
                ):
                    health[1] = 0
                else:
                    pos["current"][1] = pos["next"][1].copy()
                    field[pos["current"][1]["y"]][pos["current"][1]["x"]] = 2
                    res[1].append(f"{pos["current"][1]["x"]},{pos["current"][1]["y"]}")
            except queue.Empty:
                print(
                    "Timeout : Le sous-programme B n'a pas répondu dans le délai spécifié."
                )
    except KeyboardInterrupt:
        pass

    process_a.terminate()
    process_b.terminate()

    return "|".join(";".join(pos_player) for pos_player in res)


# if __name__ == "__main__":
#     sys.exit(main())
