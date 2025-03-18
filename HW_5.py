from datetime import datetime
from random import choice
from os import path


class News:  # Creating a class to handle News objects
    def __init__(self, text: str, city: str) -> None:  # Constructor accepting text (news body) and city as arguments
        self.text = text  # Storing the news body in an instance variable
        self.city = city  # Storing the city name in an instance variable

    def get_news_body(self):  # Method to format and return the news body
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')  # Getting the current date and time in a specific format
        return f"\nNews -------------------------\n{self.text}\n{self.city}, {current_time}\n"  # Returning the formatted news string


class PrivateAd:  # Creating a class to handle Private Ad objects
    def __init__(self, text: str, expiration_date: str) -> None:  # Constructor accepting text and expiration date
        self.text = text  # Storing the ad text in an instance variable
        self.expiration_date = datetime.strptime(expiration_date, '%d/%m/%Y').date()  # Converting the expiration date string into a date object

    def get_ad_body(self):  # Method to format and return the ad body
        delta = (self.expiration_date - datetime.now().date()).days  # Calculating the number of days until expiration
        delta_message = f"{delta} days left" if delta >= 0 else "expired"  # Creating a message depending on whether the ad has expired
        return f"\nPrivate Ad ------------------\n{self.text}\nActual until: {self.expiration_date}, {delta_message}\n"  # Returning the formatted ad string


class JokeOfTheDay:  # Creating a class to handle Joke of the Day objects
    def __init__(self, text: str) -> None:  # Constructor accepting the joke text
        self.text = text  # Storing the joke text in an instance variable

    def generate_mark(self):  # Method to generate a random "funny meter" rating
        marks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # Defining a list of possible ratings
        return f"Funny meter - {choice(marks)} out of 10"  # Returning a randomly selected rating

    def get_joke_body(self):  # Method to format and return the joke body
        funny_meter = self.generate_mark()  # Generating the funny meter rating
        return f"\nJoke of the day ------------\n{self.text}\n{funny_meter}\n"  # Returning the formatted joke string


def add_header_if_needed(file_path: str):  # Function to add a header to the file if it's empty or doesn't exist
    if not path.exists(file_path) or path.getsize(file_path) == 0:  # Checking if the file doesn't exist or is empty
        with open(file_path, 'a') as file:  # Opening the file in append mode
            file.write("News feed:\n")  # Writing the header to the file


file_path = 'news_feed.txt'  # Path to the file where news, ads, and jokes will be stored


while True:  # Starting an infinite loop to interact with the user
    print("------------------------------------------")  # Printing a separator
    data_type = input("What type of data do you want to add? Please choose from the variants below:\n1 - News, 2 - Private Ad, 3 - Joke\nTo exit, type 'exit'\n")  # Prompting the user to select the type of data to add

    if data_type.lower() == 'exit':  # If the user types "exit", break the loop and stop the program
        break
    elif data_type not in ('1', '2', '3'):  # If the user selects an invalid option
        print('Unknown option was selected. Please try again.')  # Notify the user about the invalid option
        continue  # Skip the rest of the loop and ask again

    text = input('Please enter your text: ')  # Prompting the user to enter the main text for the News, Private Ad, or Joke
    add_header_if_needed(file_path)  # Adding the header to the file if needed

    with open(file_path, 'a') as file:  # Opening the file in append mode to add new content
        match data_type:  # Using a match-case statement to handle different data types
            case '1':  # If the user selected "1" (News)
                city = input('Please enter the name of the city: ')  # Prompting the user to enter the city name
                news = News(text, city)  # Creating a News object with the entered text and city
                file.write(news.get_news_body())  # Writing the formatted news body to the file
            case '2':  # If the user selected "2" (Private Ad)
                while True:  # Start a loop to handle possible invalid date input
                    try:
                        expiration_date = input('Please enter the expiration date (dd/mm/yyyy): ')  # Prompting the user to enter the expiration date
                        ad = PrivateAd(text, expiration_date)  # Creating a Private Ad object with the entered text and expiration date
                        file.write(ad.get_ad_body())  # Writing the formatted ad body to the file
                        break  # Exit the loop if no exception is raised
                    except ValueError:  # Handling the case where the entered date is invalid
                        print("That's not a valid date. Please try again.")  # Prompt the user to try again
            case '3':  # If the user selected "3" (Joke)
                joke = JokeOfTheDay(text)  # Creating a JokeOfTheDay object with the entered text
                file.write(joke.get_joke_body())  # Writing the formatted joke body to the file

print("Thank you for using the news feed generator!")  # Messaging the user after exiting the loop