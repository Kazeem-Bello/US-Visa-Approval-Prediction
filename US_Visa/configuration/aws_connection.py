import boto3
import os
from us_visa.constant import AWS_access_env_key, AWS_secret_acces_key_env_key, region_name


class S3Client:

    s3_client = None
    s3_resource = None
    def __init__(self, region_name= region_name):
        """ 
        This Class gets aws credentials from env_variable and creates a connection with s3 bucket 
        and raise exception when environment variable is not set
        """
        
        if S3Client.s3_resource == None or S3Client.s3_client == None:
            __access_key_id = os.getenv(AWS_access_env_key)
            __secret_access_key = os.getenv(AWS_secret_acces_key_env_key)
            if __access_key_id is None:
                raise Exception(f"Environment variable: {AWS_access_env_key} is not set.")
            if __secret_access_key is None:
                raise Exception(f"Environment variable: {AWS_secret_acces_key_env_key} is not set.")
        
            S3Client.s3_resource = boto3.resource('s3',
                                            aws_access_key_id = __access_key_id,
                                            aws_secret_access_key = __secret_access_key,
                                            region_name = region_name
                                            )
            S3Client.s3_client = boto3.client('s3',
                                        aws_access_key_id = __access_key_id,
                                        aws_secret_access_key = __secret_access_key,
                                        region_name = region_name
                                        )
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client