import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from pprint import pprint

# 한글 폰트 지정 (윈도우 기본)
rc('font', family= 'Malgun Gothic')
plt.rcParams['axes.unicode_minus']= False

file_path= r"C:\Users\Admin\PycharmProjects\대시보드 프로젝트\찐보간데이터.csv"
df= pd.read_csv(file_path, encoding= 'utf-8')  # 필요한 경우 encoding='cp949'로 변경

# 타깃 열 설정
print("데이터프레임 열:", list(df.columns))
if "STATUS.xlsx" in df.columns:
    target_col= "STATUS.xlsx"
else:
    raise KeyError("타깃 열(status 또는 STATUS.xlsx)이 데이터프레임에 없습니다. 열 이름을 확인하세요.")

# 원래 값이 0,1,2,0.5 로 되어 있으므로 숫자형으로 처리
# 만약 문자열로 되어 있다면 astype(float) 등으로 변환 필요
df[target_col]= pd.to_numeric(df[target_col], errors= 'coerce')
mapping= {0.5: "abnormal", 2: "normal", 0: "special_0", 1: "special_1"}
df["label"]= df[target_col].map(mapping)

# 매핑되지 않은 값(NA)이 있는지 확인
if df["label"].isna().any():
    print("경고: 타깃에 매핑되지 않은 값이 있습니다. 해당 행들을 출력합니다:")
    print(df.loc[df["label"].isna(), target_col].value_counts())
    # 필요하면 매핑되지 않은 행 제거
    df = df.dropna(subset= ["label"]).reset_index(drop=True)

# === 날짜 컬럼 변환 ===
# 날짜 컬럼 자동 탐색
date_col_candidates = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
if not date_col_candidates:
    raise KeyError("날짜/시간 관련 열을 찾을 수 없습니다. 'date' 또는 'time'이 포함된 열 이름을 확인하세요.")
date_col = date_col_candidates[0]
print(f"선택된 날짜 컬럼: {date_col}")

# datetime으로 변환
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# 타깃/라벨 열 제거
X = df.drop(columns= [target_col, "label"])

# X에 숫자형 피처만 사용 (간단한 안전장치)
X_numeric= X.select_dtypes(include= [np.number]).copy()
if X_numeric.shape[1] == 0:
    raise ValueError("숫자형 피처가 하나도 없습니다. XGBoost 학습을 위해 숫자형 피처가 필요합니다.")

y= df["label"]

le= LabelEncoder()
y_encoded= le.fit_transform(y)
print("라벨 클래스:", le.classes_)

X_train, X_test, y_train, y_test= train_test_split(
    X_numeric, y_encoded, test_size= 0.2, random_state= 42, stratify= y_encoded
)

model= XGBClassifier(
    objective= 'multi:softmax',
    num_class=len(le.classes_),
    eval_metric= 'mlogloss',
    random_state=42
)

model.fit(X_train, y_train)

y_pred= model.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names= le.classes_))
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# # 중요도
# xgb.plot_importance(model)
# plt.title("Feature Importance")
# plt.tight_layout()
# plt.show()

# === 2022-05-13 00:00:00 이후 데이터 예측 ===
cutoff = pd.Timestamp("2022-05-13 00:00:00")
future_df = df[df[date_col] >= cutoff].copy()

if len(future_df) == 0:
    print("⚠️ 지정된 날짜 이후 데이터가 없습니다.")
else:
    # 학습에 사용한 컬럼(X_numeric.columns)만 사용
    X_future = future_df[X_numeric.columns]

    # 예측
    y_future_pred = model.predict(X_future)
    future_df["예측결과"] = le.inverse_transform(y_future_pred)

    # 결과 출력
    print(f"\n=== {cutoff} 이후 예측 결과 (상위 10개) ===")
    print(future_df[[date_col, "예측결과"]].head(10))


    # CSV 저장file_path= r"C:\Users\Admin\PycharmProjects\대시보드 프로젝트\찐보간데이터.csv"
    future_df.to_csv("predict_result_after_20220513.csv", index=False, encoding='utf-8-sig')
    print(f"\n✅ 예측 결과 CSV 저장 완료")

# # ===== 고장 확률 (abnormal 클래스 확률) 계산 =====
# # 각 클래스별 예측 확률 구하기
# y_proba = model.predict_proba(X_test)
#
# # 클래스 이름과 확률의 대응 관계 확인
# print("\n클래스 인덱스 매핑:", {i: label for i, label in enumerate(le.classes_)})
#
# # 'abnormal' 클래스 인덱스 찾기
# abnormal_index = list(le.classes_).index("abnormal")
#
# # 각 샘플별 abnormal 확률 추출
# abnormal_proba = y_proba[:, abnormal_index]
#
# # 결과를 DataFrame으로 정리
# result_df = pd.DataFrame({
#     "실제값": le.inverse_transform(y_test),
#     "예측값": le.inverse_transform(y_pred),
#     "고장확률(%)": np.round(abnormal_proba * 100, 2)
# })
#
# # 보기 좋게 정렬
# result_df = result_df.sort_values(by="고장확률(%)", ascending=False).reset_index(drop=True)
#
# # 모든 행 출력 (생략 방지)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 0)
# pd.set_option('display.max_colwidth', None)
#
# print("\n=== 고장 확률 결과 ===")
# print(result_df)  # 상위 20개만 보고 싶다면
