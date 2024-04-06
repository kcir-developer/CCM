from urllib import request
from flask import Flask, redirect, render_template, url_for
from database import connect_to_db, get_columns_from_table, insert_data_into_table
from show_columns import disconnect_from_db

app = Flask(__name__)


@app.route('/')
def index():
    conexao, cursor = connect_to_db()
    columns = get_columns_from_table(cursor)
    disconnect_from_db(conexao, cursor)
    return render_template('index.html', columns=columns)


@app.route('/new', methods=['GET', 'POST'])
def new_record():
    if request.method == 'POST':
        conexao, cursor = connect_to_db()
        columns = get_columns_from_table(cursor)

        # Preenche o dicionário com os valores dos campos do formulário
        data = {column: request.form[column] for column in columns}

        # Converte os valores para tipos de dados compatíveis com o PostgreSQL, se necessário
        for key, value in data.items():
            if value is None:
                data[key] = 'NULL'
            elif isinstance(value, str):
                data[key] = "'" + value.replace("'", "''") + "'"
            else:
                data[key] = str(value)

        # Executa a inserção no banco de dados
        insert_data_into_table(conexao, cursor, data)

        # Comita a transação e fecha a conexão
        conexao.commit()
        disconnect_from_db(conexao, cursor)

        return redirect(url_for('index'))
    else:
        # Se a solicitação for GET, renderize um formulário com todos os campos para adicionar um novo registro
        conexao, cursor = connect_to_db()
        columns = get_columns_from_table(cursor)
        disconnect_from_db(conexao, cursor)
        return render_template('new_record.html', columns=columns)


# if __name__ == '__main__':
#   app.run(host='127.0.0.1', port=3000, debug=True)
