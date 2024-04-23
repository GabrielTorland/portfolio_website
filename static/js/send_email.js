document.getElementById('emailForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);
    fetch('/send_email', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok){
            return response.json();
        }
        else {
            const responseDiv = document.getElementById('formResponse');
            responseDiv.className = 'alert alert-danger';
            console.log(response.data.message)
            responseDiv.innerHTML = "Failed to send email.";
            responseDiv.style.display = 'block';
            setTimeout(() => {
                responseDiv.style.display = 'none';
            }, 3000);
            this.reset();
        }
        
    })
    .then(data => {
        const responseDiv = document.getElementById('formResponse');
        responseDiv.className = 'alert alert-success';
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