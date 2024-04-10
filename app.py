from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/')
def home():
    return render_template('home.html', books=BOOKS)

@app.route('/api/books')
def list_books():
    return jsonify(BOOKS)

@app.route('/login')
def login():
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
