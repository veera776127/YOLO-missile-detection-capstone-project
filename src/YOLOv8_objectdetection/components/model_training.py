import os
from pathlib import Path
from shutil import copy2
from ultralytics import YOLO, settings  # Import settings from ultralytics
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.utils.common import get_size
from YOLOv8_objectdetection.entity.config_entity import ModelTrainConfig
import json

class ModelTraining:
    def __init__(self, config: ModelTrainConfig):
        self.data_yaml_path = config.training_data_yaml
        self.epochs = config.epochs
        self.output_dir = Path(config.output_dir).resolve()
        self.base_run_dir = Path(config.runs_dir).resolve()

    def train_and_save_model(self):
        # Update Ultralytics settings to enable MLflow
        logger.info("Starting MLflow tracking...")
        # Load the configuration from config.json
        with open('config.json') as config_file:
            config = json.load(config_file)

        # Update the settings with the value from the configuration file
        settings.update({'mlflow': config['mlflow']})
        logger.info("MLflow tracking is enabled.")

        # Load the pretrained model
        model = YOLO("yolov8n.pt")  # Adjust the model file as necessary
        logger.info("Model loaded successfully.")

        # Train the model with the custom dataset
        logger.info(f"Training with {self.data_yaml_path} for {self.epochs} epochs...")
        model.train(data=self.data_yaml_path, epochs=self.epochs)
        logger.info("Model training completed.")

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory verified: {self.output_dir}")

        # Dynamically find the most recent training run directory within 'runs/train'
        try:
            logger.info(f"Looking in directory: {self.base_run_dir}")
            train_runs = [run for run in self.base_run_dir.iterdir() if run.is_dir() and run.name.startswith('train')]
            logger.info(f"Found training runs: {train_runs}")
            last_run_path = sorted(train_runs, key=os.path.getmtime, reverse=True)[0] / 'weights'
            logger.info(f"Most recent training run: {last_run_path}")
        except IndexError as e:
            logger.error(f"No training runs found in {self.base_run_dir}. Please ensure training has completed successfully.", exc_info=True)
            raise FileNotFoundError(f"No training runs found in {self.base_run_dir}. Please ensure training has completed successfully.") from e

        source_best_weight_path = last_run_path / 'best.pt'

        # Check if best.pt already exists in the output directory
        target_best_weight_path = self.output_dir / 'best.pt'
        if os.path.exists(target_best_weight_path):
            logger.warning(f"'best.pt' already exists in the output directory and will be overwritten.")

        # Copy the best model weights to the specified output directory
        copy2(source_best_weight_path, target_best_weight_path)
        logger.info(f"Best model weights saved to {target_best_weight_path}")

        # Reset settings to default values after training
        settings.reset()
        logger.info("Ultralytics settings have been reset to default values.")