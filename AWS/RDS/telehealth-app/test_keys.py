import boto3

# Replace with your actual keys
ACCESS_KEY = "AKIA2ZXNEABXMWPZVLVM"
SECRET_KEY = "oJtmEFdsJn5kV5o6hJqLNMbtnTg91sTLTs9nF2QB"

try:
    # Test with explicit credentials
    client = boto3.client(
        'sts',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-east-1'
    )
    
    response = client.get_caller_identity()
    print("✅ Keys work!")
    print(f"Account: {response['Account']}")
    print(f"User: {response['Arn']}")
    
except Exception as e:
    print(f"❌ Keys don't work: {e}")
    print("💡 Check if keys are copied correctly")