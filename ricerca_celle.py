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

    scelta = checked_input("Inserisci un'opzione\n 1- Mostra elenchi\n 2- Ricerca utente sospetto\n q- Esci\n\nScelta: ")

    match scelta:
        case 1:
            mostra_elenco()
            pass

        case 2:
            ricerca_user_sospetto()
            pass

        case 3:
            localizzazione_persona()
            pass

        case 4:
            ricerca_per_luogo()

        case "q":
            print("Uscita dal programma in corso...")
            time.sleep(1)
            exit(0)

        case "_":
            print("Opzione non valida")
            input("Premi 'invio' per tornare al menu precedente...")

@schermata
def mostra_elenco():
    
    scelta = checked_input("Scegli quale lista mostrare :\n 1- Utenti\n 2- Celle\n 3- Sim\n q- Torna al menu principale\n")
    
    match scelta:

        case 1:
            mostra_match("user")

        case 2:
            mostra_match("cell")

        case 3:
            mostra_match("sim")

        case "q":
            return
        
        case "_":
            print("Opzione non valida")
            input("Premi 'invio' per tornare al menu...")


@schermata
def mostra_match(node_type):
        
    match node_type:
        
        case "sim":
            records = cells_db.match_sims()
        case "cell":    
            records = cells_db.match_cells()
        case "user":
            records = cells_db.match_users()
    
    
    print(f"Elenco di {node_type}:\n")

    for record in records:

        print("------------------------------------------------")

        for key in record.keys():
            print(f"{key}: {record.get(key)}")

    input("Premi 'invio' per tornare al menu...")

def validate_datehour_format(datehour):
    try:
        datetime.strptime(datehour, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

@schermata
def ricerca_user_sospetto():

    print("Interfaccia di ricerca di un sospetto\n\nLascia vuoto in qualsiasi momento per tornare al menu...")

    # input di nome sospetto
    nome = input("A quale nominativo sei interessato? (case-sensitive): ")

    # ritorno al menu se vuoto
    if nome == "":
        return
    
    # input di dataora minima
    while True:
        from_datehour = input("Inserisci data e ora da cui cercare (YYYY-MM-DD HH:MM): ")

        if from_datehour == "":
            return

        if validate_datehour_format(from_datehour):
            break
        else:
            print("Formato non valido.")

    # input di dataora massima
    while True:
        to_datehour = input("Inserisci data e ora a cui cercare (YYYY-MM-DD HH:MM): ")

        if to_datehour == "":
            return

        if validate_datehour_format(to_datehour):
            break
        else:
            print("Formato non valido.")

    # esecuzione query
    records = cells_db.find_suspect(nome, from_datehour, to_datehour)

    # se trovati risultati, mostrali
    if records == []:
        print("Non sono stati trovati risultati.")
        input("Premi 'invio' per tornare al menu...")
    
    mostra_sospetti(records)


@schermata
def mostra_sospetti(records):
    
    print("Elenco delle connsessioni sospette:\n")

    for record in records:
        print("------------------------------------------------")
        for key in record.keys():
            print(f"{key}: {record.get(key)}")
        print("\n")

    input("Premi 'invio' per tornare al menu...")

def is_valid_latitude(lat):
    return -90 <= lat <= 90

def is_valid_longitude(lon):
    return -180 <= lon <= 180

def get_valid_latitude_longitude():
    while True:
        try:
            latitude = input("Inserisci latitudine (da -90 a 90): ")
            longitude = input("Inserisci longitudine (da -180 a 180): ")

            if is_valid_latitude(latitude) and is_valid_longitude(longitude):
                return latitude, longitude
            else:
                print("Latitude o longitudine non valide. Riprova.")
        except ValueError:
            print("Input non valido. Inserisci dei numeri.")

@schermata
def ricerca_per_luogo():
    
    print("Interfaccia di ricerca per luogo\n\nLascia vuoto in qualsiasi momento per tornare al menu...")

    # input di luogo
    latitude, longitude = get_valid_latitude_longitude()

    # input di dataora minima
    while True:
        from_datehour = input("Inserisci data e ora da cui cercare (YYYY-MM-DD HH:MM): ")

        if from_datehour == "":
            return

        if validate_datehour_format(from_datehour):
            break
        else:
            print("Formato non valido.")

@schermata
def persone_nella_cella():
    cell_id = input("A quale cella sei interessato? ")
    data_ora = input("In quale data / orario? (YYYY-MM-DD HH:MM) ")

    if not validate_datehour_format(data_ora):
        print("Formato data/ora non valido.")
        input("Premi 'invio' per tornare al menu precedente...")
        return

    records = cells_db.find_people_in_cell(cell_id, data_ora)
    
    if records:
        print("Le SIM collegate alla cella sono:")
        for record in records:
            print(f"• {record['nome']} (con numero {record['numero']})")
    else:
        print("Nessuna SIM trovata nella cella per la data/ora specificata.")
    
    input("Premi 'invio' per tornare al menu precedente...")


if __name__ == '__main__':

    while True:
        menu()
