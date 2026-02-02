#!/usr/bin/env python
"""
Database initialization script for production deployment
Run this once on Vercel/production to create tables
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Ensure DATABASE_URL is set
if not os.environ.get('DATABASE_URL'):
    print("❌ DATABASE_URL not set. Please configure environment variables.")
    sys.exit(1)

from app import create_app, db

def init_db():
    """Initialize database with all tables"""
    app = create_app()
    
    with app.app_context():
        try:
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify tables
            from app.models.user import User
            from app.models.resume import Resume, ResumeContent
            
            print("\n📋 Tables created:")
            print("  - users")
            print("  - resumes")
            print("  - resume_content")
            
        except Exception as e:
            print(f"❌ Database initialization failed: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    init_db()
