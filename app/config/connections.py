from app.config.common import DEV_ENV, AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY, AWS_REGION_NAME

import boto3
import localstack_client.session as boto3_local


def get_aws_session():
    if DEV_ENV:
        aws_session = boto3_local.Session(localstack_host="localstack-container")
        return aws_session
    aws_session = boto3.Session(aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
                                aws_secret_access_key=AWS_SERVER_SECRET_KEY,
                                region_name=AWS_REGION_NAME)
    return aws_session


aws_session = get_aws_session()
