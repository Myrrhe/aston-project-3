# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:12:19 2023

@author: baudi
"""

import queue
import subprocess
import threading
from random import randint
from typing import IO
from contextlib import ExitStack
import time

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

NB_BOTS = 2


# Fonction pour lire la sortie du sous-programme de manière asynchrone
def read_output(output: IO[str], output_queue: queue) -> None:
    """Read the output"""
    for line in iter(output.readline, ""):
        output_queue.put(line)
    output.close()


def main_fight(bots_id: list[str]) -> dict[str | dict]:
    """The main method"""

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
        [f"{pos["init"][i]["x"]},{pos["init"][i]["y"]}"] for i in range(NB_BOTS)
    ]
    res_stderr = [
        [] for _ in range(NB_BOTS)
    ]

    health = [1 for _ in range(NB_BOTS)]

    # Créez une file pour stocker la sortie du sous-programme
    output_queue = [queue.Queue() for _ in range(NB_BOTS)]
    error_queues = [queue.Queue() for _ in range(NB_BOTS)]

    with ExitStack() as stack:
        processes = [
            stack.enter_context(subprocess.Popen(
                ["python", f"storage/bot/{bot_id}.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )) for bot_id in bots_id
        ]

        # Créez des threads pour lire la sortie des sous-programmes de manière asynchrone
        output_threads = [threading.Thread(
            target=read_output, args=(processes[i].stdout, output_queue[i])
        ) for i in range(NB_BOTS)]
        error_threads = [threading.Thread(
            target=read_output, args=(processes[i].stderr, error_queues[i])
        ) for i in range(NB_BOTS)]

        time.sleep(0.5)

        for output_thread in output_threads:
            output_thread.daemon = True
            output_thread.start()
        for error_thread in error_threads:
            error_thread.daemon = True
            error_thread.start()

        try:
            # Game loop
            while health[0] > 0 and health[1] > 0:
                # Envoyez des données au sous-programmes via l'entrée standard
                # On peut envoyer des mots séparés par des espaces, ou un mot unique

                for i in range(NB_BOTS):
                    # STDERR
                    current_stderr = []
                    while not error_queues[i].empty():
                        current_stderr.append(error_queues[i].get_nowait())
                    res_stderr[i].append(current_stderr)

                    processes[i].stdin.write("0\n")
                    processes[i].stdin.flush()
                    processes[i].stdin.write(
                        f"{pos["init"][0]["x"]} {pos["init"][0]["y"]} {pos["current"][0]["x"]} {pos["current"][0]["y"]}\n"
                    )
                    processes[i].stdin.flush()
                    processes[i].stdin.write(
                        f"{pos["init"][1]["x"]} {pos["init"][1]["y"]} {pos["current"][1]["x"]} {pos["current"][1]["y"]}\n"
                    )
                    processes[i].stdin.flush()

                    pos["next"][i] = pos["current"][i].copy()

                    # Attendez une réponse du sous-programme avec un timeout
                    try:
                        # STDOUT
                        # Définissez le timeout en secondes
                        response = output_queue[i].get(timeout=10)
                        match response:
                            case "LEFT\n":
                                pos["next"][i]["x"] -= 1
                            case "RIGHT\n":
                                pos["next"][i]["x"] += 1
                            case "UP\n":
                                pos["next"][i]["y"] -= 1
                            case "DOWN\n":
                                pos["next"][i]["y"] += 1
                            case _:
                                print(f"Error: Invalid response for {i}")
                                health[i] = 0
                                break
                        if (
                            pos["next"][i]["x"] < 0
                            or pos["next"][i]["x"] >= FIELD_WIDTH
                            or pos["next"][i]["y"] < 0
                            or pos["next"][i]["y"] >= FIELD_HEIGHT
                            or field[pos["next"][i]["y"]][pos["next"][i]["x"]] != 0
                        ):
                            health[i] = 0
                            break
                        else:
                            pos["current"][i] = pos["next"][i].copy()
                            field[pos["current"][i]["y"]][pos["current"][i]["x"]] = 1
                            res[i].append(f"{pos["current"][i]["x"]},{pos["current"][i]["y"]}")
                    except queue.Empty:
                        health[i] = 0
                        print(
                            f"Timeout : Le sous-programme {i} n'a pas répondu dans le délai spécifié."
                        )
                        break
        except KeyboardInterrupt:
            pass

        for process in processes:
            process.terminate()

    return {
        "movements": f"{"|".join(";".join(pos_player) for pos_player in res)}",
        "result": "1" if health[0] == 1 else "0",
        "stderr": res_stderr,
    }


# if __name__ == "__main__":
#     sys.exit(main())
