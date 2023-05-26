import subprocess
from minio import Minio

# Initializing localhost MinIO server
subprocess("minio server minio/ --console-adress :9090", shell=True)

# Connecting
client = Minio(
    "127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Creating WheyProtein project bucket
client.make_bucket("wheyprotein")