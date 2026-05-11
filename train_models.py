# -*- coding: utf-8 -*-
"""
Script huấn luyện và lưu 3 mô hình ML.

Dùng file dữ liệu dataset_tapchi.csv để train 3 mô hình (NB, SVM, DT)
và lưu vào folder models/ dưới dạng .pkl

Chạy: python train_models.py --csv dataset_tapchi.csv

Tác giả: Full-stack AI/ML Engineer
"""

import argparse
import os
import time
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    import pickle as joblib
    JOBLIB_AVAILABLE = False


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Train và lưu 3 mô hình ML (NB, SVM, DT)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="dataset_tapchi.csv",
        help="Đường dẫn file dữ liệu CSV"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./models",
        help="Thư mục output lưu mô hình"
    )
    parser.add_argument(
        "--text-col",
        type=str,
        default="content_cleaned",
        help="Tên cột văn bản"
    )
    parser.add_argument(
        "--label-col",
        type=str,
        default="label",
        help="Tên cột nhãn"
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Tỷ lệ test set"
    )
    return parser.parse_args()


def load_data(csv_path: str, text_col: str, label_col: str) -> tuple:
    """
    Load dữ liệu từ file CSV.
    
    Args:
        csv_path: Đường dẫn file CSV
        text_col: Tên cột văn bản
        label_col: Tên cột nhãn
    
    Returns:
        Tuple (X, y, labels_order)
    """
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"File không tìm thấy: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Kiểm tra cột
    required_cols = {text_col, label_col}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"Thiếu cột: {missing}. Cột có sẵn: {list(df.columns)}"
        )
    
    # Chuẩn bị dữ liệu
    data = df[[text_col, label_col]].dropna().copy()
    X = data[text_col].astype(str)
    y = data[label_col].astype(str)
    
    labels_order = sorted(y.unique())
    
    print(f"✅ Load dữ liệu: {len(data)} mẫu")
    print(f"   - Số danh mục: {len(labels_order)}")
    print(f"   - Danh mục: {', '.join(labels_order)}")
    
    return X, y, labels_order


def train_models(X, y, test_size: float = 0.2):
    """
    Train 3 mô hình.
    
    Args:
        X: Input features (text)
        y: Target labels
        test_size: Tỷ lệ test set
    
    Returns:
        Dict {model_name: model}
    """
    print("\n" + "="*70)
    print("CHIA DỮ LIỆU")
    print("="*70)
    
    # Chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42,
        stratify=y
    )
    
    print(f"Train size: {len(X_train)} ({(1-test_size)*100:.0f}%)")
    print(f"Test size:  {len(X_test)} ({test_size*100:.0f}%)")
    
    # TF-IDF vectorization
    print("\n" + "="*70)
    print("TF-IDF VECTORIZATION")
    print("="*70)
    
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 1),
        min_df=2,
        max_df=0.95,
        lowercase=False
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"✅ Vectorizer fit")
    print(f"   - Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train 3 mô hình
    models = {}
    
    # 1. Naive Bayes
    print("\n" + "="*70)
    print("TRAINING: NAIVE BAYES")
    print("="*70)
    
    t0 = time.time()
    nb_model = MultinomialNB()
    nb_model.fit(X_train_tfidf, y_train)
    nb_time = time.time() - t0
    
    y_pred_nb = nb_model.predict(X_test_tfidf)
    nb_acc = accuracy_score(y_test, y_pred_nb)
    
    print(f"✅ Naive Bayes trained")
    print(f"   - Training time: {nb_time:.2f}s")
    print(f"   - Test Accuracy: {nb_acc:.4f}")
    print(f"   - Report:")
    print(classification_report(y_test, y_pred_nb, digits=4, zero_division=0))
    
    models["nb"] = nb_model
    
    # 2. SVM
    print("\n" + "="*70)
    print("TRAINING: SVM LINEAR")
    print("="*70)
    
    t0 = time.time()
    svm_model = LinearSVC(random_state=42, max_iter=2000)
    svm_model.fit(X_train_tfidf, y_train)
    svm_time = time.time() - t0
    
    y_pred_svm = svm_model.predict(X_test_tfidf)
    svm_acc = accuracy_score(y_test, y_pred_svm)
    
    print(f"✅ SVM trained")
    print(f"   - Training time: {svm_time:.2f}s")
    print(f"   - Test Accuracy: {svm_acc:.4f}")
    print(f"   - Report:")
    print(classification_report(y_test, y_pred_svm, digits=4, zero_division=0))
    
    models["svm"] = svm_model
    
    # 3. Decision Tree
    print("\n" + "="*70)
    print("TRAINING: DECISION TREE")
    print("="*70)
    
    t0 = time.time()
    dt_model = DecisionTreeClassifier(
        max_depth=100,
        min_samples_split=5,
        criterion="entropy",
        random_state=42
    )
    dt_model.fit(X_train_tfidf, y_train)
    dt_time = time.time() - t0
    
    y_pred_dt = dt_model.predict(X_test_tfidf)
    dt_acc = accuracy_score(y_test, y_pred_dt)
    
    print(f"✅ Decision Tree trained")
    print(f"   - Training time: {dt_time:.2f}s")
    print(f"   - Test Accuracy: {dt_acc:.4f}")
    print(f"   - Report:")
    print(classification_report(y_test, y_pred_dt, digits=4, zero_division=0))
    
    models["dt"] = dt_model
    
    # Summary
    print("\n" + "="*70)
    print("TÓM TẮT KẾT QUẢ")
    print("="*70)
    
    results = pd.DataFrame({
        "Model": ["Naive Bayes", "SVM", "Decision Tree"],
        "Accuracy": [nb_acc, svm_acc, dt_acc],
        "Training Time (s)": [nb_time, svm_time, dt_time]
    })
    
    print(results.to_string(index=False))
    
    # Return mô hình và vectorizer
    return models, vectorizer


def save_models(models: dict, vectorizer, output_dir: str) -> bool:
    """
    Lưu mô hình vào file .pkl.
    
    Args:
        models: Dict {model_name: model}
        vectorizer: TF-IDF vectorizer
        output_dir: Thư mục output
    
    Returns:
        True nếu thành công
    """
    # Tạo thư mục nếu chưa tồn tại
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("SAVING MODELS")
    print("="*70)
    
    try:
        # Lưu mô hình
        for model_name, model in models.items():
            filepath = Path(output_dir) / f"model_{model_name}.pkl"
            
            if JOBLIB_AVAILABLE:
                joblib.dump(model, filepath)
            else:
                with open(filepath, 'wb') as f:
                    joblib.dump(model, f)
            
            print(f"✅ Lưu {model_name}: {filepath}")
        
        # Lưu vectorizer
        vectorizer_path = Path(output_dir) / "vectorizer.pkl"
        
        if JOBLIB_AVAILABLE:
            joblib.dump(vectorizer, vectorizer_path)
        else:
            with open(vectorizer_path, 'wb') as f:
                joblib.dump(vectorizer, f)
        
        print(f"✅ Lưu vectorizer: {vectorizer_path}")
        
        print(f"\n✅ Tất cả mô hình đã được lưu vào: {output_dir}")
        return True
    
    except Exception as e:
        print(f"❌ Lỗi khi lưu mô hình: {str(e)}")
        return False


def main():
    """Main function."""
    args = parse_args()
    
    print("\n" + "="*70)
    print("TRAINING & SAVING ML MODELS")
    print("="*70)
    
    try:
        # 1. Load data
        X, y, labels_order = load_data(
            args.csv,
            args.text_col,
            args.label_col
        )
        
        # 2. Train models
        models, vectorizer = train_models(X, y, test_size=args.test_size)
        
        # 3. Save models
        success = save_models(models, vectorizer, args.output_dir)
        
        if success:
            print("\n" + "="*70)
            print("✅ HOÀN TẤT THÀNH CÔNG!")
            print("="*70)
            print(f"\n📂 Các file mô hình nằm tại: {args.output_dir}/")
            print("   - model_nb.pkl")
            print("   - model_svm.pkl")
            print("   - model_dt.pkl")
            print("   - vectorizer.pkl")
            print("\n👉 Bây giờ bạn có thể chạy: streamlit run app.py")
        else:
            print("\n❌ Có lỗi khi lưu mô hình")
            return 1
    
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
