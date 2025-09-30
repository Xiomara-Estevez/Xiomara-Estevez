import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

# Update runtime and handler
lambda_client.update_function_configuration(
    FunctionName='telehealth-api',
    Runtime='python3.11',
    Handler='lambda_handler.lambda_handler',
    Timeout=30
)

print("✅ Lambda configuration updated")