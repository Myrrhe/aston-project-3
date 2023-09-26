# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:12:19 2023

@author: baudi
"""

import queue
import subprocess
import sys
import threading

# Ce programme envoi des nombre à deux autres programmes : A et B
# A et B renvoient une réponse différente selon les nombres envoyés
# Cette réponse correspond au comportement des programmes, et les nombres à
# l'état en cours. On put ettendre ce comportement pour fairs'affronter A et B
# sur un jeu comme le morpion, les dames, ou autre chose.

# Si un programme met trop de temps à renvoyer une réponse, on peut décider
# que cela le fait perdre automatiquement

# Pour exécuter ce programme, lancez 'python main.py' en ligne de commande


# Fonction pour lire la sortie du sous-programme de manière asynchrone
def read_output(output, output_queue):
    for line in iter(output.readline, ""):
        output_queue.put(line)
    output.close()


def main() -> int:
    print('Programme principal lancé\n')
    
    count = 0
    
    # Créez une file pour stocker la sortie du sous-programme
    output_queueA = queue.Queue()
    output_queueB = queue.Queue()
    
    # Lancez les sous-programmes en tant que processus enfants
    processA = subprocess.Popen(
        ["python", "a.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    processB = subprocess.Popen(
        ["python", "b.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Créez des threads pour lire la sortie des sous-programmes de manière asynchrone
    output_threadA = threading.Thread(
        target=read_output,
        args=(processA.stdout, output_queueA)
    )
    output_threadA.daemon = True
    output_threadA.start()
    
    output_threadB = threading.Thread(
        target=read_output,
        args=(processB.stdout, output_queueB)
    )
    output_threadB.daemon = True
    output_threadB.start()
    
    res = ""
    
    try:
        while res != "RIGHT-DOWN-":
            count += 1

            res = ""
            
            inp = "0" if count < 3 else "1"
            
            # Envoyez des données au sous-programmes via l'entrée standard
            # On peut envoyer des mots séparés par des expaces, ou un mot unique
            processA.stdin.write("0\n")
            processA.stdin.flush()
            processA.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            processA.stdin.flush()
            processA.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            processA.stdin.flush()
    
            # Attendez une réponse du sous-programme avec un timeout
            try:
                response = output_queueA.get(timeout=10)  # Définissez le timeout en secondes
                print("Réponse du sous-programme A :", response)
                res += response
            except queue.Empty:
                print("Timeout : Le sous-programme A n'a pas répondu dans le délai spécifié.")

            processB.stdin.write("1\n")
            processB.stdin.flush()
            processB.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            processB.stdin.flush()
            processB.stdin.write(f"{inp} {inp} {inp} {inp}\n")
            processB.stdin.flush()
    
            # Attendez une réponse du sous-programme avec un timeout
            try:
                response = output_queueB.get(timeout=10)  # Définissez le timeout en secondes
                print("Réponse du sous-programme B :", response)
                res += response
            except queue.Empty:
                print("Timeout : Le sous-programme B n'a pas répondu dans le délai spécifié.")
            
            res = res.replace("\n", "-")
            print(f"Réponse globale = {res}\n")
    except KeyboardInterrupt:
        pass
    
    processA.stdin.close()
    processA.wait()
    processB.stdin.close()
    processB.wait()
    print('Programme principal terminé')
    return 0

if __name__ == '__main__':
    sys.exit(main()) 
