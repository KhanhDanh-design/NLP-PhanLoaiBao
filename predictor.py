# -*- coding: utf-8 -*-
"""
Module dự đoán sử dụng 3 mô hình ML đã train.

Cấp các hàm/class để:
- Load 3 mô hình (Naive Bayes, SVM, Decision Tree) từ file .pkl
- Load TF-IDF vectorizer từ file
- Thực hiện dự đoán
- So sánh kết quả từ 3 mô hình

Tác giả: Full-stack AI/ML Engineer
"""

import os
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from text_processor import TextProcessor

try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    import pickle as joblib  # Fallback


class Predictor:
    """
    Class để thực hiện dự đoán sử dụng 3 mô hình đã train.
    """
    
    # Tên các mô hình
    MODEL_NAMES = {
        "nb": "Naive Bayes",
        "svm": "SVM Tuyến Tính",
        "dt": "Decision Tree"
    }
    
    def __init__(self, models_dir: str = "./models", 
                 use_stopwords: bool = True):
        """
        Khởi tạo Predictor.
        
        Args:
            models_dir: Thư mục chứa các file mô hình (.pkl)
            use_stopwords: Có sử dụng stopwords khi tiền xử lý
        """
        self.models_dir = models_dir
        self.models = {}  # Dictionary lưu các mô hình
        self.vectorizer = None
        self.text_processor = TextProcessor(use_stopwords=use_stopwords)
        self.last_prediction = None  # Lưu kết quả dự đoán lần cuối
    
    def load_models(self) -> bool:
        """
        Load 3 mô hình từ thư mục models_dir.
        
        Tìm kiếm file có tên: model_nb.pkl, model_svm.pkl, model_dt.pkl
        
        Returns:
            True nếu load thành công ít nhất 1 mô hình, False nếu lỗi
        """
        model_files = {
            "nb": "model_nb.pkl",
            "svm": "model_svm.pkl",
            "dt": "model_dt.pkl"
        }
        
        loaded_count = 0
        
        for model_key, filename in model_files.items():
            filepath = os.path.join(self.models_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"⚠️  File không tìm thấy: {filepath}")
                continue
            
            try:
                if JOBLIB_AVAILABLE:
                    model = joblib.load(filepath)
                else:
                    with open(filepath, 'rb') as f:
                        model = joblib.load(f)
                
                self.models[model_key] = model
                print(f"✅ Load {self.MODEL_NAMES[model_key]}: {filepath}")
                loaded_count += 1
            
            except Exception as e:
                print(f"❌ Lỗi khi load {filename}: {str(e)}")
        
        if loaded_count == 0:
            print("❌ Không thể load bất kỳ mô hình nào!")
            return False
        
        print(f"✅ Tổng cộng load {loaded_count}/3 mô hình thành công\n")
        return True
    
    def load_vectorizer(self, vectorizer_path: Optional[str] = None) -> bool:
        """
        Load TF-IDF vectorizer.
        
        Args:
            vectorizer_path: Đường dẫn file vectorizer (nếu None, tự tìm)
        
        Returns:
            True nếu load thành công, False nếu lỗi
        """
        if vectorizer_path is None:
            vectorizer_path = os.path.join(self.models_dir, "vectorizer.pkl")
        
        if not os.path.exists(vectorizer_path):
            print(f"⚠️  Vectorizer không tìm thấy: {vectorizer_path}")
            print("    Sẽ tạo vectorizer mới khi cần")
            return False
        
        try:
            if JOBLIB_AVAILABLE:
                self.vectorizer = joblib.load(vectorizer_path)
            else:
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = joblib.load(f)
            
            # Cập nhật vectorizer cho text processor
            self.text_processor.vectorizer = self.vectorizer
            print(f"✅ Load vectorizer từ: {vectorizer_path}\n")
            return True
        
        except Exception as e:
            print(f"❌ Lỗi khi load vectorizer: {str(e)}")
            return False
    
    def predict_single(self, text: str, 
                       return_confidence: bool = True) -> Dict:
        """
        Dự đoán danh mục cho một đoạn text sử dụng cả 3 mô hình.
        
        Args:
            text: Đoạn text cần phân loại
            return_confidence: Có trả về confidence score
        
        Returns:
            Dictionary chứa:
            - 'text': đoạn text gốc
            - 'processed_text': text đã tiền xử lý
            - 'predictions': Dictionary {model_name: prediction}
            - 'confidence': Dictionary {model_name: confidence} (nếu return_confidence=True)
            - 'consensus': Danh mục được dự đoán nhiều nhất
        """
        if not self.models:
            raise ValueError("Chưa load bất kỳ mô hình nào. Gọi load_models() trước.")
        
        if self.vectorizer is None:
            raise ValueError("Vectorizer chưa được load. Gọi load_vectorizer() trước.")
        
        # Bước 1: Tiền xử lý text
        processed_text = self.text_processor.preprocess(text)
        
        # Bước 2: Vector hóa
        text_vector = self.vectorizer.transform([processed_text])
        
        # Bước 3: Dự đoán từ 3 mô hình
        predictions = {}
        confidence = {}
        
        for model_key, model in self.models.items():
            try:
                pred = model.predict(text_vector)[0]
                predictions[model_key] = pred
                
                if return_confidence and hasattr(model, 'predict_proba'):
                    # Lấy confidence score
                    proba = model.predict_proba(text_vector)[0]
                    max_conf = np.max(proba)
                    confidence[model_key] = float(max_conf)
                else:
                    confidence[model_key] = None
            
            except Exception as e:
                print(f"⚠️  Lỗi khi dự đoán với {self.MODEL_NAMES[model_key]}: {str(e)}")
                predictions[model_key] = None
                confidence[model_key] = None
        
        # Bước 4: Tìm consensus (danh mục được dự đoán nhiều nhất)
        valid_predictions = [p for p in predictions.values() if p is not None]
        consensus = max(set(valid_predictions), key=valid_predictions.count) if valid_predictions else None
        
        # Lưu kết quả
        result = {
            "text": text,
            "processed_text": processed_text,
            "predictions": predictions,
            "confidence": confidence if return_confidence else None,
            "consensus": consensus
        }
        
        self.last_prediction = result
        return result
    
    def predict_batch(self, texts: List[str], 
                      return_confidence: bool = True) -> List[Dict]:
        """
        Dự đoán cho một danh sách text.
        
        Args:
            texts: Danh sách text
            return_confidence: Có trả về confidence score
        
        Returns:
            Danh sách kết quả dự đoán
        """
        results = []
        for text in texts:
            result = self.predict_single(text, return_confidence)
            results.append(result)
        
        return results
    
    def predict_dataframe(self, df: pd.DataFrame, 
                         text_column: str,
                         return_confidence: bool = True) -> pd.DataFrame:
        """
        Dự đoán cho một cột text trong DataFrame.
        
        Args:
            df: DataFrame
            text_column: Tên cột chứa text
            return_confidence: Có trả về confidence score
        
        Returns:
            DataFrame với các cột dự đoán được thêm vào
        """
        df_copy = df.copy()
        predictions_list = []
        
        for text in df_copy[text_column]:
            result = self.predict_single(text, return_confidence)
            predictions_list.append(result)
        
        # Thêm các cột vào DataFrame
        df_copy['processed_text'] = [r['processed_text'] for r in predictions_list]
        
        # Thêm cột dự đoán cho mỗi mô hình
        for model_key in self.MODEL_NAMES.keys():
            df_copy[f'pred_{model_key}'] = [r['predictions'].get(model_key) for r in predictions_list]
        
        # Thêm cột confidence
        if return_confidence:
            for model_key in self.MODEL_NAMES.keys():
                df_copy[f'conf_{model_key}'] = [r['confidence'].get(model_key) for r in predictions_list]
        
        # Thêm cột consensus
        df_copy['consensus'] = [r['consensus'] for r in predictions_list]
        
        return df_copy
    
    def get_comparison_table(self) -> Optional[pd.DataFrame]:
        """
        Lấy bảng so sánh kết quả dự đoán từ lần prediction cuối cùng.
        
        Returns:
            DataFrame so sánh hoặc None nếu chưa có prediction
        """
        if self.last_prediction is None:
            return None
        
        data = {
            "Mô hình": [self.MODEL_NAMES[k] for k in self.models.keys()],
            "Dự đoán": [self.last_prediction['predictions'][k] for k in self.models.keys()],
        }
        
        if self.last_prediction['confidence']:
            data["Độ tin cậy"] = [
                f"{self.last_prediction['confidence'][k]:.2%}" 
                if self.last_prediction['confidence'][k] is not None 
                else "N/A"
                for k in self.models.keys()
            ]
        
        return pd.DataFrame(data)
    
    def get_supported_categories(self) -> List[str]:
        """
        Lấy danh sách các danh mục được hỗ trợ.
        
        Lấy từ classes_ của mô hình đầu tiên.
        
        Returns:
            Danh sách danh mục hoặc None
        """
        for model in self.models.values():
            if hasattr(model, 'classes_'):
                return list(model.classes_)
        
        return None


# Hàm tiện ích cấp cao
def create_and_load_predictor(models_dir: str = "./models",
                              vectorizer_path: Optional[str] = None,
                              use_stopwords: bool = True) -> Optional[Predictor]:
    """
    Hàm tiện ích: tạo và load Predictor.
    
    Args:
        models_dir: Thư mục chứa mô hình
        vectorizer_path: Đường dẫn vectorizer
        use_stopwords: Có sử dụng stopwords
    
    Returns:
        Predictor object hoặc None nếu lỗi
    """
    predictor = Predictor(models_dir, use_stopwords)
    
    if not predictor.load_models():
        return None
    
    predictor.load_vectorizer(vectorizer_path)
    
    return predictor


if __name__ == "__main__":
    # Ví dụ sử dụng
    print("=== Test Predictor ===\n")
    
    # Tạo predictor
    predictor = Predictor(models_dir="./models")
    
    # Load mô hình
    if predictor.load_models():
        # Load vectorizer
        predictor.load_vectorizer()
        
        # Test dự đoán
        sample_text = "Đội tuyển bóng đá Việt Nam vô địch SEA Games 2023"
        
        print(f"Text: {sample_text}")
        print("\nDự đoán:\n")
        
        result = predictor.predict_single(sample_text)
        
        print(f"Text đã xử lý: {result['processed_text']}")
        print(f"\nKết quả dự đoán:")
        
        for model_key, pred in result['predictions'].items():
            conf = result['confidence'][model_key]
            if conf is not None:
                print(f"  {predictor.MODEL_NAMES[model_key]}: {pred} ({conf:.2%})")
            else:
                print(f"  {predictor.MODEL_NAMES[model_key]}: {pred}")
        
        print(f"\nConsensus: {result['consensus']}")
        
        # In bảng so sánh
        print("\n" + "="*50)
        print("BẢNG SO SÁNH KỾT QUẢ")
        print("="*50)
        comparison_df = predictor.get_comparison_table()
        if comparison_df is not None:
            print(comparison_df.to_string(index=False))
