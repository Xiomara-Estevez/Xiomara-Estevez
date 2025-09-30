import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

def delete_api_gateway():
    apigateway = boto3.client(
        'apigateway',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    try:
        apigateway.delete_rest_api(restApiId='tpku5cs7u6')
        print("✅ Deleted old API Gateway")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    delete_api_gateway()