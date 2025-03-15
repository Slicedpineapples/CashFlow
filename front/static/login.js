document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Stripping empty spaces from the username
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    // Hash the password using SHA-256
    const hashedPassword = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
    const passwordArray = Array.from(new Uint8Array(hashedPassword));
    const hashedPasswordHex = passwordArray.map(b => b.toString(16).padStart(2, '0')).join('');

    const hostname = window.location.hostname;
    let apiUrl = hostname === 'localhost' || hostname === '127.0.0.1'
        ? 'http://127.0.0.1:5000/apiLogin'
        : `http://${hostname}:5000/apiLogin`;

    // console.log("Sending Request:", JSON.stringify({ username, password: hashedPasswordHex })); // Debugging

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password: hashedPasswordHex }) // ✅ Fix field name
        });

        // console.log("Fetch Response:", response);

        if (!response.ok) {
            const errorText = await response.text(); // Get raw error message
            console.error("Error Response Body:", errorText);
            document.getElementById('loginMessage').innerText = `Login failed: ${response.status} - ${errorText}`;
            return;
        }

        const result = await response.json();
        // console.log("Parsed API Response:", result);

        // Handle login success
        if (result.message[0] !== null) {
            sessionStorage.setItem('sessionId', result.message[0]);
            sessionStorage.setItem('userName', username);
            sessionStorage.setItem('email', result.message[1]);
            sessionStorage.setItem('country', result.message[2]);
            sessionStorage.setItem('currency', result.message[3]);
            sessionStorage.setItem('phone', result.message[4]);

            document.getElementById('loginMessage').innerText = result.message[5];
            await new Promise(resolve => setTimeout(resolve, 1000));
            window.location.href = 'home.html';
        } else {
            document.getElementById('loginMessage').innerText = result.message[1];
            await new Promise(resolve => setTimeout(resolve, 1000));
            window.location.href = 'login.html';
        }
    } catch (error) {
        // console.error("Fetch Error:", error);
        document.getElementById('loginMessage').innerText = "Network error. Please try again.";
    }
});
