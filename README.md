# Transformers inferentia example


## Resources

* [Deploy Neuron Container on EC2](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-deploy/dlc-then-ec2-devflow.html)
* [Docker environment setup](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-deploy/tutorials/tutorial-docker-env-setup.html#docker-environment-setup)
* [Using the Amazon ECS-optimized Amazon Linux 2 (Inferentia) AMI](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-inference.html#ecs-inference-ami)
* [EKS Machine learning inference using AWS Inferentia](https://docs.aws.amazon.com/eks/latest/userguide/inferentia-support.html)
    * [For CDK use EKSOptimized images with NodeType INF](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_eks_legacy/EksOptimizedImage.html?highlight=nodetype#eksoptimizedimage)


## Development Enviroonment (EC2 inf instance)

Prior to running the container, make sure that the Neuron runtime on the instance is turned off, by running the command:

```bash
sudo service neuron-rtd stop
```

Build test container
```bash
docker build . -f docker/Dockerfile.neuron-torch -t neuron-test
```

test runtime

```bash
docker run -e AWS_NEURON_VISIBLE_DEVICES="0"  neuron-test neuron-ls
```

_Note: If you ran into an error check the instruction you might run on a host with an old runtime. [Instruction here](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-deploy/tutorials/tutorial-docker-env-setup.html#steps)_

# Transformers DLC

## ECR LOGIN

```bash
aws ecr get-login-password \
     --region us-east-1 \
  | docker login \
     --username AWS \
     --password-stdin 558105141721.dkr.ecr.us-east-1.amazonaws.com
```


# Build new container

```bash
docker build --tag 558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron --build-arg	TRANSFORMERS_VERSION=4.10.2 --file docker/Dockerfile.neuron .
```

```bash
docker push 558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron
```

# Run Container with bash

**check neuron devices**
```bash
docker run -ti \
  -e AWS_NEURON_VISIBLE_DEVICES="0" \
  558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron /opt/aws/neuron/bin/neuron-ls
```

**interactive session**
```bash
docker run -ti \
  -e AWS_NEURON_VISIBLE_DEVICES="0" \
    --entrypoint /bin/bash \
  558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron
```

**run container**
```bash
docker run -ti \
  -e AWS_NEURON_VISIBLE_DEVICES="0" \
  -v $(pwd)/model:/opt/ml/model \
  558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron
```

# Test SageMaker endpoint

```bash
python3 deploy.py
```

