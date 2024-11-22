
function showResponse(message, alert_type, timeout = 3000) {
    const responseDiv = document.getElementById('formResponse');

    const className = `alert alert-${alert_type}`;

    responseDiv.innerHTML = message;
    responseDiv.className = className;
    responseDiv.style.display = 'block';

    setTimeout(() => {
        responseDiv.style.display = 'none';
    }, timeout);
}


document.getElementById('emailForm').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);
    const recaptchaResponse = grecaptcha.getResponse();
    if (recaptchaResponse.length === 0) {
        showResponse('Please verify that you are not a robot.', 'danger');
        return;
    }
    fetch('/send_email', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            response_type = 'success';
        }
        else {
            response_type = 'danger';
        }
        return response.json();

    }).then(data => {
        showResponse(data.message, response_type);
        if (response_type === 'success') {
            this.reset();
        }
    }).catch(error => {
        console.error('Error:', error);
        showResponse('An error occurred. Please try again later.', 'danger');
    });
});