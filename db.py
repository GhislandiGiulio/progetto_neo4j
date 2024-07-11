import neo4j

class Cells_db:

    def __init__(self) -> None:
        
        # credenziali
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "id64eRyHBQL5Cvw"

        # creazione del driver
        self.driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))
        self.driver.verify_connectivity()

        # nome del db sul server (default)
        self.database = "neo4j"


    def get_nodes(self):

        # dalla guida ufficiale online: 
        # " Do not hardcode or concatenate parameters: use placeholders and specify the parameters as keyword arguments. "
        
        records, summary, keys = self.driver.execute_query(
                                                            "MATCH (p:Person {age: $age}) RETURN p.name AS name",
                                                            age=42,
                                                            database_=self.database,
                                                        )

if __name__ == "__main__":

    db = Cells_db()