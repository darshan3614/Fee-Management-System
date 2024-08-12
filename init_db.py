from app import db
from models import User
from werkzeug.security import generate_password_hash

def init_db():
    db.create_all()

    # Create a user with username 'test' and password 'test123'
    existing_user = User.query.filter_by(username='test').first()
    if not existing_user:
        hashed_password = generate_password_hash('test123')
        test_user = User(username='test', password_hash=hashed_password, role='parent')
        db.session.add(test_user)
        db.session.commit()

if __name__ == '__main__':
    init_db()