from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
db = SQLAlchemy(app)

from models import User, FeeRecord

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

@app.route('/dashboard')
def dashboard():
    fee_records = FeeRecord.query.all()
    return render_template('dashboard.html', fee_records=fee_records)

@app.route('/fee_record/create', methods=['POST'])
def create_fee_record():
    data = request.get_json()
    student_id = data.get('student_id')
    amount = data.get('amount')
    user_id = data.get('user_id')  # Assuming you have user_id in the request data

    new_fee_record = FeeRecord(student_id=student_id, amount=amount, user_id=user_id)
    db.session.add(new_fee_record)
    db.session.commit()
    
    return jsonify({'message': 'Fee record created successfully'}), 201

@app.route('/fee_records', methods=['GET'])
def get_fee_records():
    fee_records = FeeRecord.query.all()
    records_list = []
    for record in fee_records:
        records_list.append({
            'id': record.id,
            'student_id': record.student_id,
            'amount': record.amount,
            'date_paid': record.date_paid.strftime('%Y-%m-%d %H:%M:%S'),
            'paid': record.paid
        })
    return jsonify(records_list)

@app.route('/fee_record/update/<int:record_id>', methods=['PUT'])
def update_fee_record(record_id):
    fee_record = FeeRecord.query.get_or_404(record_id)
    data = request.get_json()
    
    # Update fields based on data received
    if 'student_id' in data:
        fee_record.student_id = data['student_id']
    if 'amount' in data:
        fee_record.amount = data['amount']
    # Update more fields as needed

    db.session.commit()
    return jsonify({'message': 'Fee record updated successfully'})

@app.route('/fee_record/delete/<int:record_id>', methods=['DELETE'])
def delete_fee_record(record_id):
    fee_record = FeeRecord.query.get_or_404(record_id)
    db.session.delete(fee_record)
    db.session.commit()
    return jsonify({'message': 'Fee record deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)