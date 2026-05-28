# 🛡️ AI Sound Guard - Hệ Thống Cảnh Báo Âm Thanh Nguy Hiểm

Dự án này là một hệ thống AI nhận diện âm thanh nguy hiểm (như tiếng súng, tiếng kính vỡ, tiếng hét, v.v.). Khi phát hiện nguy hiểm, hệ thống sẽ tự động lưu lại lịch sử, hiển thị cảnh báo trên giao diện Web và đồng thời gửi lệnh kích hoạt báo động (rung, đọc văn bản, hiện thông báo) trực tiếp đến điện thoại của bạn.

Hệ thống bao gồm 3 thành phần chính:
1. **Google Colab**: Máy chủ chạy mô hình AI (Model) và API bằng Flask + Ngrok.
2. **Giao diện Web (Local)**: Xây dựng bằng Streamlit để người dùng upload âm thanh và xem lịch sử.
3. **Điện thoại di động**: Sử dụng ứng dụng MacroDroid để nhận Webhook và phát cảnh báo.

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### Giai đoạn 1: Thiết lập Server AI trên Google Colab
Hệ thống sử dụng sức mạnh tính toán của Google Colab để chạy mô hình AI và tạo ra một đường dẫn API (thông qua Ngrok) để giao tiếp với Web.

1. **Chuẩn bị Ngrok Authtoken**:
   - Truy cập [Ngrok Dashboard](https://dashboard.ngrok.com/) và tạo tài khoản.
   - Lấy `Authtoken` của bạn.
2. **Mở file Colab của dự án**:
   - Upload file sổ tay Colab (Notebook) của dự án lên Google Drive và mở bằng Google Colab.
   - Thêm `Authtoken` của Ngrok vào phần cấu hình trong Colab.
3. **Chạy tất cả các cell**:
   - Chạy tuần tự các block code trong Colab.
   - Ở block cuối cùng (phần chạy Flask Server), hệ thống sẽ in ra một đường link có dạng: `https://<chuỗi-ngẫu-nhiên>.ngrok-free.dev/upload`.
   - **Lưu ý:** Hãy Copy đường link này lại. Chú ý rằng mỗi lần bạn restart Colab, đường link này sẽ thay đổi. Đừng tắt tab Colab này trong quá trình sử dụng.

---

### Giai đoạn 2: Cài đặt và Chạy Giao diện Web (Streamlit)
Phần giao diện người dùng được chạy trực tiếp trên máy tính cá nhân của bạn (Local).

#### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt sẵn Python trên máy tính. Mở Terminal / Command Prompt tại thư mục chứa file `app_web.py` (ví dụ: `Test_Am_Thanh/wav`) và thực hiện:

```bash
# 1. Tạo môi trường ảo (Virtual Environment)
python -m venv venv

# 2. Kích hoạt môi trường ảo
# - Trên Windows:
.\venv\Scripts\activate
# - Trên macOS/Linux:
source venv/bin/activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```
*(File `requirements.txt` đã bao gồm: `streamlit`, `pandas`, `requests`)*

#### 2. Cập nhật API Ngrok vào Web
- Mở file `app_web.py` bằng trình chỉnh sửa code (như VS Code).
- Tìm đến dòng khai báo `API_URL` (khoảng dòng 9).
- Dán đường link Ngrok mà bạn vừa copy ở Giai đoạn 1 vào biến này.
  ```python
  API_URL = "https://<chuỗi-ngẫu-nhiên>.ngrok-free.dev/upload"
  ```
- Lưu file lại.

#### 3. Khởi chạy Web
- Trong Terminal (vẫn đang bật môi trường ảo), chạy lệnh:
  ```bash
  streamlit run app_web.py
  ```
- Trình duyệt sẽ tự động mở trang web **AI Sound Guard**. Bạn có thể tải file `.wav` lên để kiểm tra!

---

### Giai đoạn 3: Cấu hình Báo động trên Điện thoại (MacroDroid)
Khi phát hiện âm thanh nguy hiểm, code ở Web sẽ gửi một request (Webhook) đến điện thoại thông qua app MacroDroid để tạo báo động.

#### 1. Cài đặt MacroDroid trên điện thoại
- Lên cửa hàng ứng dụng (Google Play Store) và tải app **MacroDroid - Device Automation**.

#### 2. Thiết lập Macro (Kịch bản tự động)
- Mở app MacroDroid, chọn **Thêm Macro** (Add Macro).
- Đặt tên cho Macro (ví dụ: *Cảnh báo nguy hiểm*).

**A. Phần "Các trình kích hoạt" (Triggers):**
- Bấm dấu **+** -> Chọn **Sự kiện thiết bị** (Device Events) -> Chọn **Webhook (URL)**.
- Đặt "Tên định danh" (Identifier). Ví dụ: `baodong`.
- App sẽ tạo cho bạn một đường link Webhook có dạng: `https://trigger.macrodroid.com/xxxx-xxxx-xxxx/baodong`.
- **Quan trọng:** Copy đường link này, quay lại file `app_web.py` trên máy tính, và dán vào biến `MACRODROID_URL` (khoảng dòng 13).

**B. Phần "Các hành động" (Actions):**
Bạn bấm dấu **+** để thêm các hành động sẽ xảy ra khi nhận được cảnh báo:
- **Hành động 1 - Rung điện thoại:** Thiết bị -> Rung (Chọn loại Buzz dài).
- **Hành động 2 - Đọc văn bản:** Hành động thiết bị -> Đọc văn bản (Nhập: *"chạy ngay đi trước khi mọi chuyện đều tồi tệ hơn"*).
- **Hành động 3 - Hiện thông báo:** Thông báo -> Thanh nổi (Nhập nội dung: *"có cảnh báo âm thanh nguy hiểm"*).

**C. Phần "Các ràng buộc" (Constraints):**
- Để trống (Không có ràng buộc).

#### 3. Lưu lại
- Bấm dấu tích (V) ở góc phải màn hình điện thoại để lưu Macro. Đảm bảo MacroDroid đang được bật.

---

### Giai đoạn 4: Cấu hình gửi cảnh báo qua Telegram (Tùy chọn)
Ngoài việc báo động qua ứng dụng MacroDroid, bạn có thể thiết lập hệ thống tự động gửi tin nhắn cảnh báo đến Telegram.

#### 1. Tạo Bot Telegram và lấy HTTP API Token
- Mở ứng dụng Telegram, tìm kiếm **@BotFather** (có dấu tích xanh).
- Nhắn lệnh `/newbot` và làm theo hướng dẫn để đặt tên và username cho Bot của bạn.
- Sau khi tạo thành công, BotFather sẽ gửi cho bạn một đoạn **HTTP API Token** (ví dụ: `123456789:ABCdefGHIjkl...`). Hãy copy đoạn token này.

#### 2. Lấy Chat ID của bạn
- Mở Telegram, tìm kiếm **@userinfobot** hoặc **@GetIDs Bot** và nhấn **Start**.
- Bot sẽ trả về cho bạn một dãy số `ID` (ví dụ: `987654321`). Đây chính là `Chat ID` của bạn.
- **Lưu ý:** Bạn cần phải tìm kiếm con Bot vừa tạo ở bước 1, bấm **Start** (Bắt đầu) để cho phép Bot nhắn tin cho bạn.

#### 3. Cập nhật mã nguồn Web (`app_web.py`)
- Mở file `app_web.py`, tìm phần CẤU HÌNH và điền Token và Chat ID của bạn vào:
  ```python
  TELEGRAM_BOT_TOKEN = "ĐIỀN_TOKEN_CỦA_BẠN_VÀO_ĐÂY"
  TELEGRAM_CHAT_ID = "ĐIỀN_CHAT_ID_CỦA_BẠN_VÀO_ĐÂY"
  ```
- Nếu code của bạn chưa có hàm gửi Telegram, hãy chèn thêm đoạn này vào dưới phần kích hoạt MacroDroid:
  ```python
  try:
      telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      requests.post(telegram_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": "🚨 CẢNH BÁO: Phát hiện âm thanh nguy hiểm!"})
      st.toast("📩 Đã gửi cảnh báo qua Telegram!", icon="✈️")
  except Exception as e:
      st.warning(f"Lỗi gửi Telegram: {e}")
  ```

---

## 🎯 Hoàn tất và Trải nghiệm
Bây giờ, hãy thử nghiệm toàn bộ hệ thống:
1. Đảm bảo **Colab** đang chạy.
2. Web **Streamlit** đã cập nhật link Ngrok mới nhất và đang chạy.
3. Điện thoại có kết nối mạng, đang bật **MacroDroid** và đã bấm Start cho Bot **Telegram**.
4. Lên Web, upload một file âm thanh nguy hiểm (như tiếng kính vỡ `tiengkinhvo.wav`) và bấm **Phân tích**.
5. Nhìn lên màn hình Web: Sẽ có cảnh báo đỏ hiện ra.
6. Đồng thời, **điện thoại của bạn sẽ rung lên, phát ra giọng nói, hiển thị thông báo khẩn cấp VÀ có tin nhắn báo động gửi đến Telegram!**

Chúc bạn cài đặt thành công!