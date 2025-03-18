from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from rawData import expensesRawData, incomeRawData, assetsRawData, liabilitiesRawData
from utils import ustVerify, userFetch

global font, font_bold, font_italic
font = "Helvetica"
font_bold = "Helvetica-Bold"
font_italic = "Helvetica-Italic"

def createPDF(file_name, reportMonth, currency):
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    
    # Title Box with Rounded Corners
    c.setFillColor(colors.gray)
    c.roundRect(50, height - 70, 510, 40, 10, stroke=1, fill=0)
    c.setFont(font_bold, 12)
    c.drawString(100, height - 55, f'Monthly Report: {reportMonth}              Report Currency: {currency}')
    return c, width, height

def addSectionTitle(c, text, x, y):
    c.setFont(font, 12)
    c.setFillColor(colors.black)
    c.drawString(x, y, text)
    c.line(x, y - 5, x + 200, y - 5)
    y -= 20
    return y

def addDataSection(c, x, y, data, section_title, width=240):
    addSectionTitle(c, section_title, x, y)
    y -= 25
    c.roundRect(x - 10, y - len(data) * 20 - 10, width, len(data) * 20 + 30, 5, stroke=1, fill=0)
    c.setFont(font, 10)
    for i, item in enumerate(data):
        c.drawString(x, y - i * 20, f"{item['name']}: {item['value']}")
        c.line(x, y - i * 20 - 2, x + width - 20, y - i * 20 - 2)
    return y - len(data) * 25 - 25

def addFinancialStanding(c, x, y, financial_data):
    # Add the section title (already adjusted above)
    addSectionTitle(c, "FINANCIAL STANDING", x, y)
    y -= 25  # Move y down after title

    # Calculate the required height based on the number of items (with some padding)
    line_height = 20  # The height per line
    box_padding = 15   # Padding for the box
    box_height = len(financial_data) * line_height + box_padding  # Total height of the box

    # Draw the box with dynamically calculated height
    c.roundRect(x - 10, y - box_height +20, 510, box_height, 10, stroke=1, fill=0)
    
    # Set font for financial data text
    c.setFont(font, 10)
    
    # Loop through each financial data item and draw it inside the box
    for i, (key, value) in enumerate(financial_data.items()):
        c.drawString(x, y - (i * line_height), f"{key}: {value}")
    
    # Return the updated y position after the financial data box
    return y - box_height - 30  # Ensure space after the box for the next section

def footer(c, width, height, email):
    c.setFont(font, 9)
    c.drawString(width - 100, 30, "Page %d" % c.getPageNumber())
    c.drawString(100, 30, f"Report generated on CashFlow for {email} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def generateReport(file_name, income, expenses, assets, liabilities, totals, end, currency, email):
    c, width, height = createPDF('reports/monthlyReports/' + file_name, end, currency)
    c.roundRect(40, height - 800, 530, 780, 15, stroke=1, fill=0)
    start_height = height - 100
    start_height = addDataSection(c, 60, start_height, income, "INCOME STATEMENT")
    start_height = addDataSection(c, 60, start_height, expenses, "EXPENSES")
    right_column_start = height - 100
    right_column_start = addDataSection(c, 310, right_column_start, assets, "BALANCE SHEET")
    right_column_start = addDataSection(c, 310, right_column_start, liabilities, "LIABILITIES")
    final_height = min(start_height, right_column_start)
    addFinancialStanding(c, 60, final_height, totals)
    footer(c, width, height, email)
    c.save()

def apiGenReport(start, end, currency, userId, ust):
    if ustVerify(userId, ust) == False:
        print("Error at summary: Invalid User Security Token")
        return "Invalid session"
    else:
        user = userFetch(userId, ust)
        userId = user['userId']
        email = user['email']
        success = f'Summary report generated successfully.\nWe have sent it to {email}.'
        rawIncome = incomeRawData(userId, start, end, currency)
        rawExpenses = expensesRawData(userId, start, end, currency)
        rawAssets = assetsRawData(userId, start, end, currency)
        rawLiabilities = liabilitiesRawData(userId, start, end, currency)
        income_data = [{'name': i['incomeName'], 'value': i['amount']} for i in rawIncome[0]]
        expenses_data = [{'name': e['expenseName'], 'value': e['total_price']} for e in rawExpenses[0]]
        assets_data = [{'name': f"{a['numberOfItems']} {a['assetName']} ({a['location']})", 'value': a['value']} for a in rawAssets[0]]
        liabilities_data = [{'name': l['liabilityName'], 'value': f"{l['grossAmount']} (Due: {l['dateDue']})"} for l in rawLiabilities[0]]
        totals = {
            "Total income": rawIncome[1],
            "Total expenses": rawExpenses[1],
            "Total assets": rawAssets[1],
            "Total liabilities": rawLiabilities[1],
            "Net savings": round((rawIncome[1] - rawExpenses[1]), 2),
            "Net investment": round(rawAssets[1] - rawLiabilities[1], 2)
        }
        month = datetime.strptime(end, '%Y-%m-%d').strftime('%B')
        year = datetime.strptime(end, '%Y-%m-%d').strftime('%Y')
        reportMonth = month + ' ' + year
        file_name = f'SR-UID-{userId}-{month}{year}-{currency}.pdf'
        generateReport(file_name, income_data, expenses_data, assets_data, liabilities_data, totals, reportMonth, currency, email)
        return 'reports/monthlyReports/' + file_name, success
