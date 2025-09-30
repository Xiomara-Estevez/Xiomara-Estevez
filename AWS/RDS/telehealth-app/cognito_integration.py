import json
import boto3

# UPDATE THESE WITH YOUR COGNITO DETAILS
USER_POOL_ID = "us-east-2_fAESHksAx"  # e.g., us-east-1_xxxxxxxxx
CLIENT_ID = "6kr0t8kp0bughr3s2ut0106mrk"        # New client without secret

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "oJtmEFdsJn5kV5o6hJqLNMbtnTg91sTLTs9nF2QB"

def lambda_handler(event, context):
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    if path == '/api/auth/login':
        try:
            request_body = event.get('body')
            if not request_body:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'success': False,
                        'error': 'Request body is required'
                    })
                }
            
            body = json.loads(request_body)
            username = body.get('username')
            password = body.get('password')
            
            if not username or not password:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'success': False,
                        'error': 'Username and password are required'
                    })
                }
            
            cognito = boto3.client(
                'cognito-idp',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name='us-east-2'  # Your Cognito pool region
            )
            
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
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': True,
                    'access_token': response['AuthenticationResult']['AccessToken'],
                    'user': username
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': str(e)
                })
            }
    
    if path == '/callback':
        # Handle Cognito callback
        code = event.get('queryStringParameters', {}).get('code')
        if code:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': f'<h2>✅ Login Successful!</h2><p>Authorization code: {code}</p>'
            }
        else:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'text/html'},
                'body': '<h2>❌ Login Failed</h2>'
            }
    
    if path == '/':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': '🏥 Telehealth API with Cognito',
                'hosted_login': 'https://us-east-2faeshksax.auth.us-east-2.amazoncognito.com/login?client_id=6kr0t8kp0bughr3s2ut0106mrk&response_type=code&scope=openid+email+profile&redirect_uri=https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/callback'
            })
        }
    
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }