CREATE DATABASE CLASHROYALE;
USE `CLASHROYALE` ;

CREATE TABLE cards (
  card_number INT(11) AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  rarity VARCHAR(10) NOT NULL,
  elixir_cost INT(11) NOT NULL,
  PRIMARY KEY (card_number)
);

CREATE TABLE decks (
  deck_code INT(11) AUTO_INCREMENT,
  description VARCHAR(200) NULL DEFAULT NULL,
  name VARCHAR(50) NOT NULL,
  elixir_cost DECIMAL(2,1)NOT NULL,
  created_at DATE NOT NULL,
  PRIMARY KEY (deck_code)
);

CREATE TABLE deck_cards (
  deck_code INT(11) NOT NULL,
  card_number INT(11) NOT NULL,
  index_card SMALLINT NOT NULL,
  PRIMARY KEY (deck_code, index_card),
  FOREIGN KEY (deck_code) REFERENCES decks (deck_code),
  FOREIGN KEY (card_number) REFERENCES cards (card_number)
);
