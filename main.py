from flask import Flask, render_template, request
from psycopg2 import connect
from database import disconnect, get_column_names

app = Flask(__name__)

# Conectar ao banco de dados ao iniciar a aplicação Flask
conexao, cursor = None, None


def connect_to_database():
    global conexao, cursor
    conexao = connect(
        dbname="postgres",
        user="postgres",
        password="genius",
        host="localhost",
        port="5432"
    )
    cursor = conexao.cursor()


def disconnect_from_database():
    global conexao, cursor
    if cursor:
        cursor.close()
    if conexao:
        conexao.close()


def get_previous_record(cursor, current_date):
    cursor.execute(
        #   "SELECT * FROM dataccm", (current_date,))
        "SELECT * FROM dataccm WHERE servico < %s ORDER BY servico DESC LIMIT 1", (current_date,))
    previous_record = cursor.fetchone()
    return previous_record if previous_record else {}


def get_next_record(cursor, current_date):
    cursor.execute(
        #   "SELECT * FROM dataccm", (current_date,))
        "SELECT * FROM dataccm WHERE servico > %s ORDER BY servico ASC LIMIT 1", (current_date,))
    next_record = cursor.fetchone()
    return next_record if next_record else {}


@app.route('/')
def index():
    try:
        connect_to_database()
        # Obtém os nomes das colunas da tabela
        columns = get_column_names(cursor)

        cursor.execute("SELECT * FROM dataccm")
        rows = cursor.fetchall()

        # Monta os dados em uma estrutura adequada para serem passados para o template
        dados = []
        for row in rows:
            # Cada linha será um dicionário onde as chaves são os nomes das colunas e os valores são os dados correspondentes
            dados.append({columns[i]: row[i] for i in range(len(columns))})

      #  print(dados)  # Adicione esta linha para imprimir os dados

        # Passa os dados para o template
        return render_template('index.html', columns=columns, dados=dados)

    except Exception as e:
        # Em caso de erro, renderiza a página de erro
        return render_template('error.html', message=str(e))
    finally:
        disconnect_from_database()


@app.route('/previous')
def previous_record():
    try:
        connect_to_database()
        current_id = request.args.get('current_id')
        previous_record_data = get_previous_record(cursor, current_id)
        columns = get_column_names(cursor)  # Obtém os nomes das colunas
        return render_template('index.html', columns=columns, form_data=previous_record_data)
    except Exception as e:
        return render_template('error.html', message=str(e))
    finally:
        disconnect_from_database()


@app.route('/next')
def next_record():
    try:
        connect_to_database()
        current_id = request.args.get('current_id')
        next_record_data = get_next_record(cursor, current_id)
        columns = get_column_names(cursor)  # Obtém os nomes das colunas
        return render_template('index.html', columns=columns, form_data=next_record_data)
    except Exception as e:
        return render_template('error.html', message=str(e))
    finally:
        disconnect_from_database()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
