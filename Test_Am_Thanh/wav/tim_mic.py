import pyaudio

p = pyaudio.PyAudio()
print("--- DANH SÁCH MICRO TRÊN MÁY TÍNH ---")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    # Chỉ lọc ra những thiết bị có khả năng thu âm (maxInputChannels > 0)
    if dev['maxInputChannels'] > 0:
        print(f"ID {i}: {dev['name']}")

p.terminate()