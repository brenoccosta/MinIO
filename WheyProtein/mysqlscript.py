import re
import mysql.connector
from minio import Minio
from datetime import datetime

# Connection with MinIO
client = Minio(
    "127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

try:
    # Connection with MySQL
    cnx = mysql.connector.connect(
        user='root'
        , password='brenomysql'
        , host='localhost'
        , database='wheyproteindb'
    )

    cursor = cnx.cursor()
except mysql.connector.Error as e:
    print(e)

v = []
bucket = "wheyprotein"

for o in client.list_objects(bucket):
    # selecting latest scraping date
    pass
print(o.object_name)

for c in client.list_objects(bucket, prefix=o.object_name):
    print(f'\t{c.object_name}')
    try:
        response = client.get_object(bucket, c.object_name)
        d = response.data.decode('utf-8').splitlines()
        for e in d:
            t = e.split(';')
            # Formatando o nome das marcas
            t[1] = t[1].title()
            # Extraindo o peso da descricao do produto
            t[2] = int(''.join(re.findall(r'\d+', t[2])).replace('3', ''))
            # Removendo o peso da descricao do produto
            b = re.findall(r'^.*?(?=9)', t[3]+'9')
            c = re.findall(r'^.*?(?=-)', b[0]+'-')
            t[3] = c[0].strip()
            t[3] = t[3].title()  # Formatando o nome dos produtos
            t[3] = t[3].partition(t[1])[0]  # Removendo a marca do nome dos produtos
            # Formatando o valor monetario
            t[4] = '.'.join(re.findall(r'\d+(?:\.\d+)?', t[4]))
            if t[4] == '': t[4] = None
            v.append(tuple(t))
            response.close()
            response.release_conn()
    except Exception as e:
        print(e)

putdata = """
    INSERT INTO TbGeneral
        (datahora, marca, peso, produto, valor, site)
    VALUES
        (%s, %s, %s, %s, %s, %s)
"""
try:
    cursor.executemany(putdata, v)
except mysql.connector.Error as e:
    print(e)

# Assuring data is commited and closing opened connections
cnx.commit()
cursor.close()
cnx.close()
