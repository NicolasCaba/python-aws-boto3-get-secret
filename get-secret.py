import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import InvalidRegionError


def get_secret(secret_name, region_name):
    try:
        session = boto3.Session(profile_name='work-account')
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
        )

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    except InvalidRegionError as e:
        print("InvalidRegionError")
    else:
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
            print(text_secret_data)
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            print(binary_secret_data)


get_secret('Outputs', 'us-east-1')
