import requests

# Đây là địa chỉ API trên Colab của bạn (nhớ copy chuẩn xác)
API_URL = "https://gallantly-sway-trapdoor.ngrok-free.dev/upload"

# Tên file âm thanh bạn vừa tải về
FILE_PATH = "tiengdiavo.wav"

def test_gui_am_thanh():
    print(f"🚀 Đang gửi file '{FILE_PATH}' lên AI trên Colab...")
    
    try:
        # Mở file và đóng gói gửi đi
        with open(FILE_PATH, 'rb') as f:
            files = {'file': (FILE_PATH, f, 'audio/wav')}
            response = requests.post(API_URL, files=files)
            
        # In kết quả trả về
        if response.status_code == 200:
            print("✅ AI đã xử lý xong! Kết quả:")
            print(response.json())
        else:
            print("❌ Có lỗi xảy ra. Mã lỗi:", response.status_code)
            
    except FileNotFoundError:
        print("❌ Không tìm thấy file âm thanh. Bạn đã để đúng tên và cùng thư mục chưa?")
    except Exception as e:
        print("❌ Lỗi kết nối:", e)

if __name__ == "__main__":
    test_gui_am_thanh()