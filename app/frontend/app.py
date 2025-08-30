import sqlite3
import os
from flask import Flask, render_template, request, g, redirect, url_for

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

# Define the HTML content for the single page
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">

    <div class="bg-white p-8 rounded-2xl shadow-lg w-full max-w-2xl">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">{{ title }}</h1>

        <!-- Add User Form -->
        <div class="bg-gray-50 p-6 rounded-xl mb-8 border border-gray-200">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">Add New User</h2>
            <form method="post" action="/add_user" class="space-y-4">
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                    <input type="text" id="name" name="name" required
                           class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                    <input type="email" id="email" name="email" required
                           class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                </div>
                <button type="submit"
                        class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200">
                    Add User
                </button>
            </form>
        </div>

        <!-- Users List -->
        <div class="bg-gray-50 p-6 rounded-xl border border-gray-200">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">Existing Users</h2>
            {% if users %}
            <ul class="divide-y divide-gray-200">
                {% for user in users %}
                <li class="py-4 flex items-center justify-between">
                    <div class="flex-1 min-w-0">
                        <p class="text-lg font-medium text-gray-900 truncate">{{ user.name }}</p>
                        <p class="text-sm text-gray-500 truncate">{{ user.email }}</p>
                    </div>
                </li>
                {% endfor %}
            </ul>
            {% else %}
            <p class="text-center text-gray-500 italic">No users found.</p>
            {% endif %}
        </div>
    </div>

</body>
</html>
"""

def get_db():
    """Establishes a database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db_path = os.path.join(app.root_path, app.config['DATABASE'])
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row # Allows access to columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database schema."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
        db.commit()

@app.route('/')
def index():
    """Main route to display users and the add user form."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users ORDER BY name")
    users = cursor.fetchall()
    return render_template_string(HTML_TEMPLATE, title="User Management App", users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    """Adds a new user to the database."""
    name = request.form['name']
    email = request.form['email']
    if name and email:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        db.commit()
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    return 'OK', 200

# Function to render a string as a template
def render_template_string(template, **kwargs):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.from_string(template)
    return template.render(**kwargs)

# Initialize the database when the app starts
with app.app_context():
    init_db()

if __name__ == '__main__':
    # Use 0.0.0.0 for Docker to expose the port to the host
    app.run(host='0.0.0.0', port=5000)
