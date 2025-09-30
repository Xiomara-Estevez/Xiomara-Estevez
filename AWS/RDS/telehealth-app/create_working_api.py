import boto3
import json

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

def create_working_api():
    apigateway = boto3.client(
        'apigateway',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    # Delete old API if exists
    try:
        apigateway.delete_rest_api(restApiId='i538kj0gzi')
        print("🗑️ Deleted old API")
    except:
        pass
    
    # Create new API
    api = apigateway.create_rest_api(
        name='telehealth-working',
        description='Working Telehealth API'
    )
    api_id = api['id']
    print(f"✅ Created API: {api_id}")
    
    # Get root resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']
    
    # Get Lambda ARN
    lambda_info = lambda_client.get_function(FunctionName='telehealth-api')
    lambda_arn = lambda_info['Configuration']['FunctionArn']
    
    # Create proxy resource {proxy+}
    proxy_resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='{proxy+}'
    )
    proxy_id = proxy_resource['id']
    
    # Add ANY method to proxy
    apigateway.put_method(
        restApiId=api_id,
        resourceId=proxy_id,
        httpMethod='ANY',
        authorizationType='NONE'
    )
    
    # Add integration
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=proxy_id,
        httpMethod='ANY',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    
    # Add ANY method to root
    apigateway.put_method(
        restApiId=api_id,
        resourceId=root_id,
        httpMethod='ANY',
        authorizationType='NONE'
    )
    
    # Add integration to root
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=root_id,
        httpMethod='ANY',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    
    # Add Lambda permission
    try:
        sts = boto3.client('sts', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        account_id = sts.get_caller_identity()['Account']
        
        lambda_client.add_permission(
            FunctionName='telehealth-api',
            StatementId=f'api-gateway-{api_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:{account_id}:{api_id}/*/*'
        )
        print("✅ Added permission")
    except Exception as e:
        print(f"Permission: {e}")
    
    # Deploy
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    
    url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod"
    print(f"🌐 API URL: {url}")
    return url

if __name__ == '__main__':
    create_working_api()