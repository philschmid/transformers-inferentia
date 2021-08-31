import argparse
import os
from uuid import uuid4

# from sagemaker import Session
from sagemaker.huggingface import HuggingFaceModel
from sagemaker.local import LocalSession


ROLE_NAME = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'

INITIAL_INSTANCE_COUNT = 1
INSTANCE_TYPE = "local"
IMAGE_URI = "558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron"
MODEL_DATA = "s3://hf-sagemaker-inference/inferentia/model.tar.gz"
REGION = "us-east-1"

os.environ["AWS_DEFAULT_REGION"] = REGION

def deploy():

    sess = LocalSession()
    sess.config = {'local': {'local_code': True}}

    # hf_model = HuggingFaceModel(
    #     image_uri=image_uri,  # A Docker image URI.
    #     # model_data=model_data,  # The S3 location of a SageMaker model data .tar.gz
    #     model_data="./src/model.tar.gz",  # The S3 location of a SageMaker model data .tar.gz
    #     role=role_name,  # An AWS IAM role (either name or full ARN).
    #     sagemaker_session=sess,
    # )
    hf_model = HuggingFaceModel(model_data='./model/model.tar.gz',
                                 role=ROLE_NAME,
                                 image_uri=IMAGE_URI,
                                 source_dir="code",
                                 py_version="py36",
                                 entry_point="inference.py")


    predictor = hf_model.deploy(initial_instance_count=INITIAL_INSTANCE_COUNT, instance_type=INSTANCE_TYPE)

    # result = predictor.predict({"inputs":"I love the new Amazon SageMaker Hugging Face Container"})
    # print(result)

    # predictor.delete_endpoint()



def create_archive():
    # TODO: not working on ec2 inferentia
    tmp_dir = os.path.join(os.getcwd(), "model")
    os.popen(f"cd {tmp_dir} && tar zcvf model.tar.gz *")

if __name__ == "__main__":
    # create_archive()
    deploy( )
