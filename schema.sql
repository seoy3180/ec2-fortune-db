-- fortunes 테이블 생성
-- emoji + 운세 메시지를 저장 (이모지 지원을 위해 utf8mb4 사용)
CREATE DATABASE IF NOT EXISTS fortunes
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE fortunes;

CREATE TABLE IF NOT EXISTS fortunes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emoji VARCHAR(10) NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
