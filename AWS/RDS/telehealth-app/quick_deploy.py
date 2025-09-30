import zipfile
import boto3
import json
import os

# Replace with your actual working keys
AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"  # Replace with your real key
AWS_SECRET_ACCESS_KEY = "oJtmEFdsJn5kV5o6hJqLNMbtnTg91sTLTs9nF2QB"  # Replace with your real key

def create_lambda_zip():
    """Create deployment package with all dependencies"""
    print("📦 Creating deployment package...")
    
    # Install dependencies to a temp directory
    print("📥 Installing dependencies...")
    os.system("pip install -t ./lambda_deps psycopg2-binary python-dotenv flask bcrypt")
    
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
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"✅ Added {file_path}")
        
        # Add dependencies
        if os.path.exists('lambda_deps'):
            for root, dirs, files in os.walk('lambda_deps'):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Get relative path for zip
                    arc_path = os.path.relpath(file_path, 'lambda_deps')
                    zipf.write(file_path, arc_path)
            print("✅ Added dependencies")
    
    # Clean up temp directory
    os.system("rm -rf lambda_deps")
    
    print("✅ Deployment package ready!")
    return 'telehealth-lambda.zip'

def create_iam_role():
    """Create IAM role for Lambda"""
    iam_client = boto3.client(
        'iam',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
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
        
        role_response = iam_client.create_role(
            RoleName='telehealth-lambda-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Execution role for Telehealth Lambda function'
        )
        
        role_arn = role_response['Role']['Arn']
        
        # Attach basic execution policy
        iam_client.attach_role_policy(
            RoleName='telehealth-lambda-role',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
        print(f"✅ IAM role created: {role_arn}")
        return role_arn
        
    except iam_client.exceptions.EntityAlreadyExistsException:
        # Role already exists, get its ARN
        print("📋 IAM role already exists, using existing one...")
        role_response = iam_client.get_role(RoleName='telehealth-lambda-role')
        role_arn = role_response['Role']['Arn']
        print(f"✅ Using existing IAM role: {role_arn}")
        return role_arn
        
    except Exception as e:
        print(f"❌ Failed to create/get IAM role: {e}")
        return None

def deploy_to_lambda(zip_file, role_arn):
    """Deploy to AWS Lambda with explicit credentials"""
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    print("🚀 Deploying to AWS Lambda...")
    
    try:
        with open(zip_file, 'rb') as f:
            zip_content = f.read()
        
        response = lambda_client.create_function(
            FunctionName='telehealth-api',
            Runtime='python3.9',
            Role=role_arn,
            Handler='lambda_handler.lambda_handler',
            Code={'ZipFile': zip_content},
            Description='Telehealth API - HIPAA Compliant',
            Timeout=30,
            MemorySize=512,
            Environment={
                'Variables': {
                    'FLASK_ENV': 'production',
                    'DEBUG': 'True'  # Enable debug mode for demo
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
        return None

if __name__ == '__main__':
    print("🚀 Starting deployment with explicit credentials...")
    
    # Test credentials first
    try:
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1'
        )
        
        identity = sts_client.get_caller_identity()
        print(f"✅ Connected as: {identity['Arn']}")
        
    except Exception as e:
        print(f"❌ Credential test failed: {e}")
        print("💡 Update your keys in this script and try again")
        exit(1)
    
    # Create zip file
    zip_file = create_lambda_zip()
    
    # Create or get IAM role
    role_arn = create_iam_role()
    
    if not role_arn:
        print("❌ Failed to create IAM role, cannot proceed")
        exit(1)
    
    # Wait for role to be ready
    print("⏳ Waiting 10 seconds for IAM role to be ready...")
    import time
    time.sleep(10)
    
    # Deploy to Lambda
    result = deploy_to_lambda(zip_file, role_arn)
    
    if result:
        print("\n🎉 Deployment successful!")
        print(f"Lambda Function: {result['FunctionName']}")
        print("\n🌐 Next step: Create API Gateway to get a public URL")
        print("Your telehealth app is now running on AWS Lambda!")
    else:
        print("\n❌ Deployment failed")