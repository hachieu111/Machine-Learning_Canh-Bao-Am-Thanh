import os
import urllib.request
import zipfile
import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import librosa
import librosa.display
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# --- CẤU HÌNH API ---
# Thay bằng link Ngrok đang chạy trên Server Colab của bạn!
API_URL = "https://gallantly-sway-trapdoor.ngrok-free.dev/upload" 

# ==============================================================
# PHẦN 1: TỰ ĐỘNG TẢI VÀ CHUẨN BỊ DỮ LIỆU
# ==============================================================
base_dir = "dataset_test"
danger_dir = os.path.join(base_dir, "danger")
safe_dir = os.path.join(base_dir, "safe")
os.makedirs(danger_dir, exist_ok=True)
os.makedirs(safe_dir, exist_ok=True)

zip_path = "esc50.zip"
if not os.path.exists(zip_path):
    print("⏳ Đang tải dữ liệu âm thanh mẫu từ Internet (Khoảng 600MB)...")
    url = "https://github.com/karolpiczak/ESC-50/archive/master.zip"
    urllib.request.urlretrieve(url, zip_path)
    print("✅ Tải xong!")

print("⏳ Đang giải nén và lọc lấy 50 file mẫu...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    count_danger, count_safe = 0, 0
    for file_info in zip_ref.infolist():
        if file_info.filename.endswith('.wav'):
            filename = os.path.basename(file_info.filename)
            category = filename.split('-')[-1].replace('.wav', '')
            
            if category in ['38', '40', '43'] and count_danger < 25:
                zip_ref.extract(file_info, danger_dir)
                count_danger += 1
            elif category in ['0', '1', '14'] and count_safe < 25:
                zip_ref.extract(file_info, safe_dir)
                count_safe += 1

print(f"✅ Đã chuẩn bị {count_danger} file Nguy hiểm và {count_safe} file An toàn.\n")

# ==============================================================
# PHẦN 2: BẮN API ĐỂ ĐÁNH GIÁ (TESTING PIPELINE)
# ==============================================================
y_true = [] 
y_pred = [] 

real_safe_dir = [os.path.join(dp, f) for dp, dn, filenames in os.walk(safe_dir) for f in filenames if f.endswith('.wav')]
real_danger_dir = [os.path.join(dp, f) for dp, dn, filenames in os.walk(danger_dir) for f in filenames if f.endswith('.wav')]

print("🚀 Bắt đầu gửi file lên Server Colab để phân tích...")
headers = {"ngrok-skip-browser-warning": "true"}

for file_path in tqdm(real_safe_dir, desc="Nhóm AN TOÀN"):
    y_true.append(0)
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(API_URL, files={'file': f}, headers=headers)
            y_pred.append(1 if response.json().get('danger_detected') else 0)
    except: 
        y_pred.append(0)
    time.sleep(0.2) # Tránh nghẽn mạng

for file_path in tqdm(real_danger_dir, desc="Nhóm NGUY HIỂM"):
    y_true.append(1)
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(API_URL, files={'file': f}, headers=headers)
            y_pred.append(1 if response.json().get('danger_detected') else 0)
    except: 
        y_pred.append(0)
    time.sleep(0.2)

# ==============================================================
# PHẦN 3: TÍNH TOÁN VÀ XUẤT BIỂU ĐỒ BÁO CÁO
# ==============================================================
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)

print("\n" + "="*45)
print("📊 BẢNG KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH THỰC TẾ 📊")
print("="*45)
print(f"Độ chính xác (Accuracy) : {acc*100:.2f}%")
print(f"Độ chuẩn xác (Precision): {prec*100:.2f}%")
print(f"Độ bao phủ (Recall)     : {rec*100:.2f}%")
print(f"Điểm F1 (F1-Score)      : {f1*100:.2f}%")
print("="*45)
print("Đang hiển thị biểu đồ. Vui lòng LƯU ẢNH LẠI trước khi tắt cửa sổ để dán vào báo cáo!")

# VẼ CONFUSION MATRIX
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(7, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['An Toàn', 'Nguy Hiểm'], 
            yticklabels=['An Toàn', 'Nguy Hiểm'], 
            annot_kws={"size": 16})
plt.title('Ma trận nhầm lẫn (Confusion Matrix)', fontsize=14)
plt.xlabel('AI Dự đoán (Server trả về)', fontsize=12)
plt.ylabel('Thực tế (Thư mục chứa file)', fontsize=12)
plt.show() # Code sẽ dừng lại ở đây để hiện cửa sổ ảnh 1

# VẼ WAVEFORM VÀ SPECTROGRAM (Lấy file đầu tiên làm mẫu)
sample_audio_path = real_danger_dir[0] 
y_audio, sr = librosa.load(sample_audio_path, sr=16000)

plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
librosa.display.waveshow(y_audio, sr=sr, color='red')
plt.title(f'Waveform thực tế - File: {os.path.basename(sample_audio_path)}', fontsize=14)
plt.xlabel('Thời gian (giây)')
plt.ylabel('Biên độ')

plt.subplot(2, 1, 2)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y_audio)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
plt.colorbar(format='%+2.0f dB')
plt.title('Phổ đồ tần số (Spectrogram) thực tế', fontsize=14)

plt.tight_layout()
plt.show() # Sau khi tắt ảnh 1, cửa sổ ảnh 2 sẽ hiện lên