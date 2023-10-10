from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
backend_url = 'http://localhost:5000'

# In-memory database (replace with a real database in a production environment)
users = {}


@app.route('/', methods=['POST'])
def login():
    error = None  # Initialize the error message variable
    success_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']        
        try:
            response = requests.post(f'{backend_url}/login', json={
                'email': email,
                'password': password
            })
            print("response: ", response)
            if response.status_code == 200:
                success_message = "Login successful"
                error = None
            else:
                error = response.error
                success_message = None
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    return render_template('login.html', error=error, success_message=success_message)  # Pass the error message to the template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success_message=None
    print('register page')
    if request.method == 'POST':
        print('clicked to post')
        role = request.form.get('role')
        email = request.form['email']
        first_name = request.form['firstName']
        middle_name = request.form['middleName']
        last_name = request.form['lastName']
        password = request.form['password']
        admin = request.form.get('admin')
        try:
            response = ''
            if(admin):
                response = requests.post(f'{backend_url}/{role}', json={
                    'email': email,
                    'firstName': first_name,
                    'middleName': middle_name,
                    'lastName': last_name,
                    'password': password,
                    'admin': True
                })
            else:
                response = requests.post(f'{backend_url}/{role}', json={
                    'email': email,
                    'firstName': first_name,
                    'middleName': middle_name,
                    'lastName': last_name,
                    'password': password
                })
            print("response: ", response)
            if response.status_code == 200:
                success_message = "Signup successful"
                error = None
            elif response.status_code == 400:
                error = "Email account exists"
                success_message = None
            else:                
                error = "Signup failed. Please try again."
                success_message = None
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    return render_template('register.html', error=error, success_message =success_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
