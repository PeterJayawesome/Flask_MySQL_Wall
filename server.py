from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
import md5
# from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z.+_-]+$')
app = Flask(__name__)
app.secret_key = 'emails'
mysql = MySQLConnector(app,'emaildb')
@app.route('/')
def index():
	if 'log' not in session or 'SL' not in session or 'user_id' not in session:
		session['log'] = False
		session['SL'] = 'l'
		session['user_id'] = None
	return render_template('index.html')
@app.route('/login',methods=['post'])
def login():
	session['SL'] = 'l'
	email = request.form['email']
	password = request.form['password']
	if email and password:
		query = "SELECT users.email,users.password,users.id FROM users WHERE users.email = '"+email+"'"
		info = mysql.query_db(query)
		print info[0]['password']
		if info !=[]:
			secure_password = md5.new(password).hexdigest()
			if info[0]['password'] == secure_password:
				# print session['user_id']
				session['log'] = True;
				session['user_id'] = info[0]['id']
				# print session['user_id']
			else:
				flash('Please enter the correct password.')
				print 1
		else:
			flash('This email has not been registed')
			print 2
	else:
		flash('Please enter the email and password')
		print session['SL']
	if session['log'] == True:
		flash('Log in successfully!')
		return redirect('/')
	else: 
		return redirect('/')
@app.route('/signup',methods=['post'])
def signup():
	session['SL'] = 's'
	if request.form['first'] and request.form['last'] and request.form['email'] and request.form['password'] and request.form['confirm']:
		query = "SELECT users.email FROM users WHERE users.email = '"+request.form['email']+"'"
		if mysql.query_db(query) == []:
			if not NAME_REGEX.match(request.form['first']):
				flash("Invalid First Name")
			elif not NAME_REGEX.match(request.form['last']):
				flash("Invalid Last Name")
			elif not EMAIL_REGEX.match(request.form['email']):
				flash("Invalid Email Adsress")
			elif len(request.form['password']) < 8:
				flash("Password Should Be Longer Than 8 Characters")
			elif request.form['password'] != request.form['confirm']:
				flash("Please Confirm Your Password Again")
			else:
				counter = [0,0]
				for i in request.form['password']:
					if i.isdigit():
						counter[0]+=1
					elif i.isupper():
						counter[1]+=1
				if counter[0] and counter[1]:
					flash("Registrate Successfully!")
					secure_password = md5.new(request.form['password']).hexdigest()
					data = {
							'first_name': request.form['first'],
							'last_name': request.form['last'],
							'email': request.form['email'],
							'password': secure_password,
							}
					query = "INSERT INTO users(first_name,last_name,email,password,created_at,updated_at) VALUES(:first_name,:last_name,:email,:password,NOW(),NOW())"
					mysql.query_db(query,data)
				else:
					flash("There must be at least one uppercase and one number in the password.")
		else:
			flash('This email has been registrated.')
	else:
		# print request.form['first']
		# print request.form['last']
		# print request.form['email']
		# print request.form['password']
		flash("Please complete the full form")
	return redirect('/')

@app.route('/wall')
def wall(){
	
}

app.run(debug = True)