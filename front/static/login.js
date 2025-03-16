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

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password: hashedPasswordHex })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Error Response Body:", errorText);
            document.getElementById('loginMessage').innerText = `Login failed: ${response.status} - ${errorText}`;
            return;
        }

        const result = await response.json();

        // If login is successful, fetch user data
        if (result.message[0] !== null) {
            const sessionId = result.message[1];

            sessionStorage.setItem('userId', result.message[0]);
            sessionStorage.setItem('sessionId', sessionId);
            // console.log("Session ID:", sessionId);

            // Fetch user data from apiUserFetch
            let userFetchUrl = hostname === 'localhost' || hostname === '127.0.0.1'
                ? 'http://127.0.0.1:5000/apiUserFetch'
                : `http://${hostname}:5000/apiUserFetch`;


            const userResponse = await fetch(userFetchUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    // 'Authorization': `Bearer ${sessionId}` // Pass session ID for authentication
                },
                body: JSON.stringify({ ust: sessionId })
            });

            if (userResponse.ok) {
                const userData = await userResponse.json();
                // console.log("User Data:", userData);
                userDetails = userData.message;
                // Store user details in sessionStorage
                sessionStorage.setItem('country', userDetails.country);
                sessionStorage.setItem('currency', userDetails.currency);
                sessionStorage.setItem('email', userDetails.email);
                sessionStorage.setItem('phone', userDetails.phone);
                sessionStorage.setItem('userName', userDetails.username);

                document.getElementById('loginMessage').innerText = "Login successful!";
                await new Promise(resolve => setTimeout(resolve, 1000));

                // Redirect to home page
                window.location.href = 'home.html';
            } else {
                document.getElementById('loginMessage').innerText = "Failed to fetch user data.";
            }
        } else {
            document.getElementById('loginMessage').innerText = result.message[1];
            await new Promise(resolve => setTimeout(resolve, 1000));
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        document.getElementById('loginMessage').innerText = "Network error. Please try again.";
    }
});
