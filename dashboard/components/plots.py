import streamlit as st
import time
import plotly.graph_objects as go

@st.fragment
def display_realtime_chart(df, upper_bound, lower_bound, target_column):
    """
    @st.fragment를 사용하여 특정 컬럼에 대한 실시간 슬라이딩 윈도우 이상치 탐지 차트를 표시합니다.
    plot_index는 app.py에서 중앙 관리 및 초기화됩니다.
    """
    # 그래프를 그릴 빈 공간(플레이스홀더)을 생성합니다.
    chart_placeholder = st.empty()

    # 데이터프레임의 총 길이를 가져옵니다.
    data_len = len(df)

    # 무한 루프를 사용하여 데이터 스트리밍을 시뮬레이션합니다.
    while True:
        # 그래프에 한 번에 표시할 데이터 포인트의 개수(창 크기)를 정의합니다.
        window_size = 100
        # app.py에서 초기화된 현재 데이터 인덱스를 가져옵니다.
        current_index = st.session_state.plot_index
        
        start_index = max(0, current_index - window_size + 1)
        end_index = current_index + 1
        
        # 현재 윈도우에 해당하는 데이터 조각을 추출합니다.
        window_df = df.iloc[start_index:end_index]

        # --- Plotly 그래프 생성 ---
        fig = go.Figure()

        # 메인 데이터 라인을 추가합니다.
        fig.add_trace(go.Scatter(
            x=window_df['Timestamp'],
            y=window_df[target_column],
            mode='lines',
            name=target_column,
            line=dict(color='blue')
        ))

        # 이상치 마커를 추가합니다.
        outliers = window_df[window_df['is_outlier']]
        if not outliers.empty:
            fig.add_trace(go.Scatter(
                x=outliers['Timestamp'],
                y=outliers[target_column],
                mode='markers',
                name='Anomaly',
                marker=dict(color='red', size=8)
            ))

        # 상한/하한 경계선을 추가합니다.
        fig.add_hline(y=upper_bound, line_dash="dash", line_color="orange", name='Upper Bound')
        fig.add_hline(y=lower_bound, line_dash="dash", line_color="orange", name='Lower Bound')

        # 그래프 레이아웃을 업데이트합니다.
        fig.update_layout(
            title=f"실시간 이상치 탐지: {target_column}",
            xaxis_title="Timestamp",
            yaxis_title="Value",
            legend_title="Legend"
        )
        
        # 플레이스홀더의 내용을 새로운 그래프로 덮어씁니다.
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # 다음 프레임을 위해 인덱스를 1 증가시키고, 데이터 끝에 도달하면 0으로 돌아갑니다.
        st.session_state.plot_index = (st.session_state.plot_index + 1) % data_len
        
        # 1초 동안 실행을 멈춰 업데이트 속도를 조절합니다.
        time.sleep(1)
