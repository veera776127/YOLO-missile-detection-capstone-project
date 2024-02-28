import os
from pathlib import Path
from ultralytics import YOLO
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.entity.config_entity import ModelPredictionConfig

class YOLOInference:
    def __init__(self, config: ModelPredictionConfig):
        self.config = config
        self.model = YOLO(self.config.trained_weights_path)
        self.confidence_threshold = self.config.confidence_threshold
        logger.info(f"YOLO model initialized with weights from {self.config.trained_weights_path} and confidence threshold set to {self.confidence_threshold}")

    def run_inference(self):
        # Ensure test_images_path directory exists
        assert os.path.isdir(self.config.test_images_path), f"Directory does not exist: {self.config.test_images_path}"
        logger.info(f"Running inference on images in {self.config.test_images_path}")

        # Collect image file paths
        image_paths = [os.path.join(self.config.test_images_path, image_file) for image_file in os.listdir(self.config.test_images_path) if image_file.endswith(('.jpg', '.png', '.jpeg'))]
        logger.info(f"Found {len(image_paths)} images for inference.")

        # Ensure results_path directory exists or create it
        Path(self.config.results_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Results will be saved to {self.config.results_path}")

        results = self.model(image_paths, conf=self.confidence_threshold)
        logger.info("Inference completed, processing results.")

        for idx, result in enumerate(results):
            original_filename = os.path.basename(image_paths[idx])
            result_filename = f"{original_filename.rsplit('.', 1)[0]}_result.jpg"
            result_path = os.path.join(self.config.results_path, result_filename)

            # Save the result
            result.save(result_path)
            logger.info(f"Result saved to {result_path}")
