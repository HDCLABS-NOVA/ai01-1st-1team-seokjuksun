import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- 메인 탭: 이상치 탐지 그래프 (크기 변경 없음) ---
def display_realtime_chart(df, upper_bound, lower_bound, target_column):
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
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
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]
    
    columns_to_plot = ['OIL_SUPPLY_PRESS', 'WORK_OIL_SUPPLY_PRESS', 'METAL_OIL_SUPPLY_PRESS_CONTR', 'METAL_OIL_SUPPLY_PRESS_CUT']
    fig = go.Figure()
    for col in columns_to_plot:
        if col in window_df.columns:
            fig.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col))
    # 그래프 높이를 350px로 설정합니다.
    fig.update_layout(title="실시간 윤활 및 냉각 데이터", xaxis_title="Timestamp", yaxis_title="Value", legend_title="Columns", height=350)
    st.plotly_chart(fig, use_container_width=True)

# --- 금속 배치 탭: 연속형/이산형 분리 그래프 ---
def create_metal_placement_charts(df):
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    continuous_col = 'TONGS_CAST_SET_CURR'
    discrete_cols = ['TONGS_CAST_SET_FREQ', 'TONGS_POS_IDX', 'TONGS_INVERTER_ALM_ERR_CD']

    fig_continuous = go.Figure()
    if continuous_col in window_df.columns:
        fig_continuous.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[continuous_col], mode='lines', name=continuous_col))
    fig_continuous.update_layout(title="실시간 집게 전류", xaxis_title="Timestamp", yaxis_title="Current", height=350)

    fig_discrete = go.Figure()
    for col in discrete_cols:
        if col in window_df.columns:
            fig_discrete.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col, line_shape='hv'))
    fig_discrete.update_layout(title="실시간 집게 상태 데이터", xaxis_title="Timestamp", yaxis_title="State/Code", height=350)

    return fig_continuous, fig_discrete

# --- 타격/스트로크 공정 탭: 2개 그래프 분리 ---
def create_stroke_process_charts(df):
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    freq_col = 'MAIN_MOTOR_SET_FREQ'
    continuous_cols = ['MAIN_MOTOR_CURR', 'MAIN_MOTOR_RPM', 'MAIN_AIR_PRESS']

    fig_freq = go.Figure()
    if freq_col in window_df.columns:
        fig_freq.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[freq_col], mode='lines', name=freq_col, line_shape='hv'))
    fig_freq.update_layout(title="실시간 모터 설정 주파수", xaxis_title="Timestamp", yaxis_title="Frequency", height=350)

    fig_continuous = go.Figure()
    for col in continuous_cols:
        if col in window_df.columns:
            fig_continuous.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col))
    fig_continuous.update_layout(title="실시간 모터/에어 연속 데이터", xaxis_title="Timestamp", yaxis_title="Value", height=350)

    return fig_freq, fig_continuous

# --- 플래시 형성 및 트리밍 탭: 2개 컬럼 통합 그래프 ---
def create_trimming_chart(df):
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    columns_to_plot = ['METAL_TEMP_CONTROL', 'METAL_TEMP_CUT']
    fig = go.Figure()
    for col in columns_to_plot:
        if col in window_df.columns:
            fig.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col))
    fig.update_layout(title="실시간 금속 온도 데이터", xaxis_title="Timestamp", yaxis_title="Temperature", height=350)

    return fig

# --- 부품 제거 탭: 6개 컬럼 통합 그래프 ---
def create_part_removal_chart(df):
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    columns_to_plot = ['KO1_MOTOR_SET_FREQ', 'KO2_MOTOR_SET_FREQ', 'KO3_MOTOR_SET_FREQ', 'KO4_MOTOR_SET_FREQ', 'KO5_MOTOR_SET_FREQ', 'KO6_MOTOR_SET_FREQ']
    fig = go.Figure()
    for col in columns_to_plot:
        if col in window_df.columns:
            fig.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col, line_shape='hv'))
    fig.update_layout(title="실시간 부품 제거 모터 주파수", xaxis_title="Timestamp", yaxis_title="Frequency", height=350)

    return fig

# --- 다단 단조/이송 공정 탭: 3개 그래프 분리 ---
def create_transfer_process_charts(df):
    df = df[df['Timestamp'] >= pd.to_datetime('2022-05-13 00:00:00')].reset_index(drop=True)
    window_size = 50
    current_index = st.session_state.plot_index
    start_index = max(0, current_index - window_size + 1)
    end_index = current_index + 1
    window_df = df.iloc[start_index:end_index]

    discrete_freq_cols = ['CUTTING_SET_FREQ', 'TRANS_SET_FREQ']
    continuous_pos_cols = ['TRANS_POS_LEFT', 'TRANS_POS_RIGHT', 'TRANS_POS_UP', 'TRANS_POS_DOWN']
    discrete_pos_set_cols = ['TRANS_POS_LEFT_SET_H', 'TRANS_POS_RIGHT_SET_H', 'TRANS_POS_UP_SET_H', 'TRANS_POS_DOWN_SET_H']

    fig_discrete_freq = go.Figure()
    for col in discrete_freq_cols:
        if col in window_df.columns:
            fig_discrete_freq.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col, line_shape='hv'))
    fig_discrete_freq.update_layout(title="실시간 절단/이송 주파수", xaxis_title="Timestamp", yaxis_title="Frequency", height=350)

    fig_continuous_pos = go.Figure()
    for col in continuous_pos_cols:
        if col in window_df.columns:
            fig_continuous_pos.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col))
    fig_continuous_pos.update_layout(title="실시간 이송 위치", xaxis_title="Timestamp", yaxis_title="Position", height=350)

    fig_discrete_pos_set = go.Figure()
    for col in discrete_pos_set_cols:
        if col in window_df.columns:
            fig_discrete_pos_set.add_trace(go.Scatter(x=window_df['Timestamp'], y=window_df[col], mode='lines', name=col, line_shape='hv'))
    fig_discrete_pos_set.update_layout(title="실시간 이송 위치 설정", xaxis_title="Timestamp", yaxis_title="Position Set", height=350)

    return fig_discrete_freq, fig_continuous_pos, fig_discrete_pos_set















































































































































































































































