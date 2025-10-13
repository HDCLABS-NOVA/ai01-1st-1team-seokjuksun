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
file_path= "../dataset/실습데이터.csv"
df_first= pd.read_csv(file_path, encoding= "cp949")

# 기상청 CSV 불러오기
file_path= "../dataset/Temp_Humid_Log.csv"
df= pd.read_csv(file_path, encoding= "cp949")

# '수원' 데이터만 추출
df_suwon= df[df["지점명"] == "수원"].copy()

# 인덱스 초기화
df_suwon.reset_index(drop= True, inplace= True)

# 일시, 기온, 습도만 남기고 열 삭제
df_suwon= df_suwon.drop(columns= ["지점", "지점명", "기온 QC플래그", "습도 QC플래그", "증기압(hPa)", "이슬점온도(°C)"])

# 수원 데이터 저장 (경로가 ../dataset/수원 온,습도 데이터.csv로 가정)
# df_suwon.to_csv("../dataset/SuwonTempData.csv", encoding= "utf-8-sig", index= True)
print("수원 기상 데이터 추출 완료!")

# 시간 컬럼을 datetime 형식으로 변환
df_first["Timestamp"]= pd.to_datetime(df_first["Timestamp"])
df_suwon["일시"]= pd.to_datetime(df_suwon["일시"])

# 실습데이터 기준으로 기상청 데이터를 병합 (정각끼리 정확히 매칭, 나머지 NaN)
df_merged= pd.merge(df_first, df_suwon, left_on= "Timestamp", right_on= "일시", how= "left")
print("데이터 병합 완료!")

# 초기 온, 습도 값 직접 설정
df_merged.loc[0, "기온(°C)"]= 9.8
df_merged.loc[0, "습도(%)"]= 91

# 마지막 온, 습도 값 직접 설정 (데이터프레임의 마지막 행을 지정)
df_merged.iloc[-1, df_merged.columns.get_loc("기온(°C)")] = 11.65
df_merged.iloc[-1, df_merged.columns.get_loc("습도(%)")] = 79.5


# 온, 습도 열이 NaN이면 선형보간 (정각 데이터 사이를 연결)
df_merged["기온(°C)"]= df_merged["기온(°C)"].interpolate(method= "linear").round(5)
df_merged["습도(%)"]= df_merged["습도(%)"].interpolate(method= "linear").round(5)

# 보간 데이터 csv 파일로 저장
df_merged.to_csv("../dataset/FinalData.csv", encoding= "utf-8-sig", index= True)
print("최종 데이터 저장 완료!")