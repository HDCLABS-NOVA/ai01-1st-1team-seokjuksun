import streamlit as st
from components.tabs import create_tabs

def main():
    # 페이지 기본 설정을 가장 먼저 수행합니다.
    st.set_page_config(layout="wide")

    # --- 세션 상태 초기화 ---
    # st.session_state는 앱의 세션 동안 데이터를 유지하는 딕셔너리 같은 객체입니다.
    # 'plot_index'가 세션 상태에 없으면, 0으로 초기화합니다.
    # 이 코드는 앱이 처음 실행될 때 한 번만 실행됩니다.
    if 'plot_index' not in st.session_state:
        st.session_state.plot_index = 0

    # 대시보드의 메인 제목을 설정합니다.
    st.title("냉간단조 공정 설비 데이터 대시보드")

    # 탭 생성 함수를 호출하여 화면을 구성합니다.
    create_tabs()

if __name__ == "__main__":
    main()
