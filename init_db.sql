-- ============================================
-- 和平、正义与强大机构 - 数据库初始化脚本
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS peace_justice_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE peace_justice_db;

-- ============================================
-- 用户表
-- ============================================
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 反馈/举报表
-- ============================================
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 清廉指数数据表
-- ============================================
CREATE TABLE cpi_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    score DECIMAL(4,1),
    rank INT,
    INDEX idx_country_year (country, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 法治指数数据表
-- ============================================
CREATE TABLE rule_of_law_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    score DECIMAL(4,1),
    INDEX idx_country_year (country, year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 初始化示例数据
-- ============================================

-- 清廉指数示例数据 (2023)
INSERT INTO cpi_data (country, year, score, rank) VALUES
('丹麦', 2023, 90.0, 1),
('新西兰', 2023, 87.0, 2),
('芬兰', 2023, 85.0, 3),
('挪威', 2023, 84.0, 4),
('新加坡', 2023, 83.0, 5),
('瑞典', 2023, 82.0, 6),
('瑞士', 2023, 81.0, 7),
('荷兰', 2023, 80.0, 8),
('德国', 2023, 79.0, 9),
('加拿大', 2023, 78.0, 10),
('中国', 2023, 45.0, 64),
('俄罗斯', 2023, 26.0, 141),
('印度', 2023, 40.0, 80);

-- 法治指数示例数据 (2023)
INSERT INTO rule_of_law_data (country, year, score) VALUES
('丹麦', 2023, 90.0),
('挪威', 2023, 88.0),
('瑞典', 2023, 87.0),
('芬兰', 2023, 86.0),
('荷兰', 2023, 84.0),
('德国', 2023, 82.0),
('英国', 2023, 80.0),
('法国', 2023, 78.0),
('日本', 2023, 85.0),
('美国', 2023, 75.0),
('中国', 2023, 52.0),
('印度', 2023, 58.0),
('巴西', 2023, 55.0);

-- ============================================
-- 测试用户（密码都是: test123）
-- ============================================
INSERT INTO users (username, email, password_hash) VALUES
('testuser', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X.VQ6fT1eDf3kB3e2');

-- ============================================
-- 显示表结构
-- ============================================
SHOW TABLES;
SELECT '数据库初始化完成！' AS status;
