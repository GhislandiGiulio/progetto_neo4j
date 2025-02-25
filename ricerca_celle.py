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

    scelta = checked_input("Inserisci un'opzione\n 1- Mostra elenchi\n 2- Ricerca utente sospetto\n 3- Ricerca per cella\n 4- Ricerca per vicinanza\n q- Esci\n\nScelta: ")

    match scelta:
        case 1:
            mostra_elenco()

        case 2:
            ricerca_user_sospetto()

        case 3:
            ricerca_persone_per_cella()

        case 4:
            ricerca_per_vicinanza()

        case "q":
            print("Uscita dal programma in corso...")
            time.sleep(1)
            exit(0)

        case _:
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
    
    print("Elenco delle connessioni sospette:\n")

    for record in records:
        print("------------------------------------------------")
        for key in record.keys():
            print(f"{key}: {record.get(key)}")
        print("\n")

    input("Premi 'invio' per tornare al menu...")

def is_valid_latitude(lat):
    try:
        lat = float(lat)
        return -90 <= lat <= 90
    except ValueError:
        return False

def is_valid_longitude(lon):
    try:
        lon = float(lon)
        return -180 <= lon <= 180
    except ValueError:
        return False

def get_valid_latitude_longitude():
    while True:
        try:
            latitude = input("Inserisci latitudine (da -90 a 90): ")

            if latitude == "":
                return "q", ""

            longitude = input("Inserisci longitudine (da -180 a 180): ")

            if longitude == "":
                return "q", ""
            
            latitude = float(latitude)
            longitude = float(longitude)

            if is_valid_latitude(latitude) and is_valid_longitude(longitude):
                return latitude, longitude
            else:
                print("Latitude o longitudine non valide. Riprova.")
        except ValueError:
            print("Input non valido. Inserisci dei numeri.")

@schermata
def ricerca_per_vicinanza():
    
    print("Interfaccia di ricerca per luogo\n\nLascia vuoto in qualsiasi momento per tornare al menu...")

    # input di luogo
    latitude, longitude = get_valid_latitude_longitude()

    # logica per tornare al menu durante inserimento luogo
    if latitude == "q" or longitude == "q":
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

    # input distanza entro la quale cercare
    while True:
        try:
            distance = float(input("Inserisci distanza (in km): "))
            break
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    # esecuzione query
    records = cells_db.find_connection_near_location(latitude, longitude, from_datehour, distance)

    # se trovati risultati, mostrali
    if records == []:
        print("Non sono stati trovati risultati.")
        input("Premi 'invio' per tornare al menu...")
    
    mostra_sospetti(records)

    

@schermata
def ricerca_persone_per_cella():
    cell_id = input("A quale cella sei interessato? ")
    data_ora = input("In quale data / orario? (YYYY-MM-DD HH:MM) ")

    if not validate_datehour_format(data_ora):
        print("Formato data/ora non valido.")
        input("Premi 'invio' per tornare al menu precedente...")
        return

    records = cells_db.find_people_from_cell(cell_id, data_ora)
    
    # se trovati risultati, mostrali
    if records == []:
        print("Non sono stati trovati risultati.")
        input("Premi 'invio' per tornare al menu...")
    
    mostra_sospetti(records)


if __name__ == '__main__':

    while True:
        menu()
