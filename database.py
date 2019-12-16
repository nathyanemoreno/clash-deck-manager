from flask import Flask, jsonify
import mysql.connector
import pandas as pd
from ast import literal_eval
from datetime import datetime

class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "hogwarts"
        db = "CLASHROYALE"
        self.con = mysql.connector.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor()
    def add_deck(self, nome, descricao, custo, cartas):
        query_deck = """INSERT INTO decks(nome , descricao, custo,data_criacao) VALUES (%s, %s, %s, %s); """
        data_criacao = datetime.today().strftime("%Y-%m-%d")
        recordTuple = (nome, descricao, custo, data_criacao)
        self.cur.execute(query_deck, recordTuple)
        codigo_deck = self.cur.lastrowid
        print("Record inserted successfully into Decks table")
        query = "INSERT INTO `deck_cartas`(codigo_deck, numero_carta, index_carta) VALUES (%s, %s, %s)"
        for carta in cartas:
            recordTuple = (codigo_deck,carta['numero_carta'], carta['index_carta'])
            self.cur.execute(query, recordTuple)
        self.con.commit()
        self.cur.close()
        self.con.close()
        print("Record inserted successfully into Decks Cartas table")
        return "Record inserted successfully"
    def remove_deck(self, codigo_deck):
        query1 = """DELETE FROM `deck_cartas` WHERE codigo_deck=%s"""
        query2 = """DELETE FROM `decks` WHERE codigo_deck=%s"""
        self.cur.execute(query1, (codigo_deck,)) 
        self.con.commit()
        print("Record removed successfully from Decks table")
        self.cur.execute(query2, (codigo_deck,)) 
        self.con.commit()
        print("Record removed successfully from Decks Cartas table")
        self.cur.close()
        self.con.close()
        return "Record removed successfully"
    def update_deck(self, codigo_deck, nome, descricao,custo,cartas):
        query1 = """UPDATE decks SET nome=%s, descricao=%s, custo=%s WHERE codigo_deck=%s"""
        recordTuple = (nome, descricao, custo, codigo_deck)
        self.cur.execute(query1, recordTuple)
        self.con.commit()
        query2 = """UPDATE deck_cartas SET numero_carta=%s WHERE codigo_deck=%s AND index_carta=%s"""
        for carta in cartas:
            recordTuple = (carta['numero_carta'],codigo_deck, carta['index_carta'])
            self.cur.execute(query2, recordTuple)
        result = self.cur.fetchall()
        return result
    def list_cartas(self):
        self.cur.execute("SELECT numero_carta,nome, custo, raridade FROM cartas")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        res = self.cur.fetchall()
        json_data = {}
        for result in res:
            json_data[result[0]] = {row_headers[0] : result[0], row_headers[1] : result[1], row_headers[2] : result[2], row_headers[3] : result[3]}
        
        self.cur.close()
        self.con.close()
        return jsonify(json_data)
    def list_decks(self):
        self.cur.execute("SELECT d.*, c.* FROM decks as d JOIN deck_cartas as dc ON dc.codigo_deck = d.codigo_deck JOIN cartas as c ON c.numero_carta = dc.numero_carta")
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
                'carta_numero': i[5],
                'carta_nome': i[6],
                'carta_raridade': i[7],
                'carta_custo': float(i[8])
            }
            if (f'Deck{i[0]}' in decks.keys()):
                temp = decks[f'Deck{i[0]}']['cartas']
                temp.append(carta)
                decks[f'Deck{i[0]}']['cartas'] = temp
            else:
                deck = {
                    'codigo': i[0],
                    'descrico': i[1],
                    'nome': i[2],
                    'custo': float(i[3]),
                    'data_criacao': f"{i[4].day}/{i[4].month}/{i[4].year}",
                    'cartas': [carta]
                }
                decks[f'Deck{i[0]}'] = deck
        response = {'decks': list(decks.values())}
        self.cur.close()
        self.con.close()
        return jsonify(response)
    def find_deck(self, criterio):
        if criterio.isnumeric():
            query = "SELECT * FROM `decks` WHERE codigo_deck = %s"
        else:
            query = "SELECT * FROM `decks` WHERE nome = %s"
        self.cur.execute(query, (criterio,))
        res = self.cur.fetchall()
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        self.con.commit()
        json_data  = {}
        for result in res:
            json_data[result[0]] = {row_headers[0] : result[0], row_headers[1] : result[1], row_headers[2] : result[2], row_headers[3] : float(result[3]), row_headers[4] : result[4]}
        self.cur.close()
        self.con.close()
        return jsonify(json_data)
        