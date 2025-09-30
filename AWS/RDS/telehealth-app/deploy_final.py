import zipfile
import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

with zipfile.ZipFile('final.zip', 'w') as zipf:
    zipf.write('final_handler.py', 'lambda_handler.py')

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

with open('final.zip', 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='telehealth-api',
        ZipFile=f.read()
    )

print("✅ Final handler deployed")