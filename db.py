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


    def match_cells(self):

        # dalla guida ufficiale online: 
        # " Do not hardcode or concatenate parameters: use placeholders and specify the parameters as keyword arguments. "

        query =  """ MATCH (p:Cell) 
                    RETURN  p.id as id,
                            p.action_range as action_range, 
                            p.location.latitude as latitude, 
                            p.location.longitude as longitude,
                            p.power as power"""
    
            
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            database_=self.database,
                                                        )
        
        return records
    
    def match_users(self):

        query =  """ MATCH (p:User) 
                    RETURN  p.id as id,
                            p.name as name, 
                            p.birth_date as birth_date"""
        
            
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            database_=self.database,
                                                        )
        
        return records
    
    def match_sims(self):

        query =  """ MATCH (p:Sim) 
                    RETURN  p.id as id,
                            p.phone_number as phone_number"""
        
            
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            database_=self.database,
                                                        )
        
        return records
    
    def find_suspect(self, name, from_datehour, to_datehour):

        query =  """MATCH (:Cell)<-[c:CONNECTED_TO]-(s:Sim)-[:OWNED_BY]->(u:User)
                    WHERE u.name STARTS WITH $prefix
                    AND c.connection_datehour >= $from_datehour AND c.connection_datehour <= $to_datehour
                    RETURN s.phone_number AS phone_number, u.name AS name, c.connection_datehour AS datehour"""
        
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            prefix=name,
                                                            from_datehour=from_datehour,
                                                            to_datehour=to_datehour,
                                                            database_=self.database
                                                        )
        
        return records
    
    def find_connection_near_location(self, latitude, longitude, from_datehour, distance):

        query =  """MATCH (c:Cell)<-[con:CONNECTED_TO]-(s:Sim)-[:OWNED_BY]->(u:User)
                    WHERE point.distance(c.location, point({latitude: $latitude, longitude: $longitude})) < $distance
                    AND con.connection_datehour >= $from_datehour
                    RETURN u.name AS name, s.phone_number AS phone_number
                    """
        
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            from_datehour=from_datehour,
                                                            latitude=latitude,
                                                            longitude=longitude,
                                                            distance=distance*1000,
                                                            database_=self.database
                                                        )
        
        return records
    
    def find_people_from_cell(self, cell_id, from_datehour):

        query =  """MATCH (c:Cell)<-[con:CONNECTED_TO]-(s:Sim)-[:OWNED_BY]->(u:User)
                    WHERE c.id = $cell_id
                    AND con.connection_datehour >= $from_datehour
                    RETURN s.phone_number AS phone_number, u.name AS name
                    """
        
        records, summary, keys = self.driver.execute_query(
                                                            query,
                                                            cell_id=cell_id,
                                                            from_datehour=from_datehour,
                                                            database_=self.database
                                                        )
        
        return records


if __name__ == "__main__":

    db = Cells_db()