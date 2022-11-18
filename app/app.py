import mysql.connector
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.urandom(32).hex()

database = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_DATABASE']
    )

cursor = database.cursor()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not re.match("^[A-Za-z0-9_-]*$", username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
            user = cursor.fetchone()
            if user and bcrypt.check_password_hash(user[1], password):
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('home'))
                msg = 'Incorrect username!'
            elif user and not bcrypt.check_password_hash(user[1], password):
                msg = 'Incorrect password!'
            else:
                msg = 'Incorrect username!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchall()
        if user:
            msg = 'Account already exists!'
        elif not re.match("^[A-Za-z0-9_-]*$", username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            val = (username, bcrypt.generate_password_hash(password))
            cursor.execute(sql, val)
            database.commit()
            msg = 'You have successfully registered!'
        #return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

@app.route('/home')
def home():
    if 'loggedin' in session:
        cursor.execute("SELECT * FROM post ORDER BY create_datetime DESC")
        posts = cursor.fetchall()
        return render_template('home.html', username=session['username'], posts=posts)
    return redirect(url_for('login'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST' and 'title' in request.form and 'content' in request.form:
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        sql = "INSERT INTO post (username, title, content) VALUES (%s, %s, %s)"
        val = (username, title, content)
        cursor.execute(sql, val)
        database.commit()
        return redirect(url_for('home'))
    else:
        flash('Something wrong!')
        return redirect(url_for('home'))

@app.route('/delete_post/<int:id>')
def delete_post(id):
    sql = "DELETE FROM post WHERE id = %s"
    cursor.execute(sql, (id,))
    database.commit()
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM user ORDER BY create_datetime")
    users = cursor.fetchall()
    return render_template('admin.html', users=users)

@app.route('/remove')
def remove():
    user_sql = "DELETE FROM user"
    cursor.execute(user_sql)
    database.commit()
    cursor.execute("SELECT * FROM user ORDER BY create_datetime")
    users = cursor.fetchall()

    return render_template('admin.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)