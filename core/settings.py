from dotenv import dotenv_values

env = dotenv_values(".env")

PATH = env.get('PATH')

USERNAME = env.get("USERNAME")

PASSWORD = env.get("PASSWORD")