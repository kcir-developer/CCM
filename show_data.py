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


def get_data_from_table(cursor):
    try:
        # Código para obter os dados da tabela do banco de dados
        cursor.execute("SELECT * FROM dataccm")
        data = cursor.fetchall()
        return data
    except psycopg2.Error as e:
        print("Erro ao obter dados da tabela:", e)
        return []


@app.route('/')
def show_data():
    # Conecta ao banco de dados
    conexao, cursor = connect_to_db()

    # Obtém os dados da tabela
    data = get_data_from_table(cursor)

    # Desconecta do banco de dados
    disconnect_from_db(conexao, cursor)

    # Renderiza o template HTML para exibir os dados da tabela
    return render_template('show_data.html', data=data)


# if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=3000, debug=True)
