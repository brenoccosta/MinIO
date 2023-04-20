from minio import Minio
from minio.error import S3Error


def main():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Bucket name, object name and file path
    BucketName = "Planalto"
    ObjectName = "Teste"
    FilePath = "Teste.txt"

    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if not found:
        client.make_bucket(BucketName)
    client.fput_object(BucketName, ObjectName, FilePath)


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)