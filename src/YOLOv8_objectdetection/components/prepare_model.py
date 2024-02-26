import os
import torch
import glob
import shutil
from ultralytics import YOLO  # Assuming this is the correct import for your YOLO model
from YOLOv8_objectdetection.entity.config_entity import LoadModelConfig

class PrepareModel:
    def __init__(self, model, config:LoadModelConfig):
        self.config = config
        self.model = model

    def get_model(self):
        # Load the model, assuming 'yolov8n.pt' is the correct model file
        self.model = YOLO('yolov8n.pt')
        print("Model loaded successfully.")

    def save_model(self):
        model_path = self.config.pretrained_weights_path
        # Ensure the directory for pretrained_weights_path exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Check if the model file already exists
        if os.path.exists(model_path):
            print(f"Model file already exists at {model_path}. No need to save again.")
        else:
            # Save the model since it doesn't exist
            torch.save(self.model.state_dict(), model_path)
            print(f"Model saved successfully at: {model_path}")
    
    def save_yaml_files(self):
        yaml_data_path = self.config.yaml_files_path
        os.makedirs(yaml_data_path, exist_ok=True)  # Ensure the directory exists

        # Directly using the known path to the 'cfg/datasets' directory
        ultralytics_base_path = self.config.ultralytics_path
        datasets_path = os.path.join(ultralytics_base_path, 'cfg', 'datasets', '*.yaml')
        
        # Use glob to find all YAML files within the 'datasets' directory
        for yaml_file in glob.glob(datasets_path):
            # Compute a relative path to keep the directory structure
            relative_path = os.path.relpath(yaml_file, start=os.path.dirname(datasets_path))
            destination_path = os.path.join(yaml_data_path, relative_path)
            # Ensure the directory for this file exists
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy(yaml_file, destination_path)
        
        print(f"All YAML files in 'datasets' copied successfully to: {yaml_data_path}")