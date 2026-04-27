"""
오늘의 운세 (DB 버전)

7주차에는 운세가 코드(server.js)에 하드코딩되어 있었지만,
9주차에는 운세 데이터가 RDS MySQL에서 옵니다.

주요 기능:
1. 운세 뽑기 — DB에서 랜덤으로 1개 SELECT
2. 운세 추가 — 사용자가 입력한 운세를 DB에 INSERT
"""

import os
from dotenv import load_dotenv
import mysql.connector
import streamlit as st

# .env 파일에서 DB 접속 정보 로드
load_dotenv()


def get_connection():
    """RDS MySQL 연결 생성"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def fetch_random_fortune():
    """DB에서 랜덤으로 운세 1개 가져오기"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, text FROM fortunes ORDER BY RAND() LIMIT 1")
    fortune = cursor.fetchone()
    cursor.close()
    conn.close()
    return fortune


def fetch_all_fortunes():
    """DB에 저장된 모든 운세 가져오기 (최신순)"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, text, created_at FROM fortunes ORDER BY id DESC")
    fortunes = cursor.fetchall()
    cursor.close()
    conn.close()
    return fortunes


def insert_fortune(text: str):
    """새 운세를 DB에 저장"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fortunes (text) VALUES (%s)",
        (text,),
    )
    conn.commit()
    cursor.close()
    conn.close()


# ===== Streamlit UI =====
st.set_page_config(page_title="오늘의 운세", layout="centered")

st.title("오늘의 운세")
st.caption("운세 데이터는 RDS MySQL에서 옵니다.")

tab1, tab2, tab3 = st.tabs(["운세 뽑기", "운세 추가하기", "전체 운세 목록"])

# --- 탭 1: 운세 뽑기 ---
with tab1:
    if st.button("운세 뽑기", type="primary", use_container_width=True):
        try:
            fortune = fetch_random_fortune()
            if fortune:
                st.markdown(f"## {fortune['text']}")
                st.caption(f"운세 ID: {fortune['id']}")
            else:
                st.warning("DB에 운세가 없습니다. '운세 추가하기' 탭에서 먼저 추가해주세요.")
        except mysql.connector.Error as e:
            st.error(f"DB 연결 실패: {e}")

# --- 탭 2: 운세 추가 ---
with tab2:
    st.write("새로운 운세를 추가하면 다른 사람도 뽑을 수 있어요!")
    with st.form("add_fortune_form", clear_on_submit=True):
        text = st.text_area("운세 메시지", placeholder="예: 오늘은 새로운 시작에 좋은 날입니다")
        submitted = st.form_submit_button("DB에 저장", type="primary")

        if submitted:
            if not text:
                st.warning("운세 메시지를 입력해주세요.")
            else:
                try:
                    insert_fortune(text.strip())
                    st.success("운세가 DB에 저장되었습니다!")
                    st.balloons()
                except mysql.connector.Error as e:
                    st.error(f"저장 실패: {e}")

# --- 탭 3: 전체 운세 목록 ---
with tab3:
    try:
        fortunes = fetch_all_fortunes()
        st.write(f"DB에 저장된 운세: **{len(fortunes)}개**")
        for f in fortunes:
            st.markdown(f"- {f['text']}")
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
