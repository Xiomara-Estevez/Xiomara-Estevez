import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# Create new client without secret
client = cognito.create_user_pool_client(
    UserPoolId='us-east-2_fAESHksAx',
    ClientName='telehealth-no-secret',
    ExplicitAuthFlows=['USER_PASSWORD_AUTH']
)

new_client_id = client['UserPoolClient']['ClientId']
print(f"✅ New Client ID: {new_client_id}")
print(f"🔧 Update cognito_integration.py:")
print(f"CLIENT_ID = '{new_client_id}'")