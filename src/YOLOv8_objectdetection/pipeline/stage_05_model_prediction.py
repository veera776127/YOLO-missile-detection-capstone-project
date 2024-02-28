from YOLOv8_objectdetection.config.configuration import ConfigurationManager
from YOLOv8_objectdetection.components.model_prediction import YOLOInference
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.utils.common import create_directories

STAGE_NAME = "Model prediction stage"

class ModelPredictionPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        model_prediction_config = config_manager.get_model_prediction_config()
        # Make sure directories exist or are created
        create_directories([model_prediction_config.results_path])
        inference = YOLOInference(model_prediction_config)
        logger.info("Predicting results.........")  # Use lowercase 'info'
        inference.run_inference()
        logger.info("saving results.........")  # Use lowercase 'info'

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")  # Use lowercase 'info'
        pipeline = ModelPredictionPipeline()
        pipeline.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")  # Use lowercase 'info'
    except Exception as e:
        logger.exception(e)
        raise e
