from flask import Flask, request, jsonify, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from gtts import gTTS
import os
import uuid
import PyPDF2
import io
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///texttalker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure the static/audio directory exists
if not os.path.exists('static/audio'):
    os.makedirs('static/audio')

# Database model for history
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_preview = db.Column(db.String(50), nullable=False)
    audio_file_path = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    slow = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text_preview': self.text_preview,
            'audio_file_path': self.audio_file_path,
            'language': self.language,
            'slow': self.slow,
            'timestamp': self.timestamp.isoformat()
        }

# Create database tables
with app.app_context():
    db.create_all()

# Expanded language options
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese (Simplified)',
    'ar': 'Arabic'
}

def extract_text_from_file(file):
    """Extract text from uploaded file (.txt or .pdf)"""
    filename = file.filename.lower()
    if filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf are supported.")

@app.route('/')
def index():
    return render_template('index.html')

def apply_emotion_to_text(text, emotion):
    """Apply emotional modifications to text for more natural speech"""
    if emotion == 'neutral':
        return text

    # Clean and prepare text
    text = text.strip()

    if emotion == 'happy':
        # Add exclamation marks and upbeat punctuation
        text = text.replace('.', '!').replace('?', '!').replace('!', '!!')
        if not text.endswith('!'):
            text += '!'
        # Add happy expressions occasionally
        text = text.replace('hello', 'hello there').replace('hi', 'hey there')

    elif emotion == 'sad':
        # Add ellipses and slower pacing indicators
        text = text.replace('.', '...').replace('!', '.').replace('?', '...')
        if not text.endswith('.'):
            text += '...'

    elif emotion == 'excited':
        # Add multiple exclamation marks and capital letters for emphasis
        text = text.replace('.', '!!!').replace('!', '!!!').replace('?', '?!')
        if not text.endswith('!'):
            text += '!!!'
        # Add excited words
        text = text.replace('great', 'awesome').replace('good', 'amazing')

    elif emotion == 'calm':
        # Add commas for pauses, slower delivery
        sentences = text.split('.')
        calm_sentences = []
        for sentence in sentences:
            if len(sentence.strip()) > 20:
                words = sentence.split()
                if len(words) > 5:
                    # Insert commas for breathing pauses
                    insert_pos = len(words) // 2
                    words.insert(insert_pos, ',')
                calm_sentences.append(' '.join(words))
            else:
                calm_sentences.append(sentence)
        text = '.'.join(calm_sentences)

    elif emotion == 'angry':
        # Add forceful punctuation and emphasis
        text = text.replace('.', '!').replace('?', '!').replace('!', '!')
        if not text.endswith('!'):
            text += '!'

    elif emotion == 'surprised':
        # Add question marks and exclamations
        text = text.replace('.', '?!').replace('!', '?!').replace('?', '?!')
        if not text.endswith('?') and not text.endswith('!'):
            text += '?!'

    elif emotion == 'serious':
        # Add periods for deliberate delivery
        text = text.replace('!', '.').replace('?', '.')
        if not text.endswith('.'):
            text += '.'

    return text

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    language = request.form.get('language', 'en')
    slow = request.form.get('slow', 'false').lower() == 'true'
    emotion = request.form.get('emotion', 'neutral')

    # Handle file upload
    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        try:
            text = extract_text_from_file(file)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400

    if not text or text.strip() == '':
        return jsonify({'error': 'Text cannot be empty'}), 400

    try:
        # Apply emotional modifications to text
        processed_text = apply_emotion_to_text(text, emotion)

        # Adjust speed based on emotion
        emotion_slow = slow
        if emotion in ['calm', 'sad', 'serious']:
            emotion_slow = True  # Force slow for calm/sad/serious emotions
        elif emotion in ['excited', 'angry', 'surprised']:
            emotion_slow = False  # Force normal speed for high-energy emotions

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join('static/audio', filename)

        # Create gTTS object and save
        tts = gTTS(text=processed_text, lang=language, slow=emotion_slow)
        tts.save(filepath)

        # Save to database
        text_preview = text[:50] + '...' if len(text) > 50 else text
        history_entry = History(
            text_preview=text_preview,
            audio_file_path=f'/static/audio/{filename}',
            language=language,
            slow=emotion_slow
        )
        db.session.add(history_entry)
        db.session.commit()

        return jsonify({
            'file_path': f'/static/audio/{filename}',
            'history_id': history_entry.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    # Get last 10 conversions ordered by timestamp descending
    history_entries = History.query.order_by(History.timestamp.desc()).limit(10).all()
    return jsonify([entry.to_dict() for entry in history_entries])

@app.route('/history/<int:history_id>', methods=['DELETE'])
def delete_history_item(history_id):
    try:
        history_item = History.query.get_or_404(history_id)
        # Delete the associated audio file
        audio_path = os.path.join('static/audio', history_item.audio_file_path.split('/')[-1])
        if os.path.exists(audio_path):
            os.remove(audio_path)
        # Delete the database record
        db.session.delete(history_item)
        db.session.commit()
        return jsonify({'message': 'History item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['DELETE'])
def clear_all_history():
    try:
        # Get all history items
        all_history = History.query.all()

        # Delete all associated audio files
        for item in all_history:
            audio_path = os.path.join('static/audio', item.audio_file_path.split('/')[-1])
            if os.path.exists(audio_path):
                os.remove(audio_path)

        # Delete all database records
        deleted_count = History.query.delete()
        db.session.commit()

        return jsonify({
            'message': f'All history cleared successfully. Deleted {deleted_count} items.',
            'deleted_count': deleted_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
