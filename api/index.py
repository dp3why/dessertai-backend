from flask import Flask
from dotenv import load_dotenv
from .controllers import user_controller, file_controller
import os

load_dotenv()
app = Flask(__name__)

# routers
app.register_blueprint(user_controller.user_blueprint)
app.register_blueprint(file_controller.file_blueprint)

@app.route('/')
def home():
    return 'server is running'




