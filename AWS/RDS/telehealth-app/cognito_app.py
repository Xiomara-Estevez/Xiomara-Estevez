import json
import boto3
from datetime import datetime, timezone

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

def lambda_handler(event, context):
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    # Health check
    if path == '/api/health':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'ok',
                'time': datetime.now(timezone.utc).isoformat() + 'Z',
                'auth': 'cognito-enabled'
            })
        }
    
    # Cognito login
    if path == '/api/auth/cognito-login':
        try:
            body = json.loads(event.get('body', '{}'))
            username = body.get('username')
            password = body.get('password')
            
            cognito = boto3.client(
                'cognito-idp',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name='us-east-1'
            )
            
            # Replace with your Cognito User Pool Client ID
            CLIENT_ID = "your-cognito-client-id"
            
            response = cognito.initiate_auth(
                ClientId=CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': True,
                    'access_token': response['AuthenticationResult']['AccessToken'],
                    'id_token': response['AuthenticationResult']['IdToken'],
                    'refresh_token': response['AuthenticationResult']['RefreshToken']
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': False,
                    'error': str(e)
                })
            }
    
    # Root
    if path == '/':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': '🏥 Telehealth API with Cognito',
                'endpoints': {
                    'health': '/api/health',
                    'cognito-login': '/api/auth/cognito-login'
                }
            })
        }
    
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }