import argparse
import os
from uuid import uuid4

from sagemaker import Session
from sagemaker.model import Model


ROLE_NAME = "sagemaker_execution_role"
INITIAL_INSTANCE_COUNT = 1
INSTANCE_TYPE = "local"
IMAGE_URI = "558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron"
MODEL_DATA = "s3://hf-sagemaker-inference/inferentia/model.tar.gz"
REGION = "us-east-1"


def deploy(image_uri, model_data, role_name, initial_instance_count, instance_type):

    sess = Session()

    hf_model = Model(
        image_uri=image_uri,  # A Docker image URI.
        model_data=model_data,  # The S3 location of a SageMaker model data .tar.gz
        role=role_name,  # An AWS IAM role (either name or full ARN).
        sagemaker_session=sess,
    )

    hf_model.deploy(
        initial_instance_count=initial_instance_count,
        instance_type=instance_type,
    )


def create_archive():
    tmp_dir = os.path.join(os.getcwd(), "src")
    os.popen(f"cd {tmp_dir} && tar zcvf model.tar.gz * && aws s3 cp model.tar.gz {MODEL_DATA}")


if __name__ == "__main__":
    create_archive()
    # deploy(
    #     image_uri=IMAGE_URI,
    #     model_data=MODEL_DATA,
    #     role_name=ROLE_NAME,
    #     initial_instance_count=INITIAL_INSTANCE_COUNT,
    #     instance_type=INSTANCE_TYPE,
    # )
