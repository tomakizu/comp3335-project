import mysql.connector
import os
import re
import base64
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet
from Cryptodome.Cipher import DES

app = Flask(__name__)
bcrypt = Bcrypt(app)
fernet_key = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
DES_key = b'88888888'
cipher_suite = Fernet(fernet_key)

app.secret_key = os.urandom(32).hex()

database = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_DATABASE']
)

cursor = database.cursor()

def des_encryption(data):
    count = 8 - (len(data) % 8)
    plaintext = data + count * "="
    des = DES.new(DES_key, DES.MODE_ECB)
    ciphertext = des.encrypt(plaintext.encode('utf-8'))
    return str(base64.b64encode(ciphertext), 'utf-8')

def des_decryption(ciphertext):
    des = DES.new(DES_key, DES.MODE_ECB)
    plaintext = des.decrypt(base64.b64decode(ciphertext))
    return plaintext.decode('utf-8').replace('=', '')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if 'loggedin' in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if not re.match("^[A-Za-z0-9_-]*$", username):
                msg = 'Username must contain only characters and numbers!'
            else:
                cursor.execute('SELECT * FROM user WHERE username = %s',
                               (des_encryption(username),))
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
        cursor.execute("SELECT * FROM user WHERE username = %s",
                       (des_encryption(username),))
        user = cursor.fetchall()
        if user:
            msg = 'Account already exists!'
        elif not re.match("^[A-Za-z0-9_-]*$", username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            query = "INSERT INTO user (username, password) VALUES (%s, %s)"
            params = (des_encryption(username),
                      bcrypt.generate_password_hash(password))
            cursor.execute(query, params)
            database.commit()
            msg = 'You have successfully registered!'
        # return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/home')
def home():
    if 'loggedin' in session:
        cursor.execute("SELECT * FROM post ORDER BY create_datetime DESC")
        encrypted_posts = cursor.fetchall()
        decrypted_posts = []
        for encrypted_post in encrypted_posts:
                decrypted_post = (encrypted_post[0],
                                  des_decryption(encrypted_post[1]),
                                  cipher_suite.decrypt(encrypted_post[2]).decode(),
                                  cipher_suite.decrypt(encrypted_post[3]).decode(),
                                  encrypted_post[4])
                decrypted_posts.append(decrypted_post)
        return render_template('home.html', username=session['username'], posts=decrypted_posts)
    return redirect(url_for('login'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST' and 'title' in request.form and 'content' in request.form:
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        query = "INSERT INTO post (username, title, content) VALUES (%s, %s, %s)"
        params = (des_encryption(username),
                  cipher_suite.encrypt(title.encode()),
                  cipher_suite.encrypt(content.encode()))
        cursor.execute(query, params)
        database.commit()
        return redirect(url_for('home'))
    else:
        flash('Something wrong!')
        return redirect(url_for('home'))

@app.route('/delete_post/<int:id>')
def delete_post(id):
    cursor.execute("SELECT username FROM post WHERE id = %s", (id,))
    username = cursor.fetchone()
    if des_decryption(username[0]) == session['username']:
        query = "DELETE FROM post WHERE id = %s"
        cursor.execute(query, (id,))
        database.commit()
        flash("Delete post successfully")
        return redirect(url_for('home'))
    else:
        flash('Sorry, you can only delete your own post!')
        return redirect(url_for('home'))

@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM user ORDER BY create_datetime")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM post ORDER BY create_datetime")
    posts = cursor.fetchall()
    return render_template('admin.html', users=users, posts=posts)

@app.route('/remove')
def remove():
    query1 = "DELETE FROM post"
    cursor.execute(query1)
    database.commit()
    query2 = "DELETE FROM user"
    cursor.execute(query2)
    database.commit()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
