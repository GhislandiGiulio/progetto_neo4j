import os
import time
from datetime import datetime
import pwinput

# importazione funzioni db
import db

# wrapper delle funzioni schermata
def schermata(f):
    def wrapper(*args, **kwargs):
        """Questa funzione pulisce il terminale e stampa delle informazioni
        """

        if os.name == 'nt':
            # Per Windows
            os.system('cls')
        else:
            # Per Unix/Linux/macOS
            os.system('clear')

        print("Portale di ricerca collegamenti a celle")

        print("\n")
        
        return f(*args, **kwargs)
    
    return wrapper



def checked_input(sentence: str):

    while True:
        
        try:
            inserimento = input(sentence)

            if inserimento == "q":
                return "q"

            inserimento = int(inserimento)

            break

        except:
            print("Input non valido. Riprova")

    return inserimento


@schermata
def menu():

    scelta = checked_input("Inserisci un'opzione\n 1- Login\n q- Esci\n\nScelta: ")

    match scelta:
        case 1:
            # ricerca
            pass

        case 2:
            # ricerca
            pass

        case 3:
            # ricerca
            pass

        case "q":
            print("Uscita dal programma in corso...")
            time.sleep(1)
            exit(0)

        case "_":
            # ricerca
            pass


if __name__ == '__main__':

    while True:
        menu()
