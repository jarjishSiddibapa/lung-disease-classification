document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const fileInput = document.getElementById('file-input');
    const resultDiv = document.getElementById('result');
    const outputDiv = document.getElementById('output');
    const previewImg = document.getElementById('preview');
    const predictionResult = document.getElementById('prediction-result');

    if (fileInput.files.length === 0) {
        resultDiv.innerText = 'Please select an image.';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    resultDiv.innerHTML = '<div class="loader"></div> Predicting...';  // Show loading spinner
    resultDiv.style.color = '#007bff';  // Change text color to blue

    fetch('/predict', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Server response:", data);  // Debug statement
        if (data.error) {
            resultDiv.innerText = data.error;
            resultDiv.style.color = '#dc3545';  // Change text color to red for errors
        } else {
            resultDiv.innerText = 'Prediction Complete!';
            resultDiv.style.color = '#28a745';  // Change text color to green for success

            // Display the image and prediction result
            previewImg.src = data.image_url;
            predictionResult.innerText = `Prediction: ${data.result}`;
            outputDiv.style.display = 'flex';  // Show the output section
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);  // Debug statement
        resultDiv.innerText = 'An error occurred. Please try again.';
        resultDiv.style.color = '#dc3545';  // Change text color to red for errors
    });
});