import csv
import sqlite3
import xml.etree.ElementTree as ET
from json import load
from datetime import datetime
from random import choice
from os import path, remove
from HW_4_3 import normalize_text_case
from re import sub


class News:  # Creating a class to handle News objects
    def __init__(self, text: str, city: str) -> None:  # Constructor to initialize text (news body) and city
        self.text = text  # Storing the news body in an instance variable
        self.city = city  # Storing the city name in an instance variable

    def get_news_body(self):  # Method to format and return the news body
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')  # Getting the current time in a specific format
        return f"\nNews -------------------------\n{self.text}\n{self.city}, {current_time}\n"  # Returning the formatted news string


class PrivateAd:  # Creating a class to handle Private Ad objects
    def __init__(self, text: str, expiration_date: str) -> None:  # Constructor to initialize text and expiration date
        self.text = text  # Storing the ad text in an instance variable
        self.expiration_date = datetime.strptime(expiration_date, '%d/%m/%Y').date()  # Converting expiration date string to a date object

    def get_ad_body(self):  # Method to format and return the ad body
        delta = (self.expiration_date - datetime.now().date()).days  # Calculating the number of days till expiration
        delta_message = f"{delta} days left" if delta >= 0 else "expired"  # Creating a message based on expiration status
        return f"\nPrivate Ad ------------------\n{self.text}\nActual until: {self.expiration_date}, {delta_message}\n"  # Returning the formatted ad string


class JokeOfTheDay:  # Creating a class to handle Joke of the Day objects
    def __init__(self, text: str) -> None:  # Constructor to initialize the joke text
        self.text = text  # Storing the joke text in an instance variable

    def generate_mark(self):  # Method to generate a random "funny meter" rating
        marks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # List of possible ratings
        return f"Funny meter - {choice(marks)} out of 10"  # Returning a randomly selected rating

    def get_joke_body(self):  # Method to format and return the joke body
        funny_meter = self.generate_mark()  # Generating the funny meter rating
        return f"\nJoke of the day ------------\n{self.text}\n{funny_meter}\n"  # Returning the formatted joke string


class DBHandler:  # Creating a class to handle database operations
    def __init__(self, db_name='news_feed.db'):  # Constructor to initialize the SQLite database
        self.conn = sqlite3.connect(db_name)  # Establishing a database connection
        self.cursor = self.conn.cursor()  # Creating a cursor object for executing SQL queries

        # Creating a table for News if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS News(
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                city TEXT NOT NULL,
                current_date TEXT NOT NULL);
        ''')

        # Creating a table for Private Ads if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PrivateAd(
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                actual_until TEXT NOT NULL,
                days_left INTEGER NOT NULL);
        ''')

        # Creating a table for Joke of the Day if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS JokeOfTheDay(
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                funny_mark TEXT NOT NULL);
        ''')

    def insert_news(self, news):  # Method to insert news into the database
        self.cursor.execute('''
            SELECT * FROM News WHERE text = ? AND city = ? AND current_date = ?;
        ''', (news['text'], news['city'], news['current_date']))  # Checking for duplicate entries

        if self.cursor.fetchone() is None:  # If no duplicate is found
            self.cursor.execute('''
                INSERT INTO News (text, city, current_date) VALUES (?, ?, ?);
            ''', (news['text'], news['city'], news['current_date']))  # Inserting the news record
            self.conn.commit()  # Committing the transaction

    def insert_private_ad(self, private_ad):  # Method to insert private ad into the database
        self.cursor.execute('''
            SELECT * FROM PrivateAd WHERE text = ? AND actual_until = ? AND days_left = ?;
        ''', (private_ad['text'], private_ad['actual_until'], private_ad['days_left']))  # Checking for duplicate entries

        if self.cursor.fetchone() is None:  # If no duplicate is found
            self.cursor.execute('''
                INSERT INTO PrivateAd (text, actual_until, days_left) VALUES (?, ?, ?);
            ''', (private_ad['text'], private_ad['actual_until'], private_ad['days_left']))  # Inserting the private ad record
            self.conn.commit()  # Committing the transaction

    def insert_joke_of_the_day(self, joke_of_the_day):  # Method to insert joke into the database
        self.cursor.execute('''
            SELECT * FROM JokeOfTheDay WHERE text = ? AND funny_mark = ?;
        ''', (joke_of_the_day['text'], joke_of_the_day['funny_mark']))  # Checking for duplicate entries

        if self.cursor.fetchone() is None:  # If no duplicate is found
            self.cursor.execute('''
                INSERT INTO JokeOfTheDay (text, funny_mark) VALUES (?, ?);
            ''', (joke_of_the_day['text'], joke_of_the_day['funny_mark']))  # Inserting the joke record
            self.conn.commit()  # Committing the transaction

    def insert_processed_records(self, records):  # Method to insert multiple processed records into the database
        for record in records:  # Iterating through the records
            if record['method'] == 'News':  # If the record is News
                self.insert_news(record)  # Insert the News record
            elif record['method'] == 'Private ad':  # If the record is Private Ad
                self.insert_private_ad(record)  # Insert the Private Ad record
            elif record['method'] == 'Joke of the day':  # If the record is Joke of the Day
                self.insert_joke_of_the_day(record)  # Insert the Joke record

    def close(self):  # Method to close the database connection
        self.conn.close()  # Closing the connection


class FileReader:  # Creating a class to handle file reading operations
    def __init__(self, file_path: str = 'data.txt'):  # Constructor to initialize the file path
        self.file_path = file_path  # Storing the file path in an instance variable

    def read_file(self):  # Method to read records from the file
        records = []  # Initializing an empty list to store records
        with open(self.file_path, 'r', encoding='utf8') as file:  # Opening the file in read mode with UTF-8 encoding
            lines = file.readlines()  # Reading all lines into the list
            i = 0
            while i < len(lines):
                if lines[i].strip().endswith('-------------------------'):
                    method = lines[i].strip().split(' ')[0]
                    text = lines[i+1].strip()
                    additional_info = lines[i+2].strip()
                    if method == 'News':
                        city, current_date = additional_info.split(', ')
                        records.append({'method': method, 'text': text, 'city': city, 'current_date': current_date})
                    elif method == 'Private':
                        actual_until, days_left = additional_info.replace('Actual until: ', '').split(', ')
                        days_left = days_left.split(' ')[0]
                        records.append({'method': method+' ad', 'text': text, 'actual_until': actual_until, 'days_left': days_left})
                    elif method == 'Joke':
                        records.append({'method': method+' of the day', 'text': text, 'funny_mark': additional_info})
                    i += 3
                else:
                    i += 1
        return records  # Returning the list of records

    def delete_read_file(self):  # Method to delete the file after its content is read
        remove(self.file_path)  # Using the remove function to delete the file


class JSONReader:  # Creating a class to handle JSON file reading operations

    def __init__(self, file_path: str = 'data.json'): # Constructor to initialize the file path
        self.file_path = file_path # Storing the file path in an instance variable

    def load_file(self):
        data = []  # Initialize an empty list to store the loaded JSON data
        with open(self.file_path, 'r', encoding='utf8') as file:  # Open the file in read mode with UTF-8 encoding
            data = load(file)  # Use the `load` function from the `json` module to parse the file content into a Python object
        return data  # Return the parsed JSON data as a Python object (e.g., list or dictionary)

    def delete_read_file(self):  # Method to delete the file after its content is read
        remove(self.file_path)  # Using the remove function to delete the file


class XMLReader:  # Creating a class to handle XML file reading operations

    def __init__(self, file_path: str = 'data.xml'):  # Constructor to initialize the default XML file path
        self.file_path = file_path  # Storing the file path in an instance variable

    def read_file(self):  # Method to read and parse the XML file
        root = ET.parse(self.file_path)  # Parse the XML file and get the root element
        data = []  # Initialize an empty list to store the parsed data
        for item in root.findall('item'):  # Iterate over each 'item' element in the XML
            item_data = {}  # Initialize an empty dictionary to store the current item's data
            item_data['method'] = item.find('method').text  # Extract the 'method' field and add it to the dictionary
            item_data['text'] = item.find('text').text  # Extract the 'text' field and add it to the dictionary

            # Check for other optional fields and add them to the dictionary if they exist
            city = item.find('city')  # Try to find the 'city' field
            if city is not None:  # If the 'city' field exists
                item_data['city'] = city.text  # Add the 'city' value to the dictionary

            current_date = item.find('current_date')  # Try to find the 'current_date' field
            if current_date is not None:  # If the 'current_date' field exists
                item_data['current_date'] = current_date.text  # Add the 'current_date' value to the dictionary

            actual_until = item.find('actual_until')  # Try to find the 'actual_until' field
            if actual_until is not None:  # If the 'actual_until' field exists
                item_data['actual_until'] = actual_until.text  # Add the 'actual_until' value to the dictionary

            days_left = item.find('days_left')  # Try to find the 'days_left' field
            if days_left is not None:  # If the 'days_left' field exists
                item_data['days_left'] = days_left.text  # Add the 'days_left' value to the dictionary

            funny_mark = item.find('funny_mark')  # Try to find the 'funny_mark' field
            if funny_mark is not None:  # If the 'funny_mark' field exists
                item_data['funny_mark'] = funny_mark.text  # Add the 'funny_mark' value to the dictionary

            data.append(item_data)  # Add the fully constructed dictionary for the current item to the data list
        return data  # Return the list of parsed data dictionaries

    def delete_read_file(self):  # Method to delete the XML file after its content is read
        remove(self.file_path)  # Use the `remove` function from the `os` module to delete the file


class FilePublisher:  # Creating a class to handle file writing operations
    def __init__(self, file_path: str = 'news_feed.txt'):  # Constructor to initialize the file path
        self.file_path = file_path  # Storing the file path in an instance variable
        self.db = DBHandler()

    def check_file_size(self):  # Method to check the size of the file
        return path.getsize(self.file_path)  # Returning the size of the file in bytes

    def transform_to_text(self, records):
        data = []  # Initialize an empty list to store formatted text data
        for record in records:  # Iterate over each record in the loaded JSON data
            method = record['method']  # Extract the method (News, Private ad, or Joke)
            hyphens = ' -------------------------\n'  # Define a separator string for formatting
            text = record['text']  # Extract the text content of the record

            # Format each block
            entry = [f"{method}{hyphens}{text}\n"]  # Start formatting each record block with method and text
            if method == 'News':
                entry.append(f"{record['city']}, {record['current_date']}\n")  # Append city and current date for News
            elif method == 'Private ad':
                entry.append(f"Actual until: {record['actual_until']}, {record['days_left']}\n")  # Append expiration details for Private Ad
            elif method == 'Joke of the day':
                entry.append(f"{record['funny_mark']}\n")  # Append funny meter for Joke of the Day

            # Append an additional newline after each block
            entry.append("\n")  # Add a newline separator after each record block
            data.extend(entry)  # Extend the list with the formatted record data

        # Remove the last newline (to avoid trailing newline at the file's end)
        if data and data[-1] == "\n":  
            data.pop()  # Remove the last newline if it exists

        return data  # Return the fully formatted data list

    def publish_record(self, data_type):  # Method to interactively publish a single record
        with open(self.file_path, 'a') as file:  # Opening the file in append mode
            file_size = self.check_file_size()  # Checking the size of the file

            if not path.exists(self.file_path) or (file_size == 0):  # If the file doesn't exist or is empty
                file.write("News feed:")  # Writing the header

            text = input('Please enter your text: ')  # Prompting the user to enter the text

            match data_type:  # Using a match-case statement to handle different data types
                case '1':  # If the user selects "1" (News)
                    city = input('Please enter the name of the city: ')  # Prompting for the city name
                    news = News(text, city)  # Creating a News object
                    file.write(news.get_news_body())  # Writing the formatted news body to the file
                    self.db.insert_news({'method': 'News', 'text': text, 'city': city, 'current_date': datetime.now().strftime('%Y-%m-%d %H:%M')})
                case '2':  # If the user selects "2" (Private Ad)
                    while True:  # Starting a loop to handle invalid date input
                        try:
                            expiration_date = input('Please enter the expiration date (dd/mm/yyyy): ')  # Prompting for expiration date
                            ad = PrivateAd(text, expiration_date)  # Creating a Private Ad object
                            file.write(ad.get_ad_body())  # Writing the formatted ad body to the file
                            self.db.insert_private_ad({'method': 'Private ad', 'text': text, 'actual_until': expiration_date, 'days_left': 
                                                       (datetime.strptime(expiration_date, '%d/%m/%Y').date() - datetime.now().date()).days})
                            break  # Breaking the loop if no exception occurs
                        except ValueError:  # Handling invalid date input
                            print("That's not a valid date. Please try again.")  # Prompting the user to try again
                case '3':  # If the user selects "3" (Joke)
                    joke = JokeOfTheDay(text)  # Creating a JokeOfTheDay object
                    file.write(joke.get_joke_body())  # Writing the formatted joke body to the file
                    self.db.insert_joke_of_the_day({'method': 'Joke of the day', 'text': text, 'funny_mark': joke.generate_mark()})

    def publish_records(self, records):  # Method to publish multiple records from a list
        with open(self.file_path, 'a') as file:  # Opening the file in append mode
            file_size = self.check_file_size()  # Checking the size of the file

            if not path.exists(self.file_path) or (file_size == 0):  # If the file doesn't exist or is empty
                file.write("News feed:\n")  # Writing the header
            else:
                file.write("\n")

            for record in records:  # Iterating over each record
                normalized_sentences = normalize_text_case(record)  # Normalize the record (returns a list of sentences)
                normalized_text = ' '.join(normalized_sentences)  # Join sentences with a period and add a trailing period
                file.write(f"{normalized_text}\n")  # Write the normalized text to the file

    def __del__(self):
        self.db.close()


class FileProcessor:
    def __init__(self, reader_path='data.txt', publisher_path='news_feed.txt'):
        self.reader = FileReader(reader_path)  # Pass the reader_path to the FileReader instance
        self.publisher = FilePublisher(publisher_path)  # Pass the publisher_path to the FilePublisher instance
        self.db = DBHandler()

    def process_file(self):
        list_of_dicts = self.reader.read_file()
        self.reader.delete_read_file()
        records = self.publisher.transform_to_text(list_of_dicts)
        self.publisher.publish_records(records)
        self.db.insert_processed_records(list_of_dicts)        

        self.db.close()


class JSONProcessor:

    def __init__(self, reader_path='data.json', publisher_path='news_feed.txt'):
        self.reader = JSONReader(reader_path) # Pass the reader_path to the JSONReader instance
        self.publisher = FilePublisher(publisher_path) # Pass the publisher_path to the FilePublisher instance
        self.db = DBHandler()

    def process_file(self):
        list_of_dicts = self.reader.load_file()
        self.reader.delete_read_file()
        records = self.publisher.transform_to_text(list_of_dicts)
        self.publisher.publish_records(records)
        self.db.insert_processed_records(list_of_dicts)        

        self.db.close()


class XMLProcessor:

    def __init__(self, reader_path='data.xml', publisher_path='news_feed.txt'):
        self.reader = XMLReader(reader_path) # Pass the reader_path to the JSONReader instance
        self.publisher = FilePublisher(publisher_path) # Pass the publisher_path to the FilePublisher instance
        self.db = DBHandler()

    def process_file(self):
        list_of_dicts = self.reader.read_file()
        self.reader.delete_read_file()
        records = self.publisher.transform_to_text(list_of_dicts)
        self.publisher.publish_records(records)
        self.db.insert_processed_records(list_of_dicts)

        self.db.close()


class CSVGenerator:

    def __init__(self, file_path: str = 'news_feed.txt'):
        self.file_path = file_path

    def get_text(self):
        with open(self.file_path) as file:
            text = file.read()
        text = text.replace('\n', ' ').replace('\r', '')
        text = sub(r'[^\w\s]|[\d]', ' ', text)  # Remove non-word characters and digits
        text = sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        return text

    def count_word(self):
        text = self.get_text().lower()
        words = text.split()
        words_counter = {}
        for word in words:
            words_counter[word] = words_counter.get(word, 0) + 1
        return words_counter

    def count_letter(self):
        letters = list(self.get_text())
        count_all_letters = len(letters)
        count_letter = []
        for letter in letters:
            if letter == ' ':
                continue
            upper = 0
            if letter.isupper():
                letter = letter.lower()
                upper = 1
            for dictionary in count_letter:
                if letter == dictionary.get('letter'):
                    dictionary['count_all'] += 1
                    dictionary['count_upper'] += upper
                    dictionary['percentage'] = (dictionary['count_all'] / count_all_letters)*100
                    break
            else:
                count_letter.append({'letter': letter, 'count_all': 1, 'count_upper': upper, 'percentage': (1/count_all_letters)*100})
        return count_letter

    def create_count_words_csv(self):
        count_words = self.count_word()
        with open('count_words.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter='-')
            for key, value in count_words.items():
                writer.writerow([key, value])

    def create_count_letters_csv(self):
        count_letter = self.count_letter()
        keys = count_letter[0].keys()
        with open('count_letters.csv', 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(count_letter)


while True:  # Starting an infinite loop to interact with the user
    print("\n------------------------------------------")  # Printing a separator
    method = input('How do you want to add a data? Please choose from the variants below:\n1 - Manually, 2 - From Text File, 3 - From JSON File, 4 - From XML File\nTo exit, type "exit"\n')  # Prompting the user for input method

    if method.lower() == 'exit':  # If the user selects "exit", break the loop and end the program
        break
    elif method == '1':  # If the user selects manual input
        data_type = input("What type of data do you want to add? Please choose from the variants below:\n1 - News, 2 - Private Ad, 3 - Joke\n")  # Prompting for data type
        publisher = FilePublisher()  # Creating an instance of FilePublisher
        publisher.publish_record(data_type)  # Publishing the record
        if data_type not in ('1', '2', '3'):  # If an invalid option is selected
            print('Unknown option was selected. Please try again')  # Prompting the user to try again
            continue  # Skipping the rest of the loop iteration
    elif method == '2':  # If the user selects file input
        location = input('Do you want to use default path file location or enter new?\n1 - Default, 2 - New\n')  # Prompting for file location
        if location == '1':  # If the user selects the default location
            processor = FileProcessor()
            processor.process_file()
        elif location == '2':  # If the user selects a new text file location
            new_location = input('Please enter new file location\n')  # Prompting for the new file path
            processor = FileProcessor(reader_path=new_location)  # Pass the new location to FileProcessor
            processor.process_file()
        else:  # If an invalid option is selected for the file location
            print('Unknown option was selected. Please try again\n')  # Prompting the user to try again
            continue  # Skipping the rest of the loop iteration
    elif method == '3':
        location = input('Do you want to use default path file location or enter new?\n1 - Default, 2 - New\n')
        if location == '1': # If the user selects the default location
            processor = JSONProcessor()
            processor.process_file()
        elif location == '2': # If the user selects a new json file location
            new_location = input('Please enter new file location\n') # Prompting for the new file path
            processor = JSONProcessor(reader_path=new_location) # Pass the new location to JSONProcessor
            processor.process_file()
    elif method == '4':
        location = input('Do you want to use default path file location or enter new?\n1 - Default, 2 - New\n')
        if location == '1': # If the user selects the default location
            processor = XMLProcessor()
            processor.process_file()
        elif location == '2': # If the user selects a new json file location
            new_location = input('Please enter new file location\n') # Prompting for the new file path
            processor = XMLProcessor(reader_path=new_location) # Pass the new location to XMLProcessor
            processor.process_file()
    else:  # If an invalid input method is selected
        print('Unknown option was selected. Please try again\n')  # Prompting the user to try again
        continue  # Skipping the rest of the loop iteration

csv_files = CSVGenerator()
csv_files.create_count_words_csv()
csv_files.create_count_letters_csv()
