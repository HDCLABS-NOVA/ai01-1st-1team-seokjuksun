import streamlit as st
import plotly.graph_objects as go

# --- 메인 탭: 이상치 탐지 그래프 ---
def display_realtime_chart(df, upper_bound, lower_bound, target_column):
    """
    현재 plot_index에 해당하는 데이터 윈도우를 사용하여 이상치 탐지 차트를 한 번 그립니다.
    시간 제어는 app.py에서 st.rerun()을 통해 중앙 관리됩니다.
    """
    window_size = 100
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    fig = go.Figure()

    # 메인 데이터 라인 추가
    fig.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[target_column], mode='lines', name=target_column, line=dict(color='blue')))
    
    # 이상치 마커 추가
    outliers = window_df[window_df['is_outlier']]
    if not outliers.empty:
        fig.add_trace(go.Scatter(x=outliers['Timestamp'], y=outliers[target_column], mode='markers', name='Anomaly', marker=dict(color='red', size=8)))
    
    # 상한/하한 경계선 추가
    fig.add_hline(y=upper_bound, line_dash="dash", line_color="orange", name='Upper Bound')
    fig.add_hline(y=lower_bound, line_dash="dash", line_color="orange", name='Lower Bound')
    
    # 그래프 레이아웃 업데이트
    fig.update_layout(title=f"실시간 이상치 탐지: {target_column}", xaxis_title="Timestamp", yaxis_title="Value", legend_title="Legend")
    
    # st.empty() 없이 차트를 직접 그립니다.
    st.plotly_chart(fig, use_container_width=True)

# --- 윤활 및 냉각 탭: 4개 컬럼 동시 표시 그래프 ---
def display_lubrication_chart(df):
    """
    현재 plot_index에 해당하는 데이터 윈도우를 사용하여 4개 컬럼의 데이터를 함께 그립니다.
    """
    window_size = 100
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]
    
    columns_to_plot = [
        'OIL_SUPPLY_PRESS',
        'WORK_OIL_SUPPLY_PRESS',
        'METAL_OIL_SUPPLY_PRESS_CONTR',
        'METAL_OIL_SUPPLY_PRESS_CUT'
    ]

    fig = go.Figure()

    # 4개의 컬럼에 대해 각각 선 그래프를 추가합니다.
    for col in columns_to_plot:
        # 데이터프레임에 해당 컬럼이 있는지 확인 후 그래프를 그립니다.
        if col in window_df.columns:
            fig.add_trace(go.Scatter(
                x=window_df['Timestamp'],
                y=window_df[col],
                mode='lines',
                name=col
            ))

    fig.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Value",
        legend_title="Columns"
    )
    
    st.plotly_chart(fig, use_container_width=True)
