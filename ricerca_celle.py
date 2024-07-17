import os
import time
from datetime import datetime
import pwinput

# importazione funzioni db
import db

# inizializzazione driver db
cells_db = db.Cells_db()

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

        print("Portale di ricerca collegamenti SIM della rete mobile.")

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

    scelta = checked_input("Inserisci un'opzione\n 1- Mostra elenchi\n 2- \n q- Esci\n\nScelta: ")

    match scelta:
        case 1:
            mostra_elenco()
            pass

        case 2:
            localizzazione_persona()
            pass

        case 3:
            # ricerca
            pass

        case "q":
            print("Uscita dal programma in corso...")
            time.sleep(1)
            exit(0)

        case "_":
            print("Opzione non valida")
            input("Premi 'invio' per tornare al menu precedente...")

@schermata
def mostra_elenco():

    while True:

        try: 
            scelta = input("Scegli quale lista mostrare :\n 1- Utenti\n 2- Celle\n 3- Sim\n q- Torna al menu principale\n")
            break

        except Exception:

            print("Input non valido. Riprova")
            continue
    
    match scelta:

        case "1":
            mostra_match("user")

        case "2":
            mostra_match("cell")

        case "3":
            mostra_match("sim")

        case "q":
            return
        
        case "_":
            print("Opzione non valida")
            input("Premi 'invio' per tornare al menu precedente...")


@schermata
def mostra_match(node_type):
        
    match node_type:
        
        case "sim":
            records = cells_db.match_sims()
        case "cell":    
            records = cells_db.match_cells()
        case "user":
            records = cells_db.match_users()
    
    
    print("Elenco di {tipologia}:\n")

    for record in records:

        print("------------------------------------------------")

        for key in record.keys():
            print(f"{key}: {record.get(key)}")

    input("Premi 'invio' per tornare al menu precedente...")

@schermata
def localizzazione_persona():
    nome = input("Inserisci il nome della persona: ")
    data = input("Inserisci la data (YYYY-MM-DD): ")
    ora = input("Inserisci l'ora (HH:MM): ")

    records = cells_db.find_cells_by_person_and_time(nome, data, ora)
    
    print(f"Elenco delle celle per {nome} alla data {data} e ora {ora}:\n")
    for record in records:
        print("------------------------------------------------")
        for key in record.keys():
            print(f"{key}: {record.get(key)}")
    
    input("Premi 'invio' per tornare al menu precedente...")


if __name__ == '__main__':

    while True:
        menu()
