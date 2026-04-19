# 和平、正义与强大机构 网站项目

## 项目概述

一个围绕"和平、正义与强大机构"主题的动态交互网站，包含用户认证系统、反馈表单、数据可视化等功能。

## 技术栈

- **前端**: HTML5, Tailwind CSS, JavaScript, ECharts
- **后端**: Python Flask
- **数据库**: MySQL
- **依赖**: Flask-SQLAlchemy, Flask-Bcrypt

## 项目结构

```
peace_justice_website/
├── app.py                 # Flask主应用
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── init_db.sql           # 数据库初始化脚本
├── templates/            # HTML模板
│   ├── base.html         # 母版
│   ├── index.html        # 首页
│   ├── peace.html        # 和平视界
│   ├── justice.html      # 正义天平
│   ├── institution.html  # 透明机构
│   ├── sdg16.html        # SDG16介绍
│   ├── login.html        # 登录
│   ├── register.html     # 注册
│   └── forgot.html       # 忘记密码
└── models/              # 数据模型
    ├── user.py
    └── feedback.py
```

## 快速运行

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+ 或 MySQL 8.0+

### 2. 安装依赖

```bash
cd peace_justice_website
pip install -r requirements.txt
```

### 3. 配置数据库

编辑 `config.py` 中的数据库连接配置:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://用户名:密码@localhost/peace_justice_db'
```

### 4. 初始化数据库

```bash
# 登录MySQL
mysql -u root -p

# 执行初始化脚本
source init_db.sql
```

### 5. 启动应用

```bash
python app.py
```

访问 http://localhost:5000

## 测试账号

| 用户名 | 邮箱 | 密码 |
|--------|------|------|
| testuser | test@example.com | test123 |

## 功能清单

### 用户系统
- [x] 用户注册
- [x] 用户登录
- [x] 会话保持
- [x] 忘记密码
- [x] 退出登录

### 页面功能
- [x] 首页 - 三大模块入口、数据概览、最新动态
- [x] 和平视界 - 和平指数可视化、项目分布
- [x] 正义天平 - 法治指数、时间线、法律援助
- [x] 透明机构 - 清廉指数、反腐动态、反馈表单
- [x] SDG16 - 目标介绍、行动倡议

### 数据可视化
- [x] ECharts 柱状图
- [x] ECharts 折线图
- [x] ECharts 雷达图

### API接口
- `/api/cpi-data` - 清廉指数数据
- `/api/rule-of-law-data` - 法治指数数据
- `/api/peace-index` - 和平指数数据
- `/api/dashboard-stats` - 仪表盘统计数据
- `/submit-feedback` - 反馈提交

## 页面截图预览

项目包含5个核心页面 + 3个认证页面，共8个完整页面。

## 开发说明

- 前端使用 Tailwind CSS CDN，无需构建
- ECharts 通过 CDN 引入
- Flask-SQLAlchemy 自动创建表结构
- 密码使用 Bcrypt 加密存储

## 注意事项

1. 首次运行会自动创建数据库表
2. 确保MySQL服务正在运行
3. 反馈表单需要登录后才能提交（如需）
4. 数据库需要支持utf8mb4编码
