import zipfile
import boto3
import json

# Create deployment package
print("📦 Creating deployment package...")
with zipfile.ZipFile('telehealth-app.zip', 'w') as zipf:
    zipf.write('app.py')
    zipf.write('lambda_handler.py') 
    zipf.write('.env')
    
    # Add config folder
    zipf.write('config/__init__.py')
    zipf.write('config/database.py')
    zipf.write('config/settings.py')

print("✅ Package created!")

# Deploy to Lambda
lambda_client = boto3.client('lambda')

print("🚀 Deploying to AWS Lambda...")

try:
    with open('telehealth-app.zip', 'rb') as f:
        response = lambda_client.create_function(
            FunctionName='telehealth-api',
            Runtime='python3.9',
            Role='arn:aws:iam::123456789012:role/lambda-execution-role',  # We'll create this
            Handler='lambda_handler.lambda_handler',
            Code={'ZipFile': f.read()},
            Description='Telehealth API - HIPAA Compliant',
            Timeout=30,
            MemorySize=512
        )
    print("✅ Lambda function created!")
    print(f"Function ARN: {response['FunctionArn']}")
    
except Exception as e:
    print(f"❌ Deployment failed: {e}")
    if "role" in str(e).lower():
        print("💡 Need to create IAM role first - I'll show you how!")