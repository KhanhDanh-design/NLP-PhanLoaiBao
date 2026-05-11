# 📋 Hướng dẫn cài đặt từng bước - TongHop

Tài liệu này hướng dẫn chi tiết cách thiết lập và chạy ứng dụng phân loại báo chí tiếng Việt.

## 🎯 Yêu cầu

- Python 3.8+ (khuyến nghị 3.10+)
- pip (Python package manager)
- ~500MB dung lượng đĩa trống

## 📋 Danh sách các bước

1. ✅ Sao chép mô hình từ XuLyBaiBao
2. ✅ Cài đặt môi trường Python
3. ✅ Cài đặt dependencies
4. ✅ Huấn luyện/Chuẩn bị mô hình
5. ✅ Chạy ứng dụng

---

## 🔄 Bước 1: Sao chép mô hình từ XuLyBaiBao

### 1a. Sao chép dữ liệu huấn luyện (Tùy chọn)

Nếu bạn muốn huấn luyện lại mô hình từ đầu:

```powershell
# Copy file dataset từ XuLyBaiBao
Copy-Item "d:\Nam_4\HocMay\XuLyBaiBao\*.csv" -Destination "d:\Nam_4\HocMay\TongHop\data\" -Force

# Hoặc manual copy file dataset_tapchi.csv vào TongHop/data/
```

### 1b. Sao chép biểu đồ đánh giá (QUAN TRỌNG)

```powershell
# Copy thư mục charts (chứa confusion matrix & metrics)
Copy-Item "d:\Nam_4\HocMay\XuLyBaiBao\chart\*" -Destination "d:\Nam_4\HocMay\TongHop\charts\" -Recurse -Force

# Hoặc manual copy:
# - confusion_matrix_nb.png
# - confusion_matrix_svm.png
# - confusion_matrix_dt.png
# - comparison_metrics.csv
# - comparison_summary.md
```

---

## 🐍 Bước 2: Cài đặt môi trường Python

### Cách 2a: Tạo môi trường ảo (VirtualEnv) - **KHUYẾN NGHỊ**

```powershell
# Mở PowerShell trong thư mục TongHop
cd d:\Nam_4\HocMay\TongHop

# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows PowerShell:
.\venv\Scripts\Activate.ps1

# (Sau kích hoạt, bạn sẽ thấy (venv) ở đầu dòng lệnh)
```

**Lưu ý:** Nếu gặp lỗi "cannot be loaded because running scripts is disabled":

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Cách 2b: Dùng môi trường Python global (Không khuyến nghị)

Nếu bạn không muốn tạo môi trường ảo, bạn có thể dùng Python global (nhưng có thể gây xung đột thư viện).

---

## 📦 Bước 3: Cài đặt Dependencies

### 3a. Cài đặt từ requirements.txt

```powershell
# Đảm bảo môi trường ảo đã được kích hoạt (nếu dùng)
# Cài đặt tất cả thư viện
pip install -r requirements.txt
```

### 3b. Nếu gặp lỗi underthesea

Một số user gặp lỗi khi cài underthesea. Nếu gặp:

```powershell
# Cách 1: Cài riêng
pip install underthesea

# Cách 2: Nếu vẫn lỗi, dùng phiên bản cũ
pip install underthesea==1.3.3

# Cách 3: Nếu không cần tokenization tiếng Việt, có thể bỏ qua
# (App sẽ fallback thành split() thay thế)
```

### Kiểm tra cài đặt thành công

```powershell
# Test import các thư viện quan trọng
python -c "import streamlit; import sklearn; import pandas; print('✅ OK')"
```

---

## 🤖 Bước 4: Huấn luyện/Chuẩn bị mô hình

### Cách 4a: Nếu bạn muốn huấn luyện lại mô hình

**Điều kiện:** Bạn phải có file `dataset_tapchi.csv` trong TongHop (copy từ XuLyBaiBao)

```powershell
# Chắc chắn đã kích hoạt môi trường ảo
cd d:\Nam_4\HocMay\TongHop

# Chạy script training
python train_models.py --csv dataset_tapchi.csv --output-dir ./models
```

**Kết quả:**

```
✅ TRAINING HOÀN TẤT!

📂 Các file mô hình nằm tại: ./models/
   - model_nb.pkl
   - model_svm.pkl
   - model_dt.pkl
   - vectorizer.pkl
```

Quá trình này sẽ mất vài phút tùy vào kích thước dataset.

### Cách 4b: Nếu bạn chỉ muốn dùng mô hình có sẵn

Bạn có thể bỏ qua bước này nếu đã copy file mô hình từ XuLyBaiBao hoặc từ người khác.

**Kiểm tra:**

```powershell
# Xem thư mục models có file .pkl không
ls .\models\
```

Sẽ thấy:

```
model_nb.pkl
model_svm.pkl
model_dt.pkl
vectorizer.pkl
```

---

## 🚀 Bước 5: Chạy ứng dụng

### 5a. Khởi động Streamlit App

```powershell
# Chắc chắn đang ở thư mục TongHop
cd d:\Nam_4\HocMay\TongHop

# Chạy app
streamlit run app.py
```

### 5b. Kết quả

```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Trình duyệt sẽ tự động mở URL này.**

### 5c. Sử dụng ứng dụng

1. **Sidebar:** Đọc giới thiệu và kiểm tra mô hình đã load
2. **Tab "Phân loại bài báo":**
   - Chọn chế độ nhập (URL, Text, hoặc RSS)
   - Nhập/dán dữ liệu
   - Bấm nút "Phân tích"
   - Xem kết quả từ 3 mô hình

3. **Tab "Đánh giá mô hình":**
   - Xem Confusion Matrix
   - Xem bảng Metrics
   - Xem tóm tắt kết quả

---

## 🐛 Troubleshooting

### Lỗi 1: "No module named 'streamlit'"

**Nguyên nhân:** Thư viện chưa cài

**Giải pháp:**

```powershell
pip install streamlit
```

### Lỗi 2: "Models not found in ./models"

**Nguyên nhân:** Thư mục models trống hoặc không tồn tại

**Giải pháp:**

- Copy file .pkl từ XuLyBaiBao, HOẶC
- Chạy: `python train_models.py --csv dataset_tapchi.csv`

### Lỗi 3: "No module named 'underthesea'"

**Nguyên nhân:** underthesea chưa cài (thường là lỗi cài)

**Giải pháp:**

```powershell
pip install underthesea --upgrade
```

Nếu vẫn lỗi, app vẫn sử dụng được (sẽ dùng split() thay thế)

### Lỗi 4: Streamlit không mở trình duyệt

**Nguyên nhân:** Cổng 8501 bị chiếm hoặc firewall chặn

**Giải pháp:**

```powershell
# Dùng cổng khác
streamlit run app.py --server.port 8502
```

Sau đó truy cập: `http://localhost:8502`

### Lỗi 5: "Vectorizer not found"

**Nguyên nhân:** File vectorizer.pkl không tồn tại

**Giải pháp:**

- Copy vectorizer.pkl từ XuLyBaiBao (nếu có), HOẶC
- Chạy lại: `python train_models.py`

### Lỗi 6: Crawl VnExpress lỗi hoặc timeout

**Nguyên nhân:**

- URL không đúng
- VnExpress rate-limit
- Kết nối internet yếu

**Giải pháp:**

- Kiểm tra URL: phải là link bài báo VnExpress
- Chờ 1-2 phút rồi thử lại
- Dùng chế độ "Dán văn bản" thay vì "Dán URL"

---

## ✅ Checklist Setup

- [ ] Copy data từ XuLyBaiBao (nếu cần train)
- [ ] Copy charts từ XuLyBaiBao ✨ **QUAN TRỌNG**
- [ ] Tạo venv: `python -m venv venv`
- [ ] Kích hoạt venv: `.\venv\Scripts\Activate.ps1`
- [ ] Cài dependencies: `pip install -r requirements.txt`
- [ ] Kiểm tra mô hình: `ls .\models\`
- [ ] Train nếu cần: `python train_models.py --csv ...`
- [ ] Chạy app: `streamlit run app.py`
- [ ] Truy cập: `http://localhost:8501`

---

## 📞 Ghi chú

- **Lần đầu:** Setup sẽ mất 10-15 phút
- **Lần sau:** Chỉ cần kích hoạt venv + `streamlit run app.py`
- **Tắt app:** Bấm `Ctrl+C` trong terminal
- **Kích hoạt venv lần tới:**
  ```powershell
  cd d:\Nam_4\HocMay\TongHop
  .\venv\Scripts\Activate.ps1
  streamlit run app.py
  ```

---

**Chúc bạn thành công! 🎉**

Nếu gặp vấn đề, kiểm tra lại README.md hoặc console output để tìm lỗi chi tiết.
