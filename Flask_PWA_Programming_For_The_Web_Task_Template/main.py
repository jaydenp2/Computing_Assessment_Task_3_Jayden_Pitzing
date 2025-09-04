from flask import Flask, render_template, request, redirect, url_for, flash, session
import database_manager as dbHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and session

dbHandler.init_db()  # Initialize the database

@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    data = dbHandler.listExtension()
    return render_template('index.html', content=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if dbHandler.validate_user(email, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "Incorrect password, try again."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)