from YOLOv8_objectdetection.constants.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from YOLOv8_objectdetection.utils.common import read_yaml,create_directories
from YOLOv8_objectdetection.entity.config_entity import (DataIngestionConfig,LoadModelConfig)
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            s3_bucket_name=config.s3_bucket_name,
            s3_object_key=config.s3_object_key
        )

        return data_ingestion_config
    
    def get_Load_model_config(self) -> LoadModelConfig:
        print("Loaded configuration:", self.config)  # Debug print
        config = self.config['Load_model']
        print("Load_model configuration:", config)  # Debug print

        create_directories([config.root_dir])
        
        Load_model_config = LoadModelConfig(root_dir=config.root_dir,
                                            pretrained_weights_path=config.pretrained_weights_path,
                                            yaml_files_path=config.yaml_files_path)

        return Load_model_config