import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

def setup_cognito():
    cognito = boto3.client(
        'cognito-idp',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    
    try:
        # Create User Pool
        user_pool = cognito.create_user_pool(
            PoolName='telehealth-users',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True
                }
            }
        )
        
        pool_id = user_pool['UserPool']['Id']
        print(f"✅ User Pool created: {pool_id}")
        
        # Create User Pool Client
        client = cognito.create_user_pool_client(
            UserPoolId=pool_id,
            ClientName='telehealth-client',
            ExplicitAuthFlows=['USER_PASSWORD_AUTH']
        )
        
        client_id = client['UserPoolClient']['ClientId']
        print(f"✅ Client created: {client_id}")
        
        print(f"\n🔧 Update cognito_app.py with:")
        print(f"CLIENT_ID = '{client_id}'")
        
        return pool_id, client_id
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    setup_cognito()