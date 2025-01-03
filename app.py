from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from model import predict_class
import json

app = Flask(__name__, template_folder='templates')

# App configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = ';aksdjf;kjkj;kj'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


# Ensure tables are created
with app.app_context():
    db.create_all()


def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('input_data'))
        else:
            flash('Login failed. Check your username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username')
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/input', methods=['GET', 'POST'])
@login_required
def input_data():
    app.logger.info("Received request: %s", request.json)
    if request.method == 'POST':
        try:
            if request.is_json:
                features = request.json.get('features')
            else:
                features = [
                    float(request.form[field])
                    for field in [
                        'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness',
                        'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry',
                        'mean fractal dimension', 'radius error', 'texture error', 'perimeter error',
                        'area error', 'smoothness error', 'compactness error', 'concavity error',
                        'concave points error', 'symmetry error', 'fractal dimension error',
                        'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness',
                        'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry',
                        'worst fractal dimension'
                    ]
                ]

            predicted_class = predict_class(features)

            # Get current user
            user = User.query.filter_by(username=session['username']).first()
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('login'))

            # Store prediction in database
            input_data = json.dumps(request.form.to_dict() if not request.is_json else {"features": features})
            result_text = "Benign" if predicted_class == 0 else "Malignant"
            new_prediction = Prediction(user_id=user.id, input_data=input_data, result=result_text)
            db.session.add(new_prediction)
            db.session.commit()

            return jsonify({"Diagnosis": result_text, "features": features}) if request.is_json else render_template('result.html', Diagnosis=result_text)
        except ValueError:
            flash('Invalid input values. Please check your data.', 'danger')
            return redirect(url_for('input_data'))

    return render_template('input.html')


@app.route('/history')
@login_required
def history():
    user = User.query.filter_by(username=session['username']).first()
    if user:
        predictions = user.predictions
        return render_template('history.html', predictions=predictions)
    return redirect(url_for('login'))


@app.route('/result')
@login_required
def result():
    return render_template('result.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
