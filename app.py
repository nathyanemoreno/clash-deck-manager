from flask import Flask, render_template, request
import json
from database import Database
from ast import literal_eval


app = Flask(__name__)

# CORS(app)


db = Database()


@app.route('/add_deck')
def add_deck(db):
    descricao = request.args.descricao
    nome = request.args.nome
    custo = request.args.custo
    data_criacao = request.args.data_criacao
    cartas = literal_eval(request.args.cartas)
    decks = db.add_deck(descricao, nome, custo, data_criacao, cartas)
    return decks

@app.route('/listar_cartas')
def list_cartas():
    cartas = db.list_cartas()
    return cartas

    # return render_template('index.html', result=res, content_type='application/json')

@app.route('/listar_decks')
def list_decks():
    decks = db.list_decks()
    return decks

@app.route('/remove_deck')
def remove_deck():
    codigo_deck = int(request.args.codigo_deck)
    res = db.remove_deck(codigo_deck)
    return res

@app.route('/update_deck')
def update_deck():
    codigo_deck = int(request.args.codigo_deck)
    descricao = request.args.descricao
    nome = request.args.nome
    cartas = literal_eval(request.args.cartas)
    res = db.update_deck(codigo_deck, nome, descricao,cartas)
    return res    

@app.route('/find_carta')
def find_carta():
    nome = request.args.nome
    res = db.find_carta(nome)
    return res    


# app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True)
