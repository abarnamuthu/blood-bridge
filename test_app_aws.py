import os
import boto3
import pytest
from moto import mock_aws

# --------------------------------------------------
# MOCK AWS CREDENTIALS (REQUIRED)
# --------------------------------------------------
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@pytest.fixture(scope="function")
def client():
    """
    Creates mocked AWS infra + Flask test client
    """
    with mock_aws():

        # ----------------------------
        # CREATE MOCKED AWS SERVICES
        # ----------------------------
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        sns = boto3.client('sns', region_name='us-east-1')

        # ----------------------------
        # CREATE DYNAMODB TABLES
        # ----------------------------
        dynamodb.create_table(
            TableName='Users',
            KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        dynamodb.create_table(
            TableName='Requests',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        dynamodb.create_table(
            TableName='DonationHistory',
            KeySchema=[{'AttributeName': 'donor_email', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'donor_email', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # ----------------------------
        # CREATE SNS TOPIC
        # ----------------------------
        topic = sns.create_topic(Name='blood_notifications')

        # ----------------------------
        # IMPORT APP AFTER MOCKING
        # ----------------------------
        import app_aws
        app_aws.SNS_TOPIC_ARN = topic['TopicArn']
        app_aws.app.config['TESTING'] = True

        with app_aws.app.test_client() as test_client:
            yield test_client