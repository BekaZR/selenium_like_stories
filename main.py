from core.settings import PATH_FIRE_FOX, PATH_CHROME, USERNAME, PASSWORD
from pprint import pprint as print
from firefoxdriver.main import Bot

if __name__ == "__main__":
    Bot.driver_path = PATH_FIRE_FOX
    bot = Bot(username=USERNAME, password=PASSWORD)
    bot.login()
    bot.get_user_profile("timurkhan.97/")
    bot.get_user_subscribers()
    bot.get_user_profile("timurkhan.97/")
    bot.get_all_post()