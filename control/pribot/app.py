from pathlib import Path
import configparser 

BASE_DIR = Path(__file__).resolve().parent.parent.parent
is_django_project = True

def configs(filedir):
    config = configparser.ConfigParser()
    config.read(filedir)
    return config


SETTINGS_CFG = BASE_DIR / 'settings.ini' if is_django_project else 'settings.ini'


BOT_TOKEN = configs(SETTINGS_CFG)["telegram"]["token"]


HOST = ''
SERVER_HOST = ''

REDIS_STORAGE = True