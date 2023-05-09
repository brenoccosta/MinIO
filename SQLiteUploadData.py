import subprocess
from minio import Minio
from pathlib import Path
from datetime import datetime
from minio.error import S3Error

import pandas as pd
import sqlite3
from sqlite3 import Error

# https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
# https://docs.python.org/3/library/sqlite3.html#tutorial

def miniolayer():
    # Connecting with localhost
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    print("Client connected")

    # Declaring main variables
    BucketName = "planalto"
    ObjectName = "AgendaPresidencial"
    FilePath = "AgendaPresidencialTESTE.txt"
    print("Variables declared")

    # Downloading file
    client.fget_object(BucketName, ObjectName, FilePath)
    print("File downloaded")


def sqlitelayer(dataframe):
    # Adding to the database
    # Connecting to database
    connection = sqlite3.connect(" Planalto.db")
    cursor = connection.cursor()
    print("Conexão com a base de dados")
    ## Location table
    data = dataframe.locais
    cursor.executemany("""
        INSERT INTO local VALUES
            (?) # local
    """, data)
    print("Inserção dos locais")

    # FORMATAÇÃO DATAHORA NECESSÁRIA
    ## Events table
    data = dataframe.drop("locais")
    cursor.executemany("""
        INSERT INTO evento VALUES
            (?, ?, ?, ?, ?) # coleta, datahora, diadasemana, local, evento
    """, data)
    print("Inserção dos eventos")

    # Submitting changes
    connection.commit()
    connection.close()
    print("Inserções confirmadas e conexão fechada")


def main():
    # MinIO will download file
    try:
        miniolayer()
    except S3Error as exc:
        print("MinIO error service:", exc)
        return

    # Reading as .csv
    dataframe = pd.read_csv("AgendaPresidencialTESTE.txt", sep=";")
    print("Leitura do .csv")

    # SQLite will insert data into tables
    sqlitelayer(dataframe)    

    # Removing local file
    # ATENÇÃO!!!! REVER
    FilePath = "AgendaPresidencialTESTE.txt"
    Path(FilePath).unlink()
    print("File deleted")
    
if __name__ == "__main__":
    try:
        main()
    except Error as exc:
        print("SQLite error occurred:", exc)
