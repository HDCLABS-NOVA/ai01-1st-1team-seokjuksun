import streamlit as st
from services.alert_msg_store import get_alert_store

def show_sidebar():
    st.sidebar.header("🔔 지난 알림 내역")
    alerts = get_alert_store()

    if not alerts:
        st.sidebar.info("아직 알림이 없습니다.")
    else:
        for alert in reversed(alerts):
            st.sidebar.warning(f"{alert['time']}  \n{alert['message']}")
