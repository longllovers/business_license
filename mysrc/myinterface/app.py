from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from apirequest import api_request

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session加密

# 配置上传文件存储路径
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'jfif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 用户数据文件路径
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'admin': {'password': generate_password_hash('password123'), 'created_at': '2024-01-01'}}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# 初始化用户数据
users = load_users()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            flash('用户名已存在！', 'error')
        elif len(username) < 3:
            flash('用户名长度必须大于3个字符！', 'error')
        elif len(password) < 6:
            flash('密码长度必须大于6个字符！', 'error')
        elif password != confirm_password:
            flash('两次输入的密码不一致！', 'error')
        else:
            from datetime import datetime
            users[username] = {
                'password': generate_password_hash(password),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_users(users)
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('已成功退出登录！', 'success')
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return jsonify({'error': '请先登录！'})

    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件！'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件！'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # 调用识别API
            result = api_request(filepath)
            # 删除临时文件
            os.remove(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return jsonify({'error': '不支持的文件类型！'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5000)