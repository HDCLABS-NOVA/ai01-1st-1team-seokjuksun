import streamlit as st
import plotly.graph_objects as go

# --- 메인 탭: 이상치 탐지 그래프 ---
def display_realtime_chart(df, upper_bound, lower_bound, target_column):
    window_size = 100
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[target_column], mode='lines', name=target_column, line=dict(color='blue')))
    outliers = window_df[window_df['is_outlier']]
    if not outliers.empty:
        fig.add_trace(go.Scatter(x=outliers['Timestamp'], y=outliers[target_column], mode='markers', name='Anomaly', marker=dict(color='red', size=8)))
    fig.add_hline(y=upper_bound, line_dash="dash", line_color="orange", name='Upper Bound')
    fig.add_hline(y=lower_bound, line_dash="dash", line_color="orange", name='Lower Bound')
    fig.update_layout(title=f"실시간 이상치 탐지: {target_column}", xaxis_title="Timestamp", yaxis_title="Value", legend_title="Legend")
    
    st.plotly_chart(fig, use_container_width=True)

# --- 윤활 및 냉각 탭: 4개 컬럼 동시 표시 그래프 ---
def display_lubrication_chart(df):
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
    for col in columns_to_plot:
        if col in window_df.columns:
            fig.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col))

    fig.update_layout(title="실시간 윤활 및 냉각 데이터", xaxis_title="Timestamp", yaxis_title="Value", legend_title="Columns")
    st.plotly_chart(fig, use_container_width=True)

# --- 금속 배치 탭: 연속형/이산형 분리 그래프 ---
def create_metal_placement_charts(df):
    """
    연속형 데이터와 이산형 데이터를 위한 두 개의 별도 그래프 객체를 생성하여 반환합니다.
    """
    window_size = 100
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    continuous_col = 'TONGS_CAST_CURR'
    discrete_cols = [
        'TONGS_CAST_SET_FREQ',
        'TONGS_POS',
        'TONGS_INVERTER_ALM_ERR_CD'
    ]

    # 그래프 1: 연속형 데이터 (Line Chart)
    fig_continuous = go.Figure()
    if continuous_col in window_df.columns:
        fig_continuous.add_trace(go.Scatter(
            x=window_df['Timestamp'],
            y=window_df[continuous_col],
            mode='lines',
            name=continuous_col
        ))
    fig_continuous.update_layout(title="변수명", xaxis_title="Timestamp", yaxis_title="Current")

    # 그래프 2: 이산형 데이터 (Step Chart)
    fig_discrete = go.Figure()
    for col in discrete_cols:
        if col in window_df.columns:
            # line_shape='hv'는 수평-수직 형태의 스텝 차트를 만듭니다.
            fig_discrete.add_trace(go.Scatter(
                x=window_df['Timestamp'],
                y=window_df[col],
                mode='lines',
                name=col,
                line_shape='hv'
            ))
    fig_discrete.update_layout(title="변수명", xaxis_title="Timestamp", yaxis_title="State")

    return fig_continuous, fig_discrete
