from flask import Flask, render_template
import psycopg2

app = Flask(__name__)


def connect_to_db():
    # Código de conexão com o banco de dados
    conexao = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="genius"
    )
    cursor = conexao.cursor()
    return conexao, cursor


def disconnect_from_db(conexao, cursor):
    # Código para desconectar do banco de dados
    cursor.close()
    conexao.close()


def get_columns_from_table(cursor):
    try:
        # Código para obter as colunas da tabela do banco de dados
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'dataccm' AND table_schema = 'public'")
        columns = [column[0] for column in cursor.fetchall()]
        return columns
    except psycopg2.Error as e:
        print("Erro ao obter colunas da tabela:", e)
        return []


@app.route('/')
def show_columns():
    # Conecta ao banco de dados
    conexao, cursor = connect_to_db()

    # Obtém os nomes das colunas da tabela
    columns = get_columns_from_table(cursor)

    # Desconecta do banco de dados
    disconnect_from_db(conexao, cursor)

    # Renderiza o template HTML para exibir os nomes das colunas
    return render_template('show_columns.html', columns=columns)


# if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=3000, debug=True)
