from typing import List
from django.db import connections
from django.conf import settings

import boto3
import os


# class BucketService:
#     def __init__(self):
#         self.bucket_name = 'integra-lmd'

#     def get_bucket_name(self):
#         return self.bucket_name

#     def get_bucket(self):
#         return connections['s3'].bucket(self.bucket_name)

#     def get_file(self, key):
#         return self.get_bucket().Object(key).get()

#     def put_file(self, key, file):
#         return self.get_bucket().put_object(Key=key, Body=file)


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
                    #s3.download_file(name_bucket, name_file, name_file)

            return list_objects
        except Exception as e:
            print("Error al testear bucket: ", e)
            raise e
    
    def upload_file(self, key, file):
        file = './tmp/test.txt'
        key = 'test.txt'

        ruta_actual = os.path.abspath(__file__)
        directorio = os.path.dirname(ruta_actual)

        print(ruta_actual)
        print(directorio)

        directorio = directorio + '/tmp/test.txt'

        try:
            res = self.s3_client.upload_file(Filename=directorio,Key=key, Bucket=self.bucket_name)
            print(res)
        except Exception as e:
            print("Error al subir archivo: ", e)
            raise e