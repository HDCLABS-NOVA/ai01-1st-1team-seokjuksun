from .alert_msg_store import add_alert

def generate_alert(prediction_result):
    """모델 예측 결과를 받아 알림 메시지 생성"""
    if prediction_result.get("is_fault"):
        msg = f"⚠️ 설비 이상 감지 ({prediction_result['machine_name']})"
        add_alert(msg, level="error")
        return msg
    return None


# def generate_alert(process, value):
#     return f"🚨 공정 {process}에서 이상치 감지됨! (현재값: {value:.2f})"
