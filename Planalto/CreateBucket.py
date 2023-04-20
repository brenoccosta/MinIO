from minio import Minio
from minio.error import S3Error


def main():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Bucket name
    BucketName = "planalto"

    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if not found:
        client.make_bucket(BucketName)
    else:
        print(f"Bucket {BucketName} already exists")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
