# pylint: disable=E0401
import psycopg2
import configparser

# Leitura das informações de conexão com o banco de dados a partir do arquivo de configuração
config = configparser.ConfigParser()
config.read('login.ini')
db_user = config['postgresql']['db_user']
db_password = config['postgresql']['db_password']
db_host = config['postgresql']['db_host']
db_port = config['postgresql']['db_port']
db_name = config['postgresql']['db_name']

# Criação da conexão com o banco de dados
try:
    conn = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
        
    )
    print('Conectado')
except psycopg2.Error as e:
    print('Erro ao conectar ao banco de dados:', e)

# Exportação do objeto de conexão
def get_db():
    return conn
