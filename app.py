from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from supabase import create_client, Client
import os

app = Flask(__name__)

# ===================== 核心配置 =====================
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'peace-justice-secret-key-2024')

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://gkbotpktujixjgqgavbn.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'sb_publishable_6ZMIZDkrnRynyi6MVjOU5Q_1jMngjS4')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
bcrypt = Bcrypt(app)

# ===================== 页面路由 =====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/institution')
def institution():
    return render_template('institution.html')

@app.route('/justice')
def justice():
    return render_template('justice.html')

@app.route('/peace')
def peace():
    return render_template('peace.html')

@app.route('/sdg16')
def sdg16():
    return render_template('sdg16.html')

# ===================== 登录注册 =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        response = supabase.table('users').select('*').eq('email', email).execute()
        users = response.data

        if len(users) == 0:
            flash('邮箱或密码错误', 'error')
            return render_template('login.html')

        user = users[0]
        if not bcrypt.check_password_hash(user['password'], password):
            flash('邮箱或密码错误', 'error')
            return render_template('login.html')

        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('登录成功！', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('两次密码不一致', 'error')
            return render_template('register.html')

        # 检查邮箱是否已存在
        response = supabase.table('users').select('id').eq('email', email).execute()
        if len(response.data) > 0:
            flash('该邮箱已被注册', 'error')
            return render_template('register.html')

        # 检查用户名是否已存在
        response = supabase.table('users').select('id').eq('username', username).execute()
        if len(response.data) > 0:
            flash('该用户名已被使用', 'error')
            return render_template('register.html')

        # 创建用户
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        supabase.table('users').insert({
            'username': username,
            'email': email,
            'password': hashed_password
        }).execute()

        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        response = supabase.table('users').select('id').eq('email', email).execute()
        if len(response.data) > 0:
            flash('密码重置链接已发送', 'success')
        else:
            flash('邮箱未注册', 'error')
    return render_template('forgot.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'success')
    return redirect(url_for('index'))

# ===================== 反馈提交 =====================
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    feedback_type = data.get('type')
    content = data.get('content')

    if not all([name, email, feedback_type, content]):
        return jsonify({'success': False, 'message': '请填写所有字段'})

    supabase.table('feedbacks').insert({
        'user_id': session.get('user_id'),
        'name': name,
        'email': email,
        'type': feedback_type,
        'content': content
    }).execute()

    return jsonify({'success': True, 'message': '反馈提交成功'})

# ===================== API 数据 =====================
@app.route('/api/cpi-data')
def get_cpi_data():
    return jsonify({
        'countries': ['丹麦', '新西兰', '芬兰', '挪威', '新加坡'],
        'scores': [90, 87, 85, 84, 83],
        'years': ['2019', '2020', '2021', '2022', '2023']
    })

@app.route('/api/rule-of-law-data')
def get_rule_of_law_data():
    return jsonify({
        'countries': ['丹麦', '挪威', '瑞典', '芬兰', '荷兰'],
        'scores': [90, 88, 87, 86, 84],
        'years': ['2019', '2020', '2021', '2022', '2023']
    })

@app.route('/api/peace-index')
def get_peace_index():
    return jsonify({
        'regions': ['欧洲', '北美', '亚太', '南美', '非洲', '中东'],
        'scores': [85, 82, 78, 65, 55, 45],
        'trend': [83, 84, 82, 85, 84, 86]
    })

@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    return jsonify({
        'peace_index': 2.8,
        'rule_of_law': 85.2,
        'cpi_score': 78.5,
        'feedback_count': 1523,
        'active_projects': 42
    })

# ===================== 启动 =====================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
