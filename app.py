from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
import sqlite3

app = Flask(__name__)
app.secret_key = "12345678"

# Creating database tables if they don't exist
con = sqlite3.connect("database.db")
con.execute("CREATE TABLE IF NOT EXISTS user(pid INTEGER PRIMARY KEY, name TEXT, username TEXT UNIQUE, password TEXT, email TEXT)")
con.close()

BOOKS = [
    {
        'id': 123,
        'Title': 'Harry Potter',
        'Author': 'J.K Rowling',
        'Volume': 7,
        'Price': 500,
        'Rating': 4.7,
        'Year': 1998,
        'img': 'static/img/harrypotter.jpeg'
    },
    {
        'id': 125,
        'Title': 'Percy Jackson & the Olympians',
        'Author': 'Rick Riordan',
        'Volume': 1,
        'Price': 500,
        'Rating': 4.7,
        'Year': 2005,
        'img': 'static/img/Percy Jackson.jpeg'
    },
    {
        'id': 122,
        'Title': 'Goosebumps',
        'Author': 'R. L. Stine',
        'Volume': 6,
        'Price': 500,
        'Rating': 4.2,
        'Year': 1998,
        'img': 'static/img/Goosebumps.jpeg'
    },
    {
        'id': 120,
        'Title': 'The Twin Serpents',
        'Author': 'Ronald Scott Thorn',
        'Volume': 6,
        'Price': 500,
        'Rating': 4.2,
        'Year': 1965,
        'img': 'static/img/The Twin Serpents.jpeg'
    }
]


@app.route('/home', methods=['GET','POST'])
@app.route('/')
def home():
    return render_template('home.html', books=BOOKS)

@app.route('/api/books')
def list_books():
    return jsonify(BOOKS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            name = request.form['name']
            password = request.form['pwd']

            # Establish connection to the database
            con = sqlite3.connect("database.db")
            cr = con.cursor()

            # Execute SQL SELECT query to retrieve user data based on username and password
            cr.execute("SELECT * FROM user WHERE username=? AND password=?", (name, password))
            data = cr.fetchone()

            if data:
                # Store user data in session upon successful login
                session["username"] = data['username']
                session["name"] = data['name']
                session["email"] = data['email']
                con.close()  # Close the database connection

                # Redirect to 'home' route upon successful login
                return redirect(url_for('home'))
            else:
                # Display flash message for invalid credentials
                flash("Invalid Username and Password. Please try again.", "danger")
                con.close()  # Close the database connection

                # Redirect back to 'login' route if login fails
                return redirect(url_for('login'))

        except Exception as e:
            # Handle any exceptions (e.g., database connection error)
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('login'))

    # Render the login.html template for GET requests
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            password = request.form['pwd']

            # Establishing database connection
            con = sqlite3.connect("database.db")
            cur = con.cursor()

            # Insert user data into the 'user' table
            cur.execute("INSERT INTO user(name, username, password, email) VALUES (?, ?, ?, ?)", (name, username, password, email))

            # Committing the transaction
            con.commit()

            # Display success message using Flask's flash
            flash("Account created successfully", "success")
        except Exception as e:
            # Display error message using Flask's flash
            flash(f"Failed to create account: {str(e)}", "danger")
        finally:
            # Closing the database connection
            con.close()
            return redirect(url_for("login"))

    # Render the signup.html template for GET requests
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
