import random
from uuid import uuid4
from neo4j import GraphDatabase

import db

class Sim:
    def __init__(self, phone_number):
        self.phone_number = phone_number

class Cell:
    def __init__(self, operator, power, action_range, location):
        self.operator = operator
        self.power = power
        self.action_range = action_range
        self.location = location

class User:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

class OWNED_BY:
    def __init__(self, sim, user):
        self.sim = sim
        self.user = user

class CONNECTED_TO:
    def __init__(self, sim, cell, connection_datehour):
        self.sim = sim
        self.cell = cell
        self.connection_datehour = connection_datehour

def random_phone_number():
    country_code = 39
    area_code = f"{random.randint(2, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    central_office_code = f"{random.randint(2, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    line_number = f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    phone_number = f"+{country_code}{area_code}{central_office_code}{line_number}"
    return phone_number

def random_name():
    first_names = [
        "Vito", "Salvatore", "Giovanni", "Francesco", "Antonio", "Mario", "Luigi", "Paolo", "Carlo", "Pietro", 
        "Alessandro", "Domenico", "Massimo", "Roberto", "Nicola", "Leonardo", "Angelo", "Raffaele", "Michele", 
        "Fabrizio", "Giorgio", "Giuseppe", "Lorenzo", "Rocco", "Silvio", "Enzo", "Marco", "Stefano", "Bruno", 
        "Riccardo", "Umberto"
    ]

    last_names = [
        "Corleone", "Gambino", "Lucchese", "Genovese", "Bonanno", "Profaci", "Colombo", "Mancini", "Russo", "Santoro",
        "Rizzo", "Costa", "Grasso", "Marino", "Bruno", "Ferrara", "Barone", "Sartori", "Esposito", "Gallo",
        "Conte", "Greco", "Ricci", "Romano", "Lombardi", "Moretti", "Amato", "Ruggiero", "Leone", "De Luca",
        "Caruso", "Giordano", "Pugliese", "Fontana", "Ferri", "Messina"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_operator():
    operators = ["OperatorA", "OperatorB", "OperatorC", "OperatorD"]
    return random.choice(operators)

def random_power():
    return random.randint(1, 100) # in kW

def random_action_range():
    return random.uniform(0.1, 10.0) # in km

def random_location():
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    return [latitude, longitude]

def random_birth_date():
    year = random.randint(1950, 2010)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def random_datehour():
    year = random.randint(1950, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    datehour = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
    return datehour

def create_sim(tx, sim):
    sim_id = str(uuid4())
    tx.run("CREATE (s:Sim {id:$id, phone_number: $phone_number})", id=sim_id, phone_number=sim.phone_number)

def create_cell(tx, cell):
    cell_id = str(uuid4())  # Generate a unique ID for each cell
    tx.run(
        "CREATE (c:Cell {id: $id, operator: $operator, power: $power, action_range: $action_range, latitude: $latitude, longitude: $longitude})",
        id=cell_id, operator=cell.operator, power=cell.power, action_range=cell.action_range,
        latitude=cell.location[0], longitude=cell.location[1]
    )

def create_user(tx, user):
    user_id = str(uuid4())  # Generate a unique ID for each cell
    tx.run("CREATE (u:User {id:$id, name: $name, birth_date: $birth_date})", id=user_id, name=user.name, birth_date=user.birth_date)

def create_owned_by(tx, sim, user):
    tx.run(
        "MATCH (s:Sim {phone_number: $phone_number}), (u:User {name: $name}) "
        "CREATE (s)-[:OWNED_BY]->(u)",
        phone_number=sim.phone_number, name=user.name
    )

def create_connected_to(tx, sim, cell, connection_datehour):
    tx.run(
        "MATCH (s:Sim {phone_number: $phone_number}), (c:Cell {operator: $operator, latitude: $latitude, longitude: $longitude}) "
        "CREATE (s)-[:CONNECTED_TO {connection_datehour: $connection_datehour}]->(c)",
        phone_number=sim.phone_number, operator=cell.operator, latitude=cell.location[0], longitude=cell.location[1],
        connection_datehour=connection_datehour
    )

if __name__ == "__main__":
    
    # Create Neo4j driver instance
    cells_db = db.Cells_db()

    with cells_db.driver.session() as session:
        # Create random instances
        sims = [Sim(random_phone_number()) for _ in range(200)]
        cells = [Cell(random_operator(), random_power(), random_action_range(), random_location()) for _ in range(10)]
        users = [User(random_name(), random_birth_date()) for _ in range(100)]

        # Insert nodes
        for sim in sims:
            session.execute_write(create_sim, sim)
        
        for cell in cells:
            session.execute_write(create_cell, cell)
        
        for user in users:
            session.execute_write(create_user, user)

        # Create random relationships
        for sim in sims:
            # Randomly select a user for the OWNED_BY relationship
            user = random.choice(users)
            session.execute_write(create_owned_by, sim, user)

            # Randomly select a cell for the CONNECTED_TO relationship
            cell = random.choice(cells)
            session.execute_write(create_connected_to, sim, cell, random_datehour())

    cells_db.driver.close()


