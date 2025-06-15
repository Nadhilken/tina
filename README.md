# Voice Q&A Web Application

A Flask-based web application that provides voice-activated question and answer functionality with media management capabilities.

## Features

- **Voice Recognition**: Click the main GIF to start listening and ask questions
- **Q&A Management**: Add, edit, and delete question-answer pairs
- **Media Upload**: Upload and manage videos and images
- **Responsive Design**: Clean, modern interface with visual feedback
- **Speech Synthesis**: AI responds with voice answers

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: Web Speech API for voice recognition and synthesis
- **File Handling**: Secure file uploads with validation

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd receptoweb
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add required images to `static/images/`:
   - `i_robotics_logo.png` - Company logo
   - `your-gif.gif` - Main interactive GIF

4. Run the application:
   ```bash
   python app.py
   ```

## Deployment on Render

1. **Connect your repository** to Render
2. **Create a new Web Service**
3. **Use the following settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: `Python 3`

## File Structure

```
receptoweb/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── render.yaml        # Render deployment config
├── Procfile           # Process file for deployment
├── qa_data.json       # Q&A data storage
├── templates/
│   └── index.html     # Main HTML template
├── static/
│   ├── images/        # Logo and GIF files
│   ├── uploads/       # User uploaded files
│   │   ├── videos/    # Uploaded videos
│   │   └── images/    # Uploaded images
│   └── styles.css     # Additional styles (if needed)
└── README.md          # This file
```

## Usage

1. **Voice Interaction**: Click the main GIF to start voice recognition
2. **Manage Q&As**: Use the menu (☰) to add, edit, or delete questions
3. **Upload Media**: Drag and drop videos/images in the media section
4. **View Media**: Click uploaded items to view in full screen

## API Endpoints

- `GET /` - Main page
- `POST /add_qa` - Add new Q&A pair
- `GET /get_qas` - Retrieve all Q&As
- `PUT /update_qa/<id>` - Update specific Q&A
- `DELETE /delete_qa/<id>` - Delete specific Q&A
- `POST /get_answer` - Get answer for a question
- `POST /upload_video` - Upload video file
- `POST /upload_image` - Upload image file
- `GET /get_videos` - Get all videos
- `GET /get_images` - Get all images
- `DELETE /delete_video/<filename>` - Delete video
- `DELETE /delete_image/<filename>` - Delete image

## Browser Compatibility

- Chrome (recommended)
- Edge
- Firefox (limited speech recognition support)
- Safari (limited speech recognition support)

## Notes

- Microphone permission is required for voice recognition
- Uploaded files are stored in `static/uploads/`
- Q&A data is stored in `qa_data.json`
- Maximum file upload size: 100MB

## License

This project is licensed under the MIT License.