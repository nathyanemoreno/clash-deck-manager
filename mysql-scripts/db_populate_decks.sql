USE CLASHROYALE;

INSERT INTO decks(name, description, elixir_cost, created_at) values
('Deck de P.E.K.K.A', 'Deck forte de P.E.K.K.A', 3.6, '2019-12-15'),
('Desafio Elixir Triplo', 'Deck de foguete para desafio do elixir triplo', 3.8, '2019-12-15'),
('Deck Supremo', 'Deck rápido de Barril de Goblins', 3.3, '2019-12-15');

INSERT INTO deck_cards (deck_code, index_card, card_number) values
(1, 0, 83),
(1, 1, 84),
(1, 2, 85),
(1, 3, 86),
(1, 4, 87),
(1, 5, 88),
(1, 6, 89),
(1, 7, 90),
(2, 0, 36);
