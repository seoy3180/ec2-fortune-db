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

# 빈티지 페이퍼 테마 CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Gowun+Batang:wght@400;700&display=swap');

    /* Streamlit 기본 UI 숨기기 */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    .stDeployButton { display: none; }

    /* 헤더 옆 앵커 링크 숨기기 */
    [data-testid="stHeaderActionElements"] { display: none !important; }
    .stHeadingContainer a,
    [data-testid="stHeading"] a,
    h1 a, h2 a, h3 a, h4 a {
        display: none !important;
    }

    /* 전체 배경 */
    .stApp {
        background: #f5f0e1;
        background-image:
            radial-gradient(at 10% 20%, rgba(180, 140, 90, 0.1) 0px, transparent 50%),
            radial-gradient(at 90% 80%, rgba(120, 80, 50, 0.08) 0px, transparent 50%);
        font-family: 'Gowun Batang', 'Nanum Myeongjo', serif;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }

    /* 헤더 영역 */
    .stApp h1,
    [data-testid="stHeading"] h1,
    .stMarkdown h1 {
        font-family: 'Nanum Myeongjo', serif !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        color: #3d2817 !important;
        text-align: center !important;
        letter-spacing: 8px !important;
        padding: 24px 0 8px 0 !important;
        border-top: 3px double #8b5a3c !important;
    }

    /* caption */
    [data-testid="stCaptionContainer"] {
        text-align: center;
        color: #8b5a3c !important;
        letter-spacing: 4px;
        padding-bottom: 24px;
        border-bottom: 3px double #8b5a3c;
        margin-bottom: 32px;
    }

    /* 탭 */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 32px;
        background: transparent;
        border-bottom: 1px solid #c9a875;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #8b5a3c !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 2px;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #3d2817 !important;
        border-bottom: 3px solid #8b5a3c !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }

    /* 버튼 */
    .stButton > button, .stFormSubmitButton > button {
        background: #3d2817 !important;
        color: #f5f0e1 !important;
        border: 2px solid #3d2817 !important;
        border-radius: 0 !important;
        padding: 18px !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 8px !important;
        transition: background 0.2s, border-color 0.2s !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: #5d3a23 !important;
        border-color: #5d3a23 !important;
        color: #f5f0e1 !important;
    }

    /* 운세 카드 */
    .fortune-card {
        margin-top: 32px;
        background: #fffbf0;
        background-image:
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(139,90,60,0.03) 35px, rgba(139,90,60,0.03) 36px);
        padding: 56px 32px;
        text-align: center;
        border: 1px solid #c9a875;
        box-shadow:
            0 1px 0 #e6dab8,
            0 4px 12px rgba(139,90,60,0.15),
            inset 0 0 60px rgba(139,90,60,0.04);
        position: relative;
    }
    .fortune-card::before, .fortune-card::after {
        content: '※';
        color: #8b5a3c;
        font-size: 1.5rem;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
    }
    .fortune-card::before { top: 16px; }
    .fortune-card::after { bottom: 16px; }
    .fortune-text {
        font-family: 'Nanum Myeongjo', serif;
        font-size: 1.7rem;
        line-height: 2;
        color: #3d2817;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
    }
    .fortune-id {
        color: #8b5a3c;
        font-size: 0.85rem;
        margin-top: 24px;
        font-family: 'Nanum Myeongjo', serif;
        letter-spacing: 4px;
    }

    /* 운세 목록 */
    .list-card {
        background: #fffbf0;
        border: 1px solid #c9a875;
        padding: 16px 24px;
        margin: 8px 0;
        font-family: 'Nanum Myeongjo', serif;
        font-size: 1.15rem;
        color: #3d2817;
        font-weight: 500;
        letter-spacing: 1px;
    }

    /* 운세 추가 폼 안내 텍스트 */
    .stMarkdown p {
        color: #5d3a23;
        font-family: 'Nanum Myeongjo', serif;
        letter-spacing: 1px;
    }

    /* input/textarea */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: #fffbf0 !important;
        border: 1px solid #c9a875 !important;
        border-radius: 0 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        color: #3d2817 !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #8b5a3c !important;
        box-shadow: 0 0 0 2px rgba(139,90,60,0.2) !important;
    }
    .stTextArea label, .stTextInput label {
        color: #3d2817 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
    }

    /* alert */
    .stAlert { border-radius: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 한자 라벨
st.markdown(
    '<div style="text-align: center; margin-bottom: -16px;">'
    '<span style="display: inline-block; padding: 4px 16px; background: #3d2817; color: #f5f0e1; '
    'font-family: \'Nanum Myeongjo\', serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 4px;">運勢</span>'
    '</div>',
    unsafe_allow_html=True,
)

st.title("오늘의 운세")
st.caption("RDS · WEEK 9")

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
                        <p class="fortune-id">FORTUNE NO. {fortune['id']:02d}</p>
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
    st.write("새로운 운세를 추가하면 다른 사람도 뽑을 수 있어요")
    with st.form("add_fortune_form", clear_on_submit=True):
        text = st.text_area("운세 메시지", placeholder="예: 오늘은 새로운 시작에 좋은 날입니다")
        submitted = st.form_submit_button("DB에 저장", type="primary", use_container_width=True)

        if submitted:
            if not text:
                st.warning("운세 메시지를 입력해주세요.")
            else:
                try:
                    insert_fortune(text.strip())
                    st.success("운세가 DB에 저장되었습니다.")
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
