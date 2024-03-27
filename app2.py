from flask import Flask, render_template, request, redirect, flash, send_from_directory, session, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image
import logging

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads/'
RESULTS_FOLDER = 'results/'
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
            
            # Save the uploaded image URL to session
            session['uploaded_file_url'] = url_for('uploaded_file', filename=filename)
            # Redirect to the results endpoint to display uploaded image
            return redirect(url_for('results'))
    
    # If there's no POST request or after the images are cleared, just render the home page
    return render_template('index1.html')

@app.route('/results')
def results():
    # Retrieve the image URLs from session
    uploaded_file_url = session.get('uploaded_file_url')
    # Render the template with the uploaded image URL
    return render_template('index1.html', uploaded_file_url=uploaded_file_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Check if the file exists in the UPLOAD_FOLDER
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
