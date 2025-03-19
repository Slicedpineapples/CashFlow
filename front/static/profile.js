if (!sessionStorage.getItem('sessionId')) {
    window.location.href = '/';
}
document.addEventListener("DOMContentLoaded", () => {
    const stylesheet = document.getElementById("theme-stylesheet");

    // Function to apply the theme
    function applyTheme(theme) {
        stylesheet.setAttribute("href", `../style/${theme}`);
    }

    // Detect system theme preference
    function detectSystemTheme() {
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? "style1.css" : "style.css";
    }

    // Initialize the theme based on stored preference or system preference
    function initializeTheme() {
        const storedTheme = localStorage.getItem("themeChoice");
        const systemTheme = detectSystemTheme();
        applyTheme(storedTheme || systemTheme);
    }

    // Toggle between themes manually
    window.toggleButton = function () {
        const currentTheme = stylesheet.getAttribute("href").includes("style1.css") ? "style.css" : "style1.css";
        applyTheme(currentTheme);
        localStorage.setItem("themeChoice", currentTheme);
    };

    // Listen for system theme changes (Works better on Firefox with explicit re-check)
    const darkModeQuery = window.matchMedia("(prefers-color-scheme: dark)");

    function handleSystemThemeChange(event) {
        if (!localStorage.getItem("themeChoice")) {
            applyTheme(event.matches ? "style1.css" : "style.css");
        }
    }

    darkModeQuery.addEventListener("change", handleSystemThemeChange);

    // Force initial check on Firefox
    handleSystemThemeChange(darkModeQuery);

    // Apply theme on page load
    initializeTheme();
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
        input.style.border = "1px solid #ccc";
        input.style.padding = "5px";
        input.style.marginRight = "5px";
        input.style.borderRadius = "4px";
        input.style.backgroundColor = "transparent";
        input.style.color = "grey";
        input.style.fontSize = "1.1rem";
        input.style.width = `${valueElement.offsetWidth + 80}px`; // Maintain the same width

        valueElement.replaceWith(input);

        const saveButton = document.createElement("button");
        saveButton.innerText = "Save";
        saveButton.style.padding = "5px 10px";
        saveButton.style.border = "none";
        saveButton.style.backgroundColor = "#4CAF50";
        saveButton.style.color = "white";
        saveButton.style.borderRadius = "4px";
        saveButton.style.cursor = "pointer";
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
        const userId = sessionStorage.getItem("userId");
        const ust = sessionStorage.getItem("sessionId");

        try {
            const response = await fetch(profileapiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ userId, newCountry: newValue, ust })
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
