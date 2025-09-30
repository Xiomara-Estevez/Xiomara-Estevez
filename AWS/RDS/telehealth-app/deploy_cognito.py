import zipfile
import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "oJtmEFdsJn5kV5o6hJqLNMbtnTg91sTLTs9nF2QB"

print("📝 Before deploying, update cognito_integration.py with:")
print("   USER_POOL_ID = 'your-actual-pool-id'")
print("   CLIENT_ID = 'your-actual-client-id'")
print()

response = input("Have you updated the IDs? (y/n): ")
if response.lower() != 'y':
    print("❌ Please update the IDs first")
    exit()

with zipfile.ZipFile('cognito.zip', 'w') as zipf:
    zipf.write('cognito_integration.py', 'lambda_handler.py')

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

with open('cognito.zip', 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='telehealth-api',
        ZipFile=f.read()
    )

print("✅ Cognito integration deployed!")
print("🌐 Test: https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/api/auth/login")