from typing import List
from django.db import connections
from django.conf import settings

import boto3
import os
import shutil

class BucketService:
    def __init__(self):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.s3_client = boto3.client('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID, aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)

    def get_bucket_name(self):
        return self.bucket_name

    def list_objects_bucket(self):
        try:
            res = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

            list_objects = []

            if 'Contents' in res:
                for obj in res['Contents']:
                    print(obj['Key'])
                    name_file = obj['Key']
                    list_objects.append(name_file)
                    #self.s3_client.download_file(Bucket=self.bucket_name, Key=name_file, Filename=name_file)
            return list_objects
        except Exception as e:
            print("Error al listar objetos del bucket: ", e)
            raise e
    
    def upload_file(self, key):
        ruta_actual = os.path.abspath(__file__)
        directorio = os.path.dirname(ruta_actual)
        directorio = os.path.join(directorio, 'tmp', key)

        # Recorrer directorio para ver si existe y cargar archivos
        for root, dirs, files in os.walk(directorio):
            for file in files:
                path_file = os.path.join(root, file)
                try:
                    self.s3_client.upload_file(Filename=path_file,Key=f'{key}/{file}', Bucket=self.bucket_name)
                except Exception as e:
                    print("Error al subir archivo: ", e)
                    raise e
        
        # Eliminar el directorio temporal después de subir los archivos
        try:
            shutil.rmtree(directorio)
        except Exception as e:
            print(f"Error al eliminar el directorio {directorio}: {e}")
            raise e