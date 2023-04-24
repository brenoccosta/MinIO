from minio import Minio
from pathlib import Path
from datetime import datetime
from minio.error import S3Error


def minioclient():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    return client


def downloadfile(client, BucketName, ObjectName, FilePath):
    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if found:
        client.fget_object(BucketName, ObjectName, FilePath)
    else:
        print(f"Bucket {BucketName} doesn't exists")


def uploadfile(client, BucketName, ObjectName, FilePath):
    found = client.bucket_exists(BucketName)
    if not found:
        client.make_bucket(BucketName)
    client.fput_object(BucketName, ObjectName, FilePath)


def main():
    # Connecting with localhost
    client = minioclient()

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
