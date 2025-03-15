document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Stripping empty spaces during signup
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value;

    // Hash the password using SHA-256
    const hashedPassword = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
    const passwordArray = Array.from(new Uint8Array(hashedPassword));
    const hashedPasswordHex = passwordArray.map(b => b.toString(16).padStart(2, '0')).join('');

    // Determine the base URL based on the hostname
    const hostname = window.location.hostname;
    let apiUrl = hostname === 'localhost' || hostname === '127.0.0.1'
        ? 'http://127.0.0.1:5000/apiSignup'
        : `http://${hostname}:5000/apiSignup`;

    // console.log("Sending Request:", JSON.stringify({ username, email, phone, password: hashedPasswordHex })); // Debugging
// 
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, phone, password: hashedPasswordHex }) // ✅ Fix: Hash password before sending
        });

        // console.log("Fetch Response:", response);

        if (!response.ok) {
            const errorText = await response.text(); // Get raw error message
            console.error("Error Response Body:", errorText);
            document.getElementById('signupMessage').innerText = `Signup failed: ${response.status} - ${errorText}`;
            return;
        }

        const result = await response.json();
        // console.log("Parsed API Response:", result);

        // Handle signup success
        if (result.message === 'User created successfully!') {
            document.getElementById('signupMessage').innerText = result.message;
            await new Promise(resolve => setTimeout(resolve, 1000));
            window.location.href = 'login.html';
        } else {
            document.getElementById('signupMessage').innerText = result.message;
        }
    } catch (error) {
        // console.error("Fetch Error:", error);
        document.getElementById('signupMessage').innerText = "Network error. Please try again.";
    }
});
