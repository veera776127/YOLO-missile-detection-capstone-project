import os
import torch
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