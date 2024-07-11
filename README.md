# progett_neo4j
L'obbiettivo del progetto è creare un'applicazione per la Polizia Postale.

## 1. Clonazione della repo 
Crea una cartella apposita per il tuo progetto. Il nome non ha importanza.

Apri una shell nella cartella in cui vuoi eseguire il progetto ed esegui i seguenti comandi:
``` powershell
git clone https://github.com/GhislandiGiulio/progetto_neo4j.git .
``` 


## 2. Download python 3.12
Se non è già installato, scarica Python 3.12. Se è già installato, assicurati che sia la versione attiva nel sistema di python.
### Windows:
```powershell
winget install -e --id Python.Python.3.12
```

### macOS (homebrew)
```powershell
brew install python@3.12
```

## 3. Creazione virtual environment

### Windows
```powershell
py -3.12 -m venv .venv
``` 

### macOS
``` powershell
python3.12 -m venv .venv
``` 

## 4. Attivazione virtual environment
### Windows Powershell
``` powershell
[PATH_DIRECTORY_PROGETTO]\.venv\Scripts\Activate.ps1
``` 
### macOS
``` powershell
source [PATH_DIRECTORY_PROGETTO]/.venv/bin/activate
``` 


## 5. Installazione delle dipendenze
Installazione moduli richiesti per eseguire lo script python:
``` powershell
pip install -r requirements.txt
```

## 6. Installazione di Neo4J server con Docker
Se non già installato, scarica l'eseguibile di Docker dal [sito ufficiale](https://www.docker.com/products/docker-desktop/).
Una volta installato, fai il pull dell'imagine di Neo4J (enterprise):
``` powershell
docker pull neo4j:enterprise 
```
Adesso crea un container con port-forwarding. Assicurati di cambiare nome utente e password:
``` powershell
docker run `
  --name my_neo `
  --publish=7474:7474 `
  --publish=7687:7687 `
  -e NEO4J_AUTH=[NOME_UTENTE]/[PASSWORD] `
  -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes `
  -d neo4j:enterprise
```

## 7. Inizializzazione del db
Se hai accesso al db, puoi eseguire lo script "inizializza_dataset.py" per inizializzare il db con 33 concerti con cui testare lo script principale.