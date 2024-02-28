import os
import shutil
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from YOLOv8_objectdetection.pipeline.stage_02_prepare_model import ModelPreparationPipeline
from YOLOv8_objectdetection.pipeline.stage_03_model_training import ModelTrainingPipeline
from YOLOv8_objectdetection.pipeline.stage_04_model_validation import ModelTrainedValidationPipeline
from YOLOv8_objectdetection.pipeline.stage_05_model_prediction import ModelPredictionPipeline
def delete_pycache(root_dir='.'):
    """
    Deletes all __pycache__ directories and .pyc files recursively starting from the specified root directory.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove __pycache__ directories
        if '__pycache__' in dirnames:
            shutil.rmtree(os.path.join(dirpath, '__pycache__'), ignore_errors=True)
        # Remove .pyc files
        for filename in filenames:
            if filename.endswith('.pyc'):
                os.remove(os.path.join(dirpath, filename))
    logger.info("Cleanup complete: __pycache__ directories and .pyc files removed.")

def formatted_stage_header(stage_name):
    return f"\n{'=' * 20} Stage: {stage_name} Started {'=' * 20}\n"

def formatted_stage_footer(stage_name):
    return f"\n{'*' * 20} Stage: {stage_name} Completed {'*' * 20}\n\n{'x' * 50}\n"

def run_data_ingestion_stage():
    STAGE_NAME = "Data Ingestion Stage"
    logger.info(formatted_stage_header(STAGE_NAME))
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(formatted_stage_footer(STAGE_NAME))

def run_model_preparation_stage():
    STAGE_NAME = "Model Preparation Stage"
    logger.info(formatted_stage_header(STAGE_NAME))
    model_preparation = ModelPreparationPipeline()
    model_preparation.main()
    logger.info(formatted_stage_footer(STAGE_NAME))

def run_model_train_stage():
    STAGE_NAME = "Model Training Stage"
    logger.info(formatted_stage_header(STAGE_NAME))
    model_training = ModelTrainingPipeline()
    model_training.main()
    logger.info(formatted_stage_footer(STAGE_NAME))

def run_model_validation_stage():
    STAGE_NAME = "Model Validating Stage"
    logger.info(formatted_stage_header(STAGE_NAME))
    model_validating = ModelTrainedValidationPipeline()
    model_validating.main()
    logger.info(formatted_stage_footer(STAGE_NAME))

def run_model_testing_stage():
    STAGE_NAME = "Model testing Stage"
    logger.info(formatted_stage_header(STAGE_NAME))
    model_predicting = ModelPredictionPipeline()
    model_predicting.main()
    logger.info(formatted_stage_footer(STAGE_NAME))

if __name__ == '__main__':
    try:
        logger.info("Starting pipeline execution...")
        logger.info("Deleting __pycache__ and .pyc files...")
        delete_pycache()

        # Run Data Ingestion Stage
        run_data_ingestion_stage()
        
        # Run Model Preparation Stage
        run_model_preparation_stage()

        # Run  Model Training Stage
        run_model_train_stage()

        #Run Model Validating Stage
        run_model_validation_stage()

        #Run Model Validating Stage
        run_model_testing_stage()

        logger.info("Pipeline execution completed successfully.")
    except Exception as e:
        logger.exception("An unexpected error occurred during pipeline execution:")
        raise e
