import json

def lambda_handler(event, context):
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    if path == '/':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': '🏥 Telehealth API is running!',
                'endpoints': {
                    'health': '/api/health',
                    'status': '/status'
                }
            })
        }
    
    if path == '/api/health':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'healthy',
                'message': 'All systems operational'
            })
        }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'message': f'Hello from {path}',
            'method': method
        })
    }