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

    /* ===== Streamlit 기본 UI 제거 ===== */
    #MainMenu, header, footer { visibility: hidden !important; }
    [data-testid="stToolbar"], [data-testid="stHeader"], [data-testid="stDecoration"], .stDeployButton { display: none !important; }
    [data-testid="stHeaderActionElements"] { display: none !important; }
    .stHeadingContainer a, [data-testid="stHeading"] a, h1 a, h2 a, h3 a, h4 a { display: none !important; }

    /* ===== 전체 배경 ===== */
    .stApp, [data-testid="stAppViewContainer"] {
        background: #f5f0e1 !important;
        background-image:
            radial-gradient(at 10% 20%, rgba(180, 140, 90, 0.1) 0px, transparent 50%),
            radial-gradient(at 90% 80%, rgba(120, 80, 50, 0.08) 0px, transparent 50%) !important;
    }
    .stApp, .stApp *, [data-testid="stAppViewContainer"] * {
        font-family: 'Gowun Batang', 'Nanum Myeongjo', serif !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 720px !important;
    }

    /* ===== 헤더 박스 (한자 + 제목 + 부제 한 묶음) ===== */
    .vintage-header {
        text-align: center;
        padding: 24px 0;
        margin-bottom: 32px;
        border-top: 3px double #8b5a3c;
        border-bottom: 3px double #8b5a3c;
    }
    .vintage-label {
        display: inline-block;
        padding: 6px 20px;
        background: #3d2817;
        color: #f5f0e1 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 6px;
        margin-bottom: 16px;
    }
    .vintage-title {
        font-family: 'Nanum Myeongjo', serif !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        color: #3d2817 !important;
        letter-spacing: 8px !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    .vintage-subtitle {
        color: #8b5a3c !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 0.95rem !important;
        margin: 8px 0 0 0 !important;
        letter-spacing: 4px;
    }

    /* ===== 탭 ===== */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center !important;
        gap: 32px !important;
        background: transparent !important;
        border-bottom: 1px solid #c9a875 !important;
        padding: 0 0 4px 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #8b5a3c !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        letter-spacing: 3px !important;
        padding: 14px 24px !important;
        height: auto !important;
    }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] div {
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3d2817 !important;
        border-bottom: 3px solid #8b5a3c !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { background: transparent !important; display: none !important; }
    .stTabs [data-baseweb="tab-border"] { background: transparent !important; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

    /* ===== 버튼 ===== */
    .stButton > button,
    .stFormSubmitButton > button,
    button[kind="primary"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-primaryFormSubmit"] {
        background: #3d2817 !important;
        color: #f5f0e1 !important;
        border: 2px solid #3d2817 !important;
        border-radius: 0 !important;
        padding: 18px !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: 8px !important;
        transition: background 0.2s, border-color 0.2s !important;
        box-shadow: none !important;
    }
    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-primaryFormSubmit"]:hover {
        background: #5d3a23 !important;
        border-color: #5d3a23 !important;
        color: #f5f0e1 !important;
    }
    .stButton > button p, .stFormSubmitButton > button p {
        font-family: 'Nanum Myeongjo', serif !important;
        letter-spacing: 8px !important;
        margin: 0 !important;
    }

    /* ===== 운세 카드 ===== */
    .fortune-card {
        margin-top: 32px;
        background: #fffbf0;
        background-image:
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(139,90,60,0.03) 35px, rgba(139,90,60,0.03) 36px);
        padding: 56px 32px 64px 32px;
        text-align: center;
        border: 1px solid #c9a875;
        box-shadow:
            0 1px 0 #e6dab8,
            0 4px 12px rgba(139,90,60,0.15),
            inset 0 0 60px rgba(139,90,60,0.04);
        position: relative;
    }
    .fortune-card .deco-top,
    .fortune-card .deco-bottom {
        color: #8b5a3c;
        font-size: 1.5rem;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
    }
    .fortune-card .deco-top { top: 16px; }
    .fortune-card .deco-bottom { bottom: 16px; }
    .fortune-text {
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 1.7rem !important;
        line-height: 2 !important;
        color: #3d2817 !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        margin: 0 !important;
    }
    .fortune-id {
        color: #8b5a3c !important;
        font-size: 0.85rem !important;
        margin-top: 24px !important;
        margin-bottom: 0 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        letter-spacing: 4px !important;
    }

    /* ===== 운세 목록 ===== */
    .list-card {
        background: #fffbf0;
        border: 1px solid #c9a875;
        padding: 16px 24px;
        margin: 8px 0;
        font-family: 'Nanum Myeongjo', serif !important;
        font-size: 1.15rem;
        color: #3d2817;
        font-weight: 500;
        letter-spacing: 1px;
        box-shadow: 0 1px 0 #e6dab8;
    }

    /* ===== 운세 추가 안내 텍스트 ===== */
    .stMarkdown p {
        color: #5d3a23 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        letter-spacing: 1px;
    }

    /* ===== input/textarea ===== */
    .stTextInput input,
    .stTextArea textarea {
        background: #fffbf0 !important;
        border: 1px solid #c9a875 !important;
        border-radius: 0 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        color: #3d2817 !important;
        letter-spacing: 1px !important;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #8b5a3c !important;
        box-shadow: 0 0 0 2px rgba(139,90,60,0.2) !important;
        outline: none !important;
    }
    .stTextArea label, .stTextInput label,
    .stTextArea label p, .stTextInput label p {
        color: #3d2817 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
    }

    /* ===== alert (success, warning, error) ===== */
    [data-testid="stAlert"] {
        border-radius: 0 !important;
        background: #fffbf0 !important;
        border: 1px solid #c9a875 !important;
        font-family: 'Nanum Myeongjo', serif !important;
        color: #3d2817 !important;
        letter-spacing: 1px;
    }
    [data-testid="stAlert"] * {
        color: #3d2817 !important;
        font-family: 'Nanum Myeongjo', serif !important;
    }

    /* ===== 폼 컨테이너 ===== */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    /* ===== 일반 텍스트 색 ===== */
    .stApp, .stMarkdown, .stMarkdown div, .stMarkdown span {
        color: #3d2817;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 헤더 박스 (한자 + 제목 + 부제)
st.markdown(
    """
    <div class="vintage-header">
        <span class="vintage-label">運勢</span>
        <h1 class="vintage-title">오늘의 운세</h1>
        <p class="vintage-subtitle">RDS · WEEK 9</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["운세 뽑기", "운세 추가", "전체 목록"])

# --- 탭 1: 운세 뽑기 ---
with tab1:
    if st.button("운세 뽑기", type="primary", use_container_width=True, key="draw"):
        try:
            fortune = fetch_random_fortune()
            if fortune:
                st.markdown(
                    f"""
                    <div class="fortune-card">
                        <span class="deco-top">※</span>
                        <p class="fortune-text">{fortune['text']}</p>
                        <p class="fortune-id">FORTUNE NO. {fortune['id']:02d}</p>
                        <span class="deco-bottom">※</span>
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
    st.write("내 DB에 새 운세를 추가하면 '운세 뽑기'에서도 나올 수 있어요")
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
        st.write(f"DB에 저장된 운세: {len(fortunes)}개")
        for f in fortunes:
            st.markdown(
                f'<div class="list-card">{f["text"]}</div>',
                unsafe_allow_html=True,
            )
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
