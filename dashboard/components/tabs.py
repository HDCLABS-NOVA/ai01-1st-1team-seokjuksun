# Streamlit 라이브러리를 임포트합니다.
import streamlit as st

# 메인 탭의 UI를 렌더링하는 함수를 components/main_page.py 파일로부터 임포트합니다.
from components.main_page import render_main_page

# 대시보드의 탭들을 생성하고 각 탭의 내용을 구성하는 함수입니다.
def create_tabs():
    # 대시보드에 표시될 탭들의 이름을 리스트로 정의합니다.
    tab_names = [
        "메인",
        "윤활 및 냉각",
        "금속 배치",
        "타격(스트로크) 공정",
        "플래시 형성 및 트리밍",
        "부품 제거",
        "다단 단조/이송 공정"
    ]

    # st.tabs() 함수를 사용하여 위에서 정의한 이름으로 실제 탭 객체들을 생성합니다.
    # 각 탭 객체는 개별 변수(tab1, tab2, ...)에 할당됩니다.
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(tab_names)

    # 'with' 구문을 사용하여 각 탭에 들어갈 내용을 정의합니다.

    # 첫 번째 '메인' 탭의 내용을 구성합니다.
    with tab1:
        # main_page.py에서 임포트한 render_main_page 함수를 호출하여
        # 메인 탭의 복잡한 UI 로직을 실행합니다.
        render_main_page()

    # 두 번째 '윤활 및 냉각' 탭의 내용을 구성합니다.
    with tab2:
        # 현재는 간단한 제목만 표시하며, 추후 이 공간에 관련 내용이 구현될 예정입니다.
        st.header("윤활 및 냉각")

    # 세 번째 '금속 배치' 탭의 내용을 구성합니다.
    with tab3:
        st.header("금속 배치")

    # 네 번째 '타격(스트로크) 공정' 탭의 내용을 구성합니다.
    with tab4:
        st.header("타격(스트로크) 공정")

    # 다섯 번째 '플래시 형성 및 트리밍' 탭의 내용을 구성합니다.
    with tab5:
        st.header("플래시 형성 및 트리밍")

    # 여섯 번째 '부품 제거' 탭의 내용을 구성합니다.
    with tab6:
        st.header("부품 제거")

    # 일곱 번째 '다단 단조/이송 공정' 탭의 내용을 구성합니다.
    with tab7:
        st.header("다단 단조/이송 공정")
