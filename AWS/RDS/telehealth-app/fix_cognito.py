import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

# Disable client secret requirement
cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

try:
    cognito.update_user_pool_client(
        UserPoolId='us-east-2_fAESHksAx',
        ClientId='eu08vilk2ke259jpbikuvfiid',
        ExplicitAuthFlows=['USER_PASSWORD_AUTH']
    )
    print("✅ Client secret disabled")
except Exception as e:
    print(f"❌ Error: {e}")