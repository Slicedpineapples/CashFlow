if (!sessionStorage.getItem('sessionId')) {
    window.location.href = '/login';
}

function generateReport() {
    let reportExtension = document.getElementById('report-extension');

    if (!document.getElementById('reportForm')) {
        fetch('reports.html')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                for (let child of doc.body.children) {
                    document.adoptNode(child);
                    reportExtension.appendChild(child);
                }
                attachFormSubmitHandler();
            });
    }
    reportExtension.style.display = reportExtension.style.display === "none" ? "block" : "none";
}

function attachFormSubmitHandler() {
    document.getElementById('reportForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const reportType = document.getElementById('reportType').value;
        const start = document.getElementById('start').value;
        const end = document.getElementById('end').value;
        const userID = sessionStorage.getItem('sessionId');

        const hostname = window.location.hostname;
        let apiUrl;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            apiUrl = `http://127.0.0.1:5000/apiGet${reportType}Report`;
        } else {
            apiUrl = `http://${hostname}:5000/apiGet${reportType}Report`;
        }

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start, end, userID })
        });
        const result = await response.json();
        displayReport(result, reportType);
    });
}

function displayReport(result, reportType) {
    const reportExtension = document.getElementById('report-extension');
    reportExtension.innerHTML = '';

    // Add close button to clear the generated report
    // Add close button to clear the generated report
    const closeButton = document.createElement('button');
    const closeIcon = document.createElement('img');
    closeIcon.src = '../assets/close-dark.svg';
    closeIcon.alt = 'Close';
    closeIcon.style.cssText = 'vertical-align: middle; width: 25px; height: 25px;';
    closeButton.appendChild(closeIcon);
    closeButton.style.cssText = 'color: red; background-color: white; border-radius: 5px; border: none; font-size: 16px; cursor: pointer; margin-left: 10px; padding: 5px 10px; float: right;';
    closeButton.addEventListener('click', () => {
        reportExtension.innerHTML = '';
        reportExtension.style.display = 'none';
    });
    //print button
    const printButton = document.createElement('button');
    const printIcon = document.createElement('img');
    printIcon.src = '../assets/print-dark.svg';
    printIcon.alt = 'Print';
    printIcon.style.cssText = 'vertical-align: middle; width: 25px; height: 25px;';
    printButton.appendChild(printIcon);
    printButton.style.cssText = 'color: blue; background-color: white; border-radius: 5px; border: none; font-size: 16px; cursor: pointer; margin-left: 10px; padding: 5px 10px; float: right;';
    printButton.addEventListener('click', () => {
        printReport();
    });
    

    const tableContainer = document.createElement('div');
    tableContainer.style.marginTop = '50px';
    tableContainer.id = 'reportTableContainer';
    tableContainer.style.display = 'flex';

    const table = document.createElement('table');
    table.id = 'reportTable';

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = getHeaders(reportType);

    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    const reportData = result.message[1];

    if (reportData.length === 0) {
        const emptyRow = document.createElement('tr');
        const emptyCell = document.createElement('td');
        emptyCell.colSpan = headers.length;
        emptyCell.textContent = 'No data available';
        emptyRow.appendChild(emptyCell);
        tbody.appendChild(emptyRow);
    } else {
        reportData.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = getRowHtml(item, reportType);
            tbody.appendChild(row);
        });
    }

    table.appendChild(tbody);
    tableContainer.appendChild(table);
    reportExtension.appendChild(closeButton);
    reportExtension.appendChild(printButton);
    reportExtension.appendChild(tableContainer);
    const totalIncomeDiv = document.createElement('div');
    totalIncomeDiv.className = 'total-income';
    totalIncomeDiv.textContent = `Total ${reportType}: ${result.message[2].Total}`;
    totalIncomeDiv.style.fontWeight = 'bold';
    totalIncomeDiv.style.marginTop = '10px';
    reportExtension.appendChild(totalIncomeDiv);

    reportExtension.style.display = 'block';
}

function printReport() {
    const reportExtension = document.getElementById('report-extension');
    const printWindow = window.open('', '_blank');
    printWindow.document.write('<html><head><title>Report</title>');
    printWindow.document.write('<style>table { border-collapse: collapse; width: 100%; } table, th, td { border: 1px solid black; padding: 8px; text-align: left; } .total-income { font-weight: bold; margin-top: 10px; }</style>');
    printWindow.document.write('</head><body>');
    printWindow.document.write(reportExtension.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

function getHeaders(reportType) {
    switch (reportType) {
        case 'Income':
            return ['Income Name', 'Category', 'Amount', 'Date'];
        case 'Expenses':
            return ['Expense Name', 'Category', 'Price', 'Date'];
        case 'Assets':
            return ['Asset Name', 'Location', 'Quantity', 'Value', 'Date'];
        case 'Liabilities':
            return ['Liability Name', 'Gross Amount', 'Remaining Amount', 'Date'];
        default:
            return [];
    }
}

function getRowHtml(item, reportType) {
    switch (reportType) {
        case 'Income':
            return `
                <td>${item.incomeName}</td>
                <td>${item.sourceName}</td>
                <td>${item.amount}</td>
                <td>${new Date(item.date).toLocaleDateString()}</td>
            `;
        case 'Expenses':
            return `
                <td>${item.expenseName}</td>
                <td>${item.itemName}</td>
                <td>${item.price}</td>
                <td>${new Date(item.date).toLocaleDateString()}</td>
            `;
        case 'Assets':
            return `
                <td>${item.assetName}</td>
                <td>${item.location}</td>
                <td>${item.numberOfItems}</td>
                <td>${item.value}</td>
                <td>${new Date(item.date).toLocaleDateString()}</td>
            `;
        case 'Liabilities':
            return `
                <td>${item.liabilityName}</td>
                <td>${item.grossAmount}</td>
                <td>${item.remainingAmount}</td>
                <td>${new Date(item.dateDue).toLocaleDateString()}</td>
            `;
        default:
            return '';
    }
}
