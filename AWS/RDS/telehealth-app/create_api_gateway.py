import boto3
import json
import time

# Use your real keys that worked before
AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "oJtmEFdsJn5kV5o6hJqLNMbtnTg91sTLTs9nF2QB"

# Your API Gateway creation code here...
def create_api_gateway():
    """Create API Gateway with Lambda integration"""
    
    # API Gateway client
    apigateway = boto3.client(
        'apigateway',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    # Lambda client
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    print("🚀 Creating API Gateway...")
    
    try:
        # Create REST API
        api_response = apigateway.create_rest_api(
            name='telehealth-api',
            description='Telehealth API Gateway for Lambda',
            endpointConfiguration={'types': ['REGIONAL']},
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "execute-api:Invoke",
                        "Resource": "*"
                    }
                ]
            })
        )
        
        api_id = api_response['id']
        print(f"✅ API Gateway created: {api_id}")
        
        # Get root resource
        resources = apigateway.get_resources(restApiId=api_id)
        root_resource_id = None
        for resource in resources['items']:
            if resource['path'] == '/':
                root_resource_id = resource['id']
                break
        
        print(f"✅ Found root resource: {root_resource_id}")
        
        # Create proxy resource
        proxy_resource = apigateway.create_resource(
            restApiId=api_id,
            parentId=root_resource_id,
            pathPart='{proxy+}'
        )

        
        proxy_resource_id = proxy_resource['id']
        print(f"✅ Created proxy resource: {proxy_resource_id}")
        
        # Get Lambda function ARN
        lambda_response = lambda_client.get_function(FunctionName='telehealth-api')
        lambda_arn = lambda_response['Configuration']['FunctionArn']
        
        # Create ANY method on proxy resource
        apigateway.put_method(
            restApiId=api_id,
            resourceId=proxy_resource_id,
            httpMethod='ANY',
            authorizationType='NONE'
        )
        
        print("✅ Created ANY method")
        
        # Set up Lambda integration
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=proxy_resource_id,
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
        )
        
        print("✅ Created Lambda integration")
        
        # Add permission for API Gateway to invoke Lambda
        try:
            lambda_client.add_permission(
                FunctionName='telehealth-api',
                StatementId='api-gateway-invoke',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f'arn:aws:execute-api:us-east-1:*:*/*/*'
            )
            print("✅ Added Lambda invoke permission")
        except Exception as e:
            if "ResourceConflictException" in str(e):
                print("✅ Lambda permission already exists")
            else:
                print(f"⚠️ Permission error: {e}")
        
        # Deploy API
        deployment = apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='Production deployment'
        )
        
        print("✅ API deployed to 'prod' stage")
        
        # Return API URL
        api_url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod"
        print(f"\n🎉 API Gateway created successfully!")
        print(f"🌐 Your API URL: {api_url}")
        print(f"\n📍 Test endpoints:")
        print(f"   Health check: {api_url}/api/health")
        print(f"   Login: {api_url}/api/auth/login")
        
        return api_url
        
    except Exception as e:
        print(f"❌ Failed to create API Gateway: {e}")
        return None

if __name__ == '__main__':
    print("🚀 Starting API Gateway creation...")
    
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
        print(f"❌ Credentials failed: {e}")
        print("💡 Update your keys in this script!")
        exit(1)
    
    # Create API Gateway
    api_url = create_api_gateway()
    
    if api_url:
        print(f"\n🎯 Next steps:")
        print(f"1. Test your API: curl {api_url}/api/health")
        print(f"2. Your telehealth app is now live on the internet!")
        print(f"3. Share this URL with others to access your API")
    else:
        print("\n❌ Failed to create API Gateway")
    

