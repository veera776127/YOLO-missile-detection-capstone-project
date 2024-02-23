import os
import shutil
from YOLOv8_objectdetection import logger
from YOLOv8_objectdetection.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

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

STAGE_NAME = "Data Ingestion stage"
try:
    logger.info("Deleting __pycache__ and .pyc files...")
    delete_pycache()  # Call the function to clean up before starting the pipeline
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
