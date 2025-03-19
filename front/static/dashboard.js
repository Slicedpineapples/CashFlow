// Check if session ID is set
if (!sessionStorage.getItem('sessionId')) {
    // Redirect to login page or display an error message
    window.location.href = '/';
}

// MISC
const userName = sessionStorage.getItem('userName');
const capitalizedUserName = userName.charAt(0).toUpperCase() + userName.slice(1);
const date = new Date();
const day = date.getDate();
const month = date.toLocaleString('default', { month: 'long' });
const fullDate = `${day} ${month}`;
document.getElementById('userName').innerText = capitalizedUserName;
document.getElementById('fullDate').innerText = fullDate;

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

// Sorting hostname for API URL
const hostname = window.location.hostname;
let apiUrl;
if (hostname === 'localhost' || hostname === '127.0.0.1') {
    apiUrl = 'http://127.0.0.1:5000/';
} else {
    apiUrl = `http://${hostname}:5000/`;
}


function plusIncome() {
    let incomeExtension = document.getElementById('income-extension');
    let incomeForm = document.getElementById('Add-Income');

    if (incomeExtension.style.display === "none" || !incomeForm) {
        if (!incomeForm) {
            fetch('addincome.html')
                .then(response => response.text())
                .then(html => {
                    const domParser = new DOMParser();
                    const parsedDoc = domParser.parseFromString(html, 'text/html');
                    for (let child of parsedDoc.body.children) {
                        document.adoptNode(child);
                        incomeExtension.appendChild(child);
                    }
                    const userID = sessionStorage.getItem('userId');
                    // console.log(userID);
                    const ust = sessionStorage.getItem('sessionId');
                    // console.log(ust);
                    document.getElementById('incomeForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const sourceName = document.getElementById('sourceName').value.trim();
                        const amount = document.getElementById('amount').value.trim();
                        const incomeCategory = document.getElementById('incomeCategory').value.trim();

                        const response = await fetch(`${apiUrl}apiAddIncome`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                            body: JSON.stringify({ sourceName, amount, incomeCategory, userID, ust })
                        });

                        const result = await response.json();
                        document.getElementById('incomeMessage').innerText = result.message;
                        setTimeout(() => {
                            document.getElementById('incomeMessage').innerText = '';
                        }, 1000);
                        setTimeout(() => {
                            document.getElementById('incomeForm').reset();
                        }, 1000);
                    });
                });
        }
        incomeExtension.style.display = "block";
    } else {
        incomeExtension.style.display = "none";
    }
}

function plusExpense() {
    let expenseExtension = document.getElementById('expense-extension');
    let expenseForm = document.getElementById('Add-Expense');

    if (expenseExtension.style.display === "none" || !expenseForm) {
        if (!expenseForm) {
            fetch('addexpenses.html')
                .then(response => response.text())
                .then(html => {
                    const domParser = new DOMParser();
                    const parsedDoc = domParser.parseFromString(html, 'text/html');
                    for (let child of parsedDoc.body.children) {
                        document.adoptNode(child);
                        expenseExtension.appendChild(child);
                    }
                    const userID = sessionStorage.getItem('userId');
                    const ust = sessionStorage.getItem('sessionId');
                    document.getElementById('expenseForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const itemName = document.getElementById('itemName').value.trim();
                        const price = document.getElementById('price').value.trim();
                        const expenseCategory = document.getElementById('expenseCategory').value.trim();

                        const response = await fetch(`${apiUrl}apiAddExpense`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ itemName, price, expenseCategory, userID, ust })
                        });

                        const result = await response.json();
                        document.getElementById('expenseMessage').innerText = result.message;
                        setTimeout(() => {
                            document.getElementById('expenseMessage').innerText = '';
                        }, 1000);
                        setTimeout(() => {
                            document.getElementById('expenseForm').reset();
                        }, 1000);
                    });
                });
        }
        expenseExtension.style.display = "block";
    } else {
        expenseExtension.style.display = "none";
    }
}

function plusAsset() {
    let assetExtension = document.getElementById('asset-extension');
    let assetForm = document.getElementById('Add-Asset');

    if (assetExtension.style.display === "none" || !assetForm) {
        if (!assetForm) {
            fetch('addassets.html')
                .then(response => response.text())
                .then(html => {
                    const domParser = new DOMParser();
                    const parsedDoc = domParser.parseFromString(html, 'text/html');
                    for (let child of parsedDoc.body.children) {
                        document.adoptNode(child);
                        assetExtension.appendChild(child);
                    }
                    const userID = sessionStorage.getItem('userId');
                    const ust = sessionStorage.getItem('sessionId');
                    // console.log(userID);
                    document.getElementById('assetForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const assetCategory = document.getElementById('assetCategory').value.trim();
                        const value = document.getElementById('value').value.trim();
                        const location = document.getElementById('location').value.trim();
                        const numberOfItems = document.getElementById('numberOfItems').value.trim();
                        const name = document.getElementById('name').value.trim();

                        const response = await fetch(`${apiUrl}apiAddAsset`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ name, value, assetCategory, userID, location, numberOfItems, ust })
                        });
                        
                        const result = await response.json();
                        document.getElementById('assetMessage').innerText = result.message;
                        setTimeout(() => {
                            document.getElementById('assetMessage').innerText = '';
                        }, 1000);
                        setTimeout(() => {
                            document.getElementById('assetForm').reset();
                        }, 1000);
                        
                    });
                });
        }
        assetExtension.style.display = "block";
    } else {
        assetExtension.style.display = "none";
    }
}

function plusLiability() {
    let liabilityExtension = document.getElementById('liability-extension');
    let liabilityForm = document.getElementById('Add-Liability');

    if (liabilityExtension.style.display === "none" || !liabilityForm) {
        if (!liabilityForm) {
            fetch('addliabilities.html')
                .then(response => response.text())
                .then(html => {
                    const domParser = new DOMParser();
                    const parsedDoc = domParser.parseFromString(html, 'text/html');
                    for (let child of parsedDoc.body.children) {
                        document.adoptNode(child);
                        liabilityExtension.appendChild(child);
                    }
                    const userID = sessionStorage.getItem('userId');
                    const ust = sessionStorage.getItem('sessionId');
                    // console.log(userID);
                    document.getElementById('liabilityForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const liabilityCategory = document.getElementById('liabilityCategory').value.trim();
                        const grossAmount = document.getElementById('grossAmount').value.trim();
                        const remainingAmount = document.getElementById('remainingAmount').value.trim();
                        const response = await fetch(`${apiUrl}apiAddLiability`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ liabilityCategory, grossAmount, remainingAmount, userID, ust })
                        });
                        const result = await response.json();
                        document.getElementById('liabilityMessage').innerText = result.message;
                        setTimeout(() => {
                            document.getElementById('liabilityMessage').innerText = '';
                        }, 1000);
                        setTimeout(() => {
                            document.getElementById('liabilityForm').reset();
                        }, 1000);
                    });
                });
        }
        liabilityExtension.style.display = "block";
    } else {
        liabilityExtension.style.display = "none";
    }
}
