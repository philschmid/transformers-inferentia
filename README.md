# ECR LOGIN

```bash
aws ecr get-login-password \
     --region us-east-1 \
  | docker login \
     --username AWS \
     --password-stdin 558105141721.dkr.ecr.us-east-1.amazonaws.com
```

# Run Container with bash

```bash
docker run -ti --entrypoint	/bin/bash 558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron
```


# Build new container

```bash
docker build --tag 558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron --build-arg	TRANSFORMERS_VERSION=4.9.2 --file docker/Dockerfile.neuron .
```