#!/usr/bin/env python3
"""Test Lambda function locally to debug issues"""

import json
import os
import sys

# Set environment variables for testing
os.environ['FLASK_ENV'] = 'production'
os.environ['DEBUG'] = 'True'

try:
    from lambda_handler import lambda_handler
    
    # Test event for health endpoint
    test_event = {
        'httpMethod': 'GET',
        'path': '/api/health',
        'headers': {},
        'body': None
    }
    
    print("🧪 Testing Lambda function locally...")
    print(f"Event: {json.dumps(test_event, indent=2)}")
    
    result = lambda_handler(test_event, {})
    print(f"\n✅ Result: {json.dumps(result, indent=2)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()