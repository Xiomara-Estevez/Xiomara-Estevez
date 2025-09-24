"""
API Testing Script for Telehealth Application
Test all endpoints with sample data
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:5000"
TEST_CREDENTIALS = {
    "provider": {"email": "dr.smith@telehealth.com", "password": "DocPass123!"},
    "patient": {"email": "patient1@telehealth.com", "password": "Patient123!"},
    "admin": {"email": "admin@telehealth.com", "password": "AdminPass123!"}
}

class TelehealthAPITester:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.tokens = {}
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("🏥 Testing health check...")
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Health check passed")
                print(f"  📊 Database: {data.get('database', 'unknown')}")
                return True
            else:
                print(f"  ❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Health check error: {e}")
            return False
    
    def test_login(self, user_type="patient"):
        """Test login for different user types"""
        print(f"🔐 Testing login for {user_type}...")
        try:
            credentials = TEST_CREDENTIALS[user_type]
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=credentials,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.tokens[user_type] = data['access_token']
                    user_info = data['user']
                    print(f"  ✅ Login successful for {user_info['first_name']} {user_info['last_name']}")
                    print(f"  👤 User Type: {user_info['user_type']}")
                    return True
                else:
                    print(f"  ❌ Login failed: {data.get('error')}")
                    return False
            else:
                print(f"  ❌ Login failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Login error: {e}")
            return False
    
    def test_profile(self, user_type="patient"):
        """Test profile retrieval"""
        print(f"👤 Testing profile for {user_type}...")
        try:
            if user_type not in self.tokens:
                print(f"  ❌ No token for {user_type}. Login first.")
                return False
            
            headers = {
                "Authorization": f"Bearer {self.tokens[user_type]}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/api/users/profile",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    profile = data['profile']
                    print(f"  ✅ Profile retrieved for {profile['first_name']} {profile['last_name']}")
                    print(f"  📧 Email: {profile['email']}")
                    if 'provider_info' in profile:
                        print(f"  👨‍⚕️ Specialty: {profile['provider_info']['specialty']}")
                    if 'patient_info' in profile:
                        print(f"  🏥 Insurance: {profile['patient_info'].get('insurance_provider', 'N/A')}")
                    return True
                else:
                    print(f"  ❌ Profile failed: {data.get('error')}")
                    return False
            else:
                print(f"  ❌ Profile failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Profile error: {e}")
            return False
    
    def test_appointments(self, user_type="patient"):
        """Test appointments retrieval"""
        print(f"📅 Testing appointments for {user_type}...")
        try:
            if user_type not in self.tokens:
                print(f"  ❌ No token for {user_type}. Login first.")
                return False
            
            headers = {
                "Authorization": f"Bearer {self.tokens[user_type]}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/api/appointments",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    appointments = data['appointments']
                    print(f"  ✅ Found {len(appointments)} appointments")
                    for apt in appointments[:3]:  # Show first 3
                        print(f"    📋 {apt['appointment_type']} - {apt['status']}")
                    return True
                else:
                    print(f"  ❌ Appointments failed: {data.get('error')}")
                    return False
            else:
                print(f"  ❌ Appointments failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Appointments error: {e}")
            return False
    
    def test_providers(self, user_type="patient"):
        """Test providers list"""
        print(f"👨‍⚕️ Testing providers list...")
        try:
            if user_type not in self.tokens:
                print(f"  ❌ No token for {user_type}. Login first.")
                return False
            
            headers = {
                "Authorization": f"Bearer {self.tokens[user_type]}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/api/providers",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    providers = data['providers']
                    print(f"  ✅ Found {len(providers)} providers")
                    for provider in providers:
                        print(f"    👨‍⚕️ Dr. {provider['first_name']} {provider['last_name']} - {provider['specialty']}")
                        print(f"       💰 ${provider['consultation_fee']:.2f} | ⭐ {provider['rating']}/5.0")
                    return True
                else:
                    print(f"  ❌ Providers failed: {data.get('error')}")
                    return False
            else:
                print(f"  ❌ Providers failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Providers error: {e}")
            return False
    
    def test_database_info(self, user_type="admin"):
        """Test database info endpoint"""
        print(f"🧪 Testing database info...")
        try:
            if user_type not in self.tokens:
                print(f"  ❌ No token for {user_type}. Login first.")
                return False
            
            headers = {
                "Authorization": f"Bearer {self.tokens[user_type]}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/api/test/database",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    db_info = data['database_info']
                    print(f"  ✅ Database has {db_info['total_tables']} tables")
                    for table in db_info['tables']:
                        print(f"    📊 {table['table_name']}: {table['rows']} rows, {table['columns']} columns")
                    return True
                else:
                    print(f"  ❌ Database info failed: {data.get('error')}")
                    return False
            else:
                print(f"  ❌ Database info failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Database info error: {e}")
            return False
    
    def run_full_test(self):
        """Run complete test suite"""
        print("🧪 Starting Telehealth API Test Suite")
        print("=" * 60)
        
        tests_passed = 0
        total_tests = 0
        
        # Health check
        total_tests += 1
        if self.test_health_check():
            tests_passed += 1
        
        print()
        
        # Test login for all user types
        for user_type in ["patient", "provider", "admin"]:
            total_tests += 1
            if self.test_login(user_type):
                tests_passed += 1
            print()
        
        # Test protected endpoints for each user type
        for user_type in ["patient", "provider"]:
            # Profile test
            total_tests += 1
            if self.test_profile(user_type):
                tests_passed += 1
            print()
            
            # Appointments test
            total_tests += 1
            if self.test_appointments(user_type):
                tests_passed += 1
            print()
        
        # Providers test (patient view)
        total_tests += 1
        if self.test_providers("patient"):
            tests_passed += 1
        print()
        
        # Database test (admin view)
        total_tests += 1
        if self.test_database_info("admin"):
            tests_passed += 1
        
        print()
        print("=" * 60)
        print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
        if tests_passed == total_tests:
            print("🎉 All tests passed! Your API is working correctly.")
        else:
            print(f"⚠️  {total_tests - tests_passed} tests failed. Check the output above.")
        print("=" * 60)
        
        return tests_passed == total_tests

if __name__ == "__main__":
    tester = TelehealthAPITester()
    tester.run_full_test()