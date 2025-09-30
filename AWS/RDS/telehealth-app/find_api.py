import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

apigateway = boto3.client(
    'apigateway',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

apis = apigateway.get_rest_apis()
for api in apis['items']:
    if 'telehealth' in api['name'].lower():
        print(f"🌐 {api['name']}: https://{api['id']}.execute-api.us-east-1.amazonaws.com/prod")