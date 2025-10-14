import streamlit as st
from datetime import datetime

def get_alert_store():
    if "alert_history" not in st.session_state:
        st.session_state["alert_history"] = []
    return st.session_state["alert_history"]

def add_alert(message, level="warning"):
    alert = {
        "message": message,
        "level": level,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state["alert_history"].append(alert)
    return alert

# _alerts = []
#
# def store_alert(msg: str):
#     _alerts.append(msg)
#
# def get_alert_messages():
#     return _alerts
