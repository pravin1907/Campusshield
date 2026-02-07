from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import uuid
import re
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'campusshield_secret'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

complaints = {}
admin_username = "admin"
admin_password = "admin123"

@app.route('/')
def report_form():
    return render_template('report_form.html')

@app.route('/submit', methods=['POST'])
def submit_report():
    category = request.form['category']
    date = request.form['date']
    location = request.form['location']
    description = request.form['description']
    file = request.files.get('photo')

    app_id = str(uuid.uuid4())[:8].upper()
    filename = None

    if file and file.filename != '':
        filename = secure_filename(app_id + "_" + file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Urgency detection using keywords and regex
    keywords = ["harassment", "abuse", "suicide", "depression", "threat", "unsafe", "crying", "molest", "violence"]
    urgency = "Low"
    words = description.lower().split()

    if any(word in words for word in keywords) or re.search(r'\b(harass|abuse|bully|threat|violence|molest)\b', description.lower()):
        urgency = "High"
    elif any(word in description.lower() for word in ["issue", "problem", "concern", "fear"]):
        urgency = "Medium"

    complaints[app_id] = {
        'category': category,
        'date': date,
        'location': location,
        'description': description,
        'photo': filename,
        'status': 'Pending',
        'urgency': urgency
    }

    return render_template('success.html', app_id=app_id)

@app.route('/track_report')
def track_report():
    return render_template('track_report.html')

@app.route('/track', methods=['POST'])
def track():
    app_id = request.form['app_id'].upper()
    data = complaints.get(app_id)
    return render_template('track_result.html', data=data, app_id=app_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == admin_username and request.form['password'] == admin_password:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html', complaints=complaints)
    return redirect('/login')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

