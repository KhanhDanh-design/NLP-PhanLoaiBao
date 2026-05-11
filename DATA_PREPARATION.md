# 📊 Hướng dẫn chuẩn bị dữ liệu

Tài liệu này hướng dẫn cách chuẩn bị dữ liệu để huấn luyện mô hình hoặc dự đoán.

## 📁 Format dữ liệu dự kiến

### CSV Format (Dùng để huấn luyện)

**Tên file:** `dataset_tapchi.csv` (hoặc tên khác)

**Cấu trúc:**

```csv
title,summary,content_cleaned,label,category
Tiêu đề bài 1,Tóm tắt bài 1,Nội dung đã làm sạch 1,Giáo dục,Giáo dục
Tiêu đề bài 2,Tóm tắt bài 2,Nội dung đã làm sạch 2,Thể thao,Thể thao
...
```

### Yêu cầu cột bắt buộc:

| Cột               | Kiểu dữ liệu | Mô tả                        | Bắt buộc |
| ----------------- | ------------ | ---------------------------- | -------- |
| `content_cleaned` | String       | Nội dung văn bản đã làm sạch | ✅       |
| `label`           | String       | Danh mục/chủ đề bài báo      | ✅       |
| `title`           | String       | Tiêu đề bài báo              | ❌       |
| `summary`         | String       | Tóm tắt bài báo              | ❌       |

## 🛠️ Cách chuẩn bị dữ liệu

### Từ VnExpress (sử dụng ThuThapBaiBao)

```powershell
# 1. Crawl bài báo
cd d:\Nam_4\HocMay\ThuThapBaiBao
# Chạy crawl.ipynb hoặc crawl_more.ipynb

# 2. Tiền xử lý
# Chạy preprocess.ipynb

# 3. Copy file xử lý xong
Copy-Item "vnexpress_processed.csv" -Destination "d:\Nam_4\HocMay\TongHop\data\"

# 4. Rename nếu cần
Rename-Item "data\vnexpress_processed.csv" "data\dataset_tapchi.csv"
```

### Từ dữ liệu cũ (XuLyBaiBao)

```powershell
# Copy file dataset_tapchi.csv từ XuLyBaiBao
Copy-Item "d:\Nam_4\HocMay\XuLyBaiBao\dataset_tapchi.csv" -Destination "./data/"
```

### Từ dữ liệu tùy chỉnh

Nếu bạn có file dữ liệu khác:

1. **Đảm bảo có 2 cột bắt buộc:**
   - `content_cleaned`: Nội dung văn bản (đã làm sạch)
   - `label`: Danh mục bài báo

2. **Nếu cột có tên khác, sửa trong `train_models.py`:**

   ```powershell
   python train_models.py --csv your_file.csv --text-col your_text_col --label-col your_label_col
   ```

3. **Format dữ liệu:**
   - Encoding: UTF-8
   - Separator: `,` (comma)
   - Header row: Có

## 🧹 Chuẩn bị dữ liệu thô (Raw data)

Nếu bạn có dữ liệu thô chưa xử lý:

### Step 1: Làm sạch văn bản

```python
import pandas as pd
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Xóa HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Xóa URL
    text = re.sub(r'http[s]?://\S+', '', text)
    # Giữ chữ tiếng Việt
    text = re.sub(r'[^\w\s\uAC00-\uD7AF]', ' ', text, flags=re.UNICODE)
    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

df = pd.read_csv("raw_data.csv")
df['content_cleaned'] = df['content'].apply(clean_text)
df.to_csv("dataset_tapchi.csv", index=False, encoding='utf-8-sig')
```

### Step 2: Chuẩn bị nhãn

```python
# Đảm bảo cột label không có giá trị trống
df = df.dropna(subset=['label'])

# Nếu label có nhiều danh mục, có thể gom lại
label_mapping = {
    'category_1': 'Giáo dục',
    'category_2': 'Thể thao',
    # ...
}
df['label'] = df['label'].map(label_mapping)

df.to_csv("dataset_tapchi.csv", index=False, encoding='utf-8-sig')
```

## 📊 Kiểm tra dữ liệu

Trước khi huấn luyện, kiểm tra dữ liệu:

```python
import pandas as pd

# Load dữ liệu
df = pd.read_csv("dataset_tapchi.csv")

# Kiểm tra kích thước
print(f"Shape: {df.shape}")  # (rows, cols)

# Kiểm tra cột
print(f"Columns: {list(df.columns)}")

# Kiểm tra giá trị trống
print(f"\nMissing values:\n{df.isnull().sum()}")

# Kiểm tra phân bố label
print(f"\nLabel distribution:\n{df['label'].value_counts()}")

# Kiểm tra sample
print(f"\nFirst row:\n{df.iloc[0]}")
```

## ⚖️ Cân bằng dữ liệu

Nếu dữ liệu không cân bằng (một danh mục có quá nhiều bài):

```python
from sklearn.utils import resample

df = pd.read_csv("dataset_tapchi.csv")

# Lấy danh mục ít nhất
min_count = df['label'].value_counts().min()

# Resample để cân bằng
balanced_frames = []
for label in df['label'].unique():
    label_df = df[df['label'] == label]
    resampled = resample(label_df, n_samples=min_count, random_state=42)
    balanced_frames.append(resampled)

df_balanced = pd.concat(balanced_frames)
df_balanced.to_csv("dataset_balanced.csv", index=False, encoding='utf-8-sig')
```

## 🚀 Huấn luyện mô hình

Khi dữ liệu đã sẵn sàng:

```powershell
# Chế độ mặc định
python train_models.py --csv dataset_tapchi.csv

# Hoặc chỉ định cột
python train_models.py --csv dataset_tapchi.csv --text-col content_cleaned --label-col label

# Hoặc thay đổi test size
python train_models.py --csv dataset_tapchi.csv --test-size 0.3
```

## 📈 Hướng dẫn tối ưu hóa dữ liệu

### Kích thước dataset

- **Tối thiểu:** 100-200 mẫu
- **Tối ưu:** 1000-10000 mẫu
- **Rất tốt:** > 10000 mẫu

### Phân bố label

- **Cân bằng:** Mỗi danh mục có số mẫu gần nhau
- **Tỷ lệ tối đa:** < 10x (không quá chênh lệch)

### Chất lượng text

- **Độ dài:** 50-1000 ký tự (tối ưu)
- **Làm sạch:** Xóa HTML, ký tự đặc biệt
- **Encoding:** UTF-8

### Chia train/test

- **Mặc định:** 80% train / 20% test
- **Lớn:** 90% train / 10% test
- **Nhỏ:** 70% train / 30% test

## 🔗 Tài liệu liên quan

- [README.md](README.md) - Tài liệu chính
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Hướng dẫn cài đặt
- [QUICKSTART.md](QUICKSTART.md) - Bắt đầu nhanh

---

**Ghi chú:** Chất lượng dữ liệu quyết định chất lượng mô hình. Hãy đầu tư thời gian để chuẩn bị dữ liệu tốt!
