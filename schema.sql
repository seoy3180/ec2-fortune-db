-- fortunes 테이블 생성
-- emoji + 운세 메시지를 저장
CREATE DATABASE IF NOT EXISTS fortunes;
USE fortunes;

CREATE TABLE IF NOT EXISTS fortunes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emoji VARCHAR(10) NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
