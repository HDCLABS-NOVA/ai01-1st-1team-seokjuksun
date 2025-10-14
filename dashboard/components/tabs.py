import streamlit as st
from components.main_page import render_main_page
from components.plots import (
    display_lubrication_chart, 
    create_metal_placement_charts, 
    create_stroke_process_charts, 
    create_trimming_chart,
    create_part_removal_chart,
    create_transfer_process_charts
)
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
        base_df = load_base_data()
        display_lubrication_chart(base_df)

    # --- 금속 배치 탭 (직렬 배열로 변경) ---
    with tab3:
        base_df = load_base_data()
        fig_continuous, fig_discrete = create_metal_placement_charts(base_df)
        # 첫 번째 그래프
        with st.container(border=True):
            st.plotly_chart(fig_continuous, use_container_width=True)
        # 두 번째 그래프
        with st.container(border=True):
            st.plotly_chart(fig_discrete, use_container_width=True)

    # --- 타격(스트로크) 공정 탭 (직렬 배열로 변경) ---
    with tab4:
        base_df = load_base_data()
        fig_freq, fig_continuous = create_stroke_process_charts(base_df)
        # 첫 번째 그래프
        with st.container(border=True):
            st.plotly_chart(fig_freq, use_container_width=True)
        # 두 번째 그래프
        with st.container(border=True):
            st.plotly_chart(fig_continuous, use_container_width=True)

    # --- 플래시 형성 및 트리밍 탭 ---
    with tab5:
        base_df = load_base_data()
        fig_trimming = create_trimming_chart(base_df)
        with st.container(border=True):
            st.plotly_chart(fig_trimming, use_container_width=True)

    # --- 부품 제거 탭 ---
    with tab6:
        base_df = load_base_data()
        fig_part_removal = create_part_removal_chart(base_df)
        with st.container(border=True):
            st.plotly_chart(fig_part_removal, use_container_width=True)

    # --- 다단 단조/이송 공정 탭 (직렬 배열로 변경) ---
    with tab7:
        base_df = load_base_data()
        fig_discrete_freq, fig_continuous_pos, fig_discrete_pos_set = create_transfer_process_charts(base_df)
        # 각 그래프를 순서대로 배치합니다.
        with st.container(border=True):
            st.plotly_chart(fig_discrete_freq, use_container_width=True)
        with st.container(border=True):
            st.plotly_chart(fig_continuous_pos, use_container_width=True)
        with st.container(border=True):
            st.plotly_chart(fig_discrete_pos_set, use_container_width=True)
