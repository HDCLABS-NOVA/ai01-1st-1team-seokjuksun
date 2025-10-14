import streamlit as st
from components.main_page import render_main_page
# 새로 추가된 그래프 함수와 데이터 로더를 임포트합니다.
from components.plots import display_lubrication_chart, create_metal_placement_charts, create_stroke_process_charts
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
        st.header("윤활 및 냉각")
        base_df = load_base_data()
        display_lubrication_chart(base_df)

    # --- 금속 배치 탭 ---
    with tab3:
        st.header("금속 배치")
        base_df = load_base_data()
        fig_continuous, fig_discrete = create_metal_placement_charts(base_df)
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.plotly_chart(fig_continuous, use_container_width=True)
        with col2:
            with st.container(border=True):
                st.plotly_chart(fig_discrete, use_container_width=True)

    # --- 타격(스트로크) 공정 탭 ---
    with tab4:
        st.header("타격(스트로크) 공정")
        base_df = load_base_data()
        # 이제 함수는 2개의 그래프 객체만 반환합니다.
        fig_freq, fig_continuous = create_stroke_process_charts(base_df)

        # 2개의 열을 만들어 각 그래프를 별도의 카드에 배치합니다.
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.plotly_chart(fig_freq, use_container_width=True)
        with col2:
            with st.container(border=True):
                st.plotly_chart(fig_continuous, use_container_width=True)

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
