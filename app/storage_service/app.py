from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/storage/uploads'
DB_PATH = '/storage/files.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for uploaded files
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            # Save filename in database
            new_file = File(filename=file.filename)
            db.session.add(new_file)
            db.session.commit()
            return f"File '{file.filename}' uploaded successfully!"
    files = File.query.all()
    return render_template_string('''
        <h1>Upload a File</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
        <h2>Uploaded Files:</h2>
        <ul>
        {% for f in files %}
            <li>{{ f.filename }}</li>
        {% endfor %}
        </ul>
    ''', files=files)

if __name__ == '__main__':
    # Run db.create_all() inside the application context
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
