import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import requests
import os

# --- CẤU HÌNH ---
API_URL = "https://gallantly-sway-trapdoor.ngrok-free.dev/upload" # Link Ngrok của bạn
DB_NAME = "history_alerts.db"

# Thêm link Webhook báo động rung điện thoại (MacroDroid)
MACRODROID_URL = "https://trigger.macrodroid.com/f8eac30e-fdcf-4d7d-b0dc-d658bee477ab/baodong"

# Thêm cấu hình Bot Telegram (Điền Token và Chat ID của bạn vào đây)
TELEGRAM_BOT_TOKEN = "" # Ví dụ: "123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"
TELEGRAM_CHAT_ID = ""   # Ví dụ: "987654321"

# --- 1. QUẢN LÝ CƠ SỞ DỮ LIỆU (SQLite) ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS alerts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, 
                  sound_type TEXT, 
                  confidence REAL)''')
    conn.commit()
    conn.close()

def save_to_db(sound, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO alerts (timestamp, sound_type, confidence) VALUES (?, ?, ?)",
              (now, sound, score))
    conn.commit()
    conn.close()

# --- 2. GIAO DIỆN WEB (Streamlit) ---
st.set_page_config(page_title="AI Sound Guard", layout="wide")
init_db()

st.title("🛡️ AI Sound Guard - Hệ thống cảnh báo âm thanh nguy hiểm")
st.markdown("---")

# Chia giao diện làm 2 phần
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🔍 Nhận diện mới")
    uploaded_file = st.file_uploader("Tải file âm thanh (.wav)", type=["wav"])
    
    if st.button("Phân tích âm thanh"):
        if uploaded_file is not None:
            with st.spinner("AI đang lắng nghe..."):
                # Gửi file lên API Server
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(API_URL, files={"file": ("test.wav", uploaded_file.getvalue())})
                
                if response.status_code == 200:
                    res = response.json()
                    is_danger = res.get('danger_detected')
                    
                    if is_danger:
                        st.error("🚨 CẢNH BÁO: Phát hiện âm thanh nguy hiểm!")
                        save_to_db("Dangerous Detected", 90.0)
                        
                        # ------ KÍCH HOẠT RUNG ĐIỆN THOẠI ------
                        try:
                            requests.get(MACRODROID_URL)
                            # Hiển thị thông báo bật lên ở góc màn hình Web
                            st.toast("📱 Đã gửi lệnh RUNG đến điện thoại thành công!", icon="🔔")
                        except Exception as e:
                            st.warning(f"Lỗi kích hoạt điện thoại: {e}")
                        # ---------------------------------------------
                        
                        # ------ GỬI TIN NHẮN TELEGRAM ------
                        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                            try:
                                telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                                requests.post(telegram_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": "🚨 CẢNH BÁO: Phát hiện âm thanh nguy hiểm!"})
                                st.toast("📩 Đã gửi cảnh báo qua Telegram!", icon="✈️")
                            except Exception as e:
                                st.warning(f"Lỗi gửi Telegram: {e}")
                        # ---------------------------------------------
                        
                    else:
                        st.success("✅ An toàn: Không phát hiện dấu hiệu bất thường.")
                        save_to_db("Normal Sound", 10.0)
                else:
                    st.warning("Lỗi kết nối Server. Kiểm tra Ngrok!")
        else:
            st.info("Vui lòng chọn file trước.")

with col2:
    st.header("📜 Lịch sử cảnh báo")
    conn = sqlite3.connect(DB_NAME)
    # Thay use_container_width thành width="stretch" để fix cảnh báo đỏ trong Terminal
    df = pd.read_sql_query("SELECT timestamp as 'Thời gian', sound_type as 'Loại âm thanh', confidence as 'Độ tin cậy %' FROM alerts ORDER BY id DESC", conn)
    st.dataframe(df, width=2000) 
    conn.close()
    
    if st.button("Làm mới danh sách"):
        st.rerun()

st.sidebar.info("Hệ thống tích hợp YAMNet & SQLite. Dữ liệu được cập nhật thời gian thực.")