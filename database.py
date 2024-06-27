from psycopg2 import connect

def connect_to_database():
    conexao = connect(
        dbname="postgres",
        user="postgres",
        password="genius",
        host="localhost",
        port="5432"
    )
    cursor = conexao.cursor()
    return conexao, cursor

def disconnect(conexao, cursor):
    cursor.close()
    conexao.close()

def get_column_names(cursor):
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'dataccm'")
    columns = [row[0] for row in cursor.fetchall()]
    return columns
