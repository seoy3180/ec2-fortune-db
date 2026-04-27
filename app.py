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

# 커스텀 CSS - 분홍 파스텔 톤
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap');

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 50%, #f48fb1 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 메인 컨텐츠 영역 */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }

    /* 제목 */
    h1 {
        font-family: 'Gaegu', cursive !important;
        color: #880e4f !important;
        text-align: center;
        font-size: 3rem !important;
        letter-spacing: 2px;
        margin-bottom: 0.5rem !important;
    }

    /* 부제목 (caption) */
    .stCaption, [data-testid="stCaptionContainer"] {
        text-align: center;
        color: #ad1457 !important;
    }

    /* 탭 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        background: rgba(255,255,255,0.5);
        border-radius: 16px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #880e4f;
        font-weight: 600;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: #fff !important;
        color: #c2185b !important;
        box-shadow: 0 4px 12px rgba(244,143,177,0.3);
    }

    /* 버튼 */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #ec407a 0%, #c2185b 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 6px 20px rgba(194,24,91,0.3) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 24px rgba(194,24,91,0.4) !important;
    }

    /* 운세 결과 카드 */
    .fortune-card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 40px 32px;
        margin: 24px 0;
        text-align: center;
        box-shadow: 0 20px 60px rgba(244,143,177,0.3);
        animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fortune-text {
        font-family: 'Gaegu', cursive;
        font-size: 1.8rem;
        color: #880e4f;
        line-height: 1.5;
        margin: 0;
    }
    .fortune-id {
        font-size: 0.85rem;
        color: #ad1457;
        margin-top: 12px;
    }

    /* 운세 목록 카드 */
    .list-card {
        background: rgba(255,255,255,0.7);
        border-radius: 16px;
        padding: 14px 20px;
        margin: 8px 0;
        font-family: 'Gaegu', cursive;
        font-size: 1.2rem;
        color: #6a1b3e;
        box-shadow: 0 4px 12px rgba(244,143,177,0.15);
    }

    /* input/textarea */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #f8bbd0 !important;
        background: rgba(255,255,255,0.8) !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #ec407a !important;
        box-shadow: 0 0 0 3px rgba(236,64,122,0.15) !important;
    }

    /* alert (success, warning, error) */
    .stAlert {
        border-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("오늘의 운세")
st.caption("운세 데이터는 RDS MySQL에서 옵니다")

tab1, tab2, tab3 = st.tabs(["운세 뽑기", "운세 추가하기", "전체 운세 목록"])

# --- 탭 1: 운세 뽑기 ---
with tab1:
    if st.button("운세 뽑기", type="primary", use_container_width=True, key="draw"):
        try:
            fortune = fetch_random_fortune()
            if fortune:
                st.markdown(
                    f"""
                    <div class="fortune-card">
                        <p class="fortune-text">{fortune['text']}</p>
                        <p class="fortune-id">운세 ID #{fortune['id']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("DB에 운세가 없습니다. '운세 추가하기' 탭에서 먼저 추가해주세요.")
        except mysql.connector.Error as e:
            st.error(f"DB 연결 실패: {e}")

# --- 탭 2: 운세 추가 ---
with tab2:
    st.write("새로운 운세를 추가하면 다른 사람도 뽑을 수 있어요!")
    with st.form("add_fortune_form", clear_on_submit=True):
        text = st.text_area("운세 메시지", placeholder="예: 오늘은 새로운 시작에 좋은 날입니다")
        submitted = st.form_submit_button("DB에 저장", type="primary", use_container_width=True)

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
            st.markdown(
                f'<div class="list-card">{f["text"]}</div>',
                unsafe_allow_html=True,
            )
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
