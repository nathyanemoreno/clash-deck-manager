from flask import Flask, render_template, request
import json
from database import Database
from ast import literal_eval

app = Flask(__name__)

db = Database()

@app.route('/add_deck', methods=["GET"])
def add_deck():
    codigo_deck = request.args.get('codigo_deck', 0)
    descricao = request.args.get('descricao', None)
    nome = request.args.get('nome', None)
    custo = request.args.get('custo', None)
    # data_criacao = request.args.get('data_criacao')
    cartas = request.args.get('cartas', None)
    decks = db.add_deck(descricao, nome, custo, cartas, codigo_deck)
    return decks

@app.route('/remove_deck', methods=["POST"])
def remove_deck():
    codigo_deck = int(request.args.codigo_deck)
    res = db.remove_deck(codigo_deck)
    return res

@app.route('/update_deck', methods=["POST"])
def update_deck():
    codigo_deck = int(request.args.codigo_deck)
    descricao = request.args.descricao
    nome = request.args.nome
    cartas = literal_eval(request.args.cartas)
    res = db.update_deck(codigo_deck, nome, descricao,cartas)
    return res    

@app.route('/list_cartas', methods=["GET"])
def list_cartas():
    cartas = db.list_cartas()
    return cartas

    # return render_template('index.html', result=res, content_type='application/json')

@app.route('/list_decks', methods=["GET"])
def list_decks():
    decks = db.list_decks()
    return decks

@app.route('/find_carta', methods=["GET"])
def find_carta():
    nome = request.args.get('nome')
    res = db.find_carta(nome)
    return res    


# app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True)
