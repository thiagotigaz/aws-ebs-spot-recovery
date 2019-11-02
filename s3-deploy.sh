#!/bin/bash

aws --profile thiago s3 cp --recursive supercloud s3://arquivos-importantes/supercloud/infra/aws-ebs-spot-recovery/supercloud/
aws --profile thiago s3 cp main.py s3://arquivos-importantes/supercloud/supercloud/infra/aws-ebs-spot-recovery/
aws --profile thiago s3 cp requirements.txt s3://arquivos-importantes/supercloud/infra/aws-ebs-spot-recovery/


aws --profile thiago s3 cp --recursive supercloud s3://supercloud-stores/infra/aws-ebs-spot-recovery/supercloud/
aws --profile thiago s3 cp main.py s3://supercloud-stores/infra/aws-ebs-spot-recovery/
aws --profile thiago s3 cp requirements.txt s3://supercloud-stores/infra/aws-ebs-spot-recovery/
