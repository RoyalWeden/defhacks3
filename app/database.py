from pymongo import MongoClient
from pprint import pprint
from app import config
from app.employee import Employee

client = MongoClient(config['MONGODB_URL'])
db = client.turnoverdb
employees = db.employees
companies = db.companies

def create_company(email, company_name):
    if company_name == None or company_name.isspace() or company_name == '':
        return {
            'status': 404,
            'msg': "Enter a valid company name."
        }
    if get_company(email=email) == None and get_company(company_name=company_name) == None:
        result = companies.insert_one({
            'email': email,
            'company_name': company_name
        })
        return {
            'status': 200,
            'id': result.inserted_id,
            'msg': "Company successfully created."
        }
    else:
        return {
            'status': 404,
            'msg': "This email or company name already exists. Please sign in instead."
        }

def create_employee(employee: Employee, company_name, stag):
    result = employees.insert_one({
        'status': 'pending',
        'employee': employee.get_json(),
        'company_name': company_name,
        'stag': stag
    })
    return {
        'status': 200,
        'id': result.inserted_id,
        'msg': "Employee applied successfully"
    }

def get_company(email='', company_name=''):
    if email != '':
        return companies.find_one({
            'email': email
        })
    elif company_name != '':
        return companies.find_one({
            'company_name': company_name
        })
    else:
        None

def get_applications(email='', company_name=''):
    company = get_company(email=email, company_name=company_name)
    result = employees.find({
        'company_name': company['company_name']
    })
    return result

def set_employee_status(employee_args, new_status):
    result = employees.find_one_and_update(employee_args, {'$set': {'status': new_status}})
    return result