from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory, session
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
from PIL import Image
import logging

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'C:/Users/vishw/Documents/flask/uploads/'
RESULTS_FOLDER = 'C:/Users/vishw/Documents/flask/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'your_very_secret_key'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def perform_object_detection(image_path):
    try:
        # Load YOLO model
        model = YOLO('yolov8n.pt')
        # Run inference on the image file
        results = model(image_path)
        
        # Visualize and save the results
        for i, result in enumerate(results):
            img_bgr = result.plot()  # Obtain the annotated image in BGR format
            img_rgb = Image.fromarray(img_bgr[..., ::-1])  # Convert BGR to RGB
            
            # Construct the result image path
            result_image_filename = f"result_{os.path.basename(image_path).split('.')[0]}_{i}.jpg"
            result_image_path = os.path.join(app.config['RESULTS_FOLDER'], result_image_filename)
            
            logging.info(f'Saving result image to: {result_image_path}')
            img_rgb.save(result_image_path)
        
        return result_image_path  # Return the path of the last result image saved
    except Exception as e:
        logging.error(f'Error occurred during object detection or image saving: {e}')
        flash(f'Error occurred during object detection: {e}')
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            result_image_path = perform_object_detection(filepath)
            
            if result_image_path:
                # Store the image URLs in the session
                session['uploaded_file_url'] = url_for('uploaded_file', filename=filename)
                session['result_image_url'] = url_for('uploaded_file', filename=os.path.basename(result_image_path))
                # Redirect to the results endpoint
                return redirect(url_for('results'))
    
    # Clear the session for the image URLs if present
    session.pop('uploaded_file_url', None)
    session.pop('result_image_url', None)
    return render_template('index.html')

@app.route('/results')
def results():
    # Get the image URLs from the session
    uploaded_file_url = session.pop('uploaded_file_url', None)
    result_image_url = session.pop('result_image_url', None)
    # Render the template with the image URLs
    return render_template('index.html', uploaded_file_url=uploaded_file_url, result_image_url=result_image_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
