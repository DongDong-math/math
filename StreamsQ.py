import streamlit as st
import random
from StreamsSideBar import Draw_sidebar  # 사이드바를 그리는 함수를 임포트
Draw_sidebar()

st.title("🔢 유리수 스트림스 카드 뽑기")
# --- 구분선 ---
st.divider()

# --- 게임 초기화 함수 ---
def initialize_game():
    """스트림스 게임에 필요한 숫자 풀과 상태 변수들을 초기화합니다."""
    number_pool = []
    number_pool.extend(list(range(1, 11)))
    number_pool.extend(list(range(11, 21)))
    number_pool.extend(list(range(11, 21)))
    number_pool.extend(list(range(21, 31)))
    random.shuffle(number_pool)
    
    st.session_state.pool_Z = number_pool
    st.session_state.draw_count_Z = 0
    st.session_state.current_number_Z = "❔"
    st.session_state.drawn_history_Z = []

# --- 메인 앱 로직 ---
if 'pool' not in st.session_state:
    initialize_game()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary",use_container_width=True):
        initialize_game()
        st.rerun()

with col2:
    is_disabled = (st.session_state.draw_count_Z >= 20)
    if st.button("다음 수 뽑기", disabled=is_disabled, use_container_width=True):
        if st.session_state.pool_Z:
            st.session_state.draw_count_Z += 1
            new_number = st.session_state.pool_Z.pop()
            st.session_state.current_number_Z = new_number
            st.session_state.drawn_history_Z.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count_Z == 0:
    st.header("첫 번째 수를 뽑아주세요.")
elif st.session_state.draw_count_Z >= 20:
    st.header("🏁 수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_Z}번째 수")

st.markdown(
    f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Z}</p>", 
    unsafe_allow_html=True
)

st.divider()

# *** 여기가 핵심 변경점입니다: 규칙과 기록을 하나의 정보 상자에 통합 ***

# 1. 정보 상자에 들어갈 각 부분의 텍스트를 정의합니다.
rule_text = "ℹ️ **수 타일 구성:** 1 ~ 10 (각 1개), 11 ~ 20 (각 2개), 21 ~ 30 (각 1개)"
history_title = "**※ 지금까지 뽑은 수들:**"

# 2. 뽑은 기록이 있을 때와 없을 때를 구분하여 텍스트를 준비합니다.
if st.session_state.drawn_history_Z:
    history_values = "  ➡️  ".join(map(str, st.session_state.drawn_history_Z))
else:
    history_values = "아직 뽑은 수가 없습니다."

# 3. 모든 텍스트를 f-string과 Markdown 문법을 사용하여 하나의 문자열로 결합합니다.
# \n\n 은 문단을 나누고, --- 는 수평선을 만듭니다.
info_box_content = f"""{rule_text}
---
{history_title} {history_values}
"""

# 4. 완성된 문자열을 st.info() 위젯에 한 번만 넣어줍니다.
st.info(info_box_content)