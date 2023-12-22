document.getElementById('emailForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);
    fetch('/send_email', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const responseDiv = document.getElementById('formResponse');
        responseDiv.className = data.error ? 'alert alert-danger' : 'alert alert-success';
        responseDiv.innerHTML = data.message;
        responseDiv.style.display = 'block';

        setTimeout(() => {
            responseDiv.style.display = 'none';  // Hide the response after 3 seconds
        }, 3000);
    })
    .catch(error => {
        console.error('Error:', error);
        const responseDiv = document.getElementById('formResponse');
        responseDiv.innerHTML = "An error occurred.";
        responseDiv.className = 'alert alert-danger';
        responseDiv.style.display = 'block';
    });
});