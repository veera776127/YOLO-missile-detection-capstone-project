from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    root_dir: str
    local_data_file: str
    unzip_dir: str
    s3_bucket_name: str
    s3_object_key: str