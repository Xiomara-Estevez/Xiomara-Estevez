import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# Update client for Hosted UI
try:
    cognito.update_user_pool_client(
        UserPoolId='us-east-2_fAESHksAx',
        ClientId='6kr0t8kp0bughr3s2ut0106mrk',
        CallbackURLs=['https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/callback'],
        LogoutURLs=['https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/logout'],
        AllowedOAuthFlows=['code'],
        AllowedOAuthScopes=['openid', 'email', 'profile'],
        AllowedOAuthFlowsUserPoolClient=True,
        SupportedIdentityProviders=['COGNITO']
    )
    
    print("✅ Hosted UI configured")
    print(f"🌐 Login URL: https://us-east-2faeshksax.auth.us-east-2.amazoncognito.com/login?client_id=6kr0t8kp0bughr3s2ut0106mrk&response_type=code&scope=openid+email+profile&redirect_uri=https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/callback")
    
except Exception as e:
    print(f"❌ Error: {e}")