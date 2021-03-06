from flask import Flask, request
from database import Database
from ast import literal_eval

app = Flask(__name__)

db = Database()


@app.route('/add_deck', methods=["POST"])
def add_deck():
    description = request.args.get('description', None)
    name = request.args.get('name', None)
    elixir_cost = request.args.get('elixir_cost', None)
    cards = literal_eval(request.args.get('cards', None))
    decks = db.add_deck(name, description, elixir_cost, cards)
    db.cur.close()
    db.con.close()
    return decks

@app.route('/remove_deck', methods=["POST"])
def remove_deck():
    deck_code = str(request.args.get('deck_code'))
    res = db.remove_deck(deck_code)
    db.cur.close()
    db.con.close()
    return res

@app.route('/update_deck', methods=["POST"])
def update_deck():
    deck_code = request.args.get('deck_code')
    description = request.args.get('description')
    name = request.args.get('name')
    elixir_cost = request.args.get('elixir_cost', None)
    cards = literal_eval(request.args.get('cards', None))
    res = db.update_deck(deck_code, name, description, elixir_cost, cards)
    db.cur.close()
    db.con.close()
    return res    

@app.route('/list_cards', methods=["GET"])
def list_cards():
    cards = db.list_cards()
    db.cur.close()
    db.con.close()
    return cards

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

if __name__ == '__main__':
    # You might want to use a custom port:
    # app.run(host='0.0.0.0', port=5000)
    
    app.run(debug=True)
