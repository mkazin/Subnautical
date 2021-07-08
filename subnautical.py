import configparser
import os

parser = configparser.RawConfigParser()
parser.read('config/subnautical.conf')

user = parser.get('DB', 'user')
password = parser.get('DB', 'password')
database = parser.get('DB', 'database')
hostname = parser.get('DB', 'hostname')

app_host = parser.get('Server', 'host')
app_port = parser.get('Server', 'port')
app_domain = parser.get('Server', 'domain')

GOOGLE_CLIENT_ID = parser.get('OAUTH', "GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = parser.get('OAUTH', "GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

config = {
    'host': f"mongodb+srv://{user}:{password}@{hostname}/{database}?retryWrites=true&w=majority",
    # 'port': 12345
}
app_config = {
    'ROOT_PATH': os.path.dirname(os.path.abspath(__file__))
}
