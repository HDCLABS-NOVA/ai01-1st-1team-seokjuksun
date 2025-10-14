import streamlit as st
import pandas as pd
from services.data_loader import load_base_data, calculate_anomaly_stats
from components.plots import display_realtime_chart

def render_main_page():
    # --- 데이터 준비 ---
    base_df = load_base_data()

    # ✅ 변경 포인트: app.py에서 st.session_state에 저장한 "current_timestamp" 사용
    target_timestamp = st.session_state.get("current_timestamp", pd.to_datetime("2022-05-13 00:00:00"))

    # ✅ 해당 시각의 행 가져오기
    specific_data_row = base_df[base_df['Timestamp'] == target_timestamp]
    specific_data = specific_data_row.iloc[0] if not specific_data_row.empty else None

    # --- 페이지를 왼쪽(정보/컨트롤)과 오른쪽(그래프) 두 개의 열로 나눕니다. ---
    # 왼쪽 열의 비율을 줄여 카드 너비를 더 좁게 만듭니다. (1:2 -> 1:3)
    col1, col2 = st.columns([1, 3])

    # --- 왼쪽 열(col1)의 내용 --- #
    with col1:
        # --- 날씨 정보 카드 ---
        with st.container(border=True):
            st.write("☀️ 현재 날씨")
            date_str = target_timestamp.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
            st.write(f"{date_str} 기준")

            if specific_data is not None:
                temperature = specific_data['기온(°C)']
                humidity = specific_data['습도(%)']
                st.metric("기온 🌡️", f"{temperature:.1f} °C")
                st.metric("습도 💧", f"{humidity:.1f} %")
            else:
                st.write("데이터를 찾을 수 없습니다.")

        # --- 설비 상태 카드 ---
        with st.container(border=True):
            st.write("⚙️ 설비 상태")

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

            st.markdown(f"<div style='text-align: center; font-size: 24px; padding: 1rem 0;'>{status_display}</div>", unsafe_allow_html=True)

        # --- 컬럼 선택 Selectbox ---
        st.selectbox(
            "표시할 데이터 선택",
            (
                "WORK_OIL_SUPPLY_PRESS",
                "METAL_OIL_SUPPLY_PRESS_CONTR",
                "METAL_OIL_SUPPLY_PRESS_CUT",
                "MAIN_MOTOR_CURR",
            ),
            key="selected_column",
            index=0
        )

    # --- 오른쪽 열(col2)의 내용 --- #
    with col2:
        selected_col = st.session_state.get("selected_column")
        if selected_col:
            plot_df, upper_bound, lower_bound = calculate_anomaly_stats(base_df, selected_col)
            display_realtime_chart(plot_df, upper_bound, lower_bound, selected_col)
