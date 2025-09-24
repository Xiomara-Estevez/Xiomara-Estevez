"""
Database initialization script for Telehealth Application
Creates all tables, indexes, and sample data
"""

from config.database import db
import bcrypt

def create_tables():
    """Create all database tables"""
    
    tables = {
        'users': """
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                user_type VARCHAR(20) CHECK (user_type IN ('patient', 'provider', 'clinic', 'admin')) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                phone VARCHAR(15),
                date_of_birth DATE,
                gender VARCHAR(20),
                address TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                email_verified BOOLEAN DEFAULT FALSE,
                mfa_enabled BOOLEAN DEFAULT FALSE,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """,
        
        'patients': """
            CREATE TABLE IF NOT EXISTS patients (
                patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE,
                emergency_contact_name VARCHAR(100),
                emergency_contact_phone VARCHAR(15),
                emergency_contact_relationship VARCHAR(50),
                insurance_provider VARCHAR(100),
                insurance_policy_number VARCHAR(50),
                insurance_group_number VARCHAR(50),
                medical_history TEXT,
                allergies TEXT,
                current_medications TEXT,
                preferred_language VARCHAR(50) DEFAULT 'English',
                communication_preferences JSONB DEFAULT '{"email": true, "sms": true, "phone": false}',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """,
        
        'providers': """
            CREATE TABLE IF NOT EXISTS providers (
                provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE,
                medical_license_number VARCHAR(50) UNIQUE NOT NULL,
                license_state VARCHAR(2) NOT NULL,
                license_expiry_date DATE,
                specialty VARCHAR(100),
                subspecialty VARCHAR(100),
                years_experience INTEGER,
                education TEXT,
                certifications TEXT,
                languages_spoken TEXT[] DEFAULT ARRAY['English'],
                bio TEXT,
                consultation_fee DECIMAL(10,2) DEFAULT 150.00,
                follow_up_fee DECIMAL(10,2) DEFAULT 75.00,
                availability_schedule JSONB DEFAULT '{}',
                is_verified BOOLEAN DEFAULT FALSE,
                is_accepting_patients BOOLEAN DEFAULT TRUE,
                rating DECIMAL(3,2) DEFAULT 5.00,
                total_reviews INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """,
        
        'appointments': """
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                patient_id UUID REFERENCES patients(patient_id) ON DELETE CASCADE,
                provider_id UUID REFERENCES providers(provider_id) ON DELETE CASCADE,
                appointment_date TIMESTAMP NOT NULL,
                duration_minutes INTEGER DEFAULT 30,
                appointment_type VARCHAR(50) DEFAULT 'consultation' CHECK (appointment_type IN ('consultation', 'follow_up', 'urgent_care', 'therapy', 'screening')),
                status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show', 'rescheduled')),
                chief_complaint TEXT,
                symptoms TEXT,
                notes TEXT,
                diagnosis TEXT,
                treatment_plan TEXT,
                prescriptions JSONB DEFAULT '[]',
                follow_up_required BOOLEAN DEFAULT FALSE,
                follow_up_date DATE,
                payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'authorized', 'paid', 'failed', 'refunded', 'cancelled')),
                stripe_payment_intent_id VARCHAR(255),
                consultation_fee DECIMAL(10,2),
                total_amount DECIMAL(10,2),
                video_call_link VARCHAR(500),
                meeting_room_id VARCHAR(100),
                reminder_sent BOOLEAN DEFAULT FALSE,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                review TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """,
        
        'audit_logs': """
            CREATE TABLE IF NOT EXISTS audit_logs (
                log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(user_id),
                action VARCHAR(100) NOT NULL,
                resource_type VARCHAR(50) NOT NULL,
                resource_id UUID,
                old_values JSONB,
                new_values JSONB,
                ip_address INET,
                user_agent TEXT,
                session_id VARCHAR(255),
                timestamp TIMESTAMP DEFAULT NOW(),
                compliance_category VARCHAR(50) DEFAULT 'general' CHECK (compliance_category IN ('general', 'phi_access', 'phi_modification', 'authentication', 'authorization', 'payment'))
            );
        """,
        
        'user_sessions': """
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
                jwt_token_hash VARCHAR(255) NOT NULL,
                ip_address INET,
                user_agent TEXT,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """
    }
    
    # Create tables
    for table_name, query in tables.items():
        try:
            db.execute_query(query)
            print(f"✅ Table '{table_name}' created successfully")
        except Exception as e:
            print(f"❌ Failed to create table '{table_name}': {e}")
            return False
    
    return True

def create_indexes():
    """Create database indexes for performance"""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
        "CREATE INDEX IF NOT EXISTS idx_users_user_type ON users(user_type);",
        "CREATE INDEX IF NOT EXISTS idx_patients_user_id ON patients(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_providers_user_id ON providers(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_providers_specialty ON providers(specialty);",
        "CREATE INDEX IF NOT EXISTS idx_providers_verified ON providers(is_verified);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_provider ON appointments(provider_id);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_payment_status ON appointments(payment_status);",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);",
        "CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_user_sessions_expires ON user_sessions(expires_at);"
    ]
    
    for index in indexes:
        try:
            db.execute_query(index)
        except Exception as e:
            print(f"❌ Failed to create index: {e}")
    
    print("✅ All indexes created successfully")

def add_sample_data():
    """Add sample data for testing"""
    
    # Hash passwords
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Sample users
    sample_users = [
        {
            'email': 'admin@telehealth.com',
            'password': 'AdminPass123!',
            'user_type': 'admin',
            'first_name': 'System',
            'last_name': 'Administrator',
            'phone': '555-0000'
        },
        {
            'email': 'dr.smith@telehealth.com',
            'password': 'DocPass123!',
            'user_type': 'provider',
            'first_name': 'Dr. Sarah',
            'last_name': 'Smith',
            'phone': '555-0101',
            'date_of_birth': '1980-05-15',
            'gender': 'Female',
            'address': '456 Medical Plaza, Healthcare City, HC 12345'
        },
        {
            'email': 'patient1@telehealth.com',
            'password': 'Patient123!',
            'user_type': 'patient',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '555-0201',
            'date_of_birth': '1985-08-20',
            'gender': 'Male',
            'address': '123 Main St, Anytown, NY 12345'
        },
        {
            'email': 'patient2@telehealth.com',
            'password': 'Patient123!',
            'user_type': 'patient',
            'first_name': 'Jane',
            'last_name': 'Johnson',
            'phone': '555-0202',
            'date_of_birth': '1992-03-10',
            'gender': 'Female',
            'address': '789 Oak Ave, Somewhere, CA 90210'
        }
    ]
    
    # Insert sample users
    user_ids = {}
    for user in sample_users:
        try:
            user_query = """
                INSERT INTO users (email, password_hash, user_type, first_name, last_name, phone, date_of_birth, gender, address, email_verified)
                VALUES (%(email)s, %(password_hash)s, %(user_type)s, %(first_name)s, %(last_name)s, %(phone)s, %(date_of_birth)s, %(gender)s, %(address)s, TRUE)
                ON CONFLICT (email) DO UPDATE SET
                    password_hash = EXCLUDED.password_hash,
                    updated_at = NOW()
                RETURNING user_id;
            """
            
            user_data = user.copy()
            # Ensure optional keys exist to avoid KeyError during formatting
            for key in ('phone', 'date_of_birth', 'gender', 'address'):
                if key not in user_data:
                    user_data[key] = None

            user_data['password_hash'] = hash_password(user['password'])
            del user_data['password']  # Remove plain password
            
            result = db.execute_query(user_query, user_data, fetch='one')
            if result:
                user_ids[user['email']] = result['user_id']
                print(f"✅ User {user['email']} created")
            
        except Exception as e:
            print(f"❌ Failed to create user {user['email']}: {e}")
    
    # Add provider details
    if 'dr.smith@telehealth.com' in user_ids:
        provider_query = """
            INSERT INTO providers (user_id, medical_license_number, license_state, specialty, years_experience, consultation_fee, bio, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                medical_license_number = EXCLUDED.medical_license_number,
                specialty = EXCLUDED.specialty,
                updated_at = NOW();
        """
        
        try:
            db.execute_query(provider_query, (
                user_ids['dr.smith@telehealth.com'],
                'MD123456789',
                'NY',
                'Family Medicine',
                15,
                150.00,
                'Board-certified family physician with 15 years of experience providing comprehensive healthcare.',
                True
            ))
            print("✅ Provider details added for Dr. Smith")
        except Exception as e:
            print(f"❌ Failed to add provider details: {e}")
    
    # Add patient details
    patient_emails = ['patient1@telehealth.com', 'patient2@telehealth.com']
    for email in patient_emails:
        if email in user_ids:
            patient_query = """
                INSERT INTO patients (user_id, emergency_contact_name, emergency_contact_phone, emergency_contact_relationship, insurance_provider)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                    emergency_contact_name = EXCLUDED.emergency_contact_name,
                    updated_at = NOW();
            """
            
            try:
                db.execute_query(patient_query, (
                    user_ids[email],
                    'Emergency Contact',
                    '555-9999',
                    'Family',
                    'Sample Insurance Co.'
                ))
                print(f"✅ Patient details added for {email}")
            except Exception as e:
                print(f"❌ Failed to add patient details for {email}: {e}")

def main():
    """Main initialization function"""
    print("🚀 Initializing Telehealth Database...")
    print("=" * 50)
    
    # Test connection
    if not db.test_connection():
        print("❌ Database connection failed. Please check your .env file.")
        return False
    
    print("\n📊 Creating database schema...")
    if not create_tables():
        print("❌ Failed to create tables.")
        return False
    
    print("\n⚡ Creating indexes...")
    create_indexes()
    
    print("\n👥 Adding sample data...")
    add_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Database initialization completed successfully!")
    print("\n🔐 Sample Login Credentials:")
    print("  Admin: admin@telehealth.com / AdminPass123!")
    print("  Provider: dr.smith@telehealth.com / DocPass123!")
    print("  Patient 1: patient1@telehealth.com / Patient123!")
    print("  Patient 2: patient2@telehealth.com / Patient123!")
    
    return True

if __name__ == "__main__":
    main()