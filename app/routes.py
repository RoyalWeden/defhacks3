from app import app, config
from flask import render_template, request, session, redirect
# app.secret_key = config['SECRET_KEY']

from app.model import predict_stag
from app.employee import Employee, Gender, Industry, Profession, Traffic, Coach, GreyWage, Way

test_employee = Employee(
    Gender.male,
    23.0,
    Industry.banks,
    Profession.accounting,
    Traffic.rabrecnerab,
    Coach.no,
    Gender.female,
    GreyWage.grey,
    Way.car,
    5.5,
    2.3,
    4.7,
    1.2,
    3.6
)

@app.route('/')
def home():
    val = predict_stag(test_employee)
    return str(val)