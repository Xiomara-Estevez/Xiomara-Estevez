import boto3

AWS_ACCESS_KEY_ID = "AKIA2ZXNEABXMWPZVLVM"
AWS_SECRET_ACCESS_KEY = "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"

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

# Find your existing User Pool
pools = cognito.list_user_pools(MaxResults=10)
for pool in pools['UserPools']:
    print(f"📋 Pool: {pool['Name']} - ID: {pool['Id']}")
    
    # Get clients for this pool
    clients = cognito.list_user_pool_clients(UserPoolId=pool['Id'])
    for client in clients['UserPoolClients']:
        print(f"  🔑 Client: {client['ClientName']} - ID: {client['ClientId']}")
    print()