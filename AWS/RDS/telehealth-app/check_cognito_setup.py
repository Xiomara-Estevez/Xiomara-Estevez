import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# Check client configuration
try:
    client_info = cognito.describe_user_pool_client(
        UserPoolId='us-east-2_fAESHksAx',
        ClientId='6kr0t8kp0bughr3s2ut0106mrk'
    )
    
    client = client_info['UserPoolClient']
    print("📋 Client Configuration:")
    print(f"  OAuth Flows: {client.get('AllowedOAuthFlows', 'None')}")
    print(f"  OAuth Scopes: {client.get('AllowedOAuthScopes', 'None')}")
    print(f"  Callback URLs: {client.get('CallbackURLs', 'None')}")
    print(f"  Supported Providers: {client.get('SupportedIdentityProviders', 'None')}")
    
    # Check if Hosted UI is enabled
    if client.get('AllowedOAuthFlows'):
        print("✅ Hosted UI is configured")
        print("🌐 Try: https://us-east-2faeshksax.auth.us-east-2.amazoncognito.com/oauth2/authorize?client_id=6kr0t8kp0bughr3s2ut0106mrk&response_type=code&scope=openid&redirect_uri=https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/callback")
    else:
        print("❌ Hosted UI not configured")
        
except Exception as e:
    print(f"❌ Error: {e}")