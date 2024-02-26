import os
from pathlib import Path
from shutil import copy2
from ultralytics import YOLO
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.utils.common import get_size
from YOLOv8_objectdetection.entity.config_entity import ModelValidationConfig



class ModelTrainedValidation:
    def __init__(self, config:ModelValidationConfig):
        self.best_weight_path = config.weights_path

    def validate_model(self):
        # Load the trained model
        logger.info(f"Loading the trained model from {self.best_weight_path}...")
        model = YOLO(self.best_weight_path)

        # Validate the model
        logger.info("Validating the model...")
        metrics = model.val()  # no arguments needed, dataset and settings remembered
        
        # Extract metrics
        map50 = metrics.box.map50
        map75 = metrics.box.map75
        maps = metrics.box.maps
        
        logger.info("Validation completed.")
        logger.info(f"Metrics Information:")
        logger.info(f"mAP@50: {map50}")
        logger.info(f"mAP@75: {map75}")
        logger.info(f"mAPs: {maps}")

        return map50, map75, maps