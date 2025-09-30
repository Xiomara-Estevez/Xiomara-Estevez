import json
from datetime import datetime, timezone

def lambda_handler(event, context):
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    if path == '/api/health':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'ok',
                'time': datetime.now(timezone.utc).isoformat() + 'Z',
                'database': 'demo mode',
                'message': 'Telehealth API is healthy'
            })
        }
    
    if path == '/api/auth/login':
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '')
        
        if email == 'patient1@telehealth.com':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': True,
                    'access_token': 'demo-token-123',
                    'user': {
                        'email': email,
                        'user_type': 'patient',
                        'first_name': 'Demo',
                        'last_name': 'Patient'
                    }
                })
            }
        
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': False, 'error': 'Invalid credentials'})
        }
    
    if path == '/':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': '🏥 Telehealth API',
                'version': '1.0',
                'endpoints': {
                    'health': '/api/health',
                    'login': '/api/auth/login'
                }
            })
        }
    
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }