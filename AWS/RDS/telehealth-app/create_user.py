import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# Create test user
try:
    cognito.admin_create_user(
        UserPoolId='us-east-2_fAESHksAx',
        Username='testuser',
        TemporaryPassword='TempPass123!',
        MessageAction='SUPPRESS'
    )
    
    # Set permanent password
    cognito.admin_set_user_password(
        UserPoolId='us-east-2_fAESHksAx',
        Username='testuser',
        Password='TestPass123!',
        Permanent=True
    )
    
    print("✅ User created:")
    print("Username: testuser")
    print("Password: TestPass123!")
    
except Exception as e:
    print(f"❌ Error: {e}")