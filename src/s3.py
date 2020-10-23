from src.core.logger import Logger
from decouple import config
import boto3
import os


log = Logger(__name__).instance


class S3:
    def __init__(self):
        self.__client = boto3.client('s3',
                                     aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
        self.__resource = boto3.resource('s3',
                                         aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                         aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))

    def upload_file(self, bucket: str, key: str, full_local_path: str = None):
        if not full_local_path:
            full_local_path = key.split('/')[-1]
        log.info(f"Uploading {full_local_path} to {bucket}/{key}")
        self.__client.upload_file(full_local_path, bucket, key)

    def download_file(self, bucket: str, key: str, local_dir: str = None) -> bool:
        file = key.split('/')[-1]
        if local_dir:
            file = os.path.join(local_dir, file)
        log.info(f"Downloading {file.split('/')[-1]} from s3://{bucket}/{key}")
        try:
            self.__resource.Bucket(bucket).download_file(key, file)
            return True
        except Exception as err:
            log.warning(err)
            log.warning(f"Couldn't download {file}")
            return False

    def list_files(self, bucket: str, folder: str) -> list:
        log.info(f"Listing files s3://{bucket}/{folder}")
        files = []
        response = self.__client.list_objects_v2(Bucket=bucket, Prefix=folder)
        for file_metadata in response.get("Contents"):
            file = file_metadata.get("Key") if file_metadata.get("Key").split('/')[-1] else None
            if file:
                files.append(file)

        return files
