#!/usr/bin/env python3
"""
Local development server script
Usage: python run_local.py
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("Starting Voice Q&A Application in development mode...")
    print("Visit: http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)