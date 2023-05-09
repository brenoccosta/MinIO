import sqlite3
from sqlite3 import Error

try:
    connection = sqlite3.connect("Planalto.db")
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE local(id, local)')
    cursor.execute('CREATE TABLE evento(id, ano, mes, dia, diadasemana, localid, evento)')
except Error as exc:
    print("SQLite error:", exc)
