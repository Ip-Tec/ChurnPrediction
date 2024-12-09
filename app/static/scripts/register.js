document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const errorMessage = document.getElementById("errorMessage");

    // Validation logic
    if (!username || !email || !password || !confirmPassword) {
        errorMessage.textContent = "All fields are required!";
        errorMessage.style.display = "block";
        return;
    }

    if (password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match!";
        errorMessage.style.display = "block";
        return;
    }

    // Mock successful registration
    alert("Registration successful! Redirecting to login...");
    window.location.href = "/login"; // Redirect to login page
});

function goToLogin() {
    window.location.href = "/login"; // Redirect to login page
}
