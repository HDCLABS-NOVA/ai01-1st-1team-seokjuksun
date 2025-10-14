import streamlit as st
import pandas as pd
from services.data_loader import load_base_data, calculate_anomaly_stats
from components.plots import display_realtime_chart

def render_main_page():
    # --- 데이터 준비 ---
    base_df = load_base_data()
    
    target_timestamp = pd.to_datetime("2022-05-13 00:00:00")
    specific_data_row = base_df[base_df['Timestamp'] == target_timestamp]
    specific_data = specific_data_row.iloc[0] if not specific_data_row.empty else None

    # --- 상단 행: 정보 카드 영역 ---
    top_col1, top_col2 = st.columns(2)

    with top_col1:
        with st.container(border=True):
            st.write("현재 날씨")
            date_str = target_timestamp.strftime('%Y년 %m월 %d일 %H시 %M분')
            st.write(f"({date_str} 기준)")

            if specific_data is not None:
                temperature = specific_data['기온(°C)']
                humidity = specific_data['습도(%)']
                st.metric("기온", f"{temperature:.1f} °C")
                st.metric("습도", f"{humidity:.1f} %")
            else:
                st.write("데이터를 찾을 수 없습니다.")

    with top_col2:
        with st.container(border=True):
            st.write("설비 상태")
            
            if specific_data is not None:
                current_status = specific_data.get('predict')
            else:
                current_status = "N/A"

            if current_status == 'normal':
                status_display = "정상 🟢"
            elif current_status == 'abnormal':
                status_display = "비정상 🔴"
            elif current_status in ['special_0', 'special_1']:
                status_display = "경고 🟡"
            else:
                status_display = "알 수 없음"

            st.markdown(f"<div style='text-align: center; font-size: 24px; padding: 2.3rem 0;'>{status_display}</div>", unsafe_allow_html=True)

    # --- 중간 행: 컨트롤 및 그래프 영역 ---
    mid_col1, mid_col2 = st.columns([1, 2])

    with mid_col1:
        COLUMN_DISPLAY_NAMES = {
            "WORK_OIL_SUPPLY_PRESS": "가공유 공급 압력",
            "METAL_OIL_SUPPLY_PRESS_CONTR": "메탈 오일 공급 압력 (조작)",
            "METAL_OIL_SUPPLY_PRESS_CUT": "메탈 오일 공급 압력 (절단)",
            "MAIN_MOTOR_CURR": "메인 에어 압력",
        }

        st.selectbox(
            "표시할 데이터 선택",
            options=list(COLUMN_DISPLAY_NAMES.keys()),
            key="selected_column",
            index=0
        )

    with mid_col2:
        selected_col = st.session_state.get("selected_column")
        if selected_col:
            plot_df, upper_bound, lower_bound = calculate_anomaly_stats(base_df, selected_col)
            display_realtime_chart(plot_df, upper_bound, lower_bound, selected_col)
