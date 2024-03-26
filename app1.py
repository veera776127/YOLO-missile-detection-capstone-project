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
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif','mp4'}
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
        model = YOLO('missile_trained_weights/best.pt')
        # Run inference on the image file
        results = model(image_path, conf=0.01211)
        
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
        # Initialize empty session data
        session['uploaded_file_url'] = None
        session['result_image_url'] = None

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
                # Redirect to the results endpoint to avoid the refresh issue
                return redirect(url_for('results'))
    
    # If there's no POST request or after the images are cleared, just render the home page
    return render_template('index.html')

@app.route('/results')
def results():
    # Retrieve the image URLs from session and then clear the session
    uploaded_file_url = session.get('uploaded_file_url')
    result_image_url = session.get('result_image_url')
    # Clear session after retrieving the URLs
    session.pop('uploaded_file_url', None)
    session.pop('result_image_url', None)
    # Render the template with the image URLs
    return render_template('index.html', uploaded_file_url=uploaded_file_url, result_image_url=result_image_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Check if the file exists in the UPLOAD_FOLDER
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # Otherwise, serve from RESULTS_FOLDER
    elif os.path.exists(os.path.join(app.config['RESULTS_FOLDER'], filename)):
        return send_from_directory(app.config['RESULTS_FOLDER'], filename)
    else:
        return "File not found", 404
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


