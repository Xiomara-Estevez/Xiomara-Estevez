import boto3
import json

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

# Test event
test_event = {
    "httpMethod": "GET",
    "path": "/",
    "headers": {},
    "body": None
}

try:
    response = lambda_client.invoke(
        FunctionName='telehealth-api',
        Payload=json.dumps(test_event)
    )
    
    result = json.loads(response['Payload'].read())
    print(f"✅ Lambda response: {json.dumps(result, indent=2)}")
    
except Exception as e:
    print(f"❌ Error: {e}")