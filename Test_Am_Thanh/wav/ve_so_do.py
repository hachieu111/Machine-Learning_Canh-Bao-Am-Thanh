import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Thiết lập kích thước khung hình (Độ phân giải cao)
fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off') # Ẩn trục tọa độ

# Hàm hỗ trợ vẽ các khối hộp vuông
def draw_box(x, y, w, h, text, color='#f0f8ff', border='#0078d4'):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=2", 
                                  linewidth=2, edgecolor=border, facecolor=color)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
            fontsize=11, fontweight='bold', color='#333333', linespacing=1.5)

# Hàm hỗ trợ vẽ khối hình trụ (CSDL)
def draw_database(x, y, w, h, text):
    ellipse_top = patches.Ellipse((x + w/2, y + h), w, h/4, edgecolor='#0078d4', facecolor='#e3f2fd', linewidth=2)
    ellipse_bottom = patches.Arc((x + w/2, y), w, h/4, theta1=180, theta2=360, edgecolor='#0078d4', linewidth=2)
    rect = patches.Rectangle((x, y), w, h, facecolor='#e3f2fd', edgecolor='none')
    line_l = patches.ConnectionPatch((x, y), (x, y+h), "data", "data", edgecolor='#0078d4', linewidth=2)
    line_r = patches.ConnectionPatch((x+w, y), (x+w, y+h), "data", "data", edgecolor='#0078d4', linewidth=2)
    
    ax.add_patch(rect)
    ax.add_patch(ellipse_top)
    ax.add_patch(ellipse_bottom)
    ax.add_artist(line_l)
    ax.add_artist(line_r)
    ax.text(x + w/2, y + h/2.5, text, ha='center', va='center', fontsize=10, fontweight='bold', color='#333333')

# Hàm vẽ mũi tên (ĐÃ ĐƯỢC NÂNG CẤP ĐỂ CHỮNG ĐÈ)
def draw_arrow(x1, y1, x2, y2, text="", text_offset=(0, 0)):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=2, color='#555555'))
    if text:
        # Tính toán vị trí, cộng thêm offset và thêm nền trắng (bbox) để chữ tách bạch khỏi đường kẻ
        ax.text((x1+x2)/2 + text_offset[0], (y1+y2)/2 + text_offset[1], text, 
                ha='center', va='center', fontsize=9, color='#d32f2f', fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=2)) 

# ==========================================
# TIẾN HÀNH VẼ CÁC KHỐI KIẾN TRÚC
# ==========================================

# 1. Tầng Client
draw_box(40, 85, 20, 8, "THIẾT BỊ NGƯỜI DÙNG\n(Trình duyệt / Micro)", color='#e1f5fe')

# 2. Tầng Giao diện
draw_box(35, 65, 30, 10, "FRONTEND\n(Giao diện Web Streamlit)", color='#fff9c4', border='#fbc02d')

# 3. Tầng Xử lý
draw_box(30, 40, 40, 12, "BACKEND SERVER\n(Flask API trên Google Colab)", color='#c8e6c9', border='#388e3c')

# Chú thích đường truyền Ngrok (thêm nền trắng cho chữ)
ax.annotate("Kết nối Tunnel (Ngrok HTTPS)", xy=(50, 65), xytext=(50, 52),
            arrowprops=dict(arrowstyle="<|-|>", lw=2, color='#1976d2', ls='dashed'),
            ha='center', va='center', fontsize=10, fontweight='bold', color='#1976d2',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=2))

# 4. Tầng Lõi
draw_box(8, 15, 22, 10, "AI ENGINE\n(Mô hình YAMNet)", color='#ffccbc', border='#e64a19')
draw_database(42, 15, 16, 10, "DATABASE\n(SQLite)")
draw_box(70, 15, 22, 10, "HỆ THỐNG CẢNH BÁO\n(Telegram / MacroDroid)", color='#d1c4e9', border='#512da8')

# ==========================================
# KẾT NỐI LUỒNG DỮ LIỆU BẰNG MŨI TÊN
# ==========================================
draw_arrow(50, 85, 50, 75) # User -> Frontend

# ĐÃ FIX: Tách 2 mũi tên gửi/nhận giữa Backend và AI ra 2 đường song song, và dịch chữ ra 2 hướng
draw_arrow(32, 40, 16, 25, "Gửi Audio", text_offset=(-4, 3))   # Dịch chữ lên trên, sang trái
draw_arrow(22, 25, 38, 40, "Kết quả %", text_offset=(4, -3)) # Dịch chữ xuống dưới, sang phải

# Các mũi tên khác
draw_arrow(50, 40, 50, 25, "Lưu Log") 
draw_arrow(65, 40, 81, 25, "Gửi Webhook") 

# ==========================================
# TIÊU ĐỀ VÀ LƯU ẢNH
# ==========================================
plt.text(50, 98, "SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG AI SOUND GUARD", 
         ha='center', fontsize=16, fontweight='heavy', color='#2c3e50')

plt.tight_layout()

# Lưu thành file ảnh HD
plt.savefig('So_Do_Kien_Truc_He_Thong_Fix.png', dpi=300, bbox_inches='tight')
print("✅ Đã vẽ và lưu thành công file mới: So_Do_Kien_Truc_He_Thong_Fix.png")