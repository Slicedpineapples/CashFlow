if (!sessionStorage.getItem('sessionId')) {
    window.location.href = '/';
}
function toggleButton() {
    var stylesheet = document.getElementById('theme-stylesheet');
    const currentTheme = stylesheet.getAttribute('href');
    const newTheme = currentTheme === '../style/style1.css' ? 'style.css' : 'style1.css';

    // Update the theme
    stylesheet.setAttribute('href', `../style/${newTheme}`);
    
    // Set expiration date for 365 days from today
    var expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 365);
    localStorage.setItem('themeChoice', newTheme);
    localStorage.setItem('themeExpiration', expirationDate.toISOString());
}

// Load stored theme choice if available and not expired
document.addEventListener("DOMContentLoaded", () => {
    const storedThemeChoice = localStorage.getItem('themeChoice');
    const storedThemeExpiration = localStorage.getItem('themeExpiration');

    if (storedThemeChoice && storedThemeExpiration) {
        const expirationDate = new Date(storedThemeExpiration);
        if (expirationDate > new Date()) {
            document.getElementById('theme-stylesheet').setAttribute('href', `../style/${storedThemeChoice}`);
        } else {
            // Remove expired theme choice
            localStorage.removeItem('themeChoice');
            localStorage.removeItem('themeExpiration');
        }
    }
});

// Profile Data Loading
document.addEventListener("DOMContentLoaded", () => {
    function loadProfile() {
        const username = sessionStorage.getItem("userName");
        const email = sessionStorage.getItem("email");
        const phone = sessionStorage.getItem("phone");
        const country = sessionStorage.getItem("country");
        const currency = sessionStorage.getItem("currency");

        document.getElementById("userName").innerText = username || "User";
        document.getElementById("profileUsername").innerText = username || "Not Set";
        document.getElementById("profileEmail").innerText = email || "Not Set";
        document.getElementById("profilePhone").innerText = phone || "Not Set";
        document.getElementById("profileCountry").innerText = country || "Not Set";
        document.getElementById("profileCurrency").innerText = currency || "Not Set";
        document.getElementById("profileBaseCurrency").innerText = "HUF" || "Not Set";
        document.getElementById("profilePassword").innerText = "********";
    }

    function makeEditable(fieldId, fieldType) {
        const valueElement = document.getElementById(fieldId);
        const oldValue = valueElement.innerText;

        const input = document.createElement("input");
        input.type = fieldType;
        input.value = oldValue;
        input.id = `${fieldId}-input`;
        valueElement.replaceWith(input);

        const saveButton = document.createElement("button");
        saveButton.innerText = "Save";
        saveButton.onclick = () => saveChanges(fieldId, input.value);
        input.insertAdjacentElement("afterend", saveButton);
    }
    

    async function saveChanges(fieldId, newValue) {
        if (!newValue.trim()) {
            displayMessage("Field cannot be empty!", false);
            return;
        }

        if (fieldId !== "profileCountry") {
            displayMessage("Only the country field can be updated.", false);
            return;
            
        }
        // Sorting hostname for API URL
        const hostname = window.location.hostname;
        let apiUrl;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            apiUrl = 'http://127.0.0.1:5000/';
        } else {
            apiUrl = `http://${hostname}:5000/`;
        }


        const profileapiUrl = `${apiUrl}apiUpdateCountry`;
        const userId = sessionStorage.getItem("sessionId");

        try {
            const response = await fetch(profileapiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ userId, newCountry: newValue })
            });

            const result = await response.json();

            if (!result.message || result.message.length < 3) {
                throw new Error("Unexpected API response format");
            }

            const newCurrency = result.message[0];
            const updatedCountry = result.message[1];
            const successMessage = result.message[2];

            sessionStorage.setItem("country", updatedCountry);
            sessionStorage.setItem("currency", newCurrency);

            const countryElement = document.getElementById("profileCountry");
            const currencyElement = document.getElementById("profileCurrency");

            if (countryElement) {
                countryElement.innerText = updatedCountry;
            }

            if (currencyElement) {
                currencyElement.innerText = newCurrency;
            }

            displayMessage(successMessage, true);

            // Refresh the page to reflect changes
            setTimeout(() => {
                location.reload();
            }, 1000); 

        } catch (error) {
            displayMessage("An error occurred while updating the profile.", false);
        }
    }

    function displayMessage(message, isSuccess) {
        const messageElement = document.getElementById("profileMessage");
        messageElement.innerText = message;
        messageElement.style.color = isSuccess ? "green" : "red";
    }

    document.getElementById("profileCountry").addEventListener("click", () => makeEditable("profileCountry", "text"));
    loadProfile();
});
