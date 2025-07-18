# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# 유리수 latex를 키우기 위한 CSS문법 추가
st.markdown("""
<style>
.stMarkdown .katex-display .katex {
    font-size: 6em;
    margin-top: 0.5em;
}
[data-testid="stAlertContainer"] .katex {
    font-size: 1.5em; /* 크기를 더 키웠습니다. 이 값을 1.8, 2.0 등으로 조절하세요. */
}
</style>
""", unsafe_allow_html=True)

st.title("🔢 유리수 타일 뽑기")
st.divider()

# --- '유리수 버전'만의 고유한 게임 초기화 함수 ---
def initialize_game_Q():
    """'유리수 버전'을 위한 게임 상태를 초기화합니다."""
    number_pool = []
    for i in range(1, 11): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
    for i in range(1, 6): number_pool.append(str(i)); number_pool.append(str(-i))
    number_pool.extend(["\\frac{5}{3}", "-\\frac{5}{3}", "\\frac{4}{3}", "-\\frac{4}{3}", "\\frac{2}{3}", "-\\frac{2}{3}", "\\frac{1}{3}", "-\\frac{1}{3}", "0", "0"])
    random.shuffle(number_pool)
    st.session_state.pool_Q, st.session_state.draw_count_Q, st.session_state.current_number_Q, st.session_state.drawn_history_Q = number_pool, 0, "❔", []

# --- 메인 앱 로직 ---
if 'pool_Q' not in st.session_state:
    initialize_game_Q()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_Q"):
        initialize_game_Q()
        st.rerun()

with col2:
    is_disabled = (st.session_state.draw_count_Q >= 20)
    
    if st.button("다음 유리수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Q"):
        if st.session_state.pool_Q:
            st.session_state.draw_count_Q += 1
            new_number = st.session_state.pool_Q.pop()
            st.session_state.current_number_Q = new_number
            st.session_state.drawn_history_Q.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count_Q == 0:
    st.header("첫 번째 유리수를 뽑아주세요.")
elif st.session_state.draw_count_Q >= 20:
    st.header("🏁 20개의 유리수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_Q}번째 유리수")

left_col, right_col = st.columns([2, 1])

# 왼쪽 컬럼: 뽑힌 숫자
with left_col:
    if st.session_state.current_number_Q == "❔":
        st.markdown(
            f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Q}</p>", 
            unsafe_allow_html=True
        )
    else:
        st.latex(st.session_state.current_number_Q)

# --- 여기가 핵심 변경점입니다 ---
# 오른쪽 컬럼: 규칙 설명 (올바른 문법으로 수정)
with right_col:
    rule_text = r"""
    ℹ️ **유리수 타일 구성:**
    - $0$ (2개)
    - 절댓값이 $1 \sim 5$ 인 수
    - 절댓값이 $\frac{1}{2} \sim \frac{10}{2}$ 인 수
    - 절댓값이 $\frac{1}{3}, \frac{2}{3}, \frac{4}{3}, \frac{5}{3}$ 인 수
    """
    st.markdown(rule_text)

# --- 뽑은 기록을 정보 상자에 담아 표시 ---
st.divider() 

history_title = "**※ 지금까지 뽑은 유리수들:**"

if st.session_state.drawn_history_Q:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유리수가 없습니다."

st.info(f"{history_title} {history_values}")