import neo4j

class Cells_db:

    def __init__(self) -> None:
    
        # Replace with your Neo4j credentials and connection details
        uri = "bolt://localhost:7687"  # Default URI for local Neo4j instance
        username = "neo4j"
        password = "id64eRyHBQL5Cvw"

        # Create a driver instance
        driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))

        if not driver.verify_connectivity():
            print("Connessione al db riuscita!")


if __name__ == "__main__":

    db = Cells_db()