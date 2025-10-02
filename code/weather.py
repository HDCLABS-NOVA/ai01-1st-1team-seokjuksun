import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import numpy as np
from scipy.interpolate import make_interp_spline

# 한글 폰트 설정 (Windows: 맑은 고딕)
rc("font", family= "Malgun Gothic")
plt.rcParams["axes.unicode_minus"]= False

# 실습데이터 불러오기
desktop= os.path.join(os.path.expanduser("~"), "Desktop")
file_path= os.path.join(desktop, "1차 프로젝트 대시보드", "실습데이터.csv")
df_first= pd.read_csv(file_path, encoding= "cp949")

# 기상청 CSV 불러오기
desktop= os.path.join(os.path.expanduser("~"), "Desktop")
file_path= os.path.join(desktop, "1차 프로젝트 대시보드", "Temp_Humid_Log.csv")
df= pd.read_csv(file_path, encoding= "cp949")

# '수원' 데이터만 추출
df_suwon= df[df["지점명"] == "수원"].copy()

# 인덱스 초기화
df_suwon.reset_index(drop= True, inplace= True)

# 일시, 기온, 습도만 남기고 열 삭제
df_suwon= df_suwon.drop(columns= ["지점", "지점명", "기온 QC플래그", "습도 QC플래그", "증기압(hPa)", "이슬점온도(°C)"])

# 수원 데이터 저장
df_suwon.to_csv("수원 온,습도 데이터.csv", encoding= "utf-8-sig", index= True)

# 시간 컬럼을 datetime 형식으로 변환
df_first["Timestamp"]= pd.to_datetime(df_first["Timestamp"])
df_suwon["일시"]= pd.to_datetime(df_suwon["일시"])

# 실습데이터 기준으로 기상청 데이터를 병합 (열 이름 달라도 가능)
df_merged= pd.merge(df_first, df_suwon, left_on= "Timestamp", right_on= "일시", how= "left")

# "일시" 열은 이제 필요 없으면 삭제
df_merged.drop(columns= ["일시"], inplace= True)

# 초기 온, 습도 값, 마지막 온, 습도 값 직접 설정
df_merged.loc[0, "기온(°C)"]= 9.9
df_merged.loc[0, "습도(%)"]= 91
df_merged.loc[579296, "기온(°C)"]= 11.65
df_merged.loc[579296, "습도(%)"]= 79.5


# 온, 습도 열이 NaN이면 선형보간
df_merged["기온(°C)"]= df_merged["기온(°C)"].interpolate(method= "linear")
df_merged["습도(%)"]= df_merged["습도(%)"].interpolate(method= "linear")

# 보간 데이터 csv 파일로 저장
df_merged.to_csv("보간 데이터.csv", encoding= "utf-8-sig", index= True)

# -------- 그래프1 --------

# # 온도와 습도 그래프
# plt.figure(figsize=(15, 6))
#
# # 온도
# plt.plot(df_merged["Timestamp"], df_merged["기온(°C)"], color="red", label="기온(°C)", linewidth=1.2)
#
# # 습도
# plt.plot(df_merged["Timestamp"], df_merged["습도(%)"], color="blue", label="습도(%)", linewidth=1.2)
#
# # 제목, 라벨, 범례
# plt.title("수원 지역 시간별 온도/습도 (선형 보간)", fontsize=16)
# plt.xlabel("시간", fontsize=12)
# plt.ylabel("값", fontsize=12)
# plt.legend()
# plt.grid(True, linestyle="--", alpha=0.5)
#
# # 그래프 표시
# plt.tight_layout()
# plt.show()

# ---------- 그래프2 ----------

# fig, ax1 = plt.subplots(figsize=(15,6))
#
# # 왼쪽 y축 (온도)
# ax1.plot(df_merged["Timestamp"], df_merged["기온(°C)"], color="red", label="기온(°C)")
# ax1.set_ylabel("기온(°C)", color="red")
# ax1.tick_params(axis="y", labelcolor="red")
#
# # 오른쪽 y축 (습도)
# ax2 = ax1.twinx()
# ax2.plot(df_merged["Timestamp"], df_merged["습도(%)"], color="blue", label="습도(%)")
# ax2.set_ylabel("습도(%)", color="blue")
# ax2.tick_params(axis="y", labelcolor="blue")
#
# # 제목
# plt.title("수원 기온 및 습도 (보간 데이터)", fontsize=16)
# plt.show()

# ---------- 그래프3 ----------

# # '수원' 데이터만 추출
# df_suwon= df[df["지점명"] == "수원"].copy()
#
# # 시간 컬럼 datetime 변환
# df_suwon["일시"]= pd.to_datetime(df_suwon["일시"])
#
# # 시간 인덱스 설정
# df_suwon.set_index("일시", inplace= True)
#
# # 1시간 단위 데이터를 초 단위로 리샘플링 후 선형보간
# df_resampled= df_suwon.resample("3s").interpolate(method= "linear")
#
# # 그래프 그리기
# plt.figure(figsize=(15,6))
#
# # 온, 습도
# plt.plot(df_suwon.index, df_suwon["기온(°C)"], 'o-', label= "온도(원 데이터)")
# plt.plot(df_resampled.index, df_resampled["기온(°C)"], '-', label= "온도(보간)")
# plt.plot(df_suwon.index, df_suwon["습도(%)"], 'o-', label= "습도(원 데이터)")
# plt.plot(df_resampled.index, df_resampled["습도(%)"], '-', label= "습도(보간)")
#
# plt.title("수원 지역 시간별 온도/습도 (선형 보간)", fontsize=16)
# plt.xlabel("시간")
# plt.ylabel("값")
# plt.legend()
# plt.grid(True)
# plt.show()