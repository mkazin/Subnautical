import configparser
import os

config = configparser.RawConfigParser()
config.read('config/subnautical.conf')

user = config.get('DB', 'user')
password = config.get('DB', 'password')
database = config.get('DB', 'database')
hostname = config.get('DB', 'hostname')

config = {
    'host': f"mongodb+srv://{user}:{password}@{hostname}/{database}?retryWrites=true&w=majority",
    # 'port': 12345
}
app_config = {
    'ROOT_PATH': os.path.dirname(os.path.abspath(__file__))
}
