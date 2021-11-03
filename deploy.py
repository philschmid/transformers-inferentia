import os
import boto3
from sagemaker.huggingface import HuggingFaceModel
from sagemaker.local import LocalSession
from sagemaker import Session

# Create model.tar.gz
# cd model
# tar zcvf model.tar.gz *
# aws s3 cp model.tar.gz <s3://{my-s3-path}>


def deploy():
    INITIAL_INSTANCE_COUNT = 1
    INSTANCE_TYPE = "ml.inf1.xlarge"
    IMAGE_URI = "558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron"
    MODEL_DATA = "s3://hf-sagemaker-inference/inferentia/model.tar.gz"
    REGION = "us-east-1"
    LOCAL = False
    os.environ["AWS_DEFAULT_REGION"] = REGION
    if LOCAL:
        sess = LocalSession()
        sess.config = {"local": {"local_code": True}}
        ROLE_NAME = "arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001"
        INSTANCE_TYPE = "local"
        MODEL_DATA = "./model/model.tar.gz"
    else:
        iam_client = boto3.client("iam")
        ROLE_NAME = iam_client.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]
        sess = Session()

    hf_model = HuggingFaceModel(
        model_data=MODEL_DATA,
        role=ROLE_NAME,
        image_uri=IMAGE_URI,
        source_dir="code",
        py_version="py38",
        entry_point="inference.py",
    )
    # Let SageMaker know that we've already compiled the model via neuron-cc
    hf_model._is_compiled_model = True

    predictor = hf_model.deploy(initial_instance_count=INITIAL_INSTANCE_COUNT, instance_type=INSTANCE_TYPE)

    result = predictor.predict({"inputs":"I love the new Amazon SageMaker Hugging Face Container"})
    print(result)

    predictor.delete_endpoint()


if __name__ == "__main__":
    # create_archive()
    deploy()
