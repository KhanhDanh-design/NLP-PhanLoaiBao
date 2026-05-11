# 🚀 Quick Start - Phân loại báo chí tiếng Việt

Bắt đầu nhanh trong 5 phút!

## 📋 Chuẩn bị

### 1. Copy dữ liệu từ XuLyBaiBao (QUAN TRỌNG)

```powershell
# Copy biểu đồ đánh giá
Copy-Item "d:\Nam_4\HocMay\XuLyBaiBao\chart\*" -Destination "./charts/" -Recurse -Force
```

### 2. Cài đặt

```powershell
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt
.\venv\Scripts\Activate.ps1

# Cài thư viện
pip install -r requirements.txt
```

### 3. Chạy

```powershell
streamlit run app.py
```

**Trình duyệt sẽ mở tại:** `http://localhost:8501`

---

## 🎯 Sử dụng

### Tab 1: Phân loại bài báo

1. Chọn chế độ nhập (URL, Text, hoặc RSS)
2. Nhập/dán dữ liệu
3. Bấm "Phân tích"
4. Xem kết quả từ 3 mô hình

### Tab 2: Đánh giá mô hình

- Xem Confusion Matrix
- Xem bảng Metrics
- Xem tóm tắt kết quả

---

## ⚠️ Lỗi phổ biến

| Lỗi                           | Giải pháp                                                       |
| ----------------------------- | --------------------------------------------------------------- |
| "No module named 'streamlit'" | `pip install streamlit`                                         |
| "Models not found"            | Copy file .pkl từ XuLyBaiBao hoặc chạy `python train_models.py` |
| "Vectorizer not found"        | Chạy `python train_models.py --csv dataset_tapchi.csv`          |

---

## 📖 Xem thêm

- **Hướng dẫn chi tiết:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Tài liệu đầy đủ:** [README.md](README.md)
- **Kiểm tra setup:** `python test_setup.py`

---

## 🆘 Cần giúp?

1. Chạy: `python test_setup.py` để kiểm tra setup
2. Xem console output để tìm lỗi cụ thể
3. Kiểm tra lại SETUP_GUIDE.md hoặc README.md

---

**Chúc bạn thành công! 🎉**
