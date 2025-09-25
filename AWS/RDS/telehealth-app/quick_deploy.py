import zipfile
import boto3
import json
import os

def create_lambda_zip():
    """Create deployment package"""
    print("📦 Creating deployment package...")
    
    with zipfile.ZipFile('telehealth-lambda.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main files
        files_to_add = ['app.py', 'lambda_handler.py', '.env']
        
        for file in files_to_add:
            if os.path.exists(file):
                zipf.write(file)
                print(f"✅ Added {file}")
            else:
                print(f"⚠️ Skipped {file} (not found)")
        
        # Add config directory
        if os.path.exists('config'):
            for root, dirs, files in os.walk('config'):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)
                    print(f"✅ Added {file_path}")
    
    print("✅ Deployment package ready!")
    return 'telehealth-lambda.zip'

def deploy_to_lambda(zip_file):
    """Deploy to AWS Lambda"""
    lambda_client = boto3.client('lambda')
    
    print("🚀 Deploying to AWS Lambda...")
    
    try:
        # First, try to create the function
        with open(zip_file, 'rb') as f:
            zip_content = f.read()
        
        response = lambda_client.create_function(
            FunctionName='telehealth-api',
            Runtime='python3.9',
            Role='arn:aws:iam::123456789012:role/service-role/telehealth-lambda-role',  # We'll create this
            Handler='lambda_handler.lambda_handler',
            Code={'ZipFile': zip_content},
            Description='Telehealth API - HIPAA Compliant',
            Timeout=30,
            MemorySize=512,
            Environment={
                'Variables': {
                    'FLASK_ENV': 'production'
                }
            }
        )
        
        print(f"✅ Lambda function created!")
        print(f"Function ARN: {response['FunctionArn']}")
        return response
        
    except lambda_client.exceptions.ResourceConflictException:
        print("Function already exists, updating code...")
        
        with open(zip_file, 'rb') as f:
            response = lambda_client.update_function_code(
                FunctionName='telehealth-api',
                ZipFile=f.read()
            )
        
        print(f"✅ Lambda function updated!")
        print(f"Function ARN: {response['FunctionArn']}")
        return response
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        
        if "role" in str(e).lower():
            print("\n💡 Need to create IAM role first!")
            print("Let's create the required IAM role...")
            return create_iam_role_and_retry(zip_file)
        
        return None

def create_iam_role_and_retry(zip_file):
    """Create IAM role and retry deployment"""
    iam = boto3.client('iam')
    
    # Trust policy for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        print("🔧 Creating IAM role...")
        
        role_response = iam.create_role(
            RoleName='telehealth-lambda-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Execution role for Telehealth Lambda function'
        )
        
        role_arn = role_response['Role']['Arn']
        
        # Attach basic execution policy
        iam.attach_role_policy(
            RoleName='telehealth-lambda-role',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
        print(f"✅ IAM role created: {role_arn}")
        
        # Wait a moment for role to be ready
        import time
        print("⏳ Waiting for role to be ready...")
        time.sleep(10)
        
        # Retry Lambda deployment
        lambda_client = boto3.client('lambda')
        
        with open(zip_file, 'rb') as f:
            response = lambda_client.create_function(
                FunctionName='telehealth-api',
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_handler.lambda_handler',
                Code={'ZipFile': f.read()},
                Description='Telehealth API - HIPAA Compliant',
                Timeout=30,
                MemorySize=512
            )
        
        print(f"✅ Lambda function created with new role!")
        print(f"Function ARN: {response['FunctionArn']}")
        return response
        
    except Exception as e:
        print(f"❌ Failed to create role or function: {e}")
        return None

if __name__ == '__main__':
    print("🚀 Starting deployment...")
    
    # Create zip file
    zip_file = create_lambda_zip()
    
    # Deploy to Lambda
    result = deploy_to_lambda(zip_file)
    
    if result:
        print("\n🎉 Deployment successful!")
        print("Next step: Create API Gateway to expose your endpoints")
    else:
        print("\n❌ Deployment failed")