from storages.backends.s3boto3 import S3Boto3Storage
from config.settings import AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY
class MediaStorage(S3Boto3Storage):
    location = 'media'
    bucket_name = AWS_STORAGE_BUCKET_NAME