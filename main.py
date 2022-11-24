from core.settings import PATH, USERNAME, PASSWORD
from pprint import pprint as print
from firefoxdriver.main import Bot

if __name__ == "__main__":
    Bot.driver_path = PATH
    bot = Bot(username=USERNAME, password=PASSWORD)
    bot.login()
    bot.get_profile("https://www.instagram.com/adis_kanatbekov_officiall/?next=%2F")
    bot.get_subscribers()
    bot.get_people_list()