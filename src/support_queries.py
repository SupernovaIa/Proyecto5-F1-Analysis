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


"""
Select queries
--------------
"""

# Driver of the day count
query_1 = """
SELECT r.driver , COUNT(*) AS times_chosen
FROM races r
GROUP BY r.driver 
ORDER BY times_chosen DESC ;
"""

# Drivers championship
query_2 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, SUM(res.points) AS total_points
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
GROUP BY d.driverid
ORDER BY total_points DESC
LIMIT 10 ;
"""

# Constructors championship
query_3 = """
SELECT con.name, SUM(res.points) AS total_points
FROM results res
INNER JOIN constructors con ON res.constructor_id = con.constructorid
INNER JOIN races r ON res.race_id = r.race_id
GROUP BY con.constructorid
ORDER BY total_points DESC ;
"""

# Alonso's results
query_4 = """
SELECT r.racename AS Name, res.position AS Position
FROM results res
INNER JOIN races r ON res.race_id = r.race_id
WHERE res.driver_id = 'alonso'
ORDER BY r.date ;
"""

# Positions gained in Bahrain (2023_1)
query_5 = """
SELECT 
	concat(d.first_name, ' ', d.last_name) AS Driver, 
	res.grid AS GridPosition, 
	res.position AS EndPosition, 
	res.delta_pos AS PositionsGained
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
WHERE res.race_id = '2023_1' ;
"""

# Number of DNF
query_6 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, COUNT(*) AS dnf_count
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
WHERE res.status != 'Finished'
GROUP BY d.driverid
ORDER BY dnf_count DESC ;
"""

# Points per race for every driver
query_7 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, round(AVG(res.points), 2) AS avg_points
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
GROUP BY d.driverid
ORDER BY avg_points DESC ;
"""

# Number of wins
query_8 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, COUNT(*) AS wins
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
WHERE res.position = 1
GROUP BY d.driverid
ORDER BY wins DESC ;
"""

# Number of podiums
query_9 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, COUNT(*) AS wins
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
WHERE res.position <= 3
GROUP BY d.driverid
ORDER BY wins DESC ;
"""

# Gained positions in the whole season
query_10 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, SUM(res.delta_pos) AS total_positions_gained
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
GROUP BY d.driverid
ORDER BY total_positions_gained DESC ;
"""

# Leclerc Specifc
query_11 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, res.delta_pos, COUNT(*) AS occurrences
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
WHERE d.last_name = 'Leclerc'
GROUP BY d.first_name, d.last_name, res.delta_pos
ORDER BY d.last_name, res.delta_pos DESC ;
"""

# Verstappen specific
query_12 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, res.delta_pos, COUNT(*) AS occurrences
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
WHERE d.last_name = 'Verstappen' 
GROUP BY d.first_name, d.last_name, res.delta_pos
ORDER BY d.last_name, res.delta_pos DESC ;
"""

# Pole position effectiveness
query_13 = """
SELECT concat(d.first_name, ' ', d.last_name) AS Driver, r.racename, res.position
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
WHERE res.grid = 1 ;
"""

# Championship evolution
query_14 = """
SELECT r.round , concat(d.first_name, ' ', d.last_name) AS Driver, 
       SUM(res.points) OVER (PARTITION BY res.driver_id ORDER BY r.date) AS cumulative_points
FROM results res
INNER JOIN drivers d ON res.driver_id = d.driverid
INNER JOIN races r ON res.race_id = r.race_id
ORDER BY r.date, Driver ;
"""