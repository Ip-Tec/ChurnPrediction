document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("errorMessage");

    // Mock validation logic
    if (email === "admin" && password === "admin") {
        alert("Login successful!");
        window.location.href = "/dashboard"; // Redirect to dashboard
    } else {
        errorMessage.textContent = "Invalid email or password!";
        errorMessage.style.display = "block";
    }
});

function register() {
    // alert("Redirecting to registration page...");
    window.location.href = "/register"; // Replace with actual registration URL
}
