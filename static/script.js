document.addEventListener('DOMContentLoaded', function() {
    // Preview the selected image before uploading
    document.getElementById('imageUpload').addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const displayImage = document.getElementById('displayImage');
                displayImage.src = e.target.result;
                displayImage.alt = "Uploaded Image";
                displayImage.style.display = 'block';
                document.querySelector('.upload-label').style.display = 'none'; // Hide the upload label once image is selected
                document.getElementById('uploadButton').style.display = 'block'; // Show the upload button
            };
            reader.readAsDataURL(this.files[0]); // Start reading the file as DataURL
        }
    });

    // Provide feedback or prevent form submission if no file is selected
    document.getElementById('uploadButton').addEventListener('click', function(event) {
        const messageDiv = document.getElementById('uploadMessage');
        if (!messageDiv) return; // Ensure messageDiv exists to avoid errors
        if (document.getElementById('imageUpload').files.length === 0) {
            messageDiv.textContent = 'Please select a file to upload first.';
            event.preventDefault(); // Prevent form submission
        } else {
            messageDiv.textContent = 'Uploading image...'; // Provide feedback
        }
    });

    // An example predict button functionality, assuming there's a specific process or action
    document.querySelector('.predict-btn').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default action (useful if this button is part of a form)

        // Example action: Copying the source of the uploaded image to a predicted image placeholder
        const displayImage = document.getElementById('displayImage');
        const predictImage = document.getElementById('predictedImage');
        
        if (predictImage) {
            predictImage.src = displayImage.src; // Copy the source
            predictImage.style.display = 'block'; // Ensure the predicted image is visible
        }
    });
});
