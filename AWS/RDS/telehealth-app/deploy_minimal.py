import zipfile
import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

def deploy_minimal():
    with zipfile.ZipFile('minimal.zip', 'w') as zipf:
        zipf.write('minimal_handler.py', 'lambda_handler.py')
    
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    with open('minimal.zip', 'rb') as f:
        lambda_client.update_function_code(
            FunctionName='telehealth-api',
            ZipFile=f.read()
        )
    
    print("✅ Minimal handler deployed")

if __name__ == '__main__':
    deploy_minimal()