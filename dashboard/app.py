import streamlit as st
import time
import pandas as pd
from components.tabs import create_tabs
from services.data_loader import load_base_data

def main():
    # 페이지 기본 설정을 가장 먼저 수행합니다.
    st.set_page_config(layout="wide")

    # --- 세션 상태 초기화 ---
    # 앱이 처음 실행될 때 한 번만 'plot_index'를 0으로 설정합니다.
    if 'plot_index' not in st.session_state:
        st.session_state.plot_index = 0

    # 대시보드의 메인 제목을 설정합니다.
    # st.title("냉간단조 공정 설비 데이터 대시보드")

    # 현재 세션 상태를 기반으로 전체 UI를 한 번 렌더링합니다.
    create_tabs()

    # --- 중앙 시간 제어 (앱의 "심장") ---
    # 그래프에 사용될 데이터의 전체 길이를 계산하여 루프를 제어합니다.
    base_df = load_base_data()
    plot_df = base_df[base_df['Timestamp'] >= pd.to_datetime('2022-05-02 00:00:00')]
    data_len = len(plot_df)

    # 다음 렌더링을 위해 인덱스를 1 증가시킵니다. 데이터 끝에 도달하면 0으로 돌아갑니다.
    st.session_state.plot_index = (st.session_state.plot_index + 1) % data_len
    
    # 1초 동안 대기합니다.
    time.sleep(1)
    
    # Streamlit에게 스크립트 전체를 처음부터 다시 실행하도록 명령합니다.
    # 이를 통해 1초마다 화면이 새로운 데이터로 업데이트되는 효과를 만듭니다.
    st.rerun()

if __name__ == "__main__":
    main()
