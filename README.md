# EC2 Fortune DB

연성대 9주차 실습용 — Streamlit + RDS MySQL 운세 앱

7주차 `ec2-fortune` 의 운세 데이터를 코드에서 분리하여 RDS MySQL에서 조회하도록 변경한 버전입니다.

## 구성

- `app.py` — Streamlit 앱 (운세 뽑기 / 운세 추가 / 전체 목록)
- `schema.sql` — fortunes 테이블 생성 DDL
- `seed.sql` — 초기 운세 10개 INSERT
- `requirements.txt` — Python 의존성
- `.env.example` — DB 접속 정보 템플릿

## 실행 방법

### 1. RDS에 스키마 + 데이터 적용

```bash
mysql -h <RDS-엔드포인트> -u admin -p < schema.sql
mysql -h <RDS-엔드포인트> -u admin -p < seed.sql
```

### 2. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. `.env` 파일 작성

`.env.example` 을 복사해서 `.env` 로 만들고 본인 RDS 정보 입력:

```bash
cp .env.example .env
# .env 파일 열어서 DB_HOST, DB_PASSWORD 수정
```

### 4. Streamlit 실행

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

브라우저에서 `http://<EC2 퍼블릭IP>:8501` 접속.

## 기능

| 탭 | 설명 |
|----|------|
| 운세 뽑기 | DB에서 랜덤 운세 1개 SELECT |
| 운세 추가하기 | 새 운세를 DB에 INSERT |
| 전체 운세 목록 | DB에 저장된 모든 운세 조회 |
