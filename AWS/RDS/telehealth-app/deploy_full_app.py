import zipfile
import boto3
import os

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

def deploy_full_telehealth_app():
    print("🚀 Deploying full telehealth app to AWS...")
    
    # Install dependencies
    os.system("pip install -t ./deps flask psycopg2-binary python-dotenv bcrypt")
    
    # Create deployment package
    with zipfile.ZipFile('telehealth-full.zip', 'w') as zipf:
        # Add main files
        zipf.write('app.py')
        zipf.write('lambda_handler.py')
        zipf.write('.env')
        
        # Add config
        for root, dirs, files in os.walk('config'):
            for file in files:
                if file.endswith('.py'):
                    zipf.write(os.path.join(root, file))
        
        # Add dependencies
        for root, dirs, files in os.walk('deps'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, 'deps')
                zipf.write(file_path, arc_path)
    
    # Deploy Lambda
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    with open('telehealth-full.zip', 'rb') as f:
        lambda_client.update_function_code(
            FunctionName='telehealth-api',
            ZipFile=f.read()
        )
    
    # Clean up
    os.system("rm -rf deps telehealth-full.zip")
    
    print("✅ Full telehealth app deployed!")
    print("🌐 Your API: https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod")

if __name__ == '__main__':
    deploy_full_telehealth_app()