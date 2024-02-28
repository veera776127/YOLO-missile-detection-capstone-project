from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from YOLOv8_objectdetection.entity.config_entity import ModelPredictionConfig
from YOLOv8_objectdetection.components.model_prediction import YOLOInference
import os
import yaml
import traceback

app = Flask(__name__)

# Set up paths based on params.yaml
params_file_path = 'C:/Users/vishw/Documents/cap_project_tulasi/YOLO-missile-detection-capstone-project/params.yaml'
with open(params_file_path, 'r') as file:
    params = yaml.safe_load(file)

# Create directories if they don't exist
os.makedirs(params['path']['test_images_path'], exist_ok=True)
os.makedirs(params['path']['results_path'], exist_ok=True)

# Set up configuration object
model_prediction_config = ModelPredictionConfig(
    trained_weights_path=os.path.join(app.root_path, params['path']['trained_weights_path']),
    test_images_path=os.path.join(app.root_path, params['path']['test_images_path']),
    results_path=os.path.join(app.root_path, params['path']['results_path']),
    confidence_threshold=params['prediction_params']['confidence_threshold']
)

# Initialize YOLO inference object
inference = YOLOInference(model_prediction_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Save the uploaded image
        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(model_prediction_config.test_images_path, filename)
        image_file.save(image_path)

        # Update test_images_path to only include the uploaded image
        inference.config.test_images_path = os.path.dirname(image_path)

        # Run inference using the YOLOInference object
        inference.run_inference()

        # Construct the path to the result image
        result_filename = f"{filename.rsplit('.', 1)[0]}_result.jpg"
        result_path = os.path.join(model_prediction_config.results_path, result_filename)

        # Check if the result image was created
        if not os.path.isfile(result_path):
            raise FileNotFoundError(f"No result image found at {result_path}")

        # Return the URL to the detected image relative to the static folder
        detected_image_url = f"/static/results/{result_filename}"

        return jsonify({'detected_image_url': detected_image_url})
    except Exception as e:
        # Log the full traceback to the console or a file
        error_trace = traceback.format_exc()
        print(error_trace)

        # Return a detailed error message in the JSON response
        return jsonify({'error': str(e), 'trace': error_trace}), 500

if __name__ == '__main__':
    app.run(debug=True)
