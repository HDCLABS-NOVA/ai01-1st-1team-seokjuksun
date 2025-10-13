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

# 현재 시점 설정
current_cut = pd.Timestamp('2024-05-12 00:00:00')

# 기준일 이전 데이터로 이상치 기준 계산
past_df = df[df['Timestamp'] < current_cut]
mean = past_df['METAL_OIL_SUPPLY_PRESS_CUT'].mean()
std = past_df['METAL_OIL_SUPPLY_PRESS_CUT'].std()
threshold = 2.5

# 이상치 플래그 추가
df['is_outlier'] = (df['METAL_OIL_SUPPLY_PRESS_CUT'] > mean + threshold * std) | \
                   (df['METAL_OIL_SUPPLY_PRESS_CUT'] < mean - threshold * std)

# 6시간 윈도우 크기 정의
WINDOW_SIZE = pd.Timedelta(hours=6)

# 그래프 초기 설정
fig, ax = plt.subplots(figsize=(14, 6))
line, = ax.plot([], [], lw=2, label='Value', color='blue')
upper_line = ax.axhline(mean + threshold * std, color='orange', linestyle='--', label='Upper Limit')
lower_line = ax.axhline(mean - threshold * std, color='orange', linestyle='--', label='Lower Limit')
scat = ax.scatter([], [], color='red', s=50, label='Outlier', zorder=5)

ax.legend(loc='upper right')
ax.set_xlabel('Time')
ax.set_ylabel('METAL_OIL_SUPPLY_PRESS_CUT')
ax.set_title('Real-time Outlier Monitoring (Sliding 6-Hour Window)')

# X축 포맷 설정
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

# 애니메이션 프레임 계산
total_duration_seconds = (df['Timestamp'].max() - df['Timestamp'].min()).total_seconds()
time_step_seconds = 3
TOTAL_FRAMES = int(np.ceil(total_duration_seconds / time_step_seconds)) + 1

# 애니메이션 업데이트 함수
shown_alert = False


def update(frame):
    global shown_alert

    # 현재 프레임에 따른 끝 시간 계산
    end_time = df['Timestamp'].min() + pd.Timedelta(seconds=frame * time_step_seconds)

    # 6시간 이전의 시작 시간 계산
    start_time = end_time - WINDOW_SIZE

    # 현재 6시간 윈도우 내 데이터만 선택
    visible_df = df[
        (df['Timestamp'] >= start_time) &
        (df['Timestamp'] <= end_time)
        ].copy()

    if visible_df.empty:
        return line, scat

    # 라인 데이터 업데이트
    line.set_data(visible_df['Timestamp'], visible_df['METAL_OIL_SUPPLY_PRESS_CUT'])

    # 이상치 표시 업데이트
    outliers = visible_df[visible_df['is_outlier']]

    if not outliers.empty:
        timestamp_numeric = mdates.date2num(outliers['Timestamp'].values)
        scat.set_offsets(np.c_[timestamp_numeric, outliers['METAL_OIL_SUPPLY_PRESS_CUT'].values])
    else:
        scat.set_offsets(np.empty((0, 2)))

    # X축 범위 업데이트: 6시간 윈도우로 고정
    ax.set_xlim(start_time, end_time)

    # ===== Y축 범위 동적 업데이트 =====
    y_min = visible_df['METAL_OIL_SUPPLY_PRESS_CUT'].min()
    y_max = visible_df['METAL_OIL_SUPPLY_PRESS_CUT'].max()

    # 여유 공간 추가 (데이터 범위의 10%)
    y_margin = (y_max - y_min) * 0.1
    if y_margin == 0:  # 모든 값이 같을 경우
        y_margin = 5

    ax.set_ylim(y_min - y_margin, y_max + y_margin)

    # 이상치 한계선 업데이트 (Y축 범위가 바뀌어도 보이도록)
    upper_line.set_ydata([mean + threshold * std, mean + threshold * std])
    lower_line.set_ydata([mean - threshold * std, mean - threshold * std])
    # ===================================

    # X축 레이블 겹침 방지
    fig.autofmt_xdate(rotation=45)

    return line, scat, upper_line, lower_line


# 애니메이션 실행
ani = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=100,
    blit=False,
    repeat=False
)

plt.tight_layout()
plt.show()