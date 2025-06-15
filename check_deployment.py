#!/usr/bin/env python3
"""
Deployment readiness checker
Run this script to verify all files are ready for Render deployment
"""

import os
import json

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MISSING")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} - MISSING")
        return False

def main():
    print("🔍 Checking deployment readiness...\n")
    
    issues = []
    
    # Core application files
    print("📁 Core Application Files:")
    if not check_file_exists("app.py", "Main Flask application"):
        issues.append("app.py is missing")
    if not check_file_exists("requirements.txt", "Python dependencies"):
        issues.append("requirements.txt is missing")
    if not check_file_exists("render.yaml", "Render configuration"):
        issues.append("render.yaml is missing")
    if not check_file_exists("Procfile", "Process file"):
        issues.append("Procfile is missing")
    
    print("\n📄 Template Files:")
    if not check_file_exists("templates/index.html", "Main HTML template"):
        issues.append("templates/index.html is missing")
    
    print("\n📊 Data Files:")
    if not check_file_exists("qa_data.json", "Q&A data"):
        issues.append("qa_data.json is missing")
    
    print("\n🖼️ Static Files:")
    check_directory_exists("static", "Static files directory")
    check_directory_exists("static/images", "Images directory")
    check_directory_exists("static/uploads", "Uploads directory")
    check_directory_exists("static/uploads/videos", "Videos upload directory")
    check_directory_exists("static/uploads/images", "Images upload directory")
    
    print("\n🎨 Required Images:")
    if not check_file_exists("static/images/i_robotics_logo.png", "I_ROBOTICS Logo"):
        issues.append("Logo image is missing - add i_robotics_logo.png to static/images/")
    if not check_file_exists("static/images/your-gif.gif", "Main interactive GIF"):
        issues.append("Main GIF is missing - add your-gif.gif to static/images/")
    
    print("\n📚 Documentation:")
    check_file_exists("README.md", "Project README")
    check_file_exists("DEPLOYMENT.md", "Deployment guide")
    
    # Check requirements.txt content
    print("\n🐍 Python Dependencies:")
    try:
        with open("requirements.txt", "r") as f:
            reqs = f.read().strip()
            if "Flask" in reqs and "gunicorn" in reqs:
                print("✅ Requirements.txt contains Flask and gunicorn")
            else:
                print("❌ Requirements.txt missing essential dependencies")
                issues.append("requirements.txt incomplete")
    except FileNotFoundError:
        pass
    
    # Check qa_data.json format
    print("\n📋 Q&A Data Format:")
    try:
        with open("qa_data.json", "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                print(f"✅ Q&A data is valid JSON list with {len(data)} entries")
            else:
                print("❌ Q&A data is not a valid list")
                issues.append("qa_data.json format incorrect")
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Q&A data is not valid JSON")
        issues.append("qa_data.json is invalid")
    
    # Summary
    print("\n" + "="*50)
    if not issues:
        print("🎉 All checks passed! Ready for deployment to Render.")
        print("\n📝 Next steps:")
        print("1. Push all files to your GitHub repository")
        print("2. Connect repository to Render")
        print("3. Deploy as web service")
        print("4. Add required images if not already present")
    else:
        print(f"⚠️  Found {len(issues)} issue(s) that need attention:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n🔧 Fix these issues before deploying to Render.")

if __name__ == "__main__":
    main()