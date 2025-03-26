from datetime import datetime
from random import choice
from os import path, remove
from HW_4_3 import normalize_text_case


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


class FileReader:  # Creating a class to handle file reading operations
    def __init__(self, file_path: str = 'data.txt'):  # Constructor to initialize the file path
        self.file_path = file_path  # Storing the file path in an instance variable

    def read_file(self):  # Method to read records from the file
        records = []  # Initializing an empty list to store records
        with open(self.file_path, 'r', encoding='utf8') as file:  # Opening the file in read mode with UTF-8 encoding
            records = file.readlines()  # Reading all lines into the list
        return records  # Returning the list of records

    def delete_read_file(self):  # Method to delete the file after its content is read
        remove(self.file_path)  # Using the remove function to delete the file


class FilePublisher:  # Creating a class to handle file writing operations
    def __init__(self, file_path: str = 'news_feed.txt'):  # Constructor to initialize the file path
        self.file_path = file_path  # Storing the file path in an instance variable

    def check_file_size(self):  # Method to check the size of the file
        return path.getsize(self.file_path)  # Returning the size of the file in bytes

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
                case '2':  # If the user selects "2" (Private Ad)
                    while True:  # Starting a loop to handle invalid date input
                        try:
                            expiration_date = input('Please enter the expiration date (dd/mm/yyyy): ')  # Prompting for expiration date
                            ad = PrivateAd(text, expiration_date)  # Creating a Private Ad object
                            file.write(ad.get_ad_body())  # Writing the formatted ad body to the file
                            break  # Breaking the loop if no exception occurs
                        except ValueError:  # Handling invalid date input
                            print("That's not a valid date. Please try again.")  # Prompting the user to try again
                case '3':  # If the user selects "3" (Joke)
                    joke = JokeOfTheDay(text)  # Creating a JokeOfTheDay object
                    file.write(joke.get_joke_body())  # Writing the formatted joke body to the file

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


while True:  # Starting an infinite loop to interact with the user
    print("\n------------------------------------------")  # Printing a separator
    method = input('How do you want to add a data? Please choose from the variants below:\n1 - Manually, 2 - From File\nTo exit, type "exit"\n')  # Prompting the user for input method

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
            reader = FileReader()  # Creating an instance of FileReader with the default path
            records = reader.read_file()  # Reading records from the file
            reader.delete_read_file()  # Deleting the file after reading
            publisher = FilePublisher()  # Creating an instance of FilePublisher
            publisher.publish_records(records)  # Publishing the read records
        elif location == '2':  # If the user selects a new file location
            new_location = input('Please enter new file location\n')  # Prompting for the new file path
            reader = FileReader(new_location)  # Creating an instance of FileReader with the new path
            records = reader.read_file()  # Reading records from the file
            reader.delete_read_file()  # Deleting the file after reading
            publisher = FilePublisher()  # Creating an instance of FilePublisher
            publisher.publish_records(records)  # Publishing the read records
        else:  # If an invalid option is selected for the file location
            print('Unknown option was selected. Please try again\n')  # Prompting the user to try again
            continue  # Skipping the rest of the loop iteration
    else:  # If an invalid input method is selected
        print('Unknown option was selected. Please try again\n')  # Prompting the user to try again
        continue  # Skipping the rest of the loop iteration