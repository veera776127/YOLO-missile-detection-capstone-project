from YOLOv8_objectdetection.config.configuration import ConfigurationManager
from YOLOv8_objectdetection.components.model_training import ModelTraining  # Adjust import as needed
from YOLOv8_objectdetection import logger

STAGE_NAME = "Model Training Stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        model_train_config = config_manager.get_model_train_config()

        trainer = ModelTraining(model_train_config)

        logger.info("Training model...")
        trainer.train_and_save_model()

        logger.info("Model training completed successfully.")

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ModelTrainingPipeline()
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
