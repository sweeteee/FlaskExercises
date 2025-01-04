from flask import Flask
import config
from exts import db
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
# app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
