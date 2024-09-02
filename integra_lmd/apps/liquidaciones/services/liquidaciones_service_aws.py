from typing import List
from django.db import connections
import boto3



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