import zipfile
import boto3
import json
import os

# Replace with your actual working keys
AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "oJtmEFdsJn5kV5o6hJqLNMbtnTg91sTLTs9nF2QB"

def create_simple_zip():
    """Create simple deployment package"""
    print("📦 Creating simple deployment package...")
    
    with zipfile.ZipFile('simple-lambda.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('simple_lambda_handler.py', 'lambda_handler.py')
        print("✅ Added simple_lambda_handler.py as lambda_handler.py")
    
    print("✅ Simple deployment package ready!")
    return 'simple-lambda.zip'

def deploy_simple_lambda(zip_file):
    """Deploy simple Lambda function"""
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    print("🚀 Updating Lambda function with simple handler...")
    
    try:
        with open(zip_file, 'rb') as f:
            response = lambda_client.update_function_code(
                FunctionName='telehealth-api',
                ZipFile=f.read()
            )
        
        print("✅ Lambda function updated with simple handler!")
        print(f"Function ARN: {response['FunctionArn']}")
        return response
        
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return None

if __name__ == '__main__':
    print("🚀 Deploying simple Lambda handler...")
    
    # Create zip file
    zip_file = create_simple_zip()
    
    # Deploy to Lambda
    result = deploy_simple_lambda(zip_file)
    
    if result:
        print("\n🎉 Simple deployment successful!")
        print("🌐 Test your API Gateway now!")
    else:
        print("\n❌ Deployment failed")