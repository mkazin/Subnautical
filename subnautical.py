import os

user = 'subnautical'
password = 'Eet2nTMBjlEB0Qev'
database = 'Subnautical'

config = {
    # 'db': database,
    'host': f"mongodb+srv://{user}:{password}@cluster0.xg0kc.mongodb.net/{database}",
    # 'host': 'mongodb+srv://cluster0.xg0kc.mongodb.net',
    # 'port': 12345
}
#    f'mongodb+srv://{username}:{password}@cluster0.xg0kc.mongodb.net/{database}?retryWrites=true&w=majority')

app_config = {
    'ROOT_PATH': os.path.dirname(os.path.abspath(__file__))
}
