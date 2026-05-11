# -*- coding: utf-8 -*-
"""
TongHop - Full-stack ML Pipeline cho phân loại báo chí tiếng Việt

Package tích hợp:
- crawler: Cào dữ liệu bài báo từ VnExpress
- text_processor: Tiền xử lý văn bản tiếng Việt
- predictor: Dự đoán danh mục bằng 3 mô hình ML

Cách dùng:
    >>> from crawler import VnExpressCrawler
    >>> from text_processor import TextProcessor
    >>> from predictor import Predictor

Tác giả: Full-stack AI/ML Engineer
Phiên bản: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Full-stack AI/ML Engineer"

# Import các module chính
try:
    from .crawler import VnExpressCrawler, crawl_from_link, crawl_articles_by_category
    from .text_processor import TextProcessor, quick_preprocess
    from .predictor import Predictor, create_and_load_predictor
    from .config import (
        BASE_DIR, MODELS_DIR, CHARTS_DIR, DATA_DIR,
        MODEL_NAMES, get_model_path, get_vectorizer_path,
        check_models_exist, check_vectorizer_exist
    )
except ImportError as e:
    print(f"⚠️  Cảnh báo: Không thể import một số module: {e}")

__all__ = [
    'VnExpressCrawler',
    'crawl_from_link',
    'crawl_articles_by_category',
    'TextProcessor',
    'quick_preprocess',
    'Predictor',
    'create_and_load_predictor',
    'BASE_DIR',
    'MODELS_DIR',
    'CHARTS_DIR',
    'DATA_DIR',
    'MODEL_NAMES',
    'get_model_path',
    'get_vectorizer_path',
    'check_models_exist',
    'check_vectorizer_exist',
]
