#TODO login authentication

from app import app

@app.route('/login')
def login():
    return render_template('auth.html') #TODO create signup form
