from YOLOv8_objectdetection.config.configuration import ConfigurationManager
from YOLOv8_objectdetection.components.prepare_model import PrepareModel  # Ensure this import matches your project structure
from YOLOv8_objectdetection import logger

STAGE_NAME = "Model Preparation Stage"

class ModelPreparationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        Load_model_config = config.get_Load_model_config()
        load_model = PrepareModel(model=None, config=Load_model_config)

        logger.info("Loading model...")
        load_model.get_model()

        logger.info("Attempting to save model...")
        load_model.save_model()

        logger.info("Model preparation and saving completed successfully.")

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ModelPreparationPipeline()
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
