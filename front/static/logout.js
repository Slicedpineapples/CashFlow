document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');

    logoutButton.addEventListener('click', async function () {
        const userId = sessionStorage.getItem('userId');
        const sessionId = sessionStorage.getItem('sessionId');

        if (!sessionId) {
            // console.error("No session ID found, user might not be logged in.");
            window.location.href = 'login.html';
            return;
        }

        const hostname = window.location.hostname;
        const apiUrl = hostname === 'localhost' || hostname === '127.0.0.1'
            ? 'http://127.0.0.1:5000/apiLogout'
            : `http://${hostname}:5000/apiLogout`;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId: userId, ust: sessionId })
            });

            const result = await response.json();
            // console.log("Logout Response:", result);

            if (result.message === "Logout successful!") {
                alert("Logout successful!");
            } else if (result.message === "Invalid session") {
                alert("You have already been logged out or logged in elsewhere.");
            } else {
                // console.warn("Unexpected response:", result.message);
            }

            // In both cases above, clear session and redirect
            sessionStorage.clear();
            Object.keys(sessionStorage).forEach(key => sessionStorage.removeItem(key));
            window.location.href = 'login.html';

        } catch (error) {
            // console.error("Logout error:", error);
            alert("Something went wrong during logout. Redirecting...");
            sessionStorage.clear();
            window.location.href = 'login.html';
        }
    });
});
