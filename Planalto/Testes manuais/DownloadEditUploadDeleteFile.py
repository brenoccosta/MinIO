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
    BucketName = "planalto"
    ObjectName = "Teste"
    FilePath = "TesteDownloadEditUploadDeleteFile.txt"

    # Downloading file
    client.fget_object(BucketName, ObjectName, FilePath)

    # Appending to file
    with open("TesteDownloadEditUploadDeleteFile.txt", "a") as file:
        file.write(f"\nThis was written {datetime.today()}.\n")

    # Uploading file
    client.fput_object(BucketName, ObjectName, FilePath)

    # Removing local file
    Path("TesteDownloadEditUploadDeleteFile.txt").unlink()
    
if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("Error occurred:", exc)
