from app.model import predict_stag
from flask.helpers import url_for
from scipy.sparse import data
from app import app, config
from flask import render_template, request, session, redirect
from sawo import createTemplate, verifyToken
import json

app.secret_key = config['SECRET_KEY']
createTemplate("app/templates/partials", flask=True)

from app.employee import Employee, Gender, Industry, Profession, Traffic, Coach, GreyWage, Way
from app import database

sawo_company_signup = {
    'auth_key': config['SAWO_SIGNUP_COMPANY_KEY'],
    'identifier': 'email',
    'to': 'signup'
}
sawo_company_signin = {
    'auth_key': config['SAWO_SIGNIN_COMPANY_KEY'],
    'identifier': 'email',
    'to': 'signin'
}
sawo_employee_apply = {
    'auth_key': config['SAWO_APPLY_EMPLOYEE_KEY'],
    'identifier': 'email',
    'to': 'apply'
}

@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html', session=session, applications=database.get_applications(email=session['email']))
    else:
        return render_template('home.html', session=session, applications=None)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        payload = json.loads(request.data)['payload']
        print(payload)
        if verifyToken(payload):
            result = database.create_company(
                payload['identifier'],
                payload['customFieldInputValues']['Enter company name']
            )
            print(result)
            if result['status'] == 200:
                session['email'] = payload['identifier']
        else:
            print('fail')

    return render_template('signup.html', session=session, sawo=sawo_company_signup, load='')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if 'email' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        payload = json.loads(request.data)['payload']
        print(payload)
        if verifyToken(payload):
            result = database.get_company(email=payload['identifier'])
            print(result)
            if result != None:
                session['email'] = payload['identifier']
            else:
                print("This email is not valid. Please sign in with a valid email.")
        else:
            print('fail')

    return render_template('signin.html', session=session, sawo=sawo_company_signin, load='')

@app.route('/signout')
def signout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/apply', methods=['GET','POST'])
def apply():
    if 'email' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        payload = json.loads(request.data)['payload']
        print(payload)
        if verifyToken(payload):
            emplye = Employee(
                payload['identifier'],
                payload['customFieldInputValues']['Enter your first name'],
                payload['customFieldInputValues']['Enter your last name'],
                payload['customFieldInputValues']['Enter your gender (male or female)'],
                payload['customFieldInputValues']['Enter your age'],
                payload['customFieldInputValues']['Enter your industry'],
                payload['customFieldInputValues']['Enter your profession'],
                payload['customFieldInputValues']['Enter how you found out about the company'],
                payload['customFieldInputValues']['Enter whether you had a coach for training'],
                payload['customFieldInputValues']['Enter your supervisor\'s gender'],
                payload['customFieldInputValues']['Enter whether you are receiving grey or white wage'],
                payload['customFieldInputValues']['Enter your way of transportation'],
                payload['customFieldInputValues']['Enter your extraversion score (1-10)'],
                payload['customFieldInputValues']['Enter your independent score (1-10)'],
                payload['customFieldInputValues']['Enter your self-control score (1-10)'],
                payload['customFieldInputValues']['Enter your anxiety score (1-10)'],
                payload['customFieldInputValues']['Enter your innovator score (1-10)']
            )
            company_name = payload['customFieldInputValues']['Enter the company name']
            stag = predict_stag(emplye)
            result = database.create_employee(emplye, company_name, stag)
            print(result)
        else:
            print('fail')

    return render_template('apply.html', session=session, sawo=sawo_employee_apply, load='')

@app.route('/approve', methods=['GET'])
def approve():
    employee_args = {
        'status': 'pending',
        'company_name': request.args.get('company_name'),
        'stag': request.args.get('stag')
    }
    result = database.set_employee_status(employee_args, 'approved')
    return redirect(url_for('home'))

@app.route('/deny', methods=['GET'])
def deny():
    emplye = Employee(
        request.args.get('email'),
        request.args.get('firstname'),
        request.args.get('lastname'),
        request.args.get('gender'),
        request.args.get('age'),
        request.args.get('industry'),
        request.args.get('profession'),
        request.args.get('traffic'),
        request.args.get('coach'),
        request.args.get('head_gender'),
        request.args.get('greywage'),
        request.args.get('way'),
        request.args.get('extraversion'),
        request.args.get('independ'),
        request.args.get('selfcontrol'),
        request.args.get('anxiety'),
        request.args.get('novator')
    )
    employee_args = {
        'status': 'pending',
        'employee': emplye.get_json(),
        'company_name': request.args.get('company_name'),
    }
    result = database.set_employee_status(employee_args, 'denied')
    print(result)
    return redirect(url_for('home'))