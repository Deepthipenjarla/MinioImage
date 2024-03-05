import json
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)

with open('config.json') as config:
    config_file = json.load(config)

class Storage:
    def __init__(self):
        self._storageClient = Minio(
            config_file['10.1.0.253:9000'],
            access_key=config_file['6ke0xHJzTchrhvUw1ij3'],
            secret_key=config_file['IOAnQgv5oO1bcPvApKMjql82aRorZm5rii58Rkk2'],
            secure=True
        )

    def upload_to_bucket(self, bucketName, objectName, objectPath):
        try:
            print(f'Uploading object {objectName} to bucket {bucketName}')
            self._storageClient.fput_object(bucketName, objectName, objectPath)
        except ResponseError as err:
            print(err)

if __name__ == "__main__":
    storage = Storage()

    bucket_name = 'photos'  # Replace with your desired bucket name
    object_name = 'hello.jpg'  # Replace with your desired object name
    object_path = 'server\hello.jpg'  # Replace with the path to your file

    # Upload the file to the specified bucket
    storage.upload_to_bucket(bucket_name, object_name, object_path)
