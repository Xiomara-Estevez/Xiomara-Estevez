import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

try:
    response = cognito.describe_user_pool(UserPoolId='us-east-2_fAESHksAx')
    domain = response.get('UserPool', {}).get('Domain')
    
    if domain:
        print(f"✅ Found domain: {domain}")
        print(f"🌐 Your Cognito login URL:")
        print(f"https://{domain}.auth.us-east-2.amazoncognito.com/login?client_id=6kr0t8kp0bughr3s2ut0106mrk&response_type=code&scope=openid+email+profile&redirect_uri=https://1fjxzto6nk.execute-api.us-east-1.amazonaws.com/prod/callback")
    else:
        print("❌ No domain found")
        
except Exception as e:
    print(f"❌ Error: {e}")