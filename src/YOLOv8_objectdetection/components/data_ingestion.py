import os
import zipfile
import boto3
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.utils.common import get_size
from YOLOv8_objectdetection.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file_from_s3(self):
        """
        Download data from an S3 bucket.
        """
        try:
            # Create an S3 client
            s3_client = boto3.client('s3')
            # Extract bucket name and object key from the S3 URL
            # Assuming the config has been updated to include s3_bucket_name and s3_object_key
            bucket_name = self.config.s3_bucket_name
            object_key = self.config.s3_object_key
            local_data_file = self.config.local_data_file

            # Ensure the local directory exists
            if not os.path.exists(os.path.dirname(local_data_file)):
                os.makedirs(os.path.dirname(local_data_file), exist_ok=True)

            logger.info(f"Downloading data from S3 bucket {bucket_name} with key {object_key} into file {local_data_file}")

            # Download the file from S3
            s3_client.download_file(bucket_name, object_key, local_data_file)

            logger.info(f"Downloaded data from S3 bucket {bucket_name} into file {local_data_file}")
        except Exception as e:
            logger.error(f"Failed to download file from S3: {e}")
            raise e

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory.
        """
        unzip_path = self.config.unzip_dir
        if not os.path.exists(unzip_path):
            os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            logger.info(f"Extracted data to {unzip_path}")
