import sys
import os
import pytest
from app import app, db,User,bcrypt

# مسیر پروژه
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), r'F:\AI\VScode\MLops_class\Ex_Mlops\EX15_MLFLOW_CICD\CICD')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['SECRET_KEY'] = 'secret'

    with app.app_context():
        db.create_all()

        # ایجاد کاربر تست با رمز عبور هش شده
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        test_user = User(username='testuser', password=hashed_password)
        db.session.add(test_user)
        db.session.commit()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()
    # پاک‌سازی بعد از تست
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_register(client):
    response = client.post('/register', data=dict(username='testuser', password='password'))
    assert response.status_code in [200, 302]  # وضعیت ممکن

def test_login(client):
    response = client.post('/login', data=dict(username='testuser', password='password'))
    assert response.status_code in [200, 302]
    
def test_input_data(client):
    response = client.get('/input')
    assert response.status_code in [200, 302]

def test_history(client):
    client.post('/login', data=dict(username='testuser', password='password'))
    response = client.get('/history')
    assert response.status_code in [200, 302]

def test_logout(client):
    client.post('/login', data=dict(username='testuser', password='password'))
    
def test_login_fail(client): 
  response = client.get('/logout')
  assert response.status_code in [200, 302]
