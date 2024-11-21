document.getElementById('emailForm').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);
    fetch('/send_email', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            const responseDiv = document.getElementById('formResponse');
            if (response.ok) {
                responseDiv.className = 'alert alert-success';
                return response.json();
            }
            else {
                responseDiv.className = 'alert alert-danger';
                return response.json();
            }

        })
        .then(data => {
            responseDiv.innerHTML = data.message;
            responseDiv.style.display = 'block';

            setTimeout(() => {
                responseDiv.style.display = 'none';  // Hide the response after 3 seconds
            }, 3000);
            this.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            const responseDiv = document.getElementById('formResponse');
            responseDiv.innerHTML = "Failed to send email.";
            responseDiv.className = 'alert alert-danger';
            responseDiv.style.display = 'block';

            setTimeout(() => {
                responseDiv.style.display = 'none';  // Hide the response after 3 seconds
            }, 3000);
            this.reset();
        });
});