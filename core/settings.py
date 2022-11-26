from dotenv import dotenv_values

env = dotenv_values(".env")

PATH_FIRE_FOX = env.get('PATH_FIRE_FOX')

PATH_CHROME = env.get('PATH_CHROME')

USERNAME = env.get("USERNAME")

PASSWORD = env.get("PASSWORD")