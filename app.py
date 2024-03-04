from flask import Flask,render_template

app=Flask(__name__)

BOOKS=[
    {
        'id':123,
        'Title':'Harry Potter',
        'Author':'J.K Rowling',
        'Volume':7,
        'Price':500,
        'Rating':4.7,
        'Year': 1998,
        
        
    },
    
    {
        'id':125,
        'Title':'Percy Jackson & the Olympians',
        'Author':'Rick Riordan',
        'Volume':1,
        'Price':500,
        'Rating':4.7,
        'Year': 2005,
        
        
    },
    
    {
        'id':122,
        'Title':'Goosebumps',
        'Author':'R. L. Stine',
        'Volume':6,
        'Price':500,
        'Rating':4.2,
        'Year': 1998,
        
        
    },
    
    {
        'id':120,
        'Title':'The Twin Serpents',
        'Author':'Ronald Scott Thorn',
        'Volume':6,
        'Price':500,
        'Rating':4.2,
        'Year': 1965,
        
        
    },
]

@app.route('/')
def hell_world():
    return render_template('home.html', books=BOOKS)

if __name__=="__main__":
    app.run(debug=True)