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
# Thay bằng link Ngrok ĐANG CHẠY MỚI NHẤT trên Server Colab của bạn!
API_URL = "https://gallantly-sway-trapdoor.ngrok-free.dev/upload" 

# ==============================================================
# PHẦN 1: DỮ LIỆU ĐÃ TẢI RỒI NÊN SẼ TỰ BỎ QUA KHÔNG TẢI LẠI
# ==============================================================
base_dir = "dataset_test"
danger_dir = os.path.join(base_dir, "danger")
safe_dir = os.path.join(base_dir, "safe")
os.makedirs(danger_dir, exist_ok=True)
os.makedirs(safe_dir, exist_ok=True)

# Lấy danh sách file
real_safe_dir = [os.path.join(dp, f) for dp, dn, filenames in os.walk(safe_dir) for f in filenames if f.endswith('.wav')]
real_danger_dir = [os.path.join(dp, f) for dp, dn, filenames in os.walk(danger_dir) for f in filenames if f.endswith('.wav')]

# ==============================================================
# PHẦN 2: BẮN API ĐỂ ĐÁNH GIÁ (CÓ THÊM LOG BÁO LỖI)
# ==============================================================
y_true = [] 
y_pred = [] 

print("🚀 Bắt đầu gửi file lên Server Colab để phân tích...")
headers = {"ngrok-skip-browser-warning": "true"}

def test_file(file_path, expected_label):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(API_URL, files={'file': f}, headers=headers)
            
            # Nếu Server trả về mã 200 (Thành công)
            if response.status_code == 200:
                result = response.json()
                y_pred.append(1 if result.get('danger_detected') else 0)
            else:
                # Nếu Ngrok bị lỗi hoặc Server sập
                print(f"\n❌ Lỗi Server {response.status_code}: Vui lòng kiểm tra lại link Ngrok!")
                y_pred.append(0)
                
    except Exception as e: 
        print(f"\n❌ Lỗi kết nối mạng: {e} (Link Ngrok có đúng không?)")
        y_pred.append(0)

# Test nhóm An Toàn
for file_path in tqdm(real_safe_dir, desc="Nhóm AN TOÀN"):
    y_true.append(0)
    test_file(file_path, 0)
    time.sleep(0.5) # Nghỉ lâu hơn chút cho Colab xử lý kịp

# Test nhóm Nguy Hiểm
for file_path in tqdm(real_danger_dir, desc="Nhóm NGUY HIỂM"):
    y_true.append(1)
    test_file(file_path, 1)
    time.sleep(0.5)

# ==============================================================
# PHẦN 3: TÍNH TOÁN VÀ LƯU BIỂU ĐỒ BÁO CÁO (KHÔNG BẬT POP-UP)
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
print("Đang tạo và lưu ảnh biểu đồ vào thư mục của bạn...")

# VẼ CONFUSION MATRIX -> LƯU THÀNH FILE
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(7, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['An Toàn', 'Nguy Hiểm'], 
            yticklabels=['An Toàn', 'Nguy Hiểm'], 
            annot_kws={"size": 16})
plt.title('Ma trận nhầm lẫn (Confusion Matrix)', fontsize=14)
plt.xlabel('AI Dự đoán (Server trả về)', fontsize=12)
plt.ylabel('Thực tế', fontsize=12)
plt.savefig("Hinh_Confusion_Matrix.png", bbox_inches='tight') # <-- LƯU ẢNH
plt.close()

# VẼ WAVEFORM VÀ SPECTROGRAM -> LƯU THÀNH FILE
if len(real_danger_dir) > 0:
    sample_audio_path = real_danger_dir[0] 
    y_audio, sr = librosa.load(sample_audio_path, sr=16000)
    y_audio, _ = librosa.effects.trim(y_audio, top_db=30)
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
    plt.savefig("Hinh_Bieu_Do_Am_Thanh.png", bbox_inches='tight') # <-- LƯU ẢNH
    plt.close()

print("✅ Đã lưu 2 ảnh thành công! Hãy mở thư mục Test_Am_Thanh để xem ảnh.")