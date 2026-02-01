#!/bin/bash

# PythonAnywhere Deployment Script for TextTalker
# Run this script in your PythonAnywhere bash console

echo "🚀 Starting TextTalker deployment to PythonAnywhere..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create database
echo "🗄️ Creating database..."
python -c "from app import db; db.create_all()"

# Set permissions for static files
echo "🔒 Setting file permissions..."
chmod 755 static/audio

# Create WSGI file
echo "📄 Creating WSGI configuration file..."
cp pythonanywhere_wsgi.py /var/www/sumedhambhore_pythonanywhere_com_wsgi.py

echo "✅ Deployment preparation complete!"
echo ""
echo "📋 Next steps in PythonAnywhere Web tab:"
echo "1. Set Source code to: /home/SumedhAmbhore/TextToSpeechApp"
echo "2. Set Working directory to: /home/SumedhAmbhore/TextToSpeechApp"
echo "3. Set WSGI configuration file to: /var/www/sumedhambhore_pythonanywhere_com_wsgi.py"
echo "4. Add static file mapping: URL=/static/ Directory=/home/SumedhAmbhore/TextToSpeechApp/static"
echo "5. Click Reload"
echo ""
echo "🎉 Your TextTalker app should be live!"
