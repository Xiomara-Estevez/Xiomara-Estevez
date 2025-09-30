import json

def lambda_handler(event, context):
    """Minimal Lambda handler for API Gateway"""
    
    # Log the event for debugging
    print(f"Event: {json.dumps(event)}")
    
    try:
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        
        if path == '/':
            body = {
                'message': 'Telehealth API is running!',
                'endpoints': ['/api/health']
            }
        elif path == '/api/health':
            body = {
                'status': 'ok',
                'message': 'Health check passed'
            }
        else:
            body = {
                'message': f'Path {path} not found',
                'method': method
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(body)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }