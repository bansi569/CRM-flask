from flask import Flask,render_template,request,redirect,jsonify
import mysql.connector
import datetime
@app.route('/')
def welcome_page():
     return render_template('welcomepage.html')