# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- CSS 스타일 정의 부분 (변경 없음) ---
# .rule-text-block 클래스는 그대로 사용합니다.
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 */
.stMarkdown .katex-display .katex {
    font-size: 6em;
    margin-top: 0.5em;
}

/* 오른쪽 열의 규칙 설명을 위한 사용자 정의 클래스 스타일 */
.rule-text-block {
    font-size: 4em !important;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

st.title("🔢 유리수 타일 뽑기")
st.divider()

# --- 게임 초기화 로직 등 (변경 없음) ---
def initialize_game_Q():
    number_pool = []
    for i in range(1, 11): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
    for i in range(1, 6): number_pool.append(str(i)); number_pool.append(str(-i))
    number_pool.extend(["\\frac{5}{3}", "-\\frac{5}{3}", "\\frac{4}{3}", "-\\frac{4}{3}", "\\frac{2}{3}", "-\\frac{2}{3}", "\\frac{1}{3}", "-\\frac{1}{3}", "0", "0"])
    random.shuffle(number_pool)
    st.session_state.pool_Q, st.session_state.draw_count_Q, st.session_state.current_number_Q, st.session_state.drawn_history_Q = number_pool, 0, "❔", []

if 'pool_Q' not in st.session_state:
    initialize_game_Q()

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

if st.session_state.draw_count_Q == 0:
    st.header("첫 번째 유리수를 뽑아주세요.")
elif st.session_state.draw_count_Q >= 20:
    st.header("🏁 20개의 유리수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_Q}번째 유리수")

left_col, right_col = st.columns([2, 1])

with left_col:
    if st.session_state.current_number_Q == "❔":
        st.markdown(
            f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Q}</p>", 
            unsafe_allow_html=True
        )
    else:
        st.latex(st.session_state.current_number_Q)

# --- 여기가 최종 핵심 변경점입니다 ---
with right_col:
    # 1. 스타일을 적용할 영역을 시작하는 div 태그를 먼저 삽입합니다.
    st.markdown('<div class="rule-text-block">', unsafe_allow_html=True)

    # "유리수 타일 구성" 텍스트 (이스케이프가 필요 없는 원본 r-string 그대로 사용)
    rule_text = r"""
    ℹ️ **유리수 타일 구성:**
    - $0$ (2개)
    - 절댓값이 $1 \sim 5$ 인 수
    - 절댓값이 $\frac{1}{2} \sim \frac{10}{2}$ 인 수
    - 절댓값이 $\frac{1}{3}, \frac{2}{3}, \frac{4}{3}, \frac{5}{3}$ 인 수
    """
    
    # 2. st.write를 사용하여 내용을 출력합니다.
    #    이제 Streamlit이 이 내용을 올바르게 파싱하여 수식을 예쁘게 렌더링합니다.
    st.write(rule_text)

    # 3. 위에서 열어두었던 div 태그를 닫아 스타일 적용 범위를 끝냅니다.
    st.markdown('</div>', unsafe_allow_html=True)


st.divider() 

history_title = "**※ 지금까지 뽑은 유리수들:**"

if st.session_state.drawn_history_Q:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유리수가 없습니다."

st.info(f"{history_title} {history_values}")