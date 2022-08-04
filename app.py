from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase 

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
	"apiKey": "AIzaSyBmh8Ep16oRIce7BeRl4htBKBKxvmGcmPI",
	"authDomain": "mini-project-1d2a7.firebaseapp.com",
	"projectId": "mini-project-1d2a7",
	"storageBucket": "mini-project-1d2a7.appspot.com",
	"messagingSenderId": "691958211021",
	"appId": "1:691958211021:web:020066c15142e9828a6484",
	"measurementId": "G-CNCP9MJZL3","databaseURL": "https://mini-project-1d2a7-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
	
@app.route('/')
def HomePage():
	if 'user' in login_session:
		if login_session['user'] != None:
			user = db.child('Users').child(login_session['user']['localId']).get().val()
			if 'username' in user:
				return render_template("GYMbrosHomePage.html", username = user['username'])
	return render_template("GYMbrosHomePage.html")

@app.route('/signup', methods = ['GET','POST'])
def SignUp():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		username = request.form['username']
		user = {"email": email, "password": password,"username":username}
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			db.child('Users').child(login_session['user']['localId']).set(user)
			return redirect(url_for("SignIn"))
		except: 
			error = "Authentication failed"
	return render_template("signup.html")

@app.route('/signin', methods = ['GET', 'POST'])
def SignIn():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('HomePage'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")

@app.route('/signout')
def SignOut():
    login_session['user'] = None
    auth.current_user = None

    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('HomePage'))

if __name__ == '__main__':
		app.run(debug=True)