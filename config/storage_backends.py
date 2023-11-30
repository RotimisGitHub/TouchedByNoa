from storages.backends.s3 import S3Storage
from config.settings import AWS_STORAGE_BUCKET_NAME


class MediaStorage(S3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME