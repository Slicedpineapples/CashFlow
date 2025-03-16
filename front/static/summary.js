if (!sessionStorage.getItem('sessionId')) {
    window.location.href = '/login';
// Sorting hostname for API URL
const hostname = window.location.hostname;
let apiUrl;
if (hostname === 'localhost' || hostname === '127.0.0.1') {
    apiUrl = 'http://127.0.0.1:5000/';
} else {
    apiUrl = `http://${hostname}:5000/`;
}
}

function summary() {
    let summaryExtension = document.getElementById('summary-extension');

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

                // Auto-fill the currency input field
                const storedCurrency = sessionStorage.getItem('currency');
                let currencyInput = document.getElementById('Currency');

                if (currencyInput && storedCurrency) {
                    currencyInput.value = storedCurrency;
                }

                const ust = sessionStorage.getItem('sessionId');

                // Getting the form data for construction of dates
                const form = document.getElementById('summaryForm');
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const month = document.getElementById('Month').value;
                    const currency = document.getElementById('Currency').value;

                    if (!month) {
                        document.getElementById('summaryMessage').innerText = 'Please select a month';
                        setTimeout(() => {
                            document.getElementById('summaryMessage').innerText = '';
                        }, 1500);
                        return;
                    }

                    // Disable the submit button and change its color to gray
                    const submitButton = form.querySelector('button[type="submit"]');
                    submitButton.disabled = true;
                    submitButton.style.backgroundColor = 'gray';

                    // Date construction
                    const start = new Date(month);
                    start.setDate(1);
                    const end = new Date(start);
                    end.setMonth(end.getMonth() + 1);
                    end.setDate(0);

                    // Formatting the dates
                    const startDate = start.toISOString().split('T')[0];
                    const endDate = end.toISOString().split('T')[0];

                    // Create JSON data object
                    const data = { ust: ust, start: startDate, end: endDate, currency: currency };

                    // Send data to API
                    const response = await fetch(apiUrl + 'apiGetSummary', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    const result = await response.json();
                    document.getElementById('summaryMessage').innerText = result.message;
                    setTimeout(() => {
                        document.getElementById('summaryMessage').innerText = '';
                    }, 3000);

                    setTimeout(() => {
                        submitButton.style.backgroundColor = '';
                        submitButton.disabled = false;

                    }, 3000);
                    // Re-enable the submit button and reset its color

                    // setTimeout(() => {
                    //     document.getElementById('summaryForm').reset();
                    // }, 1000);
                });
            });
    }

    summaryExtension.style.display = summaryExtension.style.display === "none" ? "block" : "none";
}
