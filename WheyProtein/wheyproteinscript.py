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
    ObjectName = f"{mydate.strftime('%Y-%m-%d')}/WheyProtein {mydate.strftime('%H:%M')}.txt"
    FilePath = f"{mydate.strftime('%Y-%m-%d')}/WheyProtein {mydate.strftime('%H:%M')}.txt"

    # Running crawler
    subprocess.run("scrapy crawl wheyprotein", shell=True)

    # Uploading file
    client.fput_object(BucketName, ObjectName, FilePath)

    # Removing local file
    Path(FilePath).unlink()

if __name__ == "__main__":
    try:
        main()
    except S3Error:
        subprocess.run("minio server minio/ --console-address :9090 &", shell=True)
