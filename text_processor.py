# -*- coding: utf-8 -*-
"""
Module tiền xử lý văn bản tiếng Việt.

Cấp các hàm để:
- Làm sạch text (xóa HTML, ký tự đặc biệt, chuẩn hóa)
- Tách từ (tokenization) sử dụng underthesea
- Loại bỏ stopwords
- Vector hóa văn bản (TF-IDF)

Tác giả: Full-stack AI/ML Engineer
"""

import re
from typing import List, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

try:
    from underthesea import word_tokenize
    UNDERTHESEA_AVAILABLE = True
except ImportError:
    UNDERTHESEA_AVAILABLE = False
    print("⚠️  underthesea chưa được cài. Sử dụng split() thay thế.")


# Danh sách stopwords tiếng Việt cơ bản
VIETNAMESE_STOPWORDS = {
    "và", "của", "là", "có", "trong", "được", "cho", "với",
    "các", "đã", "này", "một", "về", "không", "để", "theo",
    "tại", "từ", "khi", "đến", "những", "như", "sau", "trên",
    "người", "năm", "cũng", "đó", "hay", "vào", "ra", "lên",
    "thì", "hoặc", "hay", "nhưng", "mà", "cái", "chiếc", "những",
    "bị", "lại", "còn", "vẫn", "nên", "xong", "rồi", "hơn",
    "ít", "nhiều", "ngoài", "trong", "dưới", "trước", "sau",
    "nó", "nó", "tôi", "bạn", "chúng", "anh", "em"
}


class TextProcessor:
    """
    Class xử lý text tiếng Việt.
    
    Hỗ trợ:
    - Làm sạch text
    - Tokenization
    - Loại bỏ stopwords
    - TF-IDF vectorization
    """
    
    def __init__(self, use_stopwords: bool = True, 
                 tfidf_max_features: int = 5000,
                 tfidf_ngram_range: Tuple[int, int] = (1, 1)):
        """
        Khởi tạo TextProcessor.
        
        Args:
            use_stopwords: Có loại bỏ stopwords hay không
            tfidf_max_features: Số feature tối đa cho TF-IDF
            tfidf_ngram_range: Khoảng n-gram (1,1) = unigram
        """
        self.use_stopwords = use_stopwords
        self.tfidf_max_features = tfidf_max_features
        self.tfidf_ngram_range = tfidf_ngram_range
        self.vectorizer = None
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Làm sạch text: xóa HTML, ký tự đặc biệt, chuẩn hóa khoảng trắng.
        
        Args:
            text: Text cần xử lý
        
        Returns:
            Text đã được làm sạch
        """
        # Xử lý trường hợp input không phải string
        if not isinstance(text, str):
            return ""
        
        # Xóa HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Xóa URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Giữ lại chữ cái tiếng Việt, số, và khoảng trắng
        # Pattern này giữ: a-z, A-Z, 0-9, và tất cả ký tự có dấu tiếng Việt
        text = re.sub(
            r'[^a-zA-Z0-9\sáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]',
            ' ',
            text
        )
        
        # Xóa khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Chuyển thành chữ thường (lowercase)
        return text.lower()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tách từ (tokenization).
        
        Ưu tiên dùng underthesea nếu có, nếu không dùng split().
        
        Args:
            text: Text cần tách
        
        Returns:
            Danh sách tokens
        """
        if UNDERTHESEA_AVAILABLE:
            try:
                tokens = word_tokenize(text, format="text").split()
                return tokens
            except Exception as e:
                print(f"⚠️  Lỗi khi dùng underthesea: {e}. Dùng split() thay thế.")
                return text.split()
        else:
            return text.split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Loại bỏ stopwords khỏi danh sách tokens.
        
        Args:
            tokens: Danh sách tokens
        
        Returns:
            Danh sách tokens sau khi loại bỏ stopwords
        """
        if not self.use_stopwords:
            return tokens
        
        return [t for t in tokens if t not in VIETNAMESE_STOPWORDS and len(t) > 1]
    
    def preprocess(self, text: str) -> str:
        """
        Toàn quy trình tiền xử lý: clean -> tokenize -> remove stopwords.
        
        Args:
            text: Text cần xử lý
        
        Returns:
            Text đã được xử lý (các token được join lại bằng dấu cách)
        """
        # Bước 1: Làm sạch
        cleaned = self.clean_text(text)
        
        # Bước 2: Tách từ
        tokens = self.tokenize(cleaned)
        
        # Bước 3: Loại bỏ stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Bước 4: Join lại thành string
        return " ".join(tokens)
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """
        Tiền xử lý một danh sách text.
        
        Args:
            texts: Danh sách text
        
        Returns:
            Danh sách text đã được xử lý
        """
        return [self.preprocess(text) for text in texts]
    
    def preprocess_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Tiền xử lý một cột text trong DataFrame.
        
        Args:
            df: DataFrame
            text_column: Tên cột chứa text
        
        Returns:
            DataFrame mới với cột 'processed_text' được thêm vào
        """
        df_copy = df.copy()
        df_copy['processed_text'] = df_copy[text_column].apply(self.preprocess)
        return df_copy
    
    def fit_vectorizer(self, texts: List[str]) -> None:
        """
        Huấn luyện TF-IDF vectorizer trên danh sách text.
        
        Args:
            texts: Danh sách text đã được tiền xử lý
        """
        self.vectorizer = TfidfVectorizer(
            max_features=self.tfidf_max_features,
            ngram_range=self.tfidf_ngram_range,
            min_df=2,
            max_df=0.95,
            lowercase=False  # Text đã được lowercase trong preprocess
        )
        self.vectorizer.fit(texts)
        print(f"✅ Vectorizer được huấn luyện với {len(self.vectorizer.vocabulary_)} terms")
    
    def transform(self, texts: List[str]):
        """
        Vector hóa text sử dụng TF-IDF vectorizer đã huấn luyện.
        
        Args:
            texts: Danh sách text
        
        Returns:
            Sparse matrix (TF-IDF vectors)
        
        Raises:
            ValueError: Nếu vectorizer chưa được huấn luyện
        """
        if self.vectorizer is None:
            raise ValueError("Vectorizer chưa được huấn luyện. Gọi fit_vectorizer() trước.")
        
        return self.vectorizer.transform(texts)
    
    def fit_transform(self, texts: List[str]):
        """
        Huấn luyện vectorizer và ngay lập tức vector hóa text.
        
        Args:
            texts: Danh sách text
        
        Returns:
            Sparse matrix (TF-IDF vectors)
        """
        self.fit_vectorizer(texts)
        return self.vectorizer.transform(texts)
    
    def save_vectorizer(self, filepath: str) -> None:
        """
        Lưu vectorizer vào file (joblib).
        
        Args:
            filepath: Đường dẫn file cần lưu
        """
        if self.vectorizer is None:
            print("⚠️  Vectorizer chưa được huấn luyện.")
            return
        
        try:
            import joblib
            joblib.dump(self.vectorizer, filepath)
            print(f"✅ Vectorizer lưu vào: {filepath}")
        except ImportError:
            print("⚠️  joblib chưa được cài. Dùng pickle thay thế.")
            with open(filepath, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            print(f"✅ Vectorizer lưu vào: {filepath}")
    
    def load_vectorizer(self, filepath: str) -> None:
        """
        Tải vectorizer từ file.
        
        Args:
            filepath: Đường dẫn file vectorizer
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File không tồn tại: {filepath}")
        
        try:
            import joblib
            self.vectorizer = joblib.load(filepath)
            print(f"✅ Vectorizer tải từ: {filepath}")
        except ImportError:
            with open(filepath, 'rb') as f:
                self.vectorizer = pickle.load(f)
            print(f"✅ Vectorizer tải từ: {filepath}")


# Hàm tiện ích cấp cao
def quick_preprocess(text: str, use_stopwords: bool = True) -> str:
    """
    Hàm tiện ích: nhanh chóng tiền xử lý một đoạn text.
    
    Args:
        text: Text cần xử lý
        use_stopwords: Có loại bỏ stopwords
    
    Returns:
        Text đã xử lý
    """
    processor = TextProcessor(use_stopwords=use_stopwords)
    return processor.preprocess(text)


def preprocess_and_vectorize(texts: List[str], 
                             max_features: int = 5000) -> Tuple[List[str], object]:
    """
    Hàm tiện ích: tiền xử lý danh sách text và vector hóa.
    
    Args:
        texts: Danh sách text
        max_features: Số feature tối đa cho TF-IDF
    
    Returns:
        Tuple (danh sách text đã xử lý, TF-IDF vectors)
    """
    processor = TextProcessor(tfidf_max_features=max_features)
    
    # Tiền xử lý
    preprocessed = processor.preprocess_batch(texts)
    
    # Vector hóa
    vectors = processor.fit_transform(preprocessed)
    
    return preprocessed, vectors


if __name__ == "__main__":
    # Ví dụ sử dụng
    print("=== Test TextProcessor ===\n")
    
    processor = TextProcessor(use_stopwords=True)
    
    # Test 1: Clean text
    raw_text = "<p>Đây là bài báo <b>tuyệt vời</b> về AI 🤖 https://example.com</p>"
    cleaned = processor.clean_text(raw_text)
    print(f"Raw: {raw_text}")
    print(f"Cleaned: {cleaned}\n")
    
    # Test 2: Preprocess
    sample_texts = [
        "Trí tuệ nhân tạo là tương lai của công nghệ",
        "Cục Thể thao Quốc gia công bố kế hoạch huấn luyện đội tuyển"
    ]
    
    print("Preprocess:")
    for text in sample_texts:
        processed = processor.preprocess(text)
        print(f"  {text}")
        print(f"  → {processed}\n")
    
    # Test 3: TF-IDF
    print("TF-IDF Vectorization:")
    vectors = processor.fit_transform(sample_texts)
    print(f"  Shape: {vectors.shape}")
    print(f"  Vocabulary size: {len(processor.vectorizer.vocabulary_)}")
