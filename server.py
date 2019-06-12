from flask import Flask, render_template, request, redirect, flash, url_for
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'keep it secret'


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def email():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def email_verif():
    
    if  EMAIL_REGEX.match(request.form['email']):
        mysql = connectToMySQL('email_db')
        query = 'INSERT INTO emails (email, created_at) VALUES (%(em)s, NOW());'
        data = {
            'em': request.form['email']
        }
        emails = mysql.query_db(query, data)
        print('id:', emails)
        return redirect(url_for('display'))

    else:
        flash('Invalid email adress!')  
        return redirect('/')

@app.route('/success')
def display():
        mysql = connectToMySQL('email_db')
        emails = mysql.query_db('SELECT * FROM emails;')
        return render_template('success.html', all_users = emails)

if __name__ == "__main__":
    app.run(debug=True)