import json
from app import app

def lambda_handler(event, context):
    """AWS Lambda handler"""
    
    # Handle API Gateway requests
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/api/health')
    body = event.get('body', '')
    headers = event.get('headers', {})
    
    # Use Flask test client
    with app.test_client() as client:
        response = client.open(
            path, 
            method=method,
            data=body,
            headers=headers
        )
        
        return {
            'statusCode': response.status_code,
            'body': response.get_data(as_text=True),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }