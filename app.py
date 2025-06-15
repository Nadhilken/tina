from flask import Flask, render_template, request, jsonify
import json
import os
import logging
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# File to store questions and answers
DATA_FILE = 'qa_data.json'
# Directories for uploaded videos and images
VIDEO_UPLOAD_FOLDER = 'static/uploads/videos'
IMAGE_UPLOAD_FOLDER = 'static/uploads/images'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Ensure upload folders exist
for folder in [VIDEO_UPLOAD_FOLDER, IMAGE_UPLOAD_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Limit uploads to 100MB

# Check if file extension is allowed
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Load existing Q&A data and assign IDs to entries without them
def load_qa_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            # Assign IDs to entries missing them
            modified = False
            for qa in data:
                if 'id' not in qa:
                    qa['id'] = str(uuid.uuid4())
                    modified = True
            # Save updated data if IDs were added
            if modified:
                try:
                    with open(DATA_FILE, 'w') as f:
                        json.dump(data, f, indent=2)
                    logger.info("Assigned IDs to Q&A entries and saved updated qa_data.json")
                except Exception as e:
                    logger.error(f"Error saving updated Q&A data with IDs: {str(e)}")
            logger.debug(f"Loaded Q&A data: {data}")
            return data
        logger.debug("No Q&A file found, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error loading Q&A data: {str(e)}")
        return []

# Save Q&A data
def save_qa_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        logger.debug(f"Saved Q&A data: {data}")
    except Exception as e:
        logger.error(f"Error saving Q&A data: {str(e)}")

@app.route('/')
def index():
    try:
        logger.info("Attempting to render index.html")
        # First check if templates directory exists
        import os
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        index_file = os.path.join(templates_dir, 'index.html')
        logger.info(f"Templates directory: {templates_dir}")
        logger.info(f"Templates directory exists: {os.path.exists(templates_dir)}")
        logger.info(f"Index file exists: {os.path.exists(index_file)}")
        
        if os.path.exists(index_file):
            return render_template('index.html')
        else:
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Voice Q&A Website</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .voice-section { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 8px; }
                    .header-gif { background: linear-gradient(45deg, #1a73e8, #4285f4); width: 300px; height: 200px; margin: 0 auto 30px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; cursor: pointer; }
                    .header-gif:hover { opacity: 0.8; }
                    .header-gif.listening { border: 3px solid #ff0000; box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); background: linear-gradient(45deg, #ff6b6b, #ee5a52) !important; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header-gif" id="headerGif">Click here to start listening</div>
                    <div class="voice-section">
                        <h2>HI, HOW CAN I HELP YOU?</h2>
                        <p id="transcript">Click the box above to start listening and ask your question...</p>
                        <p id="response">Answer will appear here...</p>
                    </div>
                </div>
                
                <script>
                    const headerGif = document.getElementById('headerGif');
                    const transcript = document.getElementById('transcript');
                    const response = document.getElementById('response');
                    let isListening = false;
                    let recognition;

                    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
                        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                        recognition.lang = 'en-US';
                        recognition.interimResults = false;

                        headerGif.addEventListener('click', () => {
                            if (!isListening) {
                                try {
                                    recognition.start();
                                    transcript.textContent = 'Listening for your question...';
                                    isListening = true;
                                    headerGif.classList.add('listening');
                                } catch (error) {
                                    transcript.textContent = 'Error starting speech recognition: ' + error.message;
                                    isListening = false;
                                    headerGif.classList.remove('listening');
                                }
                            } else {
                                recognition.stop();
                                transcript.textContent = 'Click the box above to start listening...';
                                isListening = false;
                                headerGif.classList.remove('listening');
                            }
                        });

                        recognition.onresult = async (event) => {
                            const question = event.results[0][0].transcript;
                            transcript.textContent = `You asked: ${question}`;
                            isListening = false;
                            headerGif.classList.remove('listening');
                            
                            try {
                                const res = await fetch('/get_answer', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ question })
                                });
                                const data = await res.json();
                                response.textContent = `Answer: ${data.answer}`;
                                
                                const utterance = new SpeechSynthesisUtterance(data.answer);
                                utterance.lang = 'en-US';
                                window.speechSynthesis.speak(utterance);
                            } catch (error) {
                                response.textContent = 'Error getting answer. Please try again.';
                            }
                        };

                        recognition.onend = () => {
                            isListening = false;
                            headerGif.classList.remove('listening');
                        };

                        recognition.onerror = (event) => {
                            transcript.textContent = 'Error occurred in recognition: ' + event.error;
                            isListening = false;
                            headerGif.classList.remove('listening');
                        };
                    } else {
                        transcript.textContent = 'Speech recognition is not supported in this browser. Please use Chrome or Edge.';
                        headerGif.style.cursor = 'not-allowed';
                        headerGif.style.opacity = '0.5';
                    }
                </script>
            </body>
            </html>
            """
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Voice Q&A App is running'})

@app.route('/test')
def test_page():
    try:
        logger.info("Rendering test.html")
        return render_template('test.html')
    except Exception as e:
        logger.error(f"Error rendering test.html: {str(e)}")
        return f"Error: {str(e)}", 500

@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/add_qa', methods=['POST'])
def add_qa():
    try:
        question = request.form.get('question', '').lower().strip()
        answer = request.form.get('answer', '').strip()
        
        if not question or not answer:
            logger.warning("Empty question or answer received")
            return jsonify({'status': 'error', 'message': 'Question and answer cannot be empty'}), 400
        
        qa_data = load_qa_data()
        qa_id = str(uuid.uuid4())
        qa_data.append({'id': qa_id, 'question': question, 'answer': answer})
        save_qa_data(qa_data)
        
        logger.info(f"Added Q&A: {question} -> {answer} with ID: {qa_id}")
        return jsonify({'status': 'success', 'message': 'Question and answer added successfully'})
    except Exception as e:
        logger.error(f"Error in add_qa: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_qas', methods=['GET'])
def get_qas():
    try:
        qa_data = load_qa_data()
        logger.info(f"Retrieved {len(qa_data)} Q&A pairs")
        return jsonify({'status': 'success', 'qas': qa_data})
    except Exception as e:
        logger.error(f"Error in get_qas: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/update_qa/<qa_id>', methods=['PUT'])
def update_qa(qa_id):
    try:
        data = request.json
        new_question = data.get('question', '').lower().strip()
        new_answer = data.get('answer', '').strip()
        
        if not new_question or not new_answer:
            logger.warning("Empty question or answer in update request")
            return jsonify({'status': 'error', 'message': 'Question and answer cannot be empty'}), 400
        
        qa_data = load_qa_data()
        qa_found = False
        for qa in qa_data:
            if qa['id'] == qa_id:
                qa['question'] = new_question
                qa['answer'] = new_answer
                qa_found = True
                break
        
        if not qa_found:
            logger.warning(f"Q&A not found for ID: {qa_id}")
            return jsonify({'status': 'error', 'message': 'Q&A not found'}), 404
        
        save_qa_data(qa_data)
        logger.info(f"Updated Q&A with ID: {qa_id}")
        return jsonify({'status': 'success', 'message': 'Q&A updated successfully'})
    except Exception as e:
        logger.error(f"Error in update_qa: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/delete_qa/<qa_id>', methods=['DELETE'])
def delete_qa(qa_id):
    try:
        qa_data = load_qa_data()
        initial_length = len(qa_data)
        qa_data = [qa for qa in qa_data if qa['id'] != qa_id]
        
        if len(qa_data) == initial_length:
            logger.warning(f"Q&A not found for ID: {qa_id}")
            return jsonify({'status': 'error', 'message': 'Q&A not found'}), 404
        
        save_qa_data(qa_data)
        logger.info(f"Deleted Q&A with ID: {qa_id}")
        return jsonify({'status': 'success', 'message': 'Q&A deleted successfully'})
    except Exception as e:
        logger.error(f"Error in delete_qa: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        question = request.json.get('question', '').lower().strip()
        qa_data = load_qa_data()
        
        for qa in qa_data:
            if qa['question'] == question:
                logger.info(f"Found answer for question: {question}")
                return jsonify({'answer': qa['answer']})
        
        logger.warning(f"No answer found for question: {question}")
        return jsonify({'answer': 'Sorry, I don\'t know the answer to that question.'})
    except Exception as e:
        logger.error(f"Error in get_answer: {str(e)}")
        return jsonify({'answer': 'An error occurred while processing your request.'})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            logger.warning("No video file in request")
            return jsonify({'status': 'error', 'message': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            logger.warning("No selected file")
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            filename = secure_filename(file.filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            new_filename = filename
            while os.path.exists(os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], new_filename)):
                new_filename = f"{base}_{counter}{ext}"
                counter += 1
            file.save(os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], new_filename))
            video_count = len([f for f in os.listdir(app.config['VIDEO_UPLOAD_FOLDER']) if allowed_file(f, ALLOWED_VIDEO_EXTENSIONS)])
            logger.info(f"Video uploaded: {new_filename}, URL: /{VIDEO_UPLOAD_FOLDER}/{new_filename}")
            return jsonify({
                'status': 'success',
                'message': 'Video uploaded successfully',
                'filename': new_filename,
                'url': f"/{VIDEO_UPLOAD_FOLDER}/{new_filename}",
                'display_name': f"Video {video_count}"
            })
        else:
            logger.warning("Invalid file type")
            return jsonify({'status': 'error', 'message': 'Invalid file type. Only mp4, webm, and ogg are allowed.'}), 400
    except Exception as e:
        logger.error(f"Error in upload_video: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            logger.warning("No image file in request")
            return jsonify({'status': 'error', 'message': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            logger.warning("No selected file")
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            filename = secure_filename(file.filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            new_filename = filename
            while os.path.exists(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], new_filename)):
                new_filename = f"{base}_{counter}{ext}"
                counter += 1
            file.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], new_filename))
            image_count = len([f for f in os.listdir(app.config['IMAGE_UPLOAD_FOLDER']) if allowed_file(f, ALLOWED_IMAGE_EXTENSIONS)])
            logger.info(f"Image uploaded: {new_filename}, URL: /{IMAGE_UPLOAD_FOLDER}/{new_filename}")
            return jsonify({
                'status': 'success',
                'message': 'Image uploaded successfully',
                'filename': new_filename,
                'url': f"/{IMAGE_UPLOAD_FOLDER}/{new_filename}",
                'display_name': f"Image {image_count}"
            })
        else:
            logger.warning("Invalid file type")
            return jsonify({'status': 'error', 'message': 'Invalid file type. Only jpg, jpeg, png, and gif are allowed.'}), 400
    except Exception as e:
        logger.error(f"Error in upload_image: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_videos', methods=['GET'])
def get_videos():
    try:
        video_files = [f for f in os.listdir(VIDEO_UPLOAD_FOLDER) if allowed_file(f, ALLOWED_VIDEO_EXTENSIONS)]
        videos = [{'id': f, 'display_name': f"Video {i+1}", 'url': f"/{VIDEO_UPLOAD_FOLDER}/{f}"} for i, f in enumerate(video_files)]
        logger.info(f"Retrieved {len(videos)} videos: {video_files}")
        return jsonify({'status': 'success', 'videos': videos})
    except Exception as e:
        logger.error(f"Error in get_videos: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_images', methods=['GET'])
def get_images():
    try:
        image_files = [f for f in os.listdir(IMAGE_UPLOAD_FOLDER) if allowed_file(f, ALLOWED_IMAGE_EXTENSIONS)]
        logger.debug(f"Scanning folder {IMAGE_UPLOAD_FOLDER}: Found files {image_files}")
        images = [{'id': f, 'display_name': f"Image {i+1}", 'url': f"/{IMAGE_UPLOAD_FOLDER}/{f}"} for i, f in enumerate(image_files)]
        logger.info(f"Retrieved {len(images)} images: {image_files}")
        return jsonify({'status': 'success', 'images': images})
    except Exception as e:
        logger.error(f"Error in get_images: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/delete_video/<filename>', methods=['DELETE'])
def delete_video(filename):
    try:
        file_path = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Video deleted: {filename}")
            return jsonify({'status': 'success', 'message': 'Video deleted successfully'})
        else:
            logger.warning(f"Video not found: {filename}")
            return jsonify({'status': 'error', 'message': 'Video not found'}), 404
    except Exception as e:
        logger.error(f"Error in delete_video: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/delete_image/<filename>', methods=['DELETE'])
def delete_image(filename):
    try:
        file_path = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Image deleted: {filename}")
            return jsonify({'status': 'success', 'message': 'Image deleted successfully'})
        else:
            logger.warning(f"Image not found: {filename}")
            return jsonify({'status': 'error', 'message': 'Image not found'}), 404
    except Exception as e:
        logger.error(f"Error in delete_image: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)