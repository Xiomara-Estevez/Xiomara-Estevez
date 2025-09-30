import json
from app import app

def lambda_handler(event, context):
    """AWS Lambda handler for Flask app"""
    
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/api/health')
    body = event.get('body', '')
    
    with app.test_client() as client:
        response = client.open(path, method=method, data=body)
        
        return {
            'statusCode': response.status_code,
            'body': response.get_data(as_text=True),
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