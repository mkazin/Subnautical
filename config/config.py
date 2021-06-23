import configparser
import os

CONFIG_FILE = 'config/subnautical.conf'

config = configparser.RawConfigParser()

try:
     config.read(CONFIG_FILE)
     user = config.get('DB', 'user')
     password = config.get('DB', 'password')
     database = config.get('DB', 'database')
     hostname = config.get('DB', 'hostname')
except ValueError:
     print(f"ERROR: Expected configuraion file at {CONFIG_FILE}. See sample configuration file. Exiting.")
     exit(-1)

try:
     server = config['Server']
except KeyError:
     server = {}
port = server.get('port', 5000)
host = server.get('host', 'localhost')

mongo = {
    'host': f"mongodb+srv://{user}:{password}@{hostname}/{database}?retryWrites=true&w=majority",
    # 'port': 12345
}
server = {
    'port': port,
    'host': host,
}
app_config = {
    'ROOT_PATH': os.path.dirname(os.path.abspath(__file__))
}
