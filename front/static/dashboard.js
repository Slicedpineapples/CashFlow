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
const year = date.getFullYear();
const fullDate = `${day} ${month} ${year}`;
document.getElementById('userName').innerText = capitalizedUserName;
document.getElementById('fullDate').innerText = fullDate;

function toggleButton() {
    var stylesheet = document.getElementById('theme-stylesheet');
    if (stylesheet.getAttribute('href') === '../style/style1.css') {
        stylesheet.setAttribute('href', '../style/style.css');
        // Store the choice in localStorage with an expiration date of 365 days
        var expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 365);
        localStorage.setItem('themeChoice', 'style.css');
        localStorage.setItem('themeExpiration', expirationDate.toISOString());
    } else {
        stylesheet.setAttribute('href', '../style/style1.css');
        // Remove the stored choice from localStorage
        localStorage.removeItem('themeChoice');
        localStorage.removeItem('themeExpiration');
    }
}

// Check if theme choice is stored in localStorage
var storedThemeChoice = localStorage.getItem('themeChoice');
var storedThemeExpiration = localStorage.getItem('themeExpiration');
if (storedThemeChoice && storedThemeExpiration) {
    var expirationDate = new Date(storedThemeExpiration);
    if (expirationDate > new Date()) {
        var stylesheet = document.getElementById('theme-stylesheet');
        stylesheet.setAttribute('href', '../style/' + storedThemeChoice);
    } else {
        // Remove expired theme choice from localStorage
        localStorage.removeItem('themeChoice');
        localStorage.removeItem('themeExpiration');
    }
}
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
                    const userID = sessionStorage.getItem('sessionId');
                    document.getElementById('incomeForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const sourceName = document.getElementById('sourceName').value.trim();
                        const amount = document.getElementById('amount').value.trim();
                        const incomeCategory = document.getElementById('incomeCategory').value.trim();

                        const response = await fetch(`${apiUrl}apiAddIncome`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                            body: JSON.stringify({ sourceName, amount, incomeCategory, userID })
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
                    const userID = sessionStorage.getItem('sessionId');
                    document.getElementById('expenseForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const itemName = document.getElementById('itemName').value.trim();
                        const price = document.getElementById('price').value.trim();
                        const expenseCategory = document.getElementById('expenseCategory').value.trim();

                        const response = await fetch(`${apiUrl}apiAddExpense`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ itemName, price, expenseCategory, userID })
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
                    const userID = sessionStorage.getItem('sessionId');
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
                            body: JSON.stringify({ name, value, assetCategory, userID, location, numberOfItems})
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
                    const userID = sessionStorage.getItem('sessionId');
                    // console.log(userID);
                    document.getElementById('liabilityForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const liabilityCategory = document.getElementById('liabilityCategory').value.trim();
                        const grossAmount = document.getElementById('grossAmount').value.trim();
                        const remainingAmount = document.getElementById('remainingAmount').value.trim();
                        const response = await fetch(`${apiUrl}apiAddLiability`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ liabilityCategory, grossAmount, remainingAmount, userID})
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
