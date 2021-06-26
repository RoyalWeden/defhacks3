from app import app, config
from flask import render_template, request, session, redirect
app.secret_key = config['SECRET_KEY']

@app.route('/')
def home():
    return 'Home'