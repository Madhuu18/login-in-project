from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import os
import secrets
import hmac

app = Flask(__name__)  # Corrected __name__
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))  # Secure session key


# Flask-WTF Login Form with CSRF protection
class LoginForm(FlaskForm):
    username = IntegerField('Username', validators=[InputRequired(), NumberRange(1, 100)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


# Route for the Login page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user_value = form.username.data
        password_value = form.password.data

        # Secure password check (Recommended: Use hashed passwords in a database)
        if not (1 <= user_value <= 100) or not hmac.compare_digest(password_value, 'Hindustan@123'):
            return render_template_string(HTML_TEMPLATE, form=form, error_message="Invalid Username or Password!")

        session['user_id'] = user_value
        return redirect(url_for('dashboard', user_id=user_value))

    return render_template_string(HTML_TEMPLATE, form=form, error_message=None)


# Route for the Dashboard page
@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('index'))
    return render_template_string(DASHBOARD_TEMPLATE, user_id=user_id)


# Route for the Tasks page
@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template_string(TASKS_TEMPLATE)


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Main page HTML template (Login Page)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>College Dashboard</title>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #f4f4f4; padding-top: 50px; }
        h1 { font-size: 3rem; color: #333; }
        .textbox { padding: 20px; font-size: 40px; }
        .Inputbox { font-size: 20px; padding: 10px; margin: 10px; width: 250px; }
        .error { font-size: 20px; font-weight: bold; color: red; }
        .login-button { padding: 10px 20px; background-color: rgb(94, 94, 221); color: white; border: none; border-radius: 5px; cursor: pointer; }
        .login-button:hover { background-color: darkblue; }
    </style>
  </head>
  <body>
    <h1>Welcome!</h1>
    <form method="POST">
      {{ form.hidden_tag() }}
      <label class="textbox">Username :</label>
      {{ form.username(class="Inputbox", placeholder="Enter a number (1-100)") }}
      <br><br>
      <label class="textbox">Password :</label>
      {{ form.password(class="Inputbox", placeholder="Password") }}
      <br><br>
      <span class="error">{{ error_message }}</span>
      {{ form.submit(class="login-button") }}
    </form>
  </body>
</html>
"""

# Dashboard Page HTML Template
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Welcome</title>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #f4f4f4; padding-top: 50px; }
        h1 { font-size: 3rem; color: #333; }
        .btn-container { display: flex; flex-direction: column; margin-top: 60px; }
        button { width: 150px; height: 50px; font-size: 20px; padding: 10px; border: none; background-color: #007bff; color: white; cursor: pointer; border-radius: 5px; margin-bottom: 10px; }
        button:hover { background-color: #1f4163; }
    </style>
  </head>
  <body>
    <h1>Welcome Roll No: {{ user_id }}</h1>
    <div class="btn-container">
      <button onclick="window.location.href='/tasks'">Tasks</button>
      <button>Projects</button>
      <button>Documents</button>
    </div>
    <button onclick="window.location.href='/logout'" style="margin-top: 20px;">Logout</button>
  </body>
</html>
"""

# Tasks Page HTML Template
TASKS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Tasks</title>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #f4f4f4; padding-top: 50px; }
        h1 { font-size: 3rem; color: #333; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 10px; font-size: 20px; }
        .completed::after { content: " ✅"; color: green; }
        #logout-btn { padding: 10px; background-color: brown; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }
        #logout-btn:hover { background-color: red; }
    </style>
  </head>
  <body>
    <h1>Tasks</h1>
    <div class="container">
      <p class="completed">Task 1 completed</p>
      <p>Task 2 not completed</p>
      <p>Task 3 not completed</p>
      <p class="completed">Task 4 completed</p>
    </div>
    <button id="logout-btn" onclick="window.location.href='/logout'">LogOut</button>
  </body>
</html>
"""

# Run the app with dynamic port for Render deployment
if __name__ == "__main__":  # Corrected __name__
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 for Render
    app.run(host="0.0.0.0", port=port, debug=True)


  

