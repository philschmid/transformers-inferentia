# Transformers inferentia example

## Help

* bash `-S` means -> file is not zero size
* we need to add `--cap-add=IPC_LOCK` to docker run to enable shmem interface. heck for capability failed! `'CAP_IPC_LOCK'`. IPC_LOCK is required to use shmem interface.
* [Example: Run containerized neuron application](https://github.com/aws/aws-neuron-sdk/blob/master/neuron-deploy/docker-example/index.rst)

# ECR LOGIN

```bash
aws ecr get-login-password \
     --region us-east-1 \
  | docker login \
     --username AWS \
     --password-stdin 558105141721.dkr.ecr.us-east-1.amazonaws.com
```


# Build new container

```bash
docker build --tag 558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron --build-arg	TRANSFORMERS_VERSION=4.10.0 --file docker/Dockerfile.neuron .
```

```bash
docker push 558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron
```

# Run Container with bash

**check neuron devices**
```bash
docker run -ti \
  --device=/dev/neuron0 \
  --cap-add=IPC_LOCK \
  -v /tmp/neuron_rtd_sock/:/sock \
  --entrypoint /bin/bash \
  558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron /opt/aws/neuron/bin/neuron-ls
```

**interactive session**
```bash
docker run -ti \
  --device=/dev/neuron0 \
  --cap-add=IPC_LOCK \
  -v /tmp/neuron_rtd_sock/:/sock \
  --entrypoint /bin/bash \
  558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron
```

**run container**
```bash
docker run -ti \
  --env NEURON_RTD_ADDRESS=unix:/sock/neuron.sock \
  -v /tmp/neuron_rtd_sock/:/sock \
  -v $(pwd)/model:/opt/ml/model \
  --entrypoint /bin/bash \
  558105141721.dkr.ecr.us-east-1.amazonaws.com/huggingface-inference-pytorch:neuron /usr/local/bin/dockerd-entrypoint.sh
```

# Test SageMaker endpoint

```bash
python3 deploy.py
```

