from flask import Flask, jsonify
import mysql.connector

class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "hogwarts"
        db = "CLASHROYALE"
        self.con = mysql.connector.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor()
    def add_deck(self, descricao, nome, custo, data_criacao, cartas):
        self.cur.execute(f"INSERT INTO decks(descricao, nome, custo, data_criacao) VALUES ({descricao}, {nome}, {custo}, {data_criacao})")
        codigo_deck = self.cur.execute(f"SELECT (codigo_deck) FROM decks")
        for i in cartas:
            numero_carta = i["numero_carta"]
            index_carta = i["index_carta"]
            self.cur.execute(f"INSERT INTO deck_cartas(numero_carta, index_carta) VALUES ({numero_carta}, {index_carta} WHERE codigo_deck={codigo_deck}")
        result = self.cur.fetchall()
        return result
    def remove_deck(self, codigo_deck):
        self.cur.execute(f"DELETE * FROM deck_cartas WHERE codigo_deck={codigo_deck} ") 
        self.cur.execute(f"DELETE * FROM decks WHERE codigo_deck={codigo_deck} ")
        result = self.cur.fetchall()
        return result
    def update_deck(self, codigo_deck, nome, descricao, cartas):
        self.cur.execute(f"UPDATE decks SET (nome={nome}, descricao={descricao}) WHERE codigo_deck={codigo_deck} ")
        for i in cartas:
            numero_carta = i["numero_carta"]
            index_carta = i["index_carta"]
            self.cur.execute(f"UPDATE deck_cartas SET numero_carta={numero_carta}, index_carta={index_carta}, WHERE codigo_deck={codigo_deck}")
        self.cur.execute(f"UPDATE decks SET custo=(SELECT AVG(c.custo) FROM deck_cartas AS dc, cartas AS c WHERE dc.{numero_carta}=c.{numero_carta}) WHERE codigo_deck={codigo_deck}")
        result = self.cur.fetchall()
        return result
    def list_cartas(self):
        self.cur.execute("SELECT numero_carta,nome, custo FROM cartas")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        res = self.cur.fetchall()
        json_data={}
        for result in res:
            json_data[result[0]] = {row_headers[1] : result[1], row_headers[2] : result[2]}
        return jsonify(json_data)
    def list_decks(self):
        self.cur.execute("SELECT dc.codigo_deck, dc.numero_carta, c.nome, c.custo, dc.index_carta FROM deck_cartas as dc, cartas as c WHERE dc.numero_carta = c.numero_carta;")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        res = self.cur.fetchall()
        json_data={}
        temp = {}
        for result in res:
            temp[result[1]] = {row_headers[2] : result[2],row_headers[3] : result[3],row_headers[4] : result[4]}
        json_data[result[0]] = temp 
        return jsonify(json_data)
    def find_carta(self, nome):
        self.cur.execute("SELECT * FROM cartas WHERE nome={nome}")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        res = self.cur.fetchall()
        json_data={}
        for result in res: 
            json_data[result[0]] = {row_headers[1] : result[1], row_headers[2] : result[2]}
        return jsonify(json_data)