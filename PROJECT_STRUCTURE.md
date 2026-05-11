# 📂 Cấu trúc dự án - Phân loại báo chí tiếng Việt

Tài liệu này mô tả chi tiết cấu trúc toàn bộ dự án TongHop.

## 📁 Cây thư mục hoàn chỉnh

```
d:\Nam_4\HocMay\TongHop/
│
├── 📄 app.py                          # ⭐ Ứng dụng Streamlit chính
│   └── Chứa giao diện web + logic xử lý
│
├── 📄 crawler.py                      # ⭐ Module crawl bài báo
│   ├── class VnExpressCrawler
│   ├── def crawl_rss(...)
│   ├── def crawl_from_url(...)
│   └── def crawl_multiple_categories(...)
│
├── 📄 text_processor.py               # ⭐ Module xử lý text
│   ├── class TextProcessor
│   ├── def clean_text(...)
│   ├── def tokenize(...)
│   ├── def remove_stopwords(...)
│   ├── def fit_vectorizer(...)
│   └── def transform(...)
│
├── 📄 predictor.py                    # ⭐ Module dự đoán
│   ├── class Predictor
│   ├── def load_models(...)
│   ├── def predict_single(...)
│   ├── def predict_batch(...)
│   └── def get_comparison_table(...)
│
├── 📄 train_models.py                 # ⭐ Script huấn luyện mô hình
│   └── Dùng để train & lưu 3 mô hình
│
├── 📄 config.py                       # ⭐ File cấu hình
│   ├── Đường dẫn thư mục
│   ├── Tham số mô hình
│   ├── Cấu hình crawler
│   └── Helper functions
│
├── 📄 test_setup.py                   # ⭐ Script kiểm tra setup
│   └── Kiểm tra: Python, dependencies, mô hình, v.v.
│
├── 📄 __init__.py                     # Package initialization
│
│
├── 📄 requirements.txt                # Danh sách dependencies
│   ├── streamlit, pandas, numpy
│   ├── scikit-learn, joblib
│   ├── feedparser, beautifulsoup4
│   ├── matplotlib, seaborn
│   └── underthesea
│
│
├── 📂 models/                         # 🎯 Thư mục mô hình
│   ├── model_nb.pkl                  # Naive Bayes model
│   ├── model_svm.pkl                 # SVM Linear model
│   ├── model_dt.pkl                  # Decision Tree model
│   └── vectorizer.pkl                # TF-IDF Vectorizer
│
│
├── 📂 charts/                         # 📊 Thư mục biểu đồ đánh giá
│   ├── confusion_matrix_nb.png       # Confusion matrix (NB)
│   ├── confusion_matrix_svm.png      # Confusion matrix (SVM)
│   ├── confusion_matrix_dt.png       # Confusion matrix (DT)
│   ├── comparison_metrics.csv        # Bảng metrics so sánh
│   └── comparison_summary.md         # Tóm tắt kết quả
│
│
├── 📂 data/                           # 💾 Thư mục dữ liệu tạm thời
│   └── dataset_tapchi.csv            # (Optional) Dữ liệu huấn luyện
│
│
├── 📄 README.md                       # 📖 Tài liệu chính dự án
│
├── 📄 QUICKSTART.md                   # 🚀 Bắt đầu nhanh (5 phút)
│
├── 📄 SETUP_GUIDE.md                  # 📋 Hướng dẫn cài đặt chi tiết
│
├── 📄 DATA_PREPARATION.md             # 📊 Hướng dẫn chuẩn bị dữ liệu
│
├── 📄 PROJECT_STRUCTURE.md            # 📂 Tài liệu này
│
└── 📄 .gitignore                      # Git ignore file
```

---

## 🎯 Module chính (Core Modules)

### 1. **crawler.py** - Crawl dữ liệu

| Thành phần                     | Chức năng            | Sử dụng                                             |
| ------------------------------ | -------------------- | --------------------------------------------------- |
| `VnExpressCrawler`             | Class chính để crawl | `crawler = VnExpressCrawler()`                      |
| `crawl_rss()`                  | Crawl từ RSS feed    | `articles = crawler.crawl_rss("Giáo dục", url)`     |
| `crawl_from_url()`             | Crawl từ URL         | `article = crawler.crawl_from_url("https://...")`   |
| `crawl_multiple_categories()`  | Crawl nhiều danh mục | `articles = crawler.crawl_multiple_categories(...)` |
| `crawl_articles_by_category()` | Hàm tiện ích         | `articles = crawl_articles_by_category("Thể thao")` |

**Input:** URL hoặc danh mục  
**Output:** Dictionary hoặc List[Dict]  
**Format:** `{title, summary, link, category, published}`

---

### 2. **text_processor.py** - Xử lý văn bản

| Thành phần           | Chức năng         | Sử dụng                                       |
| -------------------- | ----------------- | --------------------------------------------- |
| `TextProcessor`      | Class xử lý text  | `processor = TextProcessor()`                 |
| `clean_text()`       | Làm sạch text     | `cleaned = processor.clean_text(text)`        |
| `tokenize()`         | Tách từ           | `tokens = processor.tokenize(text)`           |
| `remove_stopwords()` | Loại bỏ stopwords | `tokens = processor.remove_stopwords(tokens)` |
| `preprocess()`       | Toàn bộ pipeline  | `processed = processor.preprocess(text)`      |
| `fit_vectorizer()`   | Huấn luyện TF-IDF | `processor.fit_vectorizer(texts)`             |
| `transform()`        | Vector hóa        | `vectors = processor.transform(texts)`        |

**Quy trình:** Text → Clean → Tokenize → Remove stopwords → Join → Vector hóa

**Input:** String (text)  
**Output:** String (processed) hoặc Sparse matrix (vectors)

---

### 3. **predictor.py** - Dự đoán

| Thành phần               | Chức năng          | Sử dụng                                     |
| ------------------------ | ------------------ | ------------------------------------------- |
| `Predictor`              | Class dự đoán      | `predictor = Predictor()`                   |
| `load_models()`          | Load 3 mô hình     | `predictor.load_models()`                   |
| `load_vectorizer()`      | Load vectorizer    | `predictor.load_vectorizer()`               |
| `predict_single()`       | Dự đoán 1 text     | `result = predictor.predict_single(text)`   |
| `predict_batch()`        | Dự đoán nhiều text | `results = predictor.predict_batch(texts)`  |
| `predict_dataframe()`    | Dự đoán DataFrame  | `df = predictor.predict_dataframe(df, col)` |
| `get_comparison_table()` | Bảng so sánh       | `table = predictor.get_comparison_table()`  |

**Input:** Text string hoặc List[str]  
**Output:** Dict hoặc List[Dict]  
**Models:** Naive Bayes, SVM, Decision Tree

---

## 🔧 File hỗ trợ

### **config.py** - Cấu hình

Định nghĩa:

- Đường dẫn thư mục (`BASE_DIR`, `MODELS_DIR`, `CHARTS_DIR`, etc.)
- Tham số mô hình
- Tham số crawler
- Tham số training

### **train_models.py** - Huấn luyện mô hình

Script độc lập để:

1. Load dữ liệu từ CSV
2. Train 3 mô hình (NB, SVM, DT)
3. Đánh giá performance
4. Lưu mô hình vào file .pkl

**Chạy:** `python train_models.py --csv dataset_tapchi.csv`

### **test_setup.py** - Kiểm tra setup

Script để kiểm tra:

- ✅ Python version
- ✅ Dependencies cài chưa
- ✅ Cấu trúc thư mục
- ✅ File mô hình có tồn tại

**Chạy:** `python test_setup.py`

---

## 🌐 Ứng dụng Web (Streamlit)

### **app.py** - Giao diện chính

**Cấu trúc:**

```
Sidebar (Giới thiệu + Điều khiển)
│
├── Tab 1: 🔍 Phân loại bài báo
│   ├── Mode 1: 📎 Dán URL
│   ├── Mode 2: ✍️ Dán text
│   ├── Mode 3: 🌐 Crawl RSS
│   └── Hiển thị kết quả (3 model predictions)
│
└── Tab 2: 📊 Đánh giá mô hình
    ├── Confusion Matrix (3 hình)
    ├── Bảng metrics
    └── Tóm tắt kết quả
```

**Features:**

- Caching với `@st.cache_resource`
- Session state management
- Error handling
- Responsive layout

---

## 📦 Thư mục dữ liệu

### **models/** - Mô hình ML

```
models/
├── model_nb.pkl          # Naive Bayes (~1-2 MB)
├── model_svm.pkl         # SVM Linear (~1-2 MB)
├── model_dt.pkl          # Decision Tree (~1-2 MB)
└── vectorizer.pkl        # TF-IDF (~0.5-1 MB)
```

### **charts/** - Biểu đồ đánh giá

```
charts/
├── confusion_matrix_nb.png
├── confusion_matrix_svm.png
├── confusion_matrix_dt.png
├── comparison_metrics.csv
└── comparison_summary.md
```

### **data/** - Dữ liệu tạm

```
data/
└── dataset_tapchi.csv    # (Optional) Dữ liệu training
```

---

## 🔄 Data Flow (Quy trình dữ liệu)

```
┌─────────────────────────────────────────────────────────┐
│ INPUT (Người dùng)                                       │
│  - URL bài báo                                           │
│  - Text trực tiếp                                        │
│  - RSS feed                                              │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│ CRAWLER MODULE (crawler.py)                              │
│  - crawl_rss() / crawl_from_url()                        │
│  - Trả về: {title, summary, link, category}             │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│ TEXT PROCESSING (text_processor.py)                      │
│  1. clean_text(): Xóa HTML, chuẩn hóa                  │
│  2. tokenize(): Tách từ (underthesea)                   │
│  3. remove_stopwords(): Loại bỏ từ vô nghĩa             │
│  4. fit_vectorizer(): Train TF-IDF (nếu cần)            │
│  5. transform(): Vector hóa                             │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│ PREDICTION (predictor.py)                                │
│  - 3 mô hình predict cùng lúc                            │
│  - Naive Bayes predict: danh mục + confidence           │
│  - SVM predict: danh mục + confidence                   │
│  - Decision Tree predict: danh mục + confidence         │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│ OUTPUT (Hiển thị kết quả)                               │
│  - Bảng so sánh 3 mô hình                               │
│  - Consensus vote                                        │
│  - Confidence scores                                     │
│  - Confusion Matrix & Metrics                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎓 Mô hình ML

### Naive Bayes (`model_nb.pkl`)

- **Loại:** Multinomial Naive Bayes
- **Ưu:** Nhanh, ít dữ liệu cũng ok
- **Nhược:** Kém độ chính xác cao
- **Công dụng:** Baseline, nhanh

### SVM Tuyến Tính (`model_svm.pkl`)

- **Loại:** LinearSVC
- **Ưu:** Mạnh, chính xác cao
- **Nhược:** Chậm với dữ liệu lớn
- **Công dụng:** Production, độ chính xác cao

### Decision Tree (`model_dt.pkl`)

- **Loại:** DecisionTreeClassifier
- **Ưu:** Dễ giải thích, tự động feature selection
- **Nhược:** Overfitting nếu quá sâu
- **Công dụng:** Giải thích, debugging

---

## 📊 Performance dự kiến

| Mô hình       | Accuracy   | Training     | Prediction   |
| ------------- | ---------- | ------------ | ------------ |
| Naive Bayes   | ~0.75-0.80 | ⚡ Rất nhanh | ⚡ Rất nhanh |
| SVM           | ~0.80-0.85 | ⚡ Nhanh     | ⚡ Nhanh     |
| Decision Tree | ~0.70-0.75 | ⚡ Rất nhanh | ⚡ Rất nhanh |

---

## 🔐 Security & Error Handling

- **Crawl:** Try-except, timeout handling, rate limit
- **Text:** Null check, encoding handling, regex validation
- **Model:** File existence check, format validation, graceful fallback
- **Web:** Session state management, error messages, input validation

---

## 📚 Dependencies

| Library        | Phiên bản | Tác dụng            |
| -------------- | --------- | ------------------- |
| streamlit      | ≥1.28.0   | Web framework       |
| pandas         | ≥1.5.0    | Data processing     |
| numpy          | ≥1.23.0   | Numerical computing |
| scikit-learn   | ≥1.2.0    | ML models           |
| feedparser     | ≥6.0.0    | RSS parsing         |
| beautifulsoup4 | ≥4.11.0   | HTML parsing        |
| requests       | ≥2.28.0   | HTTP                |
| underthesea    | ≥1.3.3    | Vietnamese NLP      |
| matplotlib     | ≥3.7.0    | Plotting            |
| seaborn        | ≥0.12.0   | Visualization       |
| joblib         | ≥1.2.0    | Model serialization |

---

## 💡 Tip & Tricks

### Tối ưu hóa hiệu năng

1. **Caching:** Dùng `@st.cache_resource` cho model
2. **Batch processing:** Dự đoán nhiều text cùng lúc
3. **Vectorizer reuse:** Load 1 lần, dùng nhiều lần

### Debugging

1. **Chạy test_setup.py** để kiểm tra setup
2. **Check console output** cho error messages
3. **Enable verbose logging** trong config

### Customization

1. **Thêm danh mục RSS:** Sửa `VNEXPRESS_CATEGORIES` trong config
2. **Đổi model:** Train lại với `train_models.py`
3. **Đổi stopwords:** Sửa `VIETNAMESE_STOPWORDS` trong text_processor

---

**Tài liệu cuối cùng cập nhật:** 2024  
**Phiên bản dự án:** 1.0.0
