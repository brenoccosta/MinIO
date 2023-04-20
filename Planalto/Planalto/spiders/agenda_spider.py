#### MinIO ####
from minio import Minio
from minio.error import S3Error


def downloadfile(client):
    # Bucket name, object name and file path
    BucketName = "Planalto"
    ObjectName = "AgendaDoPresidente"
    FilePath = "AgendaFile.txt"

    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if found:
        client.fget_object(BucketName, ObjectName, FilePath)
        print(f"Object {ObjectName} uploaded to bucket {BucketName}.")


def uploadfile(client):
    # Bucket name, object name and file path
    BucketName = "Planalto"
    ObjectName = "AgendaDoPresidente"
    FilePath = "AgendaFile.txt"

    # Verify if BucketName already exists
    found = client.bucket_exists(BucketName)
    if found:
        client.fput_object(BucketName, ObjectName, FilePath)
        print(f"Object {ObjectName} uploaded to bucket {BucketName}.")

def MinIOClient():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    return client


#### CRAWLER ####
import scrapy
from pathlib import Path
from datetime import datetime

class AgendaSpider(scrapy.Spider):
    try:
        client = MinIOClient()
        downloadfile(client)
    except S3Error as exc:
        print("error occurred.", exc)
    
    
    # Crawler
    name = "agenda"
    start_urls = [
        'https://www.gov.br/planalto/pt-br'
    ]

    def parse(self, response):
        AgendaFile = open("AgendaFile.txt", "a")

        hoje = response.xpath('//*[@id="agenda-fafe1a35-be9d-4466-bc21-df0f42169d86"]/div/div[2]/ul/li[4]')
        dia = hoje.css('div.daypicker-day::text').get()
        mes = response.xpath('//*[@id="agenda-fafe1a35-be9d-4466-bc21-df0f42169d86"]/div/div[1]/div[2]/div/span[1]/text()').get()
        ano = response.xpath('//*[@id="agenda-fafe1a35-be9d-4466-bc21-df0f42169d86"]/div/div[1]/div[2]/div/span[2]/text()').get()
        diadasemana = hoje.css('div.daypicker-weekday::text').get()

        for div in response.css('div.collection-events-item'):
            evento = div.css('a.title-item::text').get()
            local = div.css('span.location::text').get()
            hora = div.css('span.timestamp::text').get()
            AgendaFile.write(f'{datetime.today()};{dia};{mes};{ano};{diadasemana};{hora};{local};{evento};\n')

        AgendaFile.close()

        # Removing local file
        Path.unlink("Teste.txt")