from flask import Flask, jsonify
import mysql.connector
import pandas as pd
from ast import literal_eval

class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "hogwarts"
        db = "CLASHROYALE"
        self.con = mysql.connector.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor()
    # def add_deck(self, descricao, nome, custo, data_criacao, cartas):
    #     self.cur.execute(f"INSERT INTO decks(descricao, nome, custo, data_criacao) VALUES ({descricao}, {nome}, {custo}, {data_criacao})")
    #     codigo_deck = self.cur.execute(f"SELECT (codigo_deck) FROM decks")
    #     for i in cartas:
    #         numero_carta = i["numero_carta"]
    #         index_carta = i["index_carta"]
    #         self.cur.execute(f"INSERT INTO deck_cartas(numero_carta, index_carta) VALUES ({numero_carta}, {index_carta} WHERE codigo_deck={codigo_deck}")
    #     result = self.cur.fetchall()
    #     return result
    def add_deck(self, descricao, nome, custo, cartas, codigo_deck):
        query = """CALL CreateDeck(%s, %s, %s, %s)"""
        codigo_deck = self.cur.execute(query, (descricao,nome, custo, codigo_deck))
        # query = "INSERT INTO deck_cartas WHERE codigo_deck={codigo_deck}"
        print(codigo_deck)
        # self.cur.executemany(query, cartas)
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
        json_data = {}
        for result in res:
            json_data[result[0]] = {row_headers[1] : result[1], row_headers[2] : result[2]}
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
        response = {'decks': decks.values()}
        return jsonify(response)
    def find_carta(self, nome):
        self.cur.execute("SELECT * FROM cartas WHERE nome={nome}")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        res = self.cur.fetchall()
        json_data={}
        for result in res: 
            json_data[result[0]] = {row_headers[1] : result[1], row_headers[2] : result[2]}
        return jsonify(json_data)