document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');

    logoutButton.addEventListener('click', async function () {
        const sessionId = sessionStorage.getItem('sessionId');

        if (!sessionId) {
            console.error("No session ID found, user might not be logged in.");
            // Redirect to login page
            window.location.href = 'login.html';
            return;
            
        }

        const hostname = window.location.hostname;
        let apiUrl = hostname === 'localhost' || hostname === '127.0.0.1'
            ? 'http://127.0.0.1:5000/apiLogout'
            : `http://${hostname}:5000/apiLogout`;

        try {

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ust: sessionId })
            });

            if (!response.ok) {
                const errorText = await response.text();
                // console.error("Error Response Body:", errorText);
                // alert(`Logout failed: ${response.status} - ${errorText}`);
                return;
            }

            const result = await response.json();
            // console.log("Logout Response:", result);

            if (result.message === "Logout successful!") {
                // Force clear session storage
                alert("Logout successful!");
                sessionStorage.clear();

                // Double-check by removing each item individually
                Object.keys(sessionStorage).forEach(key => sessionStorage.removeItem(key));

                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 500);
            } else {
                // console.error("Logout failed:", result.message);
                            }
        } catch (error) {
            // console.error("Logout error:", error);
        }
    });
});
