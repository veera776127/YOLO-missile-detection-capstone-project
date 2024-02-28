from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    root_dir: str
    local_data_file: str
    unzip_dir: str
    s3_bucket_name: str
    s3_object_key: str

@dataclass
class LoadModelConfig:
    root_dir: str
    yaml_files_path: str
    ultralytics_path: str


@dataclass
class ModelTrainConfig:
    output_dir: str
    runs_dir: str
    training_data_yaml: str
    epochs: 3


@dataclass
class ModelValidationConfig:
    weights_path: str


@dataclass
class ModelPredictionConfig:
  trained_weights_path: str
  test_images_path: str
  results_path: str
  confidence_threshold: float