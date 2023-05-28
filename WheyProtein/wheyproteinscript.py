import re
import subprocess
from minio import Minio
from pathlib import Path
from datetime import datetime
from minio.error import S3Error

def main():
    # Connecting with localhost
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Declaring main variables
    mydate = datetime.today()
    BucketName = "wheyprotein"

    # Running crawler
    subprocess.run("scrapy crawl wheyprotein", shell=True)

    # Uploading and removing local files
    k = Path('.').glob('*.txt')
    for p in list(k):
        o = re.sub("(?<=\').*?(?=\')", '', str(p))
        client.fput_object(BucketName, o, o)
        Path(p).unlink()

if __name__ == "__main__":
    try:
        main()
    except S3Error:
        subprocess.run("minio server minio/ --console-address :9090 &", shell=True)
