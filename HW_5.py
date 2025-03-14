from datetime import datetime
from random import choice
from os import path


class News:
    def __init__(self, text: str, city: str) -> None:
        self.text = text
        self.city = city

    def get_news_body(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        return f"\nNews -------------------------\n{self.text}\n{self.city}, {current_time}\n"


class PrivateAd:
    def __init__(self, text: str, expiration_date: str) -> None:
        self.text = text
        self.expiration_date = datetime.strptime(expiration_date, '%d/%m/%Y').date()

    def get_ad_body(self):
        delta = (self.expiration_date - datetime.now().date()).days
        delta_message = f"{delta} days left" if delta >= 0 else "expired"
        return f"\nPrivate Ad ------------------\n{self.text}\nActual until: {self.expiration_date}, {delta_message}\n"


class JokeOfTheDay:
    def __init__(self, text: str) -> None:
        self.text = text

    def generate_mark(self):
        marks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        return f"Funny meter - {choice(marks)} out of 10"

    def get_joke_body(self):
        funny_meter = self.generate_mark()
        return f"\nJoke of the day ------------\n{self.text}\n{funny_meter}\n"


def add_header_if_needed(file_path: str):
    if not path.exists(file_path) or path.getsize(file_path) == 0:
        with open(file_path, 'a') as file:
            file.write("News feed:\n")


file_path = 'news_feed.txt'


while True:
    print("------------------------------------------")
    data_type = input("What type of data do you want to add? Please choose from the variants below:\n1 - News, 2 - Private Ad, 3 - Joke\nTo exit, type 'exit'\n")

    if data_type.lower() == 'exit':
        break
    elif data_type not in ('1', '2', '3'):
        print('Unknown option was selected. Please try again.')
        continue

    text = input('Please enter your text: ')
    add_header_if_needed(file_path)

    with open(file_path, 'a') as file:
        match data_type:                
            case '1':
                city = input('Please enter the name of the city: ')
                news = News(text, city)
                file.write(news.get_news_body())
            case '2':
                while True:
                    try:
                        expiration_date = input('Please enter the expiration date (dd/mm/yyyy): ')
                        ad = PrivateAd(text, expiration_date)
                        file.write(ad.get_ad_body())
                        break
                    except ValueError:
                        print("That's not a valid date. Please try again.")
            case '3':
                joke = JokeOfTheDay(text)
                file.write(joke.get_joke_body())

print("Thank you for using the news feed generator!")
