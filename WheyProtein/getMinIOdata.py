import re
from minio import Minio
import mysql.connector

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
#        , auth_plugin='mysql_native_password'
    )

    cursor = cnx.cursor()
except mysql.connector.Error as e:
    print(e)

v = []
buckets = client.list_buckets()

for bucket in buckets:
    # single bucket 'wheyprotein'
    print(bucket.name, bucket.creation_date)

    for o in client.list_objects(bucket.name):
    # subfolders named after scraping date
        print(o.object_name)

        for c in client.list_objects(bucket.name, prefix=o.object_name):
        # each time that a crawler is run a .txt object is created
            print(f'\t{c.object_name}')

            try:
                response = client.get_object(bucket.name, c.object_name)
                d = response.data.decode('utf-8').splitlines()
                f = []  # [0] datahora; [1] marca; [2] peso; [3] produto; [4] valor; [5] site
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
                    f.append(t)
                v.append(f)
#                for e in f:
#                    print(f'Datahora: {e[0]}')
#                    print(f'Marca: {e[1]}')
#                    print(f'Peso: {e[2]}')
#                    print(f'Produto: {e[3]}')
#                    print(f'Valor: {e[4]}')
#                    print(f'Site: {e[5]}')
            except Exception as e:
                print(e)
            finally:
                response.close()
                response.release_conn()

putdata = """
    INSERT INTO TbGeneral
        (datahora, marca, peso, produto, valor, site)
    VALUES
        (%s, %s, %s, %s, %s, %s)
"""
testedata = """
    INSERT INTO TbTeste
        (teste, col2)
    VALUES
        (%s, %s)
"""
# t = [[3,4],[4,5]]
# t = [2,3]
try:
    # cursor.execute(putdata, v)
    # cursor.execute(testedata, t)
#    for i in t:
#        cursor.execute(testedata, i)
    for i in v:
        cursor.execute(putdata, i)
except mysql.connector.Error as e:
    print(e)

# Assuring data is commited and closing opened connections
cnx.commit()
cursor.close()
cnx.close()
