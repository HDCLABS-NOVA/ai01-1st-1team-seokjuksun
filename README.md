## 프로젝트 개요
---
 - **프로젝트 주제**: 냉간단조 공정 대시보드 제작
 - **프로젝트 설명**: 주제의 큰 틀은 냉간단조 공정 대시보드 제작이지만, 교육과정 중에 배웠던 데이터 분석 및 머신러닝 모델 학습을 응용하여 공정 예지 보전을 위한 대시보드를 제작함.

<br>

## 🎯프로젝트 목표
---
 - 냉간단조 공정 데이터 분석 및 전처리, 머신러닝 모델 학습을 통해 공정 예지 보전을 위한 대시보드 제작을 목표로 함

<br>

## 👥팀원 및 역할
---
| 이름 | 역할 및 담당 업무 | 개인 Git |
|:---:|:---:|:---:|
| <img src= "https://github.com/user-attachments/assets/17c996f7-4655-45fa-a7a0-47da3b7faa90" width= "120"/> <br> **박희선** | • 프로젝트 총괄 및 일정 관리<br>• 최종 결과 발표 | [GitHub](https://github.com/hisunhelloo) |
| <img src= "https://github.com/user-attachments/assets/06a8ded5-1079-4f0f-b4d9-04a271b4ac8c" width= "120"/> <br> **김채원** | • GitHub 관리<br>• 대시보드 제작  | [GitHub](https://github.com/bbstation09) |
| <img src= "https://github.com/user-attachments/assets/43d0bc5d-eb14-4091-bff7-c854a579794f" width= "130"/> <br> **석상훈** | • 데이터 시각화 및 백업<br>• PPT제작  | [GitHub](https://github.com/chip-cookie) |
| <img src= "https://github.com/user-attachments/assets/2b4f2bfb-f833-4f15-85cc-a42eed714ecc" width= "130" height= "120"/> <br> **이주연** | • 데이터 전처리 및 공정 상태 판별 모델링<br>• README 작성 | [GitHub](https://github.com/juyn-lee) |

<br>

## 📅프로젝트 일정
---
<img src= "https://github.com/user-attachments/assets/aadde320-44af-47b0-9460-5447e00fb900" width= "560" height= "360"/>

<br>

## 💡주요 기능
--- 
 - 공정에서의 주요 절차 모니터링
 - 공정 데이터 실시간 예측
 - 기온, 습도 정보 확인 및 날씨 확인
 - 설비 상태 확인
 - 오류 발생 시 알림 시스템

<br>

## 🛠기술 스택
---
 - **Python 3.13**
 - **데이터 수집**: Kamp 냉간단조 공정 데이터 ,기상청 온, 습도 데이터 활용
 - **데이터 처리 및 분석**: Pandas, Numpy
 - **데이터 시각화**: Matplotlib, Seaborn, Ploty, Streamlit
 - **모델링**: XGBoost, LightGBM, Random Forest

## 📁프로젝트 구조
---
```bash
project/
├── code/           # 데이터 코드
├── dashboard/      # 대시보드 코드
├── dataset/        # 사용한 데이터csv
└── README.md       # 프로젝트 설명
```

<br>

## 수행 결과
---
**이상치 모니터링**

<img src= "https://github.com/user-attachments/assets/e4608d69-8931-4bd8-b64e-fded403a2dcf" width= "560" height= "360"/>

 - 시간별 이상치를 파악해 이상치를 표시함

<br>

**공정데이터 분석 결과**

<img src= "https://github.com/user-attachments/assets/1b2fb12f-eb0c-4498-a4da-974613b3187a" width= "560" height= "360"/>

 - STATUS= 데이터에서 공정의 정상/비정상 상태를 나타내는 값
 - 시간에 따른 STATUS를 시각화하고, 비정상 상태일 때를 따로 표시함

<br>

**머신러닝 모델 학습 성능평가 및 시각화**

<img src= "https://github.com/user-attachments/assets/560ebd0e-665d-4e34-8a7a-3e97bd1405cf" width= "560" height= "360"/>

 - XGBoost, LightGBM, Random Forest 총 세 가지의 모델로 학습을 시켰고, 그중 Random Forest 모델이 타 모델들에 비해 낮은 RMSE 값과 높은 R2 값을 보여줌, 해당 그림은 Random Forest 모델로 학습시킨 결과를 시각화한 것

<br>

**최종 대시보드**

<img src= "https://github.com/user-attachments/assets/7a5f6a5d-0045-41c8-9986-d532bfab389c" width= "560" height= "360"/>

 - 냉간단조 공정에서 실시간으로 이상치를 탐지할 수 있는 대시보드
 - 냉간단조 공정 내 다양한 공정 절차들을 개별 모니터링 가능
 - 실시간 기온 및 습도 그리고 설비 상태 확인 가능

<br>

## 주요 성과
---
 -**체계적인 데이터 파이프라인 구축**: 데이터 수집부터 정제, 저장, 분석에 이르는 전 과정을 자동화하여 데이터 처리 효율성을 극대화하고, 신뢰성 있는 데이터 기반 의사결정을 위한 견고한 토대를 마련했음.

 -**실용적인 대시보드 완성**: 핵심 성과 지표(KPI)와 주요 데이터를 직관적으로 시각화한 대시보드를 개발하여, 사용자들이 복잡한 데이터를 쉽게 이해하고 필요한 정보를 즉시 파악할 수 있도록 지원했음.

 -**효과적인 팀 협업 프로세스 확립**: GitHub를 통한 코드 버전 관리, Notion을 활용한 문서화 및 지식 공유, Discord를 통한 실시간 소통 채널을 구축하여 팀원 간의 유기적인 협업을 강화하고 프로젝트 생산성을 크게 향상시켰음.
