CREATE DATABASE CLASHROYALE;
USE `CLASHROYALE` ;

CREATE TABLE cartas (
  numero_carta INT(11) AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL,
  raridade VARCHAR(10) NOT NULL,
  custo INT(11) NOT NULL,
  PRIMARY KEY (numero_carta)
);

CREATE TABLE decks (
  codigo_deck INT(11) AUTO_INCREMENT,
  descricao VARCHAR(200) NULL DEFAULT NULL,
  nome VARCHAR(50) NOT NULL,
  custo DECIMAL(2,1)NOT NULL,
  data_criacao DATE NOT NULL,
  PRIMARY KEY (codigo_deck)
);

CREATE TABLE deck_cartas (
  codigo_deck INT(11) NOT NULL,
  numero_carta INT(11) NOT NULL,
  index_carta SMALLINT NOT NULL,
  PRIMARY KEY (codigo_deck, index_carta),
  FOREIGN KEY (codigo_deck) REFERENCES decks (codigo_deck),
  FOREIGN KEY (numero_carta) REFERENCES cartas (numero_carta)
);
