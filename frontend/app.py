from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
backend_url = 'http://localhost:5000'

# In-memory database (replace with a real database in a production environment)
users = {}

@app.route('/', methods=['GET','POST'])
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
            if response.status_code == 200:
                success_message = "Login successful"
                error = None
                print('response: ', response.json())
                usertype = response.json().get('userType')
                user_email = response.json().get('email')
                if(usertype == 'facilitators'):
                    user_type = 'facilitator'
                elif(usertype == 'students'):
                    user_type = 'student'
                print('user_email: ', user_email)
                print('user_type: ', user_type)
                return redirect(f'/{user_type}/{user_email}')
            if response.status_code == 400:
                error = response.error
                success_message = None
            else:                
                error = 'Invalid Login Details'
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

@app.route('/<userType>/<userEmail>', methods=['GET', 'POST'])
def dashboard(userType, userEmail):
    userError = None
    response = requests.get(f'{backend_url}/requests/student/{userEmail}')
    the_requests = response.json()
    print('the_requests: ', the_requests)
    if userType == 'facilitator':
        if response.status_code == 200:
            _requests = [request for request in the_requests if request['facilitator'] == userEmail]
            print('_requests: ', _requests)
        return render_template('facilitator.html', userError=userError, requests=_requests)  
    else:
        if response.status_code == 200:
            _requests = [request for request in the_requests if request['student'] == userEmail]
            print('_requests: ', _requests)
        return render_template('student.html', userError=userError, requests=the_requests, userEmail=userEmail)  

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect('/')

@app.route('/new_request/<student>', methods=['GET', 'POST'])
def new_request(student):
    error=None
    success_message= None
    response = requests.get(f'{backend_url}/users/facilitators')
    facilitators = response.json()
    print('facilitators: ', facilitators)
    if request.method == 'POST':
        facilitator = request.form.get('facilitator')
        title = request.form['title']
        message = request.form['message']        
        try:
            response = requests.post(f'{backend_url}/new_request/{student}', json={
                'student': student,
                'facilitator': facilitator,
                'title': title,
                'message': message
            })
            print("submitted request: ", response.json())
            if response.status_code == 200:
                success_message = "Request successfully added"
                error=None
            else:
                error="An error occured, please submit again"
                success_message=None
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    return render_template('new_request.html',student=student, error=error, success_message=success_message, facilitators=facilitators)  

@app.route('/<requestID>/responses', methods=['GET', 'POST'])
def responses(requestID):
    error=None
    success_message= None
    responses = None
    the_response = requests.get(f'{backend_url}/requests/{requestID}')
    request_name = the_response.json().get('title')
    response = requests.get(f'{backend_url}/requests/{requestID}/responses')
    if response.status_code == 200:
        responses = response.json()
    return render_template('request_responses.html', requestID =requestID, error=error, success_message=success_message, request_name=request_name, responses=responses)  

@app.route('/<string:requestID>/responses', methods=['GET', 'POST'])
def respond(requestID):
    success_message= None
    if request.method == 'POST':
        message = request.form['message']        
        try:
            response = requests.post(f'{backend_url}/requests/{requestID}/responses', json={
                'message': message
            })
            if response.status_code == 200:
                success_message = "Request successfully added"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    else:
        return render_template('new_rjjesponse.html', requestID =requestID, success_message=success_message, responses=responses)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
