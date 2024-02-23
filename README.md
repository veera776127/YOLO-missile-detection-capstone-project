# YOLO-missile-detection-capstone-project
Fine Tuning the YOLO v5 and YOLO v8 algorithm on custom missile dataset with the custom labels for detecting missiles in images and video and deploying it in aws as an end to end project and performing modular coding.

## PROJECT WORKFLOWS

1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py
9. Update the dvc.yaml
10. app.py


## How to develop?

### INITIAL STEPS:

1.Clone the repository

```bash
https://github.com/veera776127/YOLO-missile-detection-capstone-project.git
```
2.create a template.py file where it is used to create our folder structure and commit as per your requirement <br>
3. In requirements.txt define all the required libraries to be installed in the environment <br>
4. In setup.py give all details of the project <br>

### STEP 01- Create a conda environment after opening the repository can give specific version of python or just give python so it will take latest version for downloading

```bash
conda create -n capstone python -y
```

```bash
conda activate capstone
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```
created a logging code inside the __init__.py of src and then created common.py inside the utils where we use this as common code. Used configbox as exception handler insted of writing custom exception module


### AWS credentials to access the datafile from the amazon s3 bucket 
set these keys in python environment where your project is been developed so that you can access the s3 bucket without mentioning the credentials in code.

```bash
set AWS_ACCESS_KEY_ID=AKIA5FTZFSR62Q3MO3E6

set AWS_SECRET_ACCESS_KEY=8VbAWfSXGLUxhoKmhwFWXhlOVnCkpqeyM3qF5SNB

set AWS_REGION=us-east-1
```