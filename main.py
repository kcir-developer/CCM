from flask import Flask, render_template, request, redirect, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:genius@localhost/postgres'
db = SQLAlchemy(app)


class DataCCM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Defina as colunas restantes aqui

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/')
def index():
    try:
        dados = DataCCM.query.all()
        total_registros = len(dados)
        return render_template('index.html', dados=dados, total_registros=total_registros)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/previous')
def previous_record():
    try:
        current_id = request.args.get('current_id')
        previous_record = DataCCM.query.filter(DataCCM.id < current_id).order_by(DataCCM.id.desc()).first()
        return render_template('index.html', form_data=previous_record.as_dict())
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/next')
def next_record():
    try:
        current_id = request.args.get('current_id')
        next_record = DataCCM.query.filter(DataCCM.id > current_id).order_by(DataCCM.id.asc()).first()
        return render_template('index.html', form_data=next_record.as_dict())
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/novo-registro', methods=['POST'])
def novo_registro():
    try:
        novo_registro_data = request.form.to_dict()
        novo_registro = DataCCM(**novo_registro_data)
        db.session.add(novo_registro)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/apagar-registro/<int:registro_id>', methods=['POST'])
def apagar_registro(registro_id):
    try:
        registro = DataCCM.query.get(registro_id)
        db.session.delete(registro)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/gravar-registro/<int:registro_id>', methods=['POST'])
def gravar_registro(registro_id):
    try:
        dados_formulario = request.form.to_dict()
        registro = DataCCM.query.get(registro_id)
        for key, value in dados_formulario.items():
            setattr(registro, key, value)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)