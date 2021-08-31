# ECR LOGIN

```bash
aws ecr get-login-password \
     --region us-east-1 \
  | docker login \
     --username AWS \
     --password-stdin 558105141721.dkr.ecr.us-east-1.amazonaws.com
```

