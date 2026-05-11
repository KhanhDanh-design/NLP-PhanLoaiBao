# 📰 Phân loại Báo chí Tiếng Việt - Full Stack ML Pipeline

Một ứng dụng web hoàn chỉnh để phân loại bài báo tiếng Việt từ VnExpress sử dụng 3 mô hình Machine Learning.

## 🎯 Tính năng chính

### 1. **Crawl bài báo** 📡

- Crawl từ RSS feed theo danh mục (Giáo dục, Thể thao, Kinh doanh, v.v.)
- Crawl từ URL cụ thể
- Dán trực tiếp nội dung văn bản

### 2. **Tiền xử lý văn bản** 🛠️

- Làm sạch HTML, ký tự đặc biệt
- Tách từ (tokenization) cho tiếng Việt
- Loại bỏ stopwords
- Vector hóa TF-IDF

### 3. **Dự đoán 3 mô hình** 🎯

- **Naive Bayes** (NB) - Nhanh, nhẹ
- **SVM Tuyến Tính** (SVM) - Mạnh, cân bằng
- **Decision Tree** (DT) - Dễ giải thích

### 4. **So sánh kết quả** 📊

- Bảng so sánh kết quả từ 3 mô hình
- Tính toán Consensus
- Hiển thị Confusion Matrix
- Bảng metrics (Accuracy, Precision, Recall, F1)

## 📁 Cấu trúc thư mục

```
TongHop/
├── app.py                          # Ứng dụng Streamlit chính
├── crawler.py                      # Module crawl bài báo
├── text_processor.py               # Module xử lý text
├── predictor.py                    # Module dự đoán mô hình
├── requirements.txt                # Dependencies
├── README.md                       # Tài liệu này
│
├── models/                         # Thư mục mô hình (cần copy từ XuLyBaiBao)
│   ├── model_nb.pkl               # Mô hình Naive Bayes
│   ├── model_svm.pkl              # Mô hình SVM
│   └── model_dt.pkl               # Mô hình Decision Tree
│
├── charts/                         # Thư mục biểu đồ (cần copy từ XuLyBaiBao)
│   ├── confusion_matrix_nb.png
│   ├── confusion_matrix_svm.png
│   ├── confusion_matrix_dt.png
│   ├── comparison_metrics.csv
│   └── comparison_summary.md
│
└── data/                           # Thư mục dữ liệu tạm thời
    └── (các file CSV tạm thời)
```

## 🚀 Cách chạy

### 1. **Cài đặt môi trường**

#### Bước 1a: Tạo môi trường ảo Python (Tùy chọn nhưng khuyến nghị)

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### Bước 1b: Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

Nếu gặp lỗi underthesea, bạn có thể cài thêm:

```powershell
pip install underthesea
```

### 2. **Chuẩn bị dữ liệu mô hình**

**QUAN TRỌNG:** Copy 3 file mô hình và thư mục charts từ `XuLyBaiBao`:

```powershell
# Từ thư mục XuLyBaiBao, copy các mô hình đã train
# Copy file mô hình (.pkl) vào TongHop/models/
# Copy thư mục charts vào TongHop/

# Ví dụ cấu trúc sau copy:
# TongHop/models/
#   ├── model_nb.pkl
#   ├── model_svm.pkl
#   └── model_dt.pkl
#
# TongHop/charts/
#   ├── confusion_matrix_*.png
#   ├── comparison_metrics.csv
#   └── comparison_summary.md
```

### 3. **Chạy ứng dụng**

```powershell
# Từ thư mục TongHop
streamlit run app.py
```

Trình duyệt sẽ tự động mở tại `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### **Tab 1: 🔍 Phân loại bài báo**

#### Chế độ 1: Dán URL

1. Chọn "📎 Dán URL"
2. Nhập URL bài báo VnExpress
3. Bấm "🚀 Crawl và phân tích"
4. Xem kết quả dự đoán từ 3 mô hình

Ví dụ URL:

```
https://vnexpress.net/giao-duc/...
```

#### Chế độ 2: Dán văn bản

1. Chọn "✍️ Dán văn bản"
2. Dán hoặc nhập nội dung bài báo
3. Bấm "🚀 Phân tích"
4. Xem kết quả

#### Chế độ 3: Crawl từ RSS

1. Chọn "🌐 Crawl từ RSS"
2. Chọn danh mục (Giáo dục, Thể thao, v.v.)
3. Đặt số bài tối đa
4. Bấm "🚀 Crawl và phân tích"
5. Chọn bài báo cần phân tích từ danh sách

### **Tab 2: 📊 Đánh giá mô hình**

- **Confusion Matrix**: Xem sai số phân loại từ 3 mô hình
- **Bảng metrics**: So sánh Accuracy, Precision, Recall, F1
- **Tóm tắt**: Phân tích chi tiết kết quả

## 🔄 Quy trình hoạt động

```
┌─────────────────┐
│  INPUT (Text)   │
│ - URL           │
│ - Direct text   │
│ - RSS feed      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   CRAWLER               │
│ - crawl_from_url()      │
│ - crawl_rss()           │
│ - crawl_multiple()      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  TEXT PROCESSOR         │
│ - clean_text()          │
│ - tokenize()            │
│ - remove_stopwords()    │
│ - fit_vectorizer()      │
│ - transform()           │
└────────┬────────────────┘
         │
         ▼
    TF-IDF VECTORS
         │
         ▼
┌──────────────────────────────┐
│   3 MODELS PREDICTION        │
│ ├─ Naive Bayes               │
│ ├─ SVM Tuyến Tính            │
│ └─ Decision Tree             │
└────────┬─────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  OUTPUT (Result)        │
│ - 3 Predictions         │
│ - Confidence scores     │
│ - Consensus             │
│ - Comparison table      │
└─────────────────────────┘
```

## 🛠️ API Module

### **crawler.py**

```python
from crawler import VnExpressCrawler

# Tạo crawler
crawler = VnExpressCrawler()

# Crawl từ RSS
articles = crawler.crawl_rss("Giáo dục", "https://vnexpress.net/rss/giao-duc.rss")

# Crawl từ URL
article = crawler.crawl_from_url("https://vnexpress.net/...")

# Lưu CSV
crawler.save_to_csv(articles, "articles.csv")
```

### **text_processor.py**

```python
from text_processor import TextProcessor, quick_preprocess

# Tạo processor
processor = TextProcessor(use_stopwords=True)

# Tiền xử lý
processed = processor.preprocess("Bài báo tiếng Việt...")

# Vector hóa
processor.fit_vectorizer(texts)
vectors = processor.transform(texts)

# Lưu vectorizer
processor.save_vectorizer("vectorizer.pkl")
```

### **predictor.py**

```python
from predictor import Predictor, create_and_load_predictor

# Tạo và load predictor
predictor = create_and_load_predictor(models_dir="./models")

# Dự đoán single
result = predictor.predict_single("Nội dung bài báo...")

# Dự đoán batch
results = predictor.predict_batch(texts)

# Lấy bảng so sánh
comparison_table = predictor.get_comparison_table()
```

## 📊 Kết quả mô hình

Dự kiến các mô hình có hiệu suất:

| Mô hình        | Accuracy   | Precision  | Recall     | F1-score   |
| -------------- | ---------- | ---------- | ---------- | ---------- |
| Naive Bayes    | ~0.75-0.80 | ~0.75-0.80 | ~0.75-0.80 | ~0.75-0.80 |
| SVM Tuyến Tính | ~0.80-0.85 | ~0.80-0.85 | ~0.80-0.85 | ~0.80-0.85 |
| Decision Tree  | ~0.70-0.75 | ~0.70-0.75 | ~0.70-0.75 | ~0.70-0.75 |

_(Thực tế phụ thuộc vào dữ liệu huấn luyện)_

## 🐛 Troubleshooting

### Lỗi: "ModuleNotFoundError: No module named 'underthesea'"

**Giải pháp:**

```powershell
pip install underthesea
```

### Lỗi: "Models not found in ./models"

**Giải pháp:** Copy file mô hình (.pkl) từ `XuLyBaiBao` vào `TongHop/models/`

### Lỗi: "Vectorizer not found"

**Giải pháp:** Có thể tạo lại vectorizer hoặc copy file vectorizer.pkl

### Crawl bị slow / timeout

**Giải pháp:**

- Giảm `max_items`
- Kiểm tra kết nối internet
- VnExpress có thể rate-limit, chờ 1-2 phút rồi thử lại

## 📝 Ghi chú kỹ thuật

### OOP & Module Design

- **Crawler**: Class `VnExpressCrawler` + hàm tiện ích
- **TextProcessor**: Class `TextProcessor` + static methods
- **Predictor**: Class `Predictor` + hàm cấp cao

### Error Handling

- Try-except ở mọi bước crawl/xử lý
- Logging thân thiện với người dùng
- Fallback options (ví dụ: split() thay underthesea)

### Performance

- Caching Streamlit (`@st.cache_resource`)
- Lazy loading của mô hình
- Parallel processing có thể áp dụng

## 🚀 Hướng phát triển tương lai

- [ ] Thêm mô hình PhoBERT/multilingual
- [ ] Fine-tuning trên bộ dữ liệu cụ thể
- [ ] API backend (FastAPI/Flask)
- [ ] Database lưu kết quả dự đoán
- [ ] Dashboard visualizations
- [ ] Batch prediction từ file CSV
- [ ] Model versioning & A/B testing

## 📞 Liên hệ & Hỗ trợ

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra README này
2. Kiểm tra console output
3. Đảm bảo file mô hình trong `models/` folder

## 📄 License

Dự án này là sản phẩm của buổi học Machine Learning.

---

**Tác giả:** Full-stack AI/ML Engineer  
**Ngày tạo:** 2024  
**Phiên bản:** 1.0.0
