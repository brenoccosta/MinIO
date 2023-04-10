# Redes e Comunicação, 1S 2023
## Breno Coltro da Costa, 21011999

#### Upload and download files in MinIO Ubuntu
# Reference: https://min.io/docs/minio/linux/developers/python/minio-py.html
from minio import Minio
from minio.error import S3Error


def uploadfile(client):
    print("'uploadfile' function called")

    # Choose bucket name, object name and file path
    BucketName = input("Insert bucket name: ")
    ObjectName = input("Insert object name: ")
    FilePath = input("Insert file path: ")

    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if not found:
        client.make_bucket(BucketName)
    else:
        print(f"Bucket {BucketName} already exists")

    # Upload object from existing file into selected bucket
    client.fput_object(
        BucketName, ObjectName, FilePath,
    )
    print(
        f"{FilePath} is successfully uploaded as"
        f"object {ObjectName} to bucket {BucketName}."
    )


def downloadfile(client):
    print("'downloadfile' function called")

	# Choose bucket from existing buckets
    buckets = client.list_buckets()
    print("Existing buckets:")
    for bucket in buckets:
        print(bucket.name)
        
    # Choose bucket name
    BucketName = input("Insert bucket name: ")

    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if not found:
        print(f"Bucket {BucketName} not found.")
        return False
    
    objects = client.list_objects(BucketName)
    for obj in objects:
    	print(obj)


def main():
    # Create a client with the MinIO server playground, 
    # its access key and secret key.
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Menu options
    menu = {1: uploadfile, 2: downloadfile}

    # Menu loop
    while(True):
        print("'main' function called")

        ChosenOption = int(input(
            "Choose which you prefer:\n"
            "1) Upload file\n"
            "2) Download file\n"
            "Else, end running program.\n"))
        try:
            menu[ChosenOption](client)
        except KeyError:
            break


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
