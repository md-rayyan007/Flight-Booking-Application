from app import app
from flask import render_template

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

if __name__ == "__main__":
    app.run(debug=True)
