import subprocess
from minio import Minio
from pathlib import Path
from datetime import datetime
from minio.error import S3Error

def main():
    starttime = datetime.today()
    print("Starting time: ", starttime)
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

    # Appending to file
    crawlerstarttime = datetime.today()
    print("Crawler start time: ", crawlerstarttime)
    subprocess.run("scrapy crawl agenda", shell=True)
    print("Crawler activated")
    crawlerendtime = datetime.today()
    print("Crawler end time: ", crawlerendtime)
    print("Crawler time lapse: ", crawlerendtime - crawlerstarttime)


    # Uploading file
    client.fput_object(BucketName, ObjectName, FilePath)
    print("File uploaded")

    # Removing local file
    Path(FilePath).unlink()
    print("File deleted")
    finishtime = datetime.today()
    print("Finish time: ", finishtime)
    print("Time lapse: ", finishtime - starttime)
    
if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("Error occurred:", exc)
