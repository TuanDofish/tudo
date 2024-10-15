import pandas as pd
import streamlit as st

# Cấu trúc để lưu trữ thông tin của một tiến trình
class TienTrinh:
    def __init__(self, id, thoiGianDen, thoiGianXuLy):
        self.id = id
        self.thoiGianDen = thoiGianDen
        self.thoiGianXuLy = thoiGianXuLy
        self.thoiGianCho = 0
        self.thoiGianHoanTat = 0

# Hàm mô phỏng thuật toán SJF không ưu tiên (Non-preemptive)
def sjf_non_preemptive(tienTrinhs):
    thoiGianHienTai = 0
    daHoanThanh = []
    tienTrinhsConLai = tienTrinhs.copy()
    n = len(tienTrinhs)
    
    while len(daHoanThanh) < n:
        # Lấy các tiến trình đã đến nhưng chưa hoàn thành
        tienTrinhSanSang = [tt for tt in tienTrinhsConLai if tt.thoiGianDen <= thoiGianHienTai]
        
        if tienTrinhSanSang:
            # Chọn tiến trình có thời gian xử lý ngắn nhất
            tienTrinhSanSang.sort(key=lambda x: x.thoiGianXuLy)
            tienTrinhDangChay = tienTrinhSanSang[0]
            
            # Tính thời gian chờ
            tienTrinhDangChay.thoiGianCho = thoiGianHienTai - tienTrinhDangChay.thoiGianDen
            
            # Cập nhật thời gian hiện tại và thời gian hoàn thành
            thoiGianHienTai += tienTrinhDangChay.thoiGianXuLy
            tienTrinhDangChay.thoiGianHoanTat = thoiGianHienTai
            
            # Di chuyển tiến trình sang danh sách đã hoàn thành
            daHoanThanh.append(tienTrinhDangChay)
            tienTrinhsConLai.remove(tienTrinhDangChay)
        else:
            # Nếu không có tiến trình nào sẵn sàng, tăng thời gian hiện tại
            thoiGianHienTai += 1
    
    # Tính thời gian chờ trung bình và thời gian hoàn thành trung bình
    tongThoiGianCho = sum(tt.thoiGianCho for tt in daHoanThanh)
    tongThoiGianHoanTat = sum(tt.thoiGianHoanTat for tt in daHoanThanh)
    thoiGianChoTB = tongThoiGianCho / n
    thoiGianHoanTatTB = tongThoiGianHoanTat / n
    
    return daHoanThanh, thoiGianChoTB, thoiGianHoanTatTB

# Giao diện Streamlit
st.title("Mô phỏng thuật toán SJF (Shortest Job First) với thời gian đến")

n = st.number_input("Nhập số lượng tiến trình:", min_value=1, value=3, step=1)

tienTrinhs = []
st.subheader("Nhập thông tin các tiến trình:")
for i in range(int(n)):
    st.write(f"### Tiến trình {i + 1}")
    tg_den = st.number_input(f"Thời gian đến của Tiến trình {i + 1}:", min_value=0, value=0, step=1, key=f"tg_den_{i}")
    tg_xu_ly = st.number_input(f"Thời gian xử lý của Tiến trình {i + 1}:", min_value=1, value=1, step=1, key=f"tg_xu_ly_{i}")
    tienTrinhs.append(TienTrinh(i + 1, tg_den, tg_xu_ly))

# Nút tính toán
if st.button("Tính toán"):
    # Tính toán theo thuật toán SJF
    ket_qua, thoiGianChoTB, thoiGianHoanTatTB = sjf_non_preemptive(tienTrinhs)
    
    # Hiển thị kết quả
    st.subheader("Kết quả:")
    df = pd.DataFrame([(tt.id, tt.thoiGianDen, tt.thoiGianXuLy, tt.thoiGianCho, tt.thoiGianHoanTat) for tt in ket_qua], 
                      columns=["Tiến trình", "Thời gian đến", "Thời gian xử lý", "Thời gian chờ", "Thời gian hoàn thành"])
    st.dataframe(df)
    
    st.write(f"**Thời gian chờ trung bình:** {thoiGianChoTB:.2f}")
    st.write(f"**Thời gian hoàn thành trung bình:** {thoiGianHoanTatTB:.2f}")
