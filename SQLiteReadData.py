import sqlite3
from sqlite3 import Error

try:
    connection = sqlite3.connect("Planalto.db")
    cursor = connection.cursor()

    lugares = cursor.execute("SELECT * FROM locais")
    lugares.fetchall()

    for row in cursor.execute("SELECT * FROM locais"):
        print(row)

    # print(f"""
    #     Lugares da tabela 'locais':
    #     ID: {lugares.id}, Local: {lugares.local}
    # """)

    eventos = cursor.execute("SELECT * FROM eventos")
    eventos.fetchall()

    for row in cursor.execute("SELECT * FROM eventos"):
        print(row)

    # print(f"""
    #     Compromissos da tabela 'eventos':
    #     ID: {eventos.id}, Coleta: {eventos.coleta}, Datahora: {eventos.datahora}, Dia da semana: {eventos.diadasemana}, Compromisso: {eventos.compromisso}
    # """)

    connection.close()

except Error as exc:
    print("SQLite error:", exc)