from extensions import db  

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    hash_pass = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.hash_pass = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hash_pass, password)