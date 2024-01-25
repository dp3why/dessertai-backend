from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return 'server is running'

@app.route('/about')
def about():
    return 'About'

host = os.getenv('HOST')

