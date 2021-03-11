import boto3
import os
import logging
from botocore.exceptions import ClientError
    
# Create connection clients
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Get the status of all the volumes in a region
    try:
        response = ec2.describe_volume_status(
            Filters=[
                {
                    'Name': 'volume-status.status',
                    'Values': [
                        'impaired',
                    ]
                },
            ]
        )

    except ClientError as e:
        print("Some error has occurred! ", str(e))
        exit(-1)

    else:
        volumes = []
        for volume in response['VolumeStatuses']:
            volumes.append(volume['VolumeId'])
        impaired_volumes = ','.join(volumes)

        if impaired_volumes:
            topic_arn = os.environ['sns_topic_arn']
            response = sns.publish(
                TopicArn=topic_arn,
                Message="The following volumes are impaired: {}".format(impaired_volumes)
            )
