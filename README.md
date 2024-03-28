# YOLO-missile-detection-capstone-project
Fine Tuning the YOLO v5 and YOLO v8 algorithm on custom missile dataset with the custom labels for detecting missiles in images and video and deploying it in aws as an end to end project and performing modular coding.


![alt text](<study_images\intro.png>)

![alt text](<study_images\overall_process.png>)


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

### STEP 01- Create a conda environment 
After opening the repository can give specific version of python or just give python so it will take latest version for downloading
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

# Data Ingestion
Refer below wesite for python sdk boto3 documentation for downloading data from AWS s3 bucket.
```bash
https://docs.aws.amazon.com/pythonsdk/
```
```bash
https://docs.aws.amazon.com/amazonglacier/latest/dev/sdk-general-information-section.html  #for any other launguage
```
# Model training
Refer this ultralytics documentation for full details on training
```bash
https://docs.ultralytics.com/modes/train/
```
# Model Validation
Refer this ultralytics documentation for full details on validation
```bash
https://docs.ultralytics.com/modes/val/
```

# Model Prediction
Refer this ultralytics documentation for full details on validation

```bash
https://docs.ultralytics.com/modes/predict/#probs
```
# Docker commands for containerization

```bash
#Check for existing running containers use -a for all including stopped
docker ps

#Check for existing docker images
docker images

# Build the docker 
docker build -t missile-app .

#Run the docker (before pushing to docker hub in local)
#Docker maps this port to port 5000 on your host machine. This means you should be able to access your Flask application by visiting http://localhost:5000 in your web browser.
docker run -p 5000:5000 missile-app

#eg:(After pulling from docker hub)
docker run -d -p 5000:5000 thulasiram6787/capstone-yolo_missile_detection_001:latest


#Pushing the docker to docker hub 
docker push thulasiram6787/capstone-yolo_missile_detection_001:latest

#Login to docker hub (give username and password)
docker login

#Create repository and tag it
docker tag missile-detection:latest yourusername/missile-detection:latest

#Push the docker image to the docker hub
docker push yourusername/missile-detection:latest

#Pull the docker image from the repository
docker pull thulasiram6787/capstone-yolo_missile_detection_001:latest

#Stop the running docker
docker stop

#Remove the existing image 
docker rmi missile-app:latest

#Remove the Docker
docker rm

#Tranfering image from repository to repository
docker tag existing-image:tag new-repository:new-tag
(docker tag vishwas304/missile-detection:latest thulasiram6787/capstone-yolo_missile_detection_001:latest)
docker login
(docker push thulasiram6787/capstone-yolo_missile_detection_001:latest)


```
## AWS-CICD-Deployment-with-Github-Actions
1. Login to AWS console.

2. Create IAM user for deployment #with specific access

3. Configure EC2 machine with proper setup using VPC,security group,region take below as reference
        ![alt text](<study_images\ec2_setup.png>)

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws


## Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

## Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess
3. Create ECR repo to store/save docker image
- Save the URI: 05418478717.dkr.ecr.us-east-1.amazonaws.com/missile
4. Create EC2 machine (Ubuntu)
5. Open EC2 and Install docker in EC2 Machine:
#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
6. Configure EC2 as self-hosted runner:
setting>actions>runner>new self hosted runner> choose os> then run command one by one


## Setup github secrets:
```bash
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = 905418478717.dkr.ecr.us-east-1.amazonaws.com/missile   (Thulasi aws ecr repository)

ECR_REPOSITORY_NAME = missile
```

## AWS credentials to access the datafile from the amazon s3 bucket 
set these keys in python environment where your project is been developed so that you can access the s3 bucket without mentioning the credentials in code.

```bash
set AWS_ACCESS_KEY_ID=  (contact owner for AWS_ACCESS_KEY_ID)

set AWS_SECRET_ACCESS_KEY= (contact owner for AWS_SECRET_ACCESS_KEY)

set AWS_REGION=us-east-1
```
owner - veeramangalamthulasiram@gmail.com

# AWS Aand MLFLOW credentials to access the datafile from the amazon s3 bucket 
set these keys in python environment where your project is been developed so that you can access the MLFLOW and track experiment.

### Linux or gitbash prompt
```bash
export MLFLOW_TRACKING_URI=(contact owner for MLFLOW_TRACKING_URI)
export MLFLOW_TRACKING_USERNAME=veera776127
export MLFLOW_TRACKING_PASSWORD= (contact owner for MLFLOW_TRACKING_PASSWORD)
```
### Windows cmd prompt/shell
```bash
set MLFLOW_TRACKING_URI=(contact owner for MLFLOW_TRACKING_URI)
set MLFLOW_TRACKING_USERNAME=veera776127
set MLFLOW_TRACKING_PASSWORD=(contact owner for MLFLOW_TRACKING_PASSWORD)
```
### In jupyter notebook
```bash
os.environ["MLFLOW_TRACKING_URI"]=(contact owner for MLFLOW_TRACKING_URI)
os.environ["MLFLOW_TRACKING_USERNAME"]="veera776127"
os.environ["MLFLOW_TRACKING_PASSWORD"]=(contact owner for MLFLOW_TRACKING_PASSWORD)

