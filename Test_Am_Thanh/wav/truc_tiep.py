import pyaudio
import wave
import requests
import time
import os

# --- CẤU HÌNH ---
API_URL = "https://gallantly-sway-trapdoor.ngrok-free.dev/upload"

# Cấu hình âm thanh chuẩn cho AI (YAMNet yêu cầu 16kHz)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 
CHUNK = 1024
RECORD_SECONDS = 4 # Cứ 4 giây sẽ gửi lên AI 1 lần
TEMP_FILE = "live_audio.wav"

p = pyaudio.PyAudio()

# --- CHỌN MICRO THỦ CÔNG ---
device_index = 5
print(f"✅ Đã ép buộc dùng Micro có ID: {device_index}")

def listen_and_alert():
    print("=======================================")
    print("🛡️ HỆ THỐNG TRỰC BAN ĐÃ KHỞI ĐỘNG 🛡️")
    print("Bấm Ctrl + C để dừng hệ thống.")
    print("=======================================")
    
    while True:
        try:
            # 1. Bắt đầu thu âm
            print(f"\n🎙️ Đang nghe ({RECORD_SECONDS}s)...")
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                            input=True, input_device_index=device_index,
                            frames_per_buffer=CHUNK)
            frames = []
            
            # Thu thập dữ liệu âm thanh
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
            stream.stop_stream()
            stream.close()

            # 2. Lưu thành file .wav tạm thời
            wf = wave.open(TEMP_FILE, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # 3. Gửi lên Colab phân tích
            print("🚀 Đang gửi dữ liệu lên AI...")
            headers = {"ngrok-skip-browser-warning": "true"}
            with open(TEMP_FILE, 'rb') as f:
                files = {'file': (TEMP_FILE, f, 'audio/wav')}
                response = requests.post(API_URL, files=files, headers=headers)
                
            result = response.json()
            if result.get('danger_detected'):
                print("🚨 NGUY HIỂM! Đang kích hoạt chuông báo động...")
                
                # ------ THÊM ĐOẠN CODE WEBHOOK VÀO ĐÂY ------
                macrodroid_url = "https://trigger.macrodroid.com/f8eac30e-fdcf-4d7d-b0dc-d658bee477ab/baodong" 
                try:
                    requests.get(macrodroid_url)
                    print("📱 Đã gửi lệnh RUNG đến điện thoại thành công!")
                except Exception as e:
                    print("Lỗi kích hoạt điện thoại:", e)
                # ---------------------------------------------
                
            else:
                print("✅ An toàn.")

        # --- PHẦN BỊ XÓA NHẦM ĐÃ ĐƯỢC THÊM LẠI VÀO ĐÂY ---
        except KeyboardInterrupt:
            print("\n🛑 Đã tắt hệ thống.")
            break
        except Exception as e:
            print("❌ Lỗi kết nối:", e)
            time.sleep(2) # Đợi 2s rồi thử lại nếu rớt mạng

if __name__ == "__main__":
    listen_and_alert()