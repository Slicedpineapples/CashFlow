from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from rawData import expensesRawData, incomeRawData, assetsRawData, liabilitiesRawData
from utils import getExchangeRate

# Function to create the base PDF
def createPDF(file_name, end, currency, email):
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # Title Box
    c.setStrokeColor(colors.purple)
    c.setLineWidth(1.5)
    c.rect(50, height - 58, 510, 30)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 50, f'Monthly Report: {end}                Report Currency: {currency}')
    return c, width, height

# Function to add income data
def addIncomeData(c, width, height, start_height, income_data):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, start_height, "INCOME STATEMENT")
    start_height -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, start_height-5, "Income:")
    start_height -= 20
    c.rect(50, start_height - len(income_data) * 20, 240, len(income_data) * 20 + 30)

    for i, data in enumerate(income_data):
        c.drawString(70, start_height - i * 20, f"{data['incomeName']}: {data['amount']}")
    
    return start_height - len(income_data) * 20 - 20

# Function to add expenses data
def addExpensesData(c, width, height, start_height, expenses_data):
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, start_height-5, "Expenses:")
    start_height -= 20
    c.rect(50, start_height - len(expenses_data) * 20, 240, len(expenses_data) * 20 + 30)

    for i, data in enumerate(expenses_data):
        c.drawString(70, start_height - i * 20, f"{data['expenseName']}: {data['total_price']}")
    
    return start_height - len(expenses_data) * 20 - 20

# Function to add assets data
def addAssetsData(c, width, height, start_height, assets_data):
    c.setFont("Helvetica-Bold", 10)
    c.drawString(310, start_height, "BALANCE SHEET")
    start_height -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(310, start_height-5, "Assets:")
    start_height -= 20
    c.rect(300, start_height - len(assets_data) * 20, 260, len(assets_data) * 20 + 30)

    for i, data in enumerate(assets_data):
        c.drawString(320, start_height - i * 20, f"{data['numberOfItems']} {data['assetName']} ({data['location']}): {data['value']}")
    
    return start_height - len(assets_data) * 20 - 20

# Function to add liabilities data
def addLiabilitiesData(c, width, height, start_height, liabilities_data):
    c.setFont("Helvetica-Bold", 10)
    c.drawString(310, start_height-5, "Liabilities:")
    start_height -= 20
    c.rect(300, start_height - len(liabilities_data) * 20, 260, len(liabilities_data) * 20 + 30)

    for i, data in enumerate(liabilities_data):
        c.drawString(320, start_height - i * 20, f"{data['liabilityName']}: {data['grossAmount']} (Due: {data['dateDue']})")
    
    return start_height - len(liabilities_data) * 20 - 20

# Function to add financial summary
def addFinancialStanding(c, width, height, start_height, total_income, total_expenses, total_assets, total_liabilities, net_savings, net_investment):
    c.setFont("Helvetica-Bold", 10)
    c.rect(50, start_height - 100, 510, 100)
    start_height -= 15
    c.drawString(60, start_height, "FINANCIAL STANDING")

    c.setFont("Helvetica", 10)
    c.drawString(60, start_height - 25, f"Total income: {total_income}")
    c.drawString(200, start_height - 25, f"Total assets: {total_assets}")
    c.drawString(60, start_height - 45, f"Total expenses: {total_expenses}")
    c.drawString(200, start_height - 45, f"Total liabilities: {total_liabilities}")
    c.drawString(60, start_height - 65, f"Net savings: {net_savings}")
    c.drawString(200, start_height - 65, f"Net investment: {net_investment}")

    return start_height - 100

def footer(c, width, height, email):
    c.setFont("Helvetica", 9)
    c.drawString(width - 100, 30, "Page %d" % c.getPageNumber())
    c.drawString(50, 30, f"Generated by: {email}")

# Function to generate the full report
def generateReport(file_name, income_data, expenses_data, assets_data, liabilities_data, total_income, total_expenses, total_assets, total_liabilities, net_savings, net_investment, end, currency, email):
    c, width, height = createPDF('reports/monthlyReports/' + file_name, end, currency, email)

    # Draw outer boundary
    c.rect(40, height - 800, 530, 780)

    start_height = height - 100
    start_height = addIncomeData(c, width, height, start_height, income_data)
    start_height = addExpensesData(c, width, height, start_height, expenses_data)

    right_column_start_height = height - 100
    right_column_start_height = addAssetsData(c, width, height, right_column_start_height, assets_data)
    right_column_start_height = addLiabilitiesData(c, width, height, right_column_start_height, liabilities_data)

    start_height = min(start_height, right_column_start_height)
    addFinancialStanding(c, width, height, start_height, total_income, total_expenses, total_assets, total_liabilities, net_savings, net_investment)

    footer(c, width, height, email)
    c.save()

# Function to generate report via API
def apiGenReport(userId, email, start, end, currency):
    success = 'Summary report generated successfully.\nWe have sent it to your email.'

    rawIncome = incomeRawData(userId, start, end, currency)
    income_data = rawIncome[0]

    rawExpenses = expensesRawData(userId, start, end, currency)
    expenses_data = rawExpenses[0]

    rawAssets = assetsRawData(userId, start, end, currency)
    assets_data = rawAssets[0]

    rawLiabilities = liabilitiesRawData(userId, start, end, currency)
    liabilities_data = rawLiabilities[0]

    total_income = rawIncome[1]
    total_expenses = rawExpenses[1]
    total_assets = rawAssets[1]
    total_liabilities = rawLiabilities[1]
    net_savings = round((total_income - total_expenses), 2)
    net_investment = total_assets - total_liabilities

    month = datetime.strptime(end, '%Y-%m-%d').strftime('%B')
    year = datetime.strptime(end, '%Y-%m-%d').strftime('%Y')
    end = month + ' ' + year

    file_name = f'SR-UID-{userId}-{month}{year}.pdf'
    
    generateReport(
        file_name,
        income_data,
        expenses_data,
        assets_data,
        liabilities_data,
        total_income,
        total_expenses,
        total_assets,
        total_liabilities,
        net_savings,
        net_investment,
        end,
        currency,
        email
    )

    file_path = 'reports/monthlyReports/' + file_name
    return file_path, success
