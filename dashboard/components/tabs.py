import streamlit as st
from components.main_page import render_main_page
# 새로 추가된 그래프 함수와 데이터 로더를 임포트합니다.
from components.plots import display_lubrication_chart
from services.data_loader import load_base_data

def create_tabs():
    tab_names = [
        "메인",
        "윤활 및 냉각",
        "금속 배치",
        "타격(스트로크) 공정",
        "플래시 형성 및 트리밍",
        "부품 제거",
        "다단 단조/이송 공정"
    ]

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(tab_names)

    # --- 메인 탭 ---
    with tab1:
        render_main_page()

    # --- 윤활 및 냉각 탭 ---
    with tab2:
        # 기본 데이터를 한 번 로드합니다 (캐시된 결과를 사용).
        base_df = load_base_data()
        # 윤활 및 냉각 탭을 위한 실시간 그래프 함수를 호출합니다.
        display_lubrication_chart(base_df)

    # --- 금속 배치 탭 (2행 2열) ---
    with tab3:
        st.header("금속 배치")
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            with st.container(border=True):
                st.write("카드 1-1")
        with row1_col2:
            with st.container(border=True):
                st.write("카드 1-2")
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            with st.container(border=True):
                st.write("카드 2-1")
        with row2_col2:
            with st.container(border=True):
                st.write("카드 2-2")

    # --- 타격(스트로크) 공정 탭 (2행 2열) ---
    with tab4:
        st.header("타격(스트로크) 공정")
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            with st.container(border=True):
                st.write("카드 1-1")
        with row1_col2:
            with st.container(border=True):
                st.write("카드 1-2")
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            with st.container(border=True):
                st.write("카드 2-1")
        with row2_col2:
            with st.container(border=True):
                st.write("카드 2-2")

    # --- 플래시 형성 및 트리밍 탭 (1행 2열) ---
    with tab5:
        st.header("플래시 형성 및 트리밍")
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            with st.container(border=True):
                st.write("카드 1")
        with row1_col2:
            with st.container(border=True):
                st.write("카드 2")

    # --- 부품 제거 탭 ---
    with tab6:
        st.header("부품 제거")

    # --- 다단 단조/이송 공정 탭 ---
    with tab7:
        st.header("다단 단조/이송 공정")
