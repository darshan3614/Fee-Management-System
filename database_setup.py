from app import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(164))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def init_db():
    db.create_all()

    # Create a user with username 'test' and password 'test123'
    existing_user = User.query.filter_by(username='test').first()
    if not existing_user:
        test_user = User(username='test')
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()

if __name__ == '__main__':
    init_db()