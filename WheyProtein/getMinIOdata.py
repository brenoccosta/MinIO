from minio import Minio

client = Minio(
    "127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

buckets = client.list_buckets()

# Single time usage:
"""
with open("ObjetoTeste.txt", "a") as o:
    o.write("Estive aqui `as 18:16 de 28/05/2023")
o = "ObjetoTeste.txt"
for bucket in buckets:
    client.fput_object(bucket.name, o, o)
"""

for bucket in buckets:
    print(bucket.name, bucket.creation_date)
    o = client.list_objects(bucket.name, prefix='2023-05-28/')
    r = client.list_objects(bucket.name, prefix='2023-05-29/')

for q in o:
    t = q.object_name
    print(t, type(t))
#    client.fget_object(bucket.name, q, f'dataretrieved/{t}')
for s in r:
    t = s.object_name
    print(t)
#    client.fget_objetc(bucket.name, q, f'dataretrieved/{t}')
