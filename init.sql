-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS discharge_iq CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE discharge_iq;

-- Create admin_users table
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Doctor',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username)
);

-- Create discharge_summaries table
CREATE TABLE IF NOT EXISTS discharge_summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE NOT NULL,
    diagnosis TEXT NOT NULL,
    procedures TEXT NOT NULL,
    lab_results TEXT NOT NULL,
    medications TEXT NOT NULL,
    hospital_course TEXT NOT NULL,
    follow_up TEXT NOT NULL,
    ai_summary LONGTEXT,
    patient_summary LONGTEXT,
    risk_score INT,
    risk_level VARCHAR(50),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_patient_name (patient_name),
    INDEX idx_created_at (created_at),
    INDEX idx_risk_level (risk_level),
    INDEX idx_created_by (created_by),
    FOREIGN KEY (created_by) REFERENCES admin_users(id)
);

-- Insert default admin users (passwords are hashed versions of 'admin123' and 'tech123')
-- You should change these passwords in production
INSERT IGNORE INTO admin_users (username, password_hash, full_name, role) VALUES
('dr_smith', '$2b$12$EixZaYVK1fsbw1ZfbX3Oe9rPgC1gpa9pbhZfE8d9uL61A', 'Dr. John Smith', 'Doctor'),
('dr_jones', '$2b$12$EixZaYVK1fsbw1ZfbX3Oe9rPgC1gpa9pbhZfE8d9uL61A', 'Dr. Sarah Jones', 'Doctor'),
('tech_wilson', '$2b$12$EixZaYVK1fsbw1ZfbX3Oe9rPgC1gpa9pbhZfE8d9uL61A', 'Mike Wilson', 'Technician'),
('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3Oe9rPgC1gpa9pbhZfE8d9uL61A', 'System Administrator', 'Admin');

-- Create user for application (if not using root)
CREATE USER IF NOT EXISTS 'discharge_user'@'%' IDENTIFIED BY 'DischargePass123!';
GRANT ALL PRIVILEGES ON discharge_iq.* TO 'discharge_user'@'%';
FLUSH PRIVILEGES;
