from flask import Flask, render_template, request
import json
from database import Database

app = Flask(__name__)

# CORS(app)


db = Database()

@app.route('/listar_cartas')
def list_cartas():
    def db_query():
        cartas = db.list_cartas()
        return cartas
    res = db_query()
    return res
    # return render_template('index.html', result=res, content_type='application/json')

@app.route('/listar_decks')
def list_decks():
    def db_query():
        decks = db.list_decks()
        return decks
    res = db_query()
    return res
    
# app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True)
