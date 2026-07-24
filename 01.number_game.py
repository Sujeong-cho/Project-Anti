import random
import streamlit as st

# 1. 페이지 디자인 및 메타데이터 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 2. 커스텀 CSS (모던 그래디언트 및 비주얼 요소)
st.markdown("""
<style>
    .welcome-card {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        padding: 28px;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
    }
    .welcome-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .welcome-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        line-height: 1.5;
    }
    .hint-box {
        padding: 16px 20px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.25rem;
        text-align: center;
        margin: 16px 0;
    }
    .hint-up {
        background-color: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: 1.5px solid rgba(239, 68, 68, 0.4);
    }
    .hint-down {
        background-color: rgba(59, 130, 246, 0.12);
        color: #3b82f6;
        border: 1.5px solid rgba(59, 130, 246, 0.4);
    }
    .hint-success {
        background-color: rgba(34, 197, 94, 0.12);
        color: #22c55e;
        border: 1.5px solid rgba(34, 197, 94, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 (Session State) 관리
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.last_guess = None
    st.session_state.last_result = None
    st.session_state.history = []

if "best_score" not in st.session_state:
    st.session_state.best_score = None

def reset_game():
    """게임 초기화 함수"""
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.last_guess = None
    st.session_state.last_result = None
    st.session_state.history = []

# 4. 상단 웰컴 Banner
st.markdown("""
<div class="welcome-card">
    <div class="welcome-title">안녕하세요! 👋</div>
    <div class="welcome-subtitle">
        1부터 100 사이의 임의의 숫자를 맞춰보세요.<br/>
        시도 횟수를 줄여 최단 횟수 기록에 도전하세요!
    </div>
</div>
""", unsafe_allow_html=True)

# 5. 스토어 및 현황 대시보드 (메트릭)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📊 현재 시도 횟수", value=f"{st.session_state.attempts} 회")
with col2:
    best_disp = f"{st.session_state.best_score} 회" if st.session_state.best_score is not None else "-"
    st.metric(label="🏆 최고 기록 (최저 시도)", value=best_disp)

st.divider()

# 6. 정답 맞추기 폼 & 입력부
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=False):
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            guess = st.number_input(
                "숫자를 입력하세요 (1 ~ 100):",
                min_value=1,
                max_value=100,
                step=1,
                value=50,
                key="guess_input"
            )
        with col_btn:
            st.write("") # 높이 맞춤용 여백
            st.write("")
            submit_button = st.form_submit_button(label="🎯 제출", use_container_width=True)

    if submit_button:
        st.session_state.attempts += 1
        st.session_state.last_guess = guess
        
        if guess < st.session_state.target_number:
            st.session_state.last_result = "UP"
            st.session_state.history.append((guess, "🔥 UP (더 큰 숫자)"))
        elif guess > st.session_state.target_number:
            st.session_state.last_result = "DOWN"
            st.session_state.history.append((guess, "❄️ DOWN (더 작은 숫자)"))
        else:
            st.session_state.last_result = "CORRECT"
            st.session_state.game_over = True
            st.session_state.history.append((guess, "🎉 정답!"))
            
            # 최고 기록 갱신
            if st.session_state.best_score is None or st.session_state.attempts < st.session_state.best_score:
                st.session_state.best_score = st.session_state.attempts

        st.rerun()

# 7. 힌트 메시지 및 결과 알림
if st.session_state.last_result == "UP":
    st.markdown(f'<div class="hint-box hint-up">🔥 UP! {st.session_state.last_guess}보다 더 큰 숫자입니다.</div>', unsafe_allow_html=True)
elif st.session_state.last_result == "DOWN":
    st.markdown(f'<div class="hint-box hint-down">❄️ DOWN! {st.session_state.last_guess}보다 더 작은 숫자입니다.</div>', unsafe_allow_html=True)
elif st.session_state.game_over:
    st.balloons()
    st.markdown(
        f'<div class="hint-box hint-success">🎉 축하합니다! {st.session_state.attempts}번 만에 맞추셨습니다! (정답: {st.session_state.target_number})</div>',
        unsafe_allow_html=True
    )

# 8. 게임 재시작 / 리셋 옵션
if st.session_state.game_over:
    st.markdown("### 🎮 게임이 종료되었습니다")
    st.button("🔄 다시 시도하기", on_click=reset_game, use_container_width=True, type="primary")
else:
    st.button("🔄 게임 초기화", on_click=reset_game, help="현재 진행 상태를 초기화하고 새로운 숫자로 시작합니다.")

# 9. 시도 히스토리
if st.session_state.history:
    st.markdown("---")
    with st.expander("📋 나의 시도 기록 확인", expanded=True):
        for idx, (g, res) in enumerate(reversed(st.session_state.history), start=1):
            attempt_num = len(st.session_state.history) - idx + 1
            st.write(f"**#{attempt_num}번째 시도**: `{g}` → {res}")
