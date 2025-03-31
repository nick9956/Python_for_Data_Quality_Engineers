import sqlite3


def fetch_news_feed_data():
    """
    Fetch and display all data from the tables in the 'news_feed.db' database.
    """
    try:
        with sqlite3.connect('news_feed.db') as conn:
            cursor = conn.cursor()
            for table in ['News', 'PrivateAd', 'JokeOfTheDay']:
                print(f'--- {table} ---')
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print(f"No data found in the {table} table.")

                print('\n')
    except sqlite3.Error as e:
        print(f"An error occurred while fetching data: {e}")


def fetch_city_data():
    """
    Fetch and display all data from the 'cities' table in the 'city_coordinates.db' database.
    """
    try:
        with sqlite3.connect('city_coordinates.db') as conn:
            cursor = conn.cursor()
            print('--- Cities ---')
            cursor.execute("SELECT * FROM cities")
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"City: {row[0]}, Latitude: {row[1]}, Longitude: {row[2]}")
            else:
                print("No data found in the cities database.")

            print('\n')
    except sqlite3.Error as e:
        print(f"An error occurred while fetching data: {e}")


def menu():
    """
    Display a menu for the user to select which database to view.
    """
    while True:
        print("=== Database Viewer ===")
        print("1. View data from 'news_feed.db'")
        print("2. View data from 'city_coordinates.db'")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            print("Fetching data from 'news_feed.db':")
            fetch_news_feed_data()
        elif choice == "2":
            print("Fetching data from 'city_coordinates.db':")
            fetch_city_data()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the menu
if __name__ == "__main__":
    menu()