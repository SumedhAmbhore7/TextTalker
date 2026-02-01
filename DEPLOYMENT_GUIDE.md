# 🚀 TextTalker Deployment Guide for PythonAnywhere

## 📋 Quick Deployment Checklist

### ✅ Files Ready for Upload:
- [x] `app.py` - Main Flask application (production-ready)
- [x] `requirements.txt` - All dependencies
- [x] `templates/index.html` - Frontend interface
- [x] `pythonanywhere_wsgi.py` - WSGI configuration
- [x] `deploy_pythonanywhere.sh` - Deployment script
- [x] `static/audio/` - Directory for audio files

## 🔧 Step-by-Step Deployment

### 1. Upload Files to PythonAnywhere
Upload all project files to your PythonAnywhere account:
```
/home/SumedhAmbhore/
└── TextToSpeechApp/
    ├── app.py
    ├── requirements.txt
    ├── pythonanywhere_wsgi.py
    ├── templates/
    │   └── index.html
    ├── static/
    │   └── audio/
    └── DEPLOYMENT_GUIDE.md
```

### 2. Run Deployment Script
In PythonAnywhere's Bash console:
```bash
cd TextToSpeechApp
chmod +x deploy_pythonanywhere.sh
./deploy_pythonanywhere.sh
```

### 3. Configure Web App
In PythonAnywhere → Web tab:
- **Source code**: `/home/SumedhAmbhore/TextToSpeechApp`
- **Working directory**: `/home/SumedhAmbhore/TextToSpeechApp`
- **WSGI configuration file**: `/var/www/sumedhambhore_pythonanywhere_com_wsgi.py`

### 4. Set Up Static Files
In the Web tab, add static file mapping:
- **URL**: `/static/`
- **Directory**: `/home/SumedhAmbhore/TextToSpeechApp/static`

### 5. Reload and Test
Click the green "Reload" button in the Web tab.

## 📄 WSGI Configuration Content

The `pythonanywhere_wsgi.py` file contains:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/SumedhAmbhore/TextToSpeechApp'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the FLASK_ENV environment variable
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from app import app as application

# Optional: Set up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("WSGI application loaded successfully")
```

## 🔍 Troubleshooting

### If you get import errors:
1. Check that all files are uploaded correctly
2. Verify the project path in WSGI file matches your username
3. Make sure dependencies are installed: `pip install -r requirements.txt`

### If static files don't load:
1. Check static file mapping in Web tab
2. Ensure `static/audio/` directory exists and is writable

### If database errors occur:
1. Run: `python -c "from app import db; db.create_all()"`
2. Check file permissions: `chmod 755 static/audio`

## 🎯 Your App Features

Once deployed, your TextTalker app will have:
- ✅ Text-to-speech conversion in 11 languages
- ✅ File upload support (.txt, .pdf)
- ✅ Emotional text processing
- ✅ Dark/light theme toggle
- ✅ Conversion history with delete options
- ✅ Responsive Bootstrap 5 interface

## 🌐 Access Your App

After successful deployment, your app will be available at:
`https://sumedhambhore.pythonanywhere.com/`

## 📞 Support

If you encounter issues:
1. Check PythonAnywhere error logs in the Web tab
2. Verify all files are uploaded correctly
3. Ensure the WSGI path matches your domain name

Happy deploying! 🎉
