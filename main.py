from flask import Flask, render_template, request, redirect, url_for
from psycopg2 import connect
from database import disconnect, get_column_names

app = Flask(__name__, template_folder='.')

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

       # Dentro da função index()
        total_registos = len(dados)

        # Passa os dados para o template, juntamente com o número total de registos
        return render_template('index.html', columns=columns, dados=dados, total_registos=total_registos)

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


@app.route('/novo-registo', methods=['POST'])
def novo_registo():
    try:
        connect_to_database()
        # Obtenha os dados do formulário
        novo_registo_data = {}
        for column in request.form:
            novo_registo_data[column] = request.form[column]

        # Insira o novo registo no banco de dados
        cursor.execute("INSERT INTO dataccm (coluna1, coluna2, ...) VALUES (%s, %s, ...)",
                       (novo_registo_data['coluna1'], novo_registo_data['coluna2'], ...))
        conexao.commit()  # Não esqueça de comitar a transação
        # Redireciona de volta para a página inicial
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))
    finally:
        disconnect_from_database()


@app.route('/apagar-registo/<int:registro_id>', methods=['POST'])
def apagar_registo(registro_id):
    try:
        connect_to_database()
        # Apague o registo do banco de dados
        cursor.execute("DELETE FROM dataccm WHERE id = %s", (registro_id,))
        conexao.commit()  # Não esqueça de comitar a transação
        # Redireciona de volta para a página inicial
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))
    finally:
        disconnect_from_database()


@app.route('/gravar-registo/<int:registro_id>', methods=['POST'])
def gravar_registo(registro_id):
    try:
        connect_to_database()
        # Obtenha os dados do formulário
        dados_formulario = {}
        for column in request.form:
            dados_formulario[column] = request.form[column]

        # Atualize o registo no banco de dados
        update_query = "UPDATE dataccm SET "
        update_query += ", ".join(
            [f"{coluna} = %s" for coluna in dados_formulario.keys()])
        update_query += " WHERE id = %s"
        cursor.execute(update_query, list(
            dados_formulario.values()) + [registro_id])
        conexao.commit()  # Não esqueça de comitar a transação
        # Redireciona de volta para a página inicial
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))
    finally:
        disconnect_from_database()


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
