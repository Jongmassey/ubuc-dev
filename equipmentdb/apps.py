from django.apps import AppConfig
from django.conf import settings
import boto3

class EquipmentdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipmentdb'
    def ready(self) -> None:
        AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
        AWS_S3_REGION_NAME = settings.AWS_S3_REGION_NAME
        AWS_S3_ENDPOINT_URL = None if settings.AWS_S3_ENDPOINT_URL=='' else settings.AWS_S3_ENDPOINT_URL
        s3_client = boto3.client('s3',region_name = AWS_S3_REGION_NAME,endpoint_url=AWS_S3_ENDPOINT_URL)
        buckets = s3_client.list_buckets()['Buckets']
        if not [b for b in buckets if b['Name']==AWS_STORAGE_BUCKET_NAME]:
            s3_client.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
        return super().ready()
