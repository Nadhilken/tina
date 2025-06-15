#!/usr/bin/env python3
"""
Simple test script to verify the Flask app works
Run this before deploying to catch basic issues
"""

import sys
import requests
from app import app

def test_routes():
    """Test basic routes"""
    print("🧪 Testing Flask application routes...")
    
    with app.test_client() as client:
        # Test home route
        print("Testing / route...")
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home route works")
        else:
            print(f"❌ Home route failed: {response.status_code}")
            return False
        
        # Test health route
        print("Testing /health route...")
        response = client.get('/health')
        if response.status_code == 200:
            print("✅ Health route works")
        else:
            print(f"❌ Health route failed: {response.status_code}")
            return False
        
        # Test get_qas route
        print("Testing /get_qas route...")
        response = client.get('/get_qas')
        if response.status_code == 200:
            print("✅ Get QAs route works")
        else:
            print(f"❌ Get QAs route failed: {response.status_code}")
            return False
    
    print("\n🎉 All basic tests passed!")
    return True

def test_templates():
    """Test if templates render without errors"""
    print("\n📄 Testing template rendering...")
    
    try:
        with app.test_client() as client:
            response = client.get('/')
            if b"HI,HOW CAN I HELP YOU?" in response.data:
                print("✅ Template renders correctly")
                return True
            else:
                print("❌ Template content not found")
                return False
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

def main():
    print("🚀 Starting Flask application tests...\n")
    
    success = True
    success &= test_routes()
    success &= test_templates()
    
    if success:
        print("\n✅ All tests passed! Application is ready for deployment.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())