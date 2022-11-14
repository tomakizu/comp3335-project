import mysql.connector
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    database = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_DATABASE']
    )
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)