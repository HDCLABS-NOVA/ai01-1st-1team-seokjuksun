# System related and data input controls
import os

# Ignore the warnings
import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)

# Library
import pandas as pd
import numpy as np
import math
import time

# Visualization
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

# 한글 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

FILE_PATH = '../dataset/FinalData.csv'

df = pd.read_csv(FILE_PATH, parse_dates=['Timestamp'])
df = df.sort_values('Timestamp').reset_index(drop=True)

# ===== NaN 값을 0으로 처리 =====
df['METAL_OIL_SUPPLY_PRESS_CUT'] = df['METAL_OIL_SUPPLY_PRESS_CUT'].fillna(0)

# ===== 기준 시점 설정 (5월 12일 00시) =====
BASE_TIME = pd.Timestamp('2022-05-13 00:00:00')

# 기준일 이전 데이터로 이상치 기준 계산
past_df = df[df['Timestamp'] < BASE_TIME]
mean = past_df['METAL_OIL_SUPPLY_PRESS_CUT'].mean()
std = past_df['METAL_OIL_SUPPLY_PRESS_CUT'].std()
threshold = 2.5

# 이상치 플래그 추가
df['is_outlier'] = (df['METAL_OIL_SUPPLY_PRESS_CUT'] > mean + threshold * std) | \
                   (df['METAL_OIL_SUPPLY_PRESS_CUT'] < mean - threshold * std)

# 6시간 윈도우 크기 정의
WINDOW_SIZE = pd.Timedelta(hours=6)

# ===== 애니메이션 시작 시간: 기준시간 =====
ANIMATION_START_TIME = BASE_TIME

# 그래프 초기 설정
fig, ax = plt.subplots(figsize=(14, 6))
line, = ax.plot([], [], lw=2, label='Value', color='blue')
line_no_data, = ax.plot([], [], lw=2, label='No Data (0)', color='gray', linestyle='--')  # 데이터 없을 때 회색 선
upper_line = ax.axhline(mean + threshold * std, color='orange', linestyle='--', label='Upper Limit')
lower_line = ax.axhline(mean - threshold * std, color='orange', linestyle='--', label='Lower Limit')
scat = ax.scatter([], [], color='red', s=50, label='Outlier', zorder=5)

# 기준시간 표시 (5월 12일 00시)
base_line = ax.axvline(BASE_TIME, color='green', linestyle=':', linewidth=2, label='Base Time (2024-05-12 00:00)',
                       alpha=0.7)

ax.legend(loc='upper right')
ax.set_xlabel('Time')
ax.set_ylabel('METAL_OIL_SUPPLY_PRESS_CUT')
ax.set_title('Real-time Outlier Monitoring (Starting from 2024-05-12 00:00)')

# X축 포맷 설정
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

# ===== 애니메이션 프레임 계산 =====
# 기준시간 이후 데이터 확인
future_df = df[df['Timestamp'] >= ANIMATION_START_TIME]

if future_df.empty:
    # 데이터가 없으면 기준시간부터 6시간 진행
    total_duration_seconds = 6 * 3600  # 6시간
    print("경고: 기준시간 이후 데이터가 없습니다. 6시간 동안 0 값을 표시합니다.")
else:
    total_duration_seconds = (future_df['Timestamp'].max() - ANIMATION_START_TIME).total_seconds()
    if pd.isna(total_duration_seconds) or total_duration_seconds <= 0:
        total_duration_seconds = 6 * 3600

time_step_seconds = 3
TOTAL_FRAMES = int(np.ceil(total_duration_seconds / time_step_seconds)) + 1

print(f"애니메이션 시작 시간: {ANIMATION_START_TIME}")
print(f"기준 시간: {BASE_TIME}")
print(f"총 프레임 수: {TOTAL_FRAMES}")
print(f"총 지속 시간(초): {total_duration_seconds}")


# 애니메이션 업데이트 함수
def update(frame):
    # ===== 현재 프레임에 따른 끝 시간 계산 =====
    end_time = ANIMATION_START_TIME + pd.Timedelta(seconds=frame * time_step_seconds)

    # 6시간 이전의 시작 시간 계산
    start_time = end_time - WINDOW_SIZE

    # 현재 6시간 윈도우 내 데이터만 선택
    visible_df = df[
        (df['Timestamp'] >= start_time) &
        (df['Timestamp'] <= end_time)
        ].copy()

    # ===== 데이터가 없을 때 처리 =====
    if visible_df.empty:
        # 0 값으로 채운 더미 데이터 생성 (회색 선으로 표시)
        time_range = pd.date_range(start=start_time, end=end_time, freq='1min')
        line.set_data([], [])  # 파란 선은 비움
        line_no_data.set_data(time_range, np.zeros(len(time_range)))  # 회색 선에 0 표시
        scat.set_offsets(np.empty((0, 2)))  # 이상치 없음
    else:
        # ===== 데이터가 있을 때 처리 =====
        line.set_data(visible_df['Timestamp'], visible_df['METAL_OIL_SUPPLY_PRESS_CUT'])
        line_no_data.set_data([], [])  # 회색 선은 비움

        # 이상치 표시 업데이트
        outliers = visible_df[visible_df['is_outlier']]

        if not outliers.empty:
            timestamp_numeric = mdates.date2num(outliers['Timestamp'].values)
            scat.set_offsets(np.c_[timestamp_numeric, outliers['METAL_OIL_SUPPLY_PRESS_CUT'].values])
        else:
            scat.set_offsets(np.empty((0, 2)))

    # X축 범위 업데이트: 6시간 윈도우로 고정
    ax.set_xlim(start_time, end_time)

    # Y축 범위 동적 업데이트
    if not visible_df.empty:
        y_min = visible_df['METAL_OIL_SUPPLY_PRESS_CUT'].min()
        y_max = visible_df['METAL_OIL_SUPPLY_PRESS_CUT'].max()

        # NaN 체크
        if pd.isna(y_min) or pd.isna(y_max):
            y_min, y_max = -5, 10

        # 여유 공간 추가 (데이터 범위의 10%)
        y_margin = (y_max - y_min) * 0.1
        if y_margin == 0:
            y_margin = 5

        ax.set_ylim(y_min - y_margin, y_max + y_margin)
    else:
        # 데이터가 없을 때는 -5 ~ 10 범위로 고정
        ax.set_ylim(-5, 10)

    # X축 레이블 회전
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 진행상황 출력
    if frame % 100 == 0:
        print(f"프레임 {frame}/{TOTAL_FRAMES} 처리 중... ({end_time})")

    return line, line_no_data, scat


# 애니메이션 실행
print("애니메이션 시작!")
ani = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=50,
    blit=True,
    repeat=False
)

plt.tight_layout()
plt.show()