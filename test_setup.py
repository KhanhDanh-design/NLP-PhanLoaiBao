# -*- coding: utf-8 -*-
"""
Script kiểm tra setup.

Dùng để kiểm tra:
- Dependencies đã cài chưa
- Mô hình có sẵn chưa
- Cấu hình có đúng chưa

Chạy: python test_setup.py
"""

import sys
from pathlib import Path

print("=" * 70)
print("KIỂM TRA SETUP - Phân loại báo chí tiếng Việt")
print("=" * 70)
print()

# ============================================================================
# 1. Kiểm tra Python version
# ============================================================================

print("1️⃣ Kiểm tra Python")
print("-" * 70)

python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"Python version: {python_version}")

if sys.version_info < (3, 8):
    print("❌ Python 3.8+ được yêu cầu")
    sys.exit(1)
else:
    print("✅ Python version OK\n")


# ============================================================================
# 2. Kiểm tra Dependencies
# ============================================================================

print("2️⃣ Kiểm tra Dependencies")
print("-" * 70)

required_modules = {
    "streamlit": "Streamlit (Web Framework)",
    "pandas": "Pandas (Data Processing)",
    "numpy": "NumPy (Numerical Computing)",
    "sklearn": "Scikit-Learn (ML Models)",
    "feedparser": "FeedParser (RSS Parsing)",
    "bs4": "BeautifulSoup4 (HTML Parsing)",
    "requests": "Requests (HTTP)",
    "matplotlib": "Matplotlib (Plotting)",
    "seaborn": "Seaborn (Visualization)",
}

missing_modules = []
installed_modules = []

for module, display_name in required_modules.items():
    try:
        __import__(module)
        print(f"✅ {display_name}")
        installed_modules.append(module)
    except ImportError:
        print(f"❌ {display_name}")
        missing_modules.append(module)

print()

if missing_modules:
    print(f"⚠️  Thiếu {len(missing_modules)} thư viện:")
    print()
    print("Cài đặt bằng:")
    print("    pip install -r requirements.txt")
    print()
    print("Hoặc cài riêng:")
    for module in missing_modules:
        print(f"    pip install {module}")
    print()
else:
    print("✅ Tất cả dependencies đã cài\n")


# ============================================================================
# 3. Kiểm tra Underthesea (Optional nhưng quan trọng)
# ============================================================================

print("3️⃣ Kiểm tra Underthesea (Optional)")
print("-" * 70)

try:
    from underthesea import word_tokenize
    print("✅ Underthesea (Tokenization NLP tiếng Việt)")
    print("   - App sẽ dùng underthesea cho tokenization")
except ImportError:
    print("⚠️  Underthesea chưa cài")
    print("   - App sẽ fallback thành split()")
    print("   - Cài: pip install underthesea")

print()


# ============================================================================
# 4. Kiểm tra cấu trúc thư mục
# ============================================================================

print("4️⃣ Kiểm tra cấu trúc thư mục")
print("-" * 70)

base_dir = Path(__file__).parent

required_dirs = {
    "models": "Thư mục mô hình",
    "charts": "Thư mục biểu đồ",
    "data": "Thư mục dữ liệu tạm",
}

for dirname, display_name in required_dirs.items():
    dir_path = base_dir / dirname
    if dir_path.exists():
        print(f"✅ {display_name}: {dirname}/")
    else:
        print(f"❌ {display_name}: {dirname}/ (Sẽ tạo khi chạy app)")

print()


# ============================================================================
# 5. Kiểm tra file mô hình
# ============================================================================

print("5️⃣ Kiểm tra file mô hình")
print("-" * 70)

models_dir = base_dir / "models"
model_files = {
    "model_nb.pkl": "Naive Bayes",
    "model_svm.pkl": "SVM Tuyến Tính",
    "model_dt.pkl": "Decision Tree",
    "vectorizer.pkl": "TF-IDF Vectorizer"
}

models_found = 0
for filename, display_name in model_files.items():
    filepath = models_dir / filename
    if filepath.exists():
        filesize = filepath.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ {display_name}: {filename} ({filesize:.1f}MB)")
        models_found += 1
    else:
        print(f"❌ {display_name}: {filename} (MISSING)")

print()

if models_found < 4:
    print(f"⚠️  Chỉ tìm được {models_found}/4 file mô hình")
    print()
    print("Giải pháp:")
    print("1. Copy file .pkl từ XuLyBaiBao, HOẶC")
    print("2. Chạy: python train_models.py --csv dataset_tapchi.csv")
    print()


# ============================================================================
# 6. Kiểm tra file main
# ============================================================================

print("6️⃣ Kiểm tra file chính")
print("-" * 70)

main_files = {
    "app.py": "Ứng dụng Streamlit",
    "crawler.py": "Module Crawl",
    "text_processor.py": "Module Text Processing",
    "predictor.py": "Module Prediction",
    "train_models.py": "Script Training",
    "config.py": "File cấu hình",
}

for filename, display_name in main_files.items():
    filepath = base_dir / filename
    if filepath.exists():
        filesize = filepath.stat().st_size / 1024  # KB
        print(f"✅ {display_name}: {filename} ({filesize:.1f}KB)")
    else:
        print(f"❌ {display_name}: {filename} (MISSING)")

print()


# ============================================================================
# 7. SUMMARY & RECOMMENDATIONS
# ============================================================================

print("=" * 70)
print("TÓM TẮT")
print("=" * 70)
print()

all_good = len(missing_modules) == 0 and models_found == 4

if all_good:
    print("✅ SETUP HỢP LỆ!")
    print()
    print("Bạn có thể chạy:")
    print("    streamlit run app.py")
    print()
    print("Sau đó truy cập: http://localhost:8501")
else:
    print("⚠️  CỘT HÀNG CẦN HOÀN TẤT:")
    print()
    
    if missing_modules:
        print(f"1. Cài {len(missing_modules)} thư viện bị thiếu:")
        print("   pip install -r requirements.txt")
        print()
    
    if models_found < 4:
        print(f"2. Chuẩn bị {4 - models_found} file mô hình bị thiếu:")
        print("   - Copy từ XuLyBaiBao, HOẶC")
        print("   - Chạy: python train_models.py --csv dataset_tapchi.csv")
        print()
    
    print("Sau khi hoàn tất, chạy lại script này để xác nhận.")

print()
print("=" * 70)
print("📖 Xem SETUP_GUIDE.md để hướng dẫn chi tiết")
print("=" * 70)
