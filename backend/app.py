from flask import Flask, render_template, request
import json
from database import Database
from ast import literal_eval


app = Flask(__name__)

db = Database()


@app.route('/add_deck', methods=["POST"])
def add_deck():
    descricao = request.args.get('descricao', None)
    nome = request.args.get('nome', None)
    custo = request.args.get('custo', None)
    cartas = literal_eval(request.args.get('cartas', None))
    decks = db.add_deck(nome,descricao, custo, cartas)
    db.cur.close()
    db.con.close()
    return decks

@app.route('/remove_deck', methods=["POST"])
def remove_deck():
    codigo_deck = str(request.args.get('codigo_deck'))
    res = db.remove_deck(codigo_deck)
    db.cur.close()
    db.con.close()
    return res

@app.route('/update_deck', methods=["POST"])
def update_deck():
    codigo_deck = request.args.get('codigo_deck')
    descricao = request.args.get('descricao')
    nome = request.args.get('nome')
    custo = request.args.get('custo', None)
    cartas = literal_eval(request.args.get('cartas', None))
    res = db.update_deck(codigo_deck, nome, descricao, custo, cartas)
    db.cur.close()
    db.con.close()
    return res    

@app.route('/list_cartas', methods=["GET"])
def list_cartas():
    cartas = db.list_cartas()
    db.cur.close()
    db.con.close()
    return cartas

    # return render_template('index.html', result=res, content_type='application/json')

@app.route('/list_decks', methods=["GET"])
def list_decks():
    decks = db.list_decks()
    db.cur.close()
    db.con.close()
    return decks

@app.route('/find_deck', methods=["GET"])
def find_deck():
    query = request.args.get('query')
    res = db.find_deck(query)
    db.cur.close()
    db.con.close()
    return res    

# app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True)
