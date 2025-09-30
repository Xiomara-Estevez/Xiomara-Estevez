import json
from datetime import datetime, timezone

def lambda_handler(event, context):
    """Simple AWS Lambda handler for testing"""
    
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Handle root path
    if path == '/' or path == '':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Telehealth API is running',
                'endpoints': {
                    'health': '/api/health'
                }
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    # Simple health check without database dependency
    if path == '/api/health':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'ok',
                'time': datetime.now(timezone.utc).isoformat() + 'Z',
                'message': 'Telehealth API is running'
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    # Default response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello from {path}',
            'method': method
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

# Test locally
if __name__ == '__main__':
    test_event = {
        'httpMethod': 'GET',
        'path': '/api/health'
    }
    result = lambda_handler(test_event, {})
    print(json.dumps(result, indent=2))