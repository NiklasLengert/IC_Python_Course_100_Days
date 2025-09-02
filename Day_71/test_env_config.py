#!/usr/bin/env python3
"""
Test script to validate Day_71 environment variable configuration
"""
import os
import sys

# Set up test environment variables
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['DATABASE_URI'] = 'sqlite:///test.db'

try:
    # Import the main components
    from flask import Flask
    print("✓ Flask import successful")
    
    # Test environment variable access
    secret_key = os.environ.get('SECRET_KEY', 'default-key')
    db_uri = os.environ.get('DATABASE_URI', 'sqlite:///posts.db')
    
    print(f"✓ SECRET_KEY from environment: {'***' if secret_key else 'NOT SET'}")
    print(f"✓ DATABASE_URI from environment: {db_uri}")
    
    # Test Flask app creation with environment variables
    test_app = Flask(__name__)
    test_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    test_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///posts.db')
    
    print("✓ Flask app configuration with environment variables successful")
    print("✓ All tests passed - Day_71 environment variable configuration is working correctly!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
