from flask import Flask, render_template, request, redirect, url_for, flash, session
import database_manager as dbHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_DURATION'] = 0  # Session cookie expires when browser closes

dbHandler.init_db()  # Initialize the database

@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    data = dbHandler.listExtension()
    user_name = session.get('user_name')
    return render_template('index.html', content=data, user_name=user_name)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = dbHandler.get_user_by_email(email)
    if user and dbHandler.validate_user(email, password):
        session['logged_in'] = True
        session['user_name'] = f"{user['First_Name']} {user['Surname']}"
        session['user_email'] = email
        session.permanent = False
        return redirect(url_for('index'))
    else:
        # Show modal with error on main page
        data = dbHandler.listExtension()
        return render_template('index.html', content=data, user_name=None, show_auth_modal=True, auth_error="Incorrect password, try again.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
def signup():
    full_name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user_id = dbHandler.create_user(full_name, email, password)
    session['logged_in'] = True
    session['user_name'] = full_name
    session['user_email'] = email
    session.permanent = False
    # Show main page, signed in
    data = dbHandler.listExtension()
    return render_template('index.html', content=data, user_name=full_name)

@app.route('/resources')
def resources():
    user_name = session.get('user_name')
    return render_template('resources.html', user_name=user_name)

@app.route('/time-management')
def time_management():
    user_name = session.get('user_name')
    # Renders the template as HTML
    return render_template('time-management.html', user_name=user_name)

@app.route('/admin/populate-timemanagement-demo')
def admin_populate_timemanagement_demo():
    dbHandler.populate_user_timemanagement_with_demo()
    return "User_TimeManagement table populated with random demo data."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)