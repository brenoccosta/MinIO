import mysql.connector
from minio import Minio
"""
client = Minio(
    '127.0.0.1:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)

bucket = 'wheyprotein'

for o in client.list_objects(bucket):
    print(o.object_name)
"""
try:
    cnx = mysql.connector.connect(
        user='root'
        , password='brenomysql'
        , host='localhost'
        , database='wheyproteindb'
        , auth_plugin='mysql_native_password'
    )

    cursor = cnx.cursor()
    create_table = '''
        CREATE TABLE TbGeneral (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            datahora DATETIME,
            marca VARCHAR(255),
            peso SMALLINT,
            produto VARCHAR(255),
            valor DECIMAL(7,2),
            site TEXT
        )'''

#    cursor.execute(create_table)
    cnx.close()
except mysql.connector.Error as e:
    print(e)
