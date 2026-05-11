# -*- coding: utf-8 -*-
"""
Configuration file cho ứng dụng phân loại báo chí tiếng Việt.

Định nghĩa các hằng số, đường dẫn, và cấu hình mặc định.

Tác giả: Full-stack AI/ML Engineer
"""

import os
from pathlib import Path

# ============================================================================
# ĐƯỜNG DẪN (PATHS)
# ============================================================================

# Thư mục gốc (TongHop)
BASE_DIR = Path(__file__).parent

# Các thư mục con
MODELS_DIR = BASE_DIR / "models"
CHARTS_DIR = BASE_DIR / "charts"
DATA_DIR = BASE_DIR / "data"

# Tạo thư mục nếu chưa tồn tại
MODELS_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CẤU HÌNH MÔ HÌNH
# ============================================================================

# Tên file mô hình
MODEL_NAMES = {
    "nb": "Naive Bayes",
    "svm": "SVM Tuyến Tính",
    "dt": "Decision Tree"
}

MODEL_FILES = {
    "nb": "model_nb.pkl",
    "svm": "model_svm.pkl",
    "dt": "model_dt.pkl"
}

# File vectorizer
VECTORIZER_FILE = "vectorizer.pkl"

# ============================================================================
# CẤU HÌNH TEXT PROCESSING
# ============================================================================

# Dùng stopwords khi tiền xử lý
USE_STOPWORDS = True

# TF-IDF configuration
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 1)
TFIDF_MIN_DF = 2
TFIDF_MAX_DF = 0.95

# ============================================================================
# CẤU HÌNH CRAWLER
# ============================================================================

# Timeout khi crawl (giây)
CRAWLER_TIMEOUT = 10

# Delay giữa các request (giây)
CRAWLER_DELAY = 0.5

# Danh sách chuyên mục VnExpress
VNEXPRESS_CATEGORIES = {
    "Giáo dục": "https://vnexpress.net/rss/giao-duc.rss",
    "Thể thao": "https://vnexpress.net/rss/the-thao.rss",
    "Kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "Giải trí": "https://vnexpress.net/rss/giai-tri.rss",
    "Khoa học công nghệ": "https://vnexpress.net/rss/khoa-hoc-cong-nghe.rss",
    "Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
    "Sức khỏe": "https://vnexpress.net/rss/suc-khoe.rss",
}

# ============================================================================
# CẤU HÌNH STREAMLIT
# ============================================================================

# Tiêu đề app
APP_TITLE = "📰 Phân loại báo chí tiếng Việt"
APP_DESCRIPTION = "Full-stack ML Pipeline cho phân loại bài báo"

# Số items tối đa hiển thị
MAX_ARTICLES_DISPLAY = 10

# ============================================================================
# CẤU HÌNH TRAINING
# ============================================================================

# Test size khi train
TRAIN_TEST_SIZE = 0.2

# Random state (để tái lập kết quả)
RANDOM_STATE = 42

# Decision Tree parameters
DT_MAX_DEPTH = 100
DT_MIN_SAMPLES_SPLIT = 5
DT_CRITERION = "entropy"

# SVM parameters
SVM_MAX_ITER = 2000

# ============================================================================
# CẤU HÌNH LOGGING
# ============================================================================

# Log level
LOG_LEVEL = "INFO"

# ============================================================================
# HÀM HELPER
# ============================================================================

def get_model_path(model_key: str) -> Path:
    """Lấy đường dẫn file mô hình."""
    return MODELS_DIR / MODEL_FILES.get(model_key, "")


def get_vectorizer_path() -> Path:
    """Lấy đường dẫn file vectorizer."""
    return MODELS_DIR / VECTORIZER_FILE


def check_models_exist() -> dict:
    """
    Kiểm tra các file mô hình có tồn tại không.
    
    Returns:
        Dict {model_name: bool} - True nếu file tồn tại
    """
    result = {}
    for model_key in MODEL_FILES.keys():
        path = get_model_path(model_key)
        result[model_key] = path.exists()
    return result


def check_vectorizer_exist() -> bool:
    """Kiểm tra vectorizer có tồn tại không."""
    return get_vectorizer_path().exists()


# ============================================================================
# DEBUGGING
# ============================================================================

if __name__ == "__main__":
    print("Cấu hình ứng dụng:")
    print(f"  BASE_DIR: {BASE_DIR}")
    print(f"  MODELS_DIR: {MODELS_DIR}")
    print(f"  CHARTS_DIR: {CHARTS_DIR}")
    print(f"  DATA_DIR: {DATA_DIR}")
    print()
    
    models_status = check_models_exist()
    print("Trạng thái mô hình:")
    for model_key, exists in models_status.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {MODEL_NAMES[model_key]}: {models_status[model_key]}")
    
    print()
    vectorizer_status = check_vectorizer_exist()
    status = "✅" if vectorizer_status else "❌"
    print(f"  {status} Vectorizer: {vectorizer_status}")
