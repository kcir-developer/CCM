import dash
from dash import dcc, html, Input, Output, State
import pandas as pd

# Inicializando o aplicativo Dash
app = dash.Dash(__name__)

# Layout geral
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Página de entrada para a base de dados


def input_page():
    return html.Div([
        html.H1('Inserir Dados na Base de Dados'),
        html.Div([
            html.Label('Nome:'),
            dcc.Input(id='input-name', type='text', value=''),

            html.Label('Idade:'),
            dcc.Input(id='input-age', type='number', value=''),

            html.Button('Enviar', id='submit-val', n_clicks=0),
            html.Div(id='container-button-basic')
        ])
    ])

# Função de callback para inserir dados na base de dados


@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('input-name', 'value'),
     State('input-age', 'value')])
def insert_data(n_clicks, name, age):
    if n_clicks > 0:
        # Aqui você pode escrever o código para inserir os dados em sua base de dados
        # Neste exemplo, apenas exibimos uma mensagem de confirmação
        return html.Div([
            f'Dados inseridos na base de dados: Nome - {name}, Idade - {age}'
        ])

# Atualização do conteúdo da página com base na URL


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return input_page()
    else:
        return '404 - Página não encontrada'


if __name__ == '__main__':
    app.run_server(debug=True)
