const BASE_URL = 'http://127.0.0.1:5000'; // غيّره إلى رابط السيرفر عند النشر

// ======= create_account.js =======
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm-password");
    const successMessage = document.getElementById("success-message");

    if (form && password && confirmPassword && successMessage) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            if (password.value !== confirmPassword.value) {
                alert("The password and confirmation do not match.!");
                confirmPassword.focus();
                return;
            }

            const email = document.getElementById("email").value.trim();
            const role = document.getElementById("role").value;

            if (!email || !password.value || !role) {
                alert("يرجى تعبئة جميع الحقول.");
                return;
            }

            successMessage.style.display = "block";

            setTimeout(() => {
                form.reset();
                successMessage.style.display = "none";
            }, 3000);
        });
    }
});

// ======= forgot_password.js =======
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    const emailInput = document.getElementById('email');
    const successMessage = document.getElementById('success-message');

    if (form && emailInput && successMessage) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const email = emailInput.value.trim();
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$/;

            if (!emailRegex.test(email)) {
                alert("Please enter a valid email address.");
                return;
            }

            successMessage.style.display = 'block';
            successMessage.textContent = "A password reset link will be sent to your email.";

            fetch(`${BASE_URL}/forgot-password`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: email })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                })
                .catch(error => {
                    alert("Error: " + error);
                    console.error("Error:", error);
                });
        });
    }
});

// ======= Login.js =======
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            fetch(`${BASE_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username: username, password: password })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = `${BASE_URL}/dashboard`;
                    } else {
                        alert("Login failed: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("Login error");
                });
        });
    }
});

// ======= register.js =======
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("input_with_icon");
    const authButton = document.getElementById("authBtn");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase();
            console.log("Searching for: " + query);
        });
    }

    if (authButton) {
        authButton.addEventListener("click", function () {
            alert("You have successfully logged out");
            window.location.href = "Login.html";
        });
    }
});
