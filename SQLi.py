from server import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

# Function to initialize the database with users and insert test data
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )''')

    # Insert dummy user data (used in the challenge)
    conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'user123')")
    
    conn.commit()
    conn.close()

# Function to read the flag from a text file
def get_flag():
    return "\nUHB{SQL_Injection_Bypassed_Successfully!!}"

# Home route to render the login page
@app.route('/')
def home():
    return render_template('login.html')

# Login route that processes the form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']  # User input for the username
    password = request.form['password']  # User input for the password

    conn = get_db_connection()

    # Vulnerable SQL query: directly injecting the username into the query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    # Execute the query and fetch the user
    user = conn.execute(query).fetchone()
    
    conn.close()

    # Check if the user is found and return the flag
    if user:
        flag = get_flag()  # If the login is successful, return the flag
        return f"Login successful! Welcome, {user['username']}. {flag}"
    else:
        return "Login failed. Invalid username or password."

# Run the Flask app
if __name__ == '__main__':
    init_db()  # Initialize the database with users
    app.run(debug=True)
