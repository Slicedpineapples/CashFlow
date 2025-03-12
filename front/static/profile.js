document.addEventListener("DOMContentLoaded", () => {
    // Fetch user details from session storage
    function loadProfile() {
        const username = sessionStorage.getItem("userName");
        const email = sessionStorage.getItem("email");
        const phone = sessionStorage.getItem("phone");
        const currency = sessionStorage.getItem("currency");

        document.getElementById("userName").innerText = username || "User";
        document.getElementById("profileUsername").innerText = username || "Not Set";
        document.getElementById("profileEmail").innerText = email || "Not Set";
        document.getElementById("profilePhone").innerText = phone || "Not Set";
        document.getElementById("profilePassword").innerText = "********"; // Masked for security
    }

    // Function to make profile fields editable
    function makeEditable(fieldId, fieldType) {
        const valueElement = document.getElementById(fieldId);
        const oldValue = valueElement.innerText;
        
        const input = document.createElement("input");
        input.type = fieldType;
        input.value = (fieldId === "profilePassword") ? "" : oldValue; // Don't pre-fill password
        valueElement.replaceWith(input);
        
        const saveButton = document.createElement("button");
        saveButton.innerText = "Save";
        saveButton.onclick = () => saveChanges(fieldId, input.value);
        input.insertAdjacentElement("afterend", saveButton);
    }

    // Function to save the updated user information
    async function saveChanges(fieldId, newValue) {
        if (!newValue.trim()) {
            alert("Field cannot be empty!");
            return;
        }

        let fieldKey;
        if (fieldId === "profileEmail") fieldKey = "email";
        else if (fieldId === "profilePhone") fieldKey = "phone";
        else if (fieldId === "profilePassword") fieldKey = "password";

        const apiUrl = "http://127.0.0.1:5000/updateProfile";
        const sessionId = sessionStorage.getItem("sessionId");

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ sessionId, [fieldKey]: newValue })
            });

            const result = await response.json();

            if (result.success) {
                sessionStorage.setItem(fieldKey, newValue); // Update session storage
                alert("Profile updated successfully!");
                location.reload(); // Refresh to load new values
            } else {
                alert(result.message || "Failed to update profile.");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }

    // Event Listeners to make fields editable
    document.getElementById("profileEmail").addEventListener("click", () => makeEditable("profileEmail", "email"));
    document.getElementById("profilePhone").addEventListener("click", () => makeEditable("profilePhone", "tel"));
    document.getElementById("profilePassword").addEventListener("click", () => makeEditable("profilePassword", "password"));

    // Load profile data
    loadProfile();
});
