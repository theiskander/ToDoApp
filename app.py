from flask import Flask
from extensions import db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd123e4f5g678h901i2j3k4l5m6n7o8p9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return "It works!"

if __name__ == "__main__":
    app.run(debug=True)