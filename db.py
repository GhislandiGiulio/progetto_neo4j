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
        print("Connection established")

        # nome del db sul server (default)
        self.database = "neo4j"


    def match_cells(self, date=None):

        # dalla guida ufficiale online: 
        # " Do not hardcode or concatenate parameters: use placeholders and specify the parameters as keyword arguments. "

        if date:
            query = """ MATCH (p:Cell {date: $date}) 
                        RETURN  p.id as id,
                                p.action_range as action_range, 
                                p.latitude as latitude, 
                                p.longitude as longitude,
                                p.power as power"""
        else:

            query =  """ MATCH (p:Cell) 
                        RETURN  p.id as id,
                                p.action_range as action_range, 
                                p.latitude as latitude, 
                                p.longitude as longitude,
                                p.power as power"""
        
            
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            date=date,
                                                            database_=self.database,
                                                        )
        
        return records
    
    def match_users(self, name=None):


        if name:
            query = """ MATCH (p:User {name: $name}) 
                        RETURN  p.id as id,
                                p.name as name, 
                                p.birth_date as birth_date"""
        else:

            query =  """ MATCH (p:User) 
                        RETURN  p.id as id,
                                p.name as name, 
                                p.birth_date as birth_date"""
        
            
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            name=name,
                                                            database_=self.database,
                                                        )
        
        return records
    
    def match_sims(self, phone_number=None):


        if phone_number:
            query = """ MATCH (p:Sim {phone_number: $phone_number}) 
                        RETURN  p.id as id,
                                p.phone_number as phone_number"""
        else:

            query =  """ MATCH (p:Sim) 
                        RETURN  p.id as id,
                                p.phone_number as phone_number"""
        
            
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            phone_number=phone_number,
                                                            database_=self.database,
                                                        )
        
        return records

if __name__ == "__main__":

    db = Cells_db()