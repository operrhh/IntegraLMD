from typing import List
from django.db import connections
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
    def test_bucket(self):
        try:
            name_bucket = os.getenv('BK_AWS_BUCKET_NAME')

            s3 = boto3.client('s3',aws_access_key_id = os.getenv('BK_AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('BK_AWS_SECRET_ACCESS_KEY'))

            res = s3.list_objects_v2(Bucket=name_bucket)

            if 'Contents' in res:
                for obj in res['Contents']:
                    print(obj['Key'])
                    name_file = obj['Key']
                    #s3.download_file(name_bucket, name_file, name_file)


            return 'test_bucket'
        except Exception as e:
            raise e