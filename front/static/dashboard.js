// Unified session check at the top
const sessionId = sessionStorage.getItem('sessionId');
const userId = sessionStorage.getItem('userId');
if (!sessionId) {
    window.location.href = '/';
}

// Global API base URL
const hostname = window.location.hostname;
const apiUrl = (hostname === 'localhost' || hostname === '127.0.0.1')
    ? 'http://127.0.0.1:5000/'
    : `http://${hostname}:5000/`;

// Display User Info
const userName = sessionStorage.getItem('userName') || '';
document.getElementById('userName').innerText = userName.charAt(0).toUpperCase() + userName.slice(1);

const date = new Date();
document.getElementById('fullDate').innerText = `${date.getDate()} ${date.toLocaleString('default', { month: 'long' })}`;

// Theme handling
document.addEventListener("DOMContentLoaded", () => {
    const stylesheet = document.getElementById("theme-stylesheet");

    function applyTheme(theme) {
        stylesheet.setAttribute("href", `../style/${theme}`);
    }

    function detectSystemTheme() {
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? "style1.css" : "style.css";
    }

    function initializeTheme() {
        const storedTheme = localStorage.getItem("themeChoice");
        applyTheme(storedTheme || detectSystemTheme());
    }

    window.toggleButton = function () {
        const currentTheme = stylesheet.getAttribute("href").includes("style1.css") ? "style.css" : "style1.css";
        applyTheme(currentTheme);
        localStorage.setItem("themeChoice", currentTheme);
    };

    const darkModeQuery = window.matchMedia("(prefers-color-scheme: dark)");
    darkModeQuery.addEventListener("change", e => {
        if (!localStorage.getItem("themeChoice")) {
            applyTheme(e.matches ? "style1.css" : "style.css");
        }
    });

    initializeTheme();
});

// General POST wrapper with session invalidation
async function postWithSessionCheck(url, payload) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!result || result.message === 'Something went wrong at income()' || result.message === "Something went wrong at expenses()" || result.message === "Something went wrong at assets()" || result.message === "Something went wrong at liabilities()" || result === false || result.message === 'Invalid token' || result.message === 'Invalid session') {
            
            alert("You have been logged out because your session is active elsewhere.");
            sessionStorage.clear();
            window.location.href = '/templates/login.html';
            return null;
        }

        return result;
    } catch (err) {
        console.error("API error:", err);
        return { message: "Something went wrong. Try again." };
    }
}

// Generic form toggle and fetch utility
async function loadForm(endpoint, containerId, formId, callback) {
    const container = document.getElementById(containerId);
    const existingForm = document.getElementById(formId);

    if (container.style.display === "none" || !existingForm) {
        if (!existingForm) {
            const html = await (await fetch(endpoint)).text();
            const doc = new DOMParser().parseFromString(html, 'text/html');
            for (let child of doc.body.children) {
                document.adoptNode(child);
                container.appendChild(child);
            }
            callback();
        }
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
}

// Feature: Income
function plusIncome() {
    loadForm('addincome.html', 'income-extension', 'Add-Income', () => {
        document.getElementById('incomeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                sourceName: document.getElementById('sourceName').value.trim(),
                amount: document.getElementById('amount').value.trim(),
                incomeCategory: document.getElementById('incomeCategory').value.trim(),
                userID: userId,
                ust: sessionId
            };
            const result = await postWithSessionCheck(`${apiUrl}apiAddIncome`, data);
            if (result) {
                document.getElementById('incomeMessage').innerText = result.message;
                setTimeout(() => {
                    document.getElementById('incomeMessage').innerText = '';
                    document.getElementById('incomeForm').reset();
                }, 1000);
            }
        });
    });
}

// Feature: Expense
function plusExpense() {
    loadForm('addexpenses.html', 'expense-extension', 'Add-Expense', () => {
        document.getElementById('expenseForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                itemName: document.getElementById('itemName').value.trim(),
                price: document.getElementById('price').value.trim(),
                expenseCategory: document.getElementById('expenseCategory').value.trim(),
                userID: userId,
                ust: sessionId
            };
            const result = await postWithSessionCheck(`${apiUrl}apiAddExpense`, data);
            if (result) {
                document.getElementById('expenseMessage').innerText = result.message;
                setTimeout(() => {
                    document.getElementById('expenseMessage').innerText = '';
                    document.getElementById('expenseForm').reset();
                }, 1000);
            }
        });
    });
}

// Feature: Asset
function plusAsset() {
    loadForm('addassets.html', 'asset-extension', 'Add-Asset', () => {
        document.getElementById('assetForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                assetCategory: document.getElementById('assetCategory').value.trim(),
                value: document.getElementById('value').value.trim(),
                location: document.getElementById('location').value.trim(),
                numberOfItems: document.getElementById('numberOfItems').value.trim(),
                name: document.getElementById('name').value.trim(),
                userID: userId,
                ust: sessionId
            };
            const result = await postWithSessionCheck(`${apiUrl}apiAddAsset`, data);
            if (result) {
                document.getElementById('assetMessage').innerText = result.message;
                setTimeout(() => {
                    document.getElementById('assetMessage').innerText = '';
                    document.getElementById('assetForm').reset();
                }, 1000);
            }
        });
    });
}

// Feature: Liability
function plusLiability() {
    loadForm('addliabilities.html', 'liability-extension', 'Add-Liability', () => {
        document.getElementById('liabilityForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                liabilityCategory: document.getElementById('liabilityCategory').value.trim(),
                grossAmount: document.getElementById('grossAmount').value.trim(),
                remainingAmount: document.getElementById('remainingAmount').value.trim(),
                userID: userId,
                ust: sessionId
            };
            const result = await postWithSessionCheck(`${apiUrl}apiAddLiability`, data);
            if (result) {
                document.getElementById('liabilityMessage').innerText = result.message;
                setTimeout(() => {
                    document.getElementById('liabilityMessage').innerText = '';
                    document.getElementById('liabilityForm').reset();
                }, 1000);
            }
        });
    });
}
