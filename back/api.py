from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
from flask_cors import CORS
import logging
from liabilities import liabilities, liabilitiescategory
from welcome import login, signUp
from income import income, incomeCategory, incomeSource
from expenses import expenses, expensesCategory, expensesPrice
from assets import assetsCategory, assets
from reports import incomeReport, expensesReport, assetsReport, liabilitiesReport
from pdfGen import apiGenReport
from mess import send_email
from utils import Convert, seed, makeDir
from update import updateCountry

makeDir() #creting the directories

seed() # seeding the database 


# app = Flask(__name__)
app = Flask(__name__)
CORS(app) # Allow CORS for all routes

# Setup logging
logging.basicConfig(level=logging.INFO)

# Schemas for request validation
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class SignupSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Length(equal=10))
    password = fields.Str(required=True)

class AddIncomeSchema(Schema):
    sourceName = fields.Str(required=True)
    amount = fields.Float(required=True)
    incomeCategory = fields.Str(required=True)
    userID = fields.Int(required=True)
    ust = fields.Str(required=True)

class AddExpenseSchema(Schema):
    itemName = fields.Str(required=True)
    price = fields.Float(required=True)
    expenseCategory = fields.Str(required=True)
    userID = fields.Int(required=True)
    ust = fields.Str(required=True)


class AddAssetSchema(Schema):
    assetCategory = fields.Str(required=True)
    userID = fields.Int(required=True)
    value = fields.Float(required=True)
    numberOfItems = fields.Int(required=True)
    location = fields.Str(required=True)
    name = fields.Str(required=True)
    ust = fields.Str(required=True)


class AddLiabilitySchema(Schema):
    liabilityCategory = fields.Str(required=True)
    userID = fields.Int(required=True)
    grossAmount = fields.Float(required=True)
    remainingAmount = fields.Float(required=True)
    ust = fields.Str(required=True)


class ReportSchema(Schema):
    userID = fields.Int(required=True)
    start = fields.Date(required=True)
    end = fields.Date(required=True)
    ust = fields.Str(required=True)


class SummarySchema(Schema):
    userId = fields.Int(required=True)
    email = fields.Email(required=True)
    start = fields.Str(required=True)
    end = fields.Str(required=True)
    currency = fields.Str(required=True)
    ust = fields.Str(required=True)


class UpdateCountrySchema(Schema):
    userId = fields.Int(required=True)
    newCountry = fields.Str(required=True)
    ust = fields.Str(required=True)


# class EmailSchema(Schema):
#     email = fields.Email(required=True)
#     attachment = fields.Str(required=True)

# Utility function for validation
def validate_input(schema, data):
    try:
        validated_data = schema.load(data)
        return validated_data, None
    except ValidationError as err:
        return None, err.messages

@app.route('/apiLogin', methods=['POST'])
def api_login():
    data, errors = validate_input(LoginSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
    
    response = login(data['username'], data['password'])
    return jsonify({'message': response})

@app.route('/apiSignup', methods=['POST'])
def api_signup():
    data, errors = validate_input(SignupSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
    
    response = signUp(data['username'], data['email'], data['password'], data['phone'])
    return jsonify({'message': response[1]})

@app.route('/apiAddIncome', methods=['POST'])
def api_addIncome():
    data, errors = validate_input(AddIncomeSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400

    sourceID = incomeSource(data['sourceName'], data['amount'])
    if sourceID:
        categoryID = incomeCategory(data['incomeCategory'])
        if categoryID:
            response = income(data['userID'], sourceID, categoryID, data['ust'])
            if response == "success":
                return jsonify({'message': "Income added!"}), 200
            return jsonify({'message': 'Something went wrong at income()'}), 500
        return jsonify({'message': 'Invalid income category'}), 400
    return jsonify({'message': 'Invalid income source'}), 400

@app.route('/apiAddExpense', methods=['POST'])
def api_addExpense():
    data, errors = validate_input(AddExpenseSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400

    priceID = expensesPrice(data['itemName'], data['price'])
    if priceID:
        categoryID = expensesCategory(data['expenseCategory'])
        if categoryID:
            response = expenses(priceID, categoryID, data['userID'], data['ust'])
            if response == "success":
                return jsonify({'message': "Expense added!"}), 200
            return jsonify({'message': 'Something went wrong at expenses()'}), 500
        return jsonify({'message': 'Invalid expense category'}), 400
    return jsonify({'message': 'Invalid expense price'}), 400

@app.route('/apiAddAsset', methods=['POST'])
def api_addAsset():
    data, errors = validate_input(AddAssetSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400

    assetCategoryID = assetsCategory(data['name'], data['numberOfItems'], data['location'])
    if assetCategoryID:
        response = assets(assetCategoryID, data['userID'], data['value'], data['ust'])
        if response == "success":
            return jsonify({'message': "Asset added!"}), 200
        return jsonify({'message': 'Something went wrong at assets()'}), 500
    return jsonify({'message': 'Invalid asset category'}), 400

@app.route('/apiAddLiability', methods=['POST'])
def api_addLiability():
    data, errors = validate_input(AddLiabilitySchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400

    liabilityCategoryID = liabilitiescategory(data['liabilityCategory'], data['grossAmount'], data['remainingAmount'])
    if liabilityCategoryID:
        response = liabilities(liabilityCategoryID, data['userID'], data['ust'])
        if response == "success":
            return jsonify({'message': "Liability added!"}), 200
        return jsonify({'message': 'Something went wrong at liabilities()'}), 500
    return jsonify({'message': 'Invalid liability category'}), 400

@app.route('/apiGetIncomeReport', methods=['POST'])
def api_getIncomeReport():
    data, errors = validate_input(ReportSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
    
    response = incomeReport(data['userID'], data['start'], data['end'], data['ust'])
    # print(response) # Debugging only
    return jsonify({'message': response}), 200

@app.route('/apiGetExpensesReport', methods=['POST'])
def api_getExpensesReport():
    data, errors = validate_input(ReportSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
    
    response = expensesReport(data['userID'], data['start'], data['end'], data['ust'])
    return jsonify({'message': response}), 200

@app.route('/apiGetAssetsReport', methods=['POST'])
def api_getAssetsReport():
    data, errors = validate_input(ReportSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
    
    response = assetsReport(data['userID'], data['start'], data['end'], data['ust'])
    return jsonify({'message': response}), 200

@app.route('/apiGetLiabilitiesReport', methods=['POST'])
def getLiabilitiesReport():
    data, errors = validate_input(ReportSchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
    
    response = liabilitiesReport(data['userID'], data['start'], data['end'], data['ust'])
    return jsonify({'message': response}), 200

@app.route('/apiGetSummary', methods=['POST'])
def getSummary():
    data, errors = validate_input(SummarySchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400
 
    response = apiGenReport(data['userId'], data['email'], data['start'], data['end'], data['currency'], data['ust'])
    if response:
        endMonth = data['end'].split('-')[1]
        end = Convert(endMonth)+' '+data['end'].split('-')[0]
        # print(end) # Debugging only
        
        send_email(data['email'], response[0], end) # response[0] is the file path
        return jsonify({'message': response[1]}), 200 # response[1] is the success message
    return jsonify({'message': 'Something went wrong'}), 500


@app.route('/apiUpdateCountry', methods=['POST'])
def updateCountryAPI():
    data, errors = validate_input(UpdateCountrySchema(), request.get_json())
    if errors:
        return jsonify({'errors': errors}), 400

    response = updateCountry(data['userId'], data['newCountry'])
    return jsonify({'message': response}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
