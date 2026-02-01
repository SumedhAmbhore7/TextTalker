# TextTalker - Advanced Text to Speech Flask App

A modern, feature-rich Flask application that converts text to speech using Google Text-to-Speech (gTTS) with an enhanced web interface.

## Features

### Core Functionality
- Convert text to speech in 11 languages (English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese Simplified, Arabic)
- Web interface with responsive Bootstrap 5 design
- Audio files saved in MP3 format
- Error handling for various input scenarios

### Advanced Features
- **File Upload Support**: Upload .txt and .pdf files for conversion
- **Slow Mode**: Option to generate slower-paced speech for better comprehension
- **Emotion Control**: 8 different emotional tones (Happy, Sad, Excited, Calm, Angry, Surprised, Serious, Neutral) for more natural speech
- **Dark/Light Mode Toggle**: Switch between themes with persistent preference
- **Tabbed Interface**: Separate tabs for text input and file upload
- **Conversion History**: View and replay previous conversions in a collapsible sidebar
- **Enhanced Audio Player**: Styled audio controls with download option
- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop support

## Installation

1. Clone or download the project files.
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

   Note: If you encounter permission issues with virtual environments, you may need to run the command as an administrator or use a different directory.

## Usage

1. Run the Flask application:

   ```
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`

3. Choose your input method:
   - **Text Input Tab**: Enter text directly in the textarea
   - **File Upload Tab**: Drag & drop or browse to select a .txt or .pdf file

4. Configure options:
   - Select language from the dropdown
   - Enable slow mode if desired (checkbox)

5. Click "Convert to Speech" or "Convert File to Speech"

6. The audio will be generated and played directly in the browser

7. Additional features:
   - Toggle between dark and light themes using the button in the top-right
   - View conversion history by clicking "View History" after a conversion
   - Download audio files using the download button
   - Replay previous conversions from the history sidebar

## Project Structure

- `app.py`: Main Flask application with routes and backend logic
- `templates/index.html`: Modern HTML template with Bootstrap 5 and interactive features
- `static/audio/`: Directory where generated MP3 files are stored
- `requirements.txt`: Python dependencies
- `TODO.md`: Development task tracking (internal use)

## Dependencies

- **Flask==2.3.3**: Web framework for the application
- **gTTS==2.4.0**: Google Text-to-Speech library for audio generation
- **PyPDF2==3.0.1**: PDF text extraction library for file upload support
- **Flask-SQLAlchemy==3.0.5**: SQLAlchemy integration for Flask (database support)

## API Endpoints

- `GET /`: Main application page
- `POST /convert`: Convert text or uploaded file to speech
- `GET /history`: Retrieve conversion history (JSON)

## Browser Support

The application works in all modern browsers that support:
- HTML5 Audio
- ES6 JavaScript features
- CSS Custom Properties (CSS Variables)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
