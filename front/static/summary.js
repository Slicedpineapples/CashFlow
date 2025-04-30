// Initial session check
if (!sessionStorage.getItem('sessionId')) {
    window.location.href = '/login';
}

// Set API base URL based on environment
let summaryHost = window.location.hostname;
let summaryApiUrl = (summaryHost === 'localhost' || summaryHost === '127.0.0.1')
    ? 'http://127.0.0.1:5000/'
    : `http://${summaryHost}:5000/`;

// Global function accessible from HTML onclick
window.summary = function summary() {
    const summaryExtension = document.getElementById('summary-extension');

    // Prevent duplicate form loading
    if (!document.getElementById('summaryForm')) {
        fetch('summary.html')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');

                for (let child of doc.body.children) {
                    document.adoptNode(child);
                    summaryExtension.appendChild(child);
                }

                // Autofill stored currency if available
                const storedCurrency = sessionStorage.getItem('currency');
                const currencyInput = document.getElementById('Currency');
                if (currencyInput && storedCurrency) {
                    currencyInput.value = storedCurrency;
                }

                const userId = sessionStorage.getItem('userId');
                const ust = sessionStorage.getItem('sessionId');
                const form = document.getElementById('summaryForm');

                form.addEventListener('submit', async (e) => {
                    e.preventDefault();

                    const month = document.getElementById('Month').value;
                    const currency = document.getElementById('Currency').value;

                    if (!month) {
                        const messageEl = document.getElementById('summaryMessage');
                        messageEl.innerText = 'Please select a month';
                        setTimeout(() => messageEl.innerText = '', 1500);
                        return;
                    }

                    const submitButton = form.querySelector('button[type="submit"]');
                    submitButton.disabled = true;
                    submitButton.style.backgroundColor = 'gray';

                    const start = new Date(month);
                    start.setDate(1);
                    const end = new Date(start);
                    end.setMonth(end.getMonth() + 1);
                    end.setDate(0);

                    const startDate = start.toISOString().split('T')[0];
                    const endDate = end.toISOString().split('T')[0];

                    const data = { ust, start: startDate, end: endDate, currency, userId };

                    try {
                        const response = await fetch(summaryApiUrl + 'apiGetSummary', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });

                        const result = await response.json();

                        // Handle invalid session (e.g., user logged in elsewhere)
                        if (!result || result.message === 'n' || result === false) {
                            alert("You have been logged out because your session is active elsewhere.");
                            sessionStorage.clear();
                            window.location.href = '/templates/login.html';
                            return;
                        }

                        document.getElementById('summaryMessage').innerText = result.message;
                    } catch (err) {
                        console.error("Summary fetch error:", err);
                        document.getElementById('summaryMessage').innerText = 'Failed to load summary.';
                    }

                    setTimeout(() => {
                        submitButton.disabled = false;
                        submitButton.style.backgroundColor = '';
                        document.getElementById('summaryMessage').innerText = '';
                    }, 3000);
                });
            });
    }

    // Toggle visibility
    summaryExtension.style.display = summaryExtension.style.display === "none" ? "block" : "none";
};
