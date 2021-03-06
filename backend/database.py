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
    def add_deck(self, name, description, elixir_cost, cards):
        self.createConnection()
        query_deck = "INSERT INTO decks(name , description, elixir_cost,created_at) VALUES (%s, %s, %s, %s)"
        created_at = datetime.today().strftime("%Y-%m-%d")
        recordTuple = (name, description, elixir_cost, created_at)
        self.cur.execute(query_deck, recordTuple)
        deck_code = self.cur.lastrowid
        query = "INSERT INTO deck_cards(deck_code, card_number, index_card) VALUES (%s, %s, %s)"
        for card in cards:
            self.cur.execute(query, (deck_code,card["card_number"], 1+card["index_card"]))
        self.con.commit()
        return "Record inserted successfully"
    def remove_deck(self, deck_code):
        self.createConnection()
        query1 = "DELETE FROM `deck_cards` WHERE deck_code=%s"
        query2 = "DELETE FROM `decks` WHERE deck_code=%s"
        self.cur.execute(query1, (deck_code,)) 
        self.cur.execute(query2, (deck_code,))
        self.con.commit()
        return "Record removed successfully"
    def update_deck(self, deck_code, name, description,elixir_cost,cards):
        self.createConnection()
        query1 = "UPDATE decks SET name=%s, description=%s, elixir_cost=%s WHERE deck_code=%s" 
        self.cur.execute(query1, (name, description, elixir_cost, deck_code,))
        for i in cards:    
            query2 = "INSERT INTO deck_cards(deck_code, card_number, index_card) VALUES (%s,%s,%s) \
                      ON DUPLICATE KEY UPDATE card_number=%s"
            self.cur.execute(query2, (deck_code, i["card_number"], 1+i["index_card"], i["card_number"]))
        self.con.commit()
        return "Updated successfully"
    def list_cards(self):
        self.createConnection()
        self.cur.execute("SELECT card_number,name, elixir_cost, rarity FROM cards")
        res = self.cur.fetchall()
        self.con.commit()
        json_data = {}
        for result in res:
            json_data[result[0]] = {"card_number" : result[0], "name" : result[1], "elixir_cost" : result[2], "rarity" : result[3]}
        return jsonify(json_data)
    def list_decks(self):
        self.createConnection()
        self.cur.execute("SELECT d.*, c.* FROM decks as d \
                            JOIN deck_cards as dc ON dc.deck_code = d.deck_code \
                            JOIN cards as c ON c.card_number = dc.card_number")
        res = self.cur.fetchall()
        decks = {}
        for i in res:
            # 0 -> deck_code
            # 1 -> description_deck
            # 2 -> name_deck
            # 3 -> elixir_cost_deck
            # 4 -> created_at_deck
            # 5 -> card_index
            # 6 -> card_name
            # 7 -> card_rarity
            # 8 -> card_elixir_cost
            card = {
                "card_number": i[5],
                "card_name": i[6],
                "card_rarity": i[7],
                "card_elixir_cost": float(i[8])
            }
            if (f"Deck{i[0]}" in decks.keys()):
                temp = decks[f"Deck{i[0]}"]["cards"]
                temp.append(card)
                decks[f"Deck{i[0]}"]["cards"] = temp
            else:
                deck = {
                    "deck_code": i[0],
                    "descrico": i[1],
                    "name": i[2],
                    "elixir_cost": float(i[3]),
                    "created_at": f"{i[4].day}/{i[4].month}/{i[4].year}",
                    "cards": [card]
                }
                decks[f"Deck{i[0]}"] = deck
        response = {"decks": list(decks.values())}
        return jsonify(response)
    def find_deck(self, criterio):
        self.createConnection()
        if criterio.isnumeric():
            query = "SELECT d.* , c.* FROM decks as d \
                JOIN deck_cards as dc ON dc.deck_code = d.deck_code \
                    JOIN cards as c ON c.card_number = dc.card_number \
                    WHERE dc.deck_code = %s"
        if bool(re.match("\d\d\d\d-\d\d-\d\d", '-'.join(criterio.split('/')[::-1]))):
            criterio = '-'.join(criterio.split('/')[::-1])
            query = "SELECT d.* , c.* FROM decks as d \
                JOIN deck_cards as dc ON dc.deck_code = d.deck_code \
                    JOIN cards as c ON c.card_number = dc.card_number \
                    WHERE d.created_at = %s"
        else:
            query = "SELECT d.*, c.* FROM decks as d \
                JOIN deck_cards as dc ON dc.deck_code = d.deck_code \
                JOIN cards as c ON c.card_number = dc.card_number \
                WHERE d.name = %s"
        self.cur.execute(query,(criterio,))
        res = self.cur.fetchall()
        self.con.commit()
        decks = {}
        for i in res:
            print(i)
            card = {
                "card_number": i[5],
                "card_name": i[6],
                "card_rarity": i[7],
                "card_elixir_cost": float(i[8])
            }
            if (f"Deck{i[0]}" in decks.keys()):
                temp = decks[f"Deck{i[0]}"]["cards"]
                temp.append(card)
                decks[f"Deck{i[0]}"]["cards"] = temp
            else:
                deck = {
                    "deck_code": i[0],
                    "description": i[1],
                    "name": i[2],
                    "elixir_cost": float(i[3]),
                    "created_at": f"{i[4].day}/{i[4].month}/{i[4].year}",
                    "cards": [card]
                }
                decks[f"Deck{i[0]}"] = deck
        response = {"decks": list(decks.values())}
        print(response)
        return jsonify(response)
        
