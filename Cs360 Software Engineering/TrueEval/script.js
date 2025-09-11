document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', (event) => {
        // Prevent the form from submitting normally
        event.preventDefault();

        const patientId = document.getElementById('patient-id').value;
        const password = document.getElementById('password').value;

        // Simple validation check
        if (patientId.trim() === '' || password.trim() === '') {
            alert('Please fill out all fields.');
            return;
        }

        // For a simple project, you can simulate a successful login
        // In a real-world application, you would send this data to a server.
        alert('Login successful! Welcome, ' + patientId + '.');
        
        // After showing the alert, you can redirect the user to another page
        // window.location.href = "dashboard.html";
    });
});
