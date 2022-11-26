from core.settings import PATH_FIRE_FOX, PATH_CHROME, USERNAME, PASSWORD
from pprint import pprint as print
from firefoxdriver.main import Bot

if __name__ == "__main__":
    Bot.driver_path = PATH_CHROME
    bot = Bot(username=USERNAME, password=PASSWORD)
    bot.login()
    bot.get_profile("https://www.instagram.com/didarmatiyev/?next=%2F")
    bot.get_subscribers()
    bot.get_people_list()