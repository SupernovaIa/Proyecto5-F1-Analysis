"""
Creation queries
-----------------
"""

# Circuits
query_creation_circuits = """
CREATE TABLE IF NOT EXISTS circuits (
    circuitId VARCHAR(50) primary key,
    url VARCHAR(200),
    circuitName VARCHAR(100) not null,
    capacity INT,
    website VARCHAR(200),
    architect VARCHAR(200),
    lat FLOAT not null,
    long FLOAT not null,
    locality VARCHAR(100) not null,
    country VARCHAR(50) not null
);
"""

# Races
query_creation_races = """
CREATE TABLE IF NOT EXISTS races (
    race_id VARCHAR(50) primary key,
    circuit_id VARCHAR(50) not null,
    raceName VARCHAR(100) not null,
    season INT not null,
    round INT not null,
    url VARCHAR(200),
    date VARCHAR(50) not null,
    driver VARCHAR(100),
    foreign key (circuit_id) references circuits(circuitId)
);
"""

# Drivers
query_creation_drivers = """
CREATE TABLE IF NOT EXISTS drivers (
    driverId VARCHAR(50) primary key,
    permanentNumber INT unique not null,
    code CHAR(3) unique not null,
    url VARCHAR(200),
    first_name VARCHAR(50) not null,
    last_name VARCHAR(50) not null,
    dateOfBirth VARCHAR(50) not null,
    nationality VARCHAR(50) not null
);
"""

# Constructors
query_creation_constructors = """
CREATE TABLE IF NOT EXISTS constructors (
    constructorId VARCHAR(50) primary key,
    url VARCHAR(200),
    name VARCHAR(50) not null,
    nationality VARCHAR(50) not null
);
"""

# Results
query_creation_results = """
CREATE TABLE IF NOT EXISTS results (
    id SERIAL primary key,
    race_id VARCHAR(10),
    position INT not null,
    positionText VARCHAR(5) not null,
    points INT not null,
    grid INT not null,
    laps INT not null,
    status VARCHAR(50) not null,
    driver_id VARCHAR(50) not null,
    constructor_id VARCHAR(50) not null,
    delta_pos INT not null,
    time VARCHAR(20),
    foreign key (race_id) references races(race_id),
    foreign key (driver_id) references drivers(driverId),
    foreign key (constructor_id) references constructors(constructorId)
);
"""

# List of queries ordered
queries_creation = [
    query_creation_circuits, 
    query_creation_races, 
    query_creation_drivers, 
    query_creation_constructors, 
    query_creation_results
    ]


"""
Insertion queries
-----------------
"""

# Insert query for circuits table
query_insertion_circuits = """
INSERT INTO circuits (
    circuitId, url, circuitName, capacity, website, architect, lat, long, locality, country
) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Insert query for races table
query_insertion_races = """
INSERT INTO races (
    race_id, circuit_id, raceName, season, round, url, date, driver
) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s);
"""

# Insert query for drivers table
query_insertion_drivers = """
INSERT INTO drivers (
    driverId, permanentNumber, code, url, first_name, last_name, dateOfBirth, nationality
) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s);
"""

# Insert query for constructors table
query_insertion_constructors = """
INSERT INTO constructors (
    constructorId, url, name, nationality
) VALUES
(%s, %s, %s, %s);
"""

# Insert query for results table
query_insertion_results = """
INSERT INTO results (
    race_id, position, positionText, points, grid, laps, status, driver_id, constructor_id, delta_pos, time
) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# List of queries ordered
queries_insertion = [
    query_insertion_circuits, 
    query_insertion_races, 
    query_insertion_drivers,
    query_insertion_constructors,
    query_insertion_results
    ]