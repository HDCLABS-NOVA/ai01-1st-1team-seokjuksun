import pandas as pd
import streamlit as st

# --- 함수 1: 모든 곳에서 공유하는 기본 데이터 로딩 ---
# show_spinner 파라미터를 사용하여 로딩 중에 표시될 메시지를 지정합니다.
@st.cache_data(show_spinner="설비 데이터 준비중...")
def load_base_data():
    """
    앱 세션 동안 단 한 번만 실행되어 기본 데이터프레임을 로드하고 캐시합니다.
    """
    df = pd.read_csv("../dataset/FinalData.csv", parse_dates=['Timestamp'], low_memory=False)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values('Timestamp').reset_index(drop=True)
    return df

# --- 함수 2: 그래프에 필요한 동적 이상치 계산 ---
# 이 함수가 실행될 때도 사용자 친화적인 메시지를 표시합니다.
@st.cache_data(show_spinner="그래프 준비중...")
def calculate_anomaly_stats(_df, target_column):
    """
    입력받은 데이터프레임과 컬럼명에 따라 이상치 통계를 계산합니다.
    """
    df = _df.copy()

    # --- 이상치 탐지 로직 ---
    df[target_column] = df[target_column].fillna(0)

    base_time = pd.Timestamp('2022-05-13 00:00:00')
    past_df = df[df['Timestamp'] < base_time]

    if not past_df.empty:
        mean = past_df[target_column].mean()
        std = past_df[target_column].std()
    else:
        mean = 0
        std = 0

    threshold = 2.5
    upper_bound = mean + threshold * std
    lower_bound = mean - threshold * std
    df['is_outlier'] = (df[target_column] > upper_bound) | (df[target_column] < lower_bound)
    
    plot_df = df[df['Timestamp'] >= base_time].reset_index(drop=True)
    
    return plot_df, upper_bound, lower_bound

# --- 함수 3: 날씨 카드용 고정 데이터 로딩 (변경 없음) ---
def get_data_for_specific_time(timestamp_str):
    df = pd.read_csv("../dataset/FinalData.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    specific_data = df[df['Timestamp'] == pd.to_datetime(timestamp_str)]
    if not specific_data.empty:
        return specific_data.iloc[0]
    return None
