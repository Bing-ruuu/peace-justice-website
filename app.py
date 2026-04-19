from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

# ===================== 核心配置（直接写在这里，不依赖外部文件）=====================
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-test')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库和加密
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ===================== 用户模型 =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# ===================== 反馈模型 =====================
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

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
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('邮箱或密码错误', 'error')

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

        if User.query.filter_by(email=email).first():
            flash('该邮箱已被注册', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('该用户名已被使用', 'error')
            return render_template('register.html')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
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

    new_feedback = Feedback(
        user_id=session.get('user_id'),
        name=name,
        email=email,
        type=feedback_type,
        content=content
    )
    db.session.add(new_feedback)
    db.session.commit()
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
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)