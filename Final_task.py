import sqlite3
import math

# Constants
DB_FILE = "city_coordinates.db"
EARTH_RADIUS_KM = 6371.0


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth
    using the Haversine formula.
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS_KM * c
    return distance


def initialize_database():
    """
    Initialize the SQLite database, creating the 'cities' table if it doesn't exist.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        """)


def get_city_coordinates(city_name):
    """
    Retrieve the latitude and longitude of a city from the database.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (city_name,))
        return cursor.fetchone()


def add_city_to_database(city_name, latitude, longitude):
    """
    Add a city's coordinates to the database.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                           (city_name, latitude, longitude))
            conn.commit()
        print(f"Successfully added {city_name} to the database.")
    except sqlite3.IntegrityError:
        print(f"Error: City '{city_name}' already exists in the database.")


def get_coordinates_from_user(city_name):
    """
    Prompt the user for latitude and longitude of a city.
    """
    while True:
        try:
            lat = float(input(f"Enter latitude for {city_name}: "))
            lon = float(input(f"Enter longitude for {city_name}: "))
            return lat, lon
        except ValueError:
            print("Invalid input. Please enter numeric values for latitude and longitude.")


def main():
    """
    Main program to calculate the distance between two cities.
    """
    initialize_database()

    print("=== City Distance Calculator ===")
    city1 = input("Enter the name of the first city: ").strip()
    city2 = input("Enter the name of the second city: ").strip()

    # Get coordinates for the first city
    city1_coordinates = get_city_coordinates(city1)
    if city1_coordinates is None:
        print(f"Coordinates for '{city1}' not found in the database.")
        lat1, lon1 = get_coordinates_from_user(city1)
        add_city_to_database(city1, lat1, lon1)
    else:
        lat1, lon1 = city1_coordinates

    # Get coordinates for the second city
    city2_coordinates = get_city_coordinates(city2)
    if city2_coordinates is None:
        print(f"Coordinates for '{city2}' not found in the database.")
        lat2, lon2 = get_coordinates_from_user(city2)
        add_city_to_database(city2, lat2, lon2)
    else:
        lat2, lon2 = city2_coordinates

    # Calculate and display the distance
    distance = haversine(lat1, lon1, lat2, lon2)
    print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} kilometers.")


if __name__ == "__main__":
    main()
