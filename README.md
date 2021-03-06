# Clash Royale Deck Manager

![](https://img.shields.io/badge/build-100%-success)
![](https://img.shields.io/badge/JavaScript-v5.7.33-blue?logo=JavaScript)
![](https://img.shields.io/badge/Pythob-v3.6-blue?logo=Python)
![](https://img.shields.io/badge/MySQL-v5.7.33-blue?logo=mysql)

## Technologies
![](https://img.shields.io/badge/React-v16.12.0-blue?logo=react)
![](https://img.shields.io/badge/Flask-v1.1.2-blue?logo=flask)
![](https://img.shields.io/badge/Material_UI-v4.8.0-blue?logo=material-ui)

## Information
The project is a manager for Clash Royale decks. The user can fully CRUD their decks and also see the total _exilir_ cost of each deck. This project includes all 96 cards from the game. All cards images were obtained from the [Oficial Clash Royale Wiki](https://clashroyale.fandom.com/wiki/Clash_Royale_Wiki).

This project was created for learning both Flask and mainly MySQL. As a first try, the code may be no optimized and a bit ugly, we become better with our mistakes! This project was created at December of 2019, any new update to the game will not be included in this project, but it might be updated (See [Updates.md](./Updates.md)). Feel free to use this project as you want.

## Full Local Development
How to run locally:

### Backend
#### MySQL
Install MySQL:
- **Linux**: Run `sudo apt install mysql-server`
- **Windows**: Download and install it from their [oficial download page](https://dev.mysql.com/downloads/installer/).

Start MySQL Server:
- **Linux**: Run `systemctl start mysql.service`
- **Windows**: Run `"C:\Program Files\MySQL\MySQL Server 5.6\bin\mysqld"`

Create a user:
- For connect to the database, it is need a `host`, `user`, `password` and a `database`. Those values must be provided in `database.py` on the `Database` class on `createConnection` method. The application has some values by default, so you can just:
  - Create a database called `CLASHROYALE`:
    - **SQL**: `CREATE DATABASE CLASHROYALE;`
  - Create a user called `newuser` with password `user_password`:
    - **SQL**: `CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'user_password';`
  - Grant all privileges for `newuser`:
    - **SQL**: `GRANT ALL PRIVILEGES ON CLASHROYALE.* TO 'newuser'@'localhost';`

Populate the database:
- Execute the SQL queries inside `mysql-scripts` folder in the following order:
  - `db_create.sql`
  - `db_populate_cards.sql`
  - `db_populate_decks.sql` (optional)

#### Flask
Navigate to `/backend`:
- **Linux**: Run `cd backend/`
- **Windows**: Run `cd backend/`

Create an environment (venv):
- **Linux**: Run `python3 -m venv venv`
- **Windows**: Run `py -3 -m venv venv`

Activate the environment:
- **Linux**: Run `. venv/bin/activate`
- **Windows**: Run `venv\Scripts\activate`

Install Flask:
- **Linux**: Run `pip install Flask`
- **Windows**: Run `python -m pip install Flask`

Install MySQL Connector:
- **Linux**: Run `pip install mysql-connector-python`
- **Windows**: Run `python -m pip install mysql-connector-python`

Start the server:
- **Linux**: Run `python app.py`
- **Windows**: Run `python app.py`

### Frontend
**Make sure that the backend server is running!**

Navigate to `/frontend`:
- **Linux**: Run `cd backend/`
- **Windows**: Run `cd backend/`

Install dependencies:
- **Linux**: Run `npm i`
- **Windows**: Run `npm i`

Start the app:
- **Linux**: Run `npm start`
- **Windows**: Run `npm start`

## Contribuitors
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/alexaragao">
        <img src="https://avatars.githubusercontent.com/u/43763150?s=100" width="100px;" alt="Alexandre Aragão"/>
        <br />
        <b>Alexandre Aragão</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/alexaragao">
        <img src="https://avatars.githubusercontent.com/u/40841909?s=100" width="100px;" alt="Nathyane Moreno"/>
        <br />
        <b>Nathyane Moreno</b>
      </a>
    </td>
  </tr>
</table>