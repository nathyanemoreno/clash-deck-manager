from flask import Flask, jsonify
import mysql.connector
from ast import literal_eval
import re 
from datetime import datetime

class Database:
    def _init_(self):
        pass
    def createConnection(self):
        host = "localhost"
        user = "root"
        password = "hogwarts"
        db = "CLASHROYALE"
        self.con = mysql.connector.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor()
    def add_deck(self, nome, descricao, custo, cartas):
        self.createConnection()
        query_deck = "INSERT INTO decks(nome , descricao, custo,data_criacao) VALUES (%s, %s, %s, %s)"
        data_criacao = datetime.today().strftime("%Y-%m-%d")
        recordTuple = (nome, descricao, custo, data_criacao)
        self.cur.execute(query_deck, recordTuple)
        codigo_deck = self.cur.lastrowid
        query = "INSERT INTO deck_cartas(codigo_deck, numero_carta, index_carta) VALUES (%s, %s, %s)"
        for carta in cartas:
            self.cur.execute(query, (codigo_deck,carta["numero_carta"], 1+carta["index_carta"]))
        self.con.commit()
        return "Record inserted successfully"
    def remove_deck(self, codigo_deck):
        self.createConnection()
        query1 = "DELETE FROM `deck_cartas` WHERE codigo_deck=%s"
        query2 = "DELETE FROM `decks` WHERE codigo_deck=%s"
        self.cur.execute(query1, (codigo_deck,)) 
        self.cur.execute(query2, (codigo_deck,))
        self.con.commit()
        return "Record removed successfully"
    def update_deck(self, codigo_deck, nome, descricao,custo,cartas):
        self.createConnection()
        query1 = "UPDATE decks SET nome=%s, descricao=%s, custo=%s WHERE codigo_deck=%s" 
        self.cur.execute(query1, (nome, descricao, custo, codigo_deck,))
        for i in cartas:    
            query2 = "INSERT INTO deck_cartas(codigo_deck, numero_carta, index_carta) VALUES (%s,%s,%s) \
                      ON DUPLICATE KEY UPDATE numero_carta=%s"
            self.cur.execute(query2, (codigo_deck, i["numero_carta"], 1+i["index_carta"], i["numero_carta"]))
        self.con.commit()
        return "Updated successfully"
    def list_cartas(self):
        self.createConnection()
        self.cur.execute("SELECT numero_carta,nome, custo, raridade FROM cartas")
        res = self.cur.fetchall()
        self.con.commit()
        json_data = {}
        for result in res:
            json_data[result[0]] = {"numero_carta" : result[0], "nome" : result[1], "custo" : result[2], "raridade" : result[3]}
        return jsonify(json_data)
    def list_decks(self):
        self.createConnection()
        self.cur.execute("SELECT d.*, c.* FROM decks as d \
                            JOIN deck_cartas as dc ON dc.codigo_deck = d.codigo_deck \
                            JOIN cartas as c ON c.numero_carta = dc.numero_carta")
        res = self.cur.fetchall()
        decks = {}
        for i in res:
            # 0 -> codigo_deck
            # 1 -> descricao_deck
            # 2 -> nome_deck
            # 3 -> custo_deck
            # 4 -> data_criacao_deck
            # 5 -> carta_index
            # 6 -> carta_nome
            # 7 -> carta_raridade
            # 8 -> carta_custo
            carta = {
                "numero_carta": i[5],
                "carta_nome": i[6],
                "carta_raridade": i[7],
                "carta_custo": float(i[8])
            }
            if (f"Deck{i[0]}" in decks.keys()):
                temp = decks[f"Deck{i[0]}"]["cartas"]
                temp.append(carta)
                decks[f"Deck{i[0]}"]["cartas"] = temp
            else:
                deck = {
                    "codigo_deck": i[0],
                    "descrico": i[1],
                    "nome": i[2],
                    "custo": float(i[3]),
                    "data_criacao": f"{i[4].day}/{i[4].month}/{i[4].year}",
                    "cartas": [carta]
                }
                decks[f"Deck{i[0]}"] = deck
        response = {"decks": list(decks.values())}
        return jsonify(response)
    def find_deck(self, criterio):
        self.createConnection()
        if criterio.isnumeric():
            query = "SELECT d.* , c.* FROM decks as d \
                JOIN deck_cartas as dc ON dc.codigo_deck = d.codigo_deck \
                    JOIN cartas as c ON c.numero_carta = dc.numero_carta \
                    WHERE dc.codigo_deck = %s"
        if bool(re.match("\d\d\d\d-\d\d-\d\d", '-'.join(criterio.split('/')[::-1]))):
            criterio = '-'.join(criterio.split('/')[::-1])
            query = "SELECT d.* , c.* FROM decks as d \
                JOIN deck_cartas as dc ON dc.codigo_deck = d.codigo_deck \
                    JOIN cartas as c ON c.numero_carta = dc.numero_carta \
                    WHERE d.data_criacao = %s"
        else:
            query = "SELECT d.*, c.* FROM decks as d \
                JOIN deck_cartas as dc ON dc.codigo_deck = d.codigo_deck \
                JOIN cartas as c ON c.numero_carta = dc.numero_carta \
                WHERE d.nome = %s"
        self.cur.execute(query,(criterio,))
        res = self.cur.fetchall()
        self.con.commit()
        decks = {}
        for i in res:
            print(i)
            carta = {
                "numero_carta": i[5],
                "carta_nome": i[6],
                "carta_raridade": i[7],
                "carta_custo": float(i[8])
            }
            if (f"Deck{i[0]}" in decks.keys()):
                temp = decks[f"Deck{i[0]}"]["cartas"]
                temp.append(carta)
                decks[f"Deck{i[0]}"]["cartas"] = temp
            else:
                deck = {
                    "codigo_deck": i[0],
                    "descricao": i[1],
                    "nome": i[2],
                    "custo": float(i[3]),
                    "data_criacao": f"{i[4].day}/{i[4].month}/{i[4].year}",
                    "cartas": [carta]
                }
                decks[f"Deck{i[0]}"] = deck
        response = {"decks": list(decks.values())}
        print(response)
        return jsonify(response)
        
