# -*- coding: utf-8 -*-
"""
Ứng dụng Web Streamlit để demo pipeline phân loại bài báo tiếng Việt.

Pipeline hoàn chỉnh:
1. Crawl bài báo (từ URL hoặc RSS feed)
2. Tiền xử lý văn bản
3. Dự đoán danh mục bằng 3 mô hình
4. Hiển thị kết quả và biểu đồ đánh giá

Chạy: streamlit run app.py

Tác giả: Full-stack AI/ML Engineer
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys
from io import StringIO
import traceback
from PIL import Image

# Import các module tự tạo
try:
    from crawler import VnExpressCrawler, crawl_from_link, crawl_articles_by_category
    from text_processor import TextProcessor, quick_preprocess
    from predictor import Predictor, create_and_load_predictor
except ImportError as e:
    st.error(f"❌ Lỗi import module: {e}")
    st.stop()


# ============================================================================
# CẤU HÌNH STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="Phân loại báo chí tiếng Việt",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .metric-box {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# KHỞI TẠO SESSION STATE
# ============================================================================

@st.cache_resource
def init_predictor():
    """Khởi tạo predictor (chỉ một lần, cache result)."""
    try:
        # Xác định thư mục models
        models_dir = Path(__file__).parent / "models"
        
        predictor = create_and_load_predictor(
            models_dir=str(models_dir),
            use_stopwords=True
        )
        
        if predictor is None:
            st.error("❌ Không thể load mô hình. Kiểm tra folder 'models'.")
            return None
        
        return predictor
    except Exception as e:
        st.error(f"❌ Lỗi khi khởi tạo predictor: {str(e)}")
        return None


@st.cache_resource
def init_crawler():
    """Khởi tạo crawler."""
    return VnExpressCrawler()


if 'predictor' not in st.session_state:
    st.session_state.predictor = init_predictor()

if 'crawler' not in st.session_state:
    st.session_state.crawler = init_crawler()

if 'last_result' not in st.session_state:
    st.session_state.last_result = None

if 'articles' not in st.session_state:
    st.session_state.articles = []


# ============================================================================
# SIDEBAR - GIỚI THIỆU VÀ ĐIỀU KHIỂN
# ============================================================================

with st.sidebar:
    st.title("📰 Phân loại báo chí")
    st.markdown("""
    ### Giới thiệu dự án
    
    Ứng dụng này demo pipeline machine learning hoàn chỉnh để:
    - **Crawl** bài báo tiếng Việt từ VnExpress
    - **Xử lý** văn bản (làm sạch, tokenize, tính TF-IDF)
    - **Dự đoán** danh mục bài báo bằng 3 mô hình:
      - 🎯 Naive Bayes
      - 🎯 SVM Tuyến Tính
      - 🎯 Decision Tree
    
    ### Hướng dẫn sử dụng
    
    1. **Tab "Phân loại"**: Nhập URL bài báo hoặc văn bản → Phân tích
    2. **Tab "Đánh giá"**: Xem hiệu suất 3 mô hình
    """)
    
    st.divider()
    
    # Thông tin về mô hình
    if st.session_state.predictor:
        st.success("✅ Mô hình đã load sẵn sàng")
        
        categories = st.session_state.predictor.get_supported_categories()
        if categories:
            st.info(f"📂 Danh mục hỗ trợ: {', '.join(categories)}")
    else:
        st.error("❌ Mô hình chưa load. Vui lòng kiểm tra.")


# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

tab1, tab2 = st.tabs(["🔍 Phân loại bài báo", "📊 Đánh giá mô hình"])


# ============================================================================
# TAB 1: PHÂN LOẠI BÀI BÁO
# ============================================================================

with tab1:
    st.title("🔍 Phân loại bài báo tiếng Việt")
    
    if st.session_state.predictor is None:
        st.error("❌ Mô hình chưa được khởi tạo. Vui lòng tải lại trang.")
        st.stop()
    
    # Option: Chọn cách nhập dữ liệu
    input_mode = st.radio(
        "Chọn cách nhập bài báo:",
        ["📎 Dán URL", "✍️ Dán văn bản", "🌐 Crawl từ RSS"],
        horizontal=True
    )
    
    # ========== MODE 1: NHẬP URL ==========
    if input_mode == "📎 Dán URL":
        st.subheader("Nhập URL bài báo VnExpress")
        
        url_input = st.text_input(
            "URL bài báo:",
            placeholder="https://vnexpress.net/...",
            key="url_input"
        )
        
        if st.button("🚀 Crawl và phân tích", key="btn_crawl_url"):
            if not url_input.strip():
                st.warning("⚠️  Vui lòng nhập URL")
            else:
                with st.spinner("⏳ Đang crawl bài báo..."):
                    try:
                        article = st.session_state.crawler.crawl_from_url(url_input)
                        
                        if article is None:
                            st.error("❌ Không thể crawl URL này. Vui lòng kiểm tra lại.")
                        else:
                            # Kết hợp title và content
                            full_text = f"{article.get('title', '')} {article.get('content', '')}"
                            
                            # Tiên xử lý
                            with st.spinner("⏳ Đang xử lý text..."):
                                result = st.session_state.predictor.predict_single(full_text)
                            
                            st.session_state.last_result = {
                                **result,
                                "source": "URL",
                                "title": article.get('title', 'Không xác định'),
                                "category_actual": article.get('category', 'Không xác định')
                            }
                            
                            st.success("✅ Phân tích hoàn tất!")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
    
    # ========== MODE 2: NHẬP VĂN BẢN ==========
    elif input_mode == "✍️ Dán văn bản":
        st.subheader("Nhập văn bản bài báo")
        
        text_input = st.text_area(
            "Văn bản bài báo:",
            placeholder="Nhập hoặc dán nội dung bài báo tiếng Việt...",
            height=200,
            key="text_input"
        )
        
        if st.button("🚀 Phân tích", key="btn_analyze_text"):
            if not text_input.strip():
                st.warning("⚠️  Vui lòng nhập văn bản")
            else:
                with st.spinner("⏳ Đang xử lý text..."):
                    try:
                        result = st.session_state.predictor.predict_single(text_input)
                        
                        st.session_state.last_result = {
                            **result,
                            "source": "Text Input",
                            "title": text_input[:100] + "..." if len(text_input) > 100 else text_input,
                            "category_actual": "Không xác định"
                        }
                        
                        st.success("✅ Phân tích hoàn tất!")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
    
    # ========== MODE 3: CRAWL TỪ RSS ==========
    else:  # "🌐 Crawl từ RSS"
        st.subheader("Crawl từ RSS Feed VnExpress")
        
        available_categories = list(st.session_state.crawler.RSS_SOURCES.keys())
        selected_categories = st.multiselect(
            "Chọn danh mục:",
            available_categories,
            default=["Giáo dục", "Thể thao"]
        )
        
        max_items = st.number_input(
            "Số bài tối đa mỗi danh mục:",
            min_value=1,
            max_value=50,
            value=5
        )
        
        if st.button("🚀 Crawl và phân tích", key="btn_crawl_rss"):
            if not selected_categories:
                st.warning("⚠️  Vui lòng chọn ít nhất một danh mục")
            else:
                with st.spinner("⏳ Đang crawl bài báo từ RSS..."):
                    try:
                        articles = st.session_state.crawler.crawl_multiple_categories(
                            categories=selected_categories,
                            max_items_per_category=max_items
                        )
                        
                        if not articles:
                            st.error("❌ Không crawl được bài nào")
                        else:
                            st.session_state.articles = articles
                            st.success(f"✅ Crawl được {len(articles)} bài báo")
                            
                            # Hiển thị danh sách bài báo
                            st.subheader("Danh sách bài báo")
                            
                            for idx, article in enumerate(articles[:10], 1):  # Hiển thị tối đa 10
                                with st.expander(f"📄 {idx}. {article['title'][:80]}"):
                                    st.write(f"**Danh mục:** {article['category']}")
                                    st.write(f"**Link:** {article['link']}")
                                    st.write(f"**Nội dung:** {article['summary'][:300]}...")
                                    
                                    if st.button(f"🔍 Phân tích bài này", key=f"btn_analyze_{idx}"):
                                        full_text = f"{article['title']} {article['summary']}"
                                        
                                        with st.spinner("⏳ Đang phân tích..."):
                                            result = st.session_state.predictor.predict_single(full_text)
                                        
                                        st.session_state.last_result = {
                                            **result,
                                            "source": "RSS",
                                            "title": article['title'],
                                            "category_actual": article['category']
                                        }
                                        
                                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Lỗi khi crawl: {str(e)}")
    
    # ========== HIỂN THỊ KỾT QUẢ ==========
    if st.session_state.last_result:
        st.divider()
        st.subheader("📋 Kết quả phân tích")
        
        result = st.session_state.last_result
        
        # Hiển thị bài báo
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Tiêu đề:** {result['title']}")
            st.caption(f"Nguồn: {result['source']}")
        
        with col2:
            st.info(f"**Danh mục thực tế:** {result['category_actual']}")
            st.caption("(Từ thông tin crawl)")
        
        # Bảng so sánh kết quả từ 3 mô hình
        st.subheader("🎯 So sánh kết quả 3 mô hình")
        
        comparison_data = []
        for model_key in ["nb", "svm", "dt"]:
            pred = result['predictions'].get(model_key)
            conf = result['confidence'].get(model_key)
            
            row = {
                "Mô hình": {
                    "nb": "Naive Bayes",
                    "svm": "SVM Tuyến Tính",
                    "dt": "Decision Tree"
                }[model_key],
                "Dự đoán": pred if pred else "❓ Lỗi",
                "Độ tin cậy": f"{conf:.2%}" if conf else "N/A"
            }
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Tô màu dòng theo consensus
        consensus = result.get('consensus')
        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Consensus
        st.success(f"✅ **CONSENSUS:** {consensus}")
        
        # Hiển thị text đã xử lý
        with st.expander("📝 Xem text đã xử lý"):
            st.text_area(
                "Text đã được tiền xử lý:",
                value=result['processed_text'],
                height=150,
                disabled=True
            )


# ============================================================================
# TAB 2: ĐÁNH GIÁ MÔ HÌNH
# ============================================================================

with tab2:
    st.title("📊 Đánh giá hiệu suất 3 mô hình")
    
    charts_dir = Path(__file__).parent / "charts"
    
    if not charts_dir.exists():
        st.warning("⚠️  Thư mục 'charts' không tìm thấy")
    else:
        # ===== HIỂN THỊ CONFUSION MATRIX =====
        st.subheader("🔲 Ma trận nhầm lẫn (Confusion Matrix)")
        
        confusion_matrices = {
            "Naive Bayes": "confusion_matrix_nb.png",
            "SVM Tuyến Tính": "confusion_matrix_svm.png",
            "Decision Tree": "confusion_matrix_dt.png"
        }
        
        # Layout 3 cột
        cols = st.columns(3)
        
        for col, (model_name, filename) in zip(cols, confusion_matrices.items()):
            filepath = charts_dir / filename
            
            if filepath.exists():
                with col:
                    st.subheader(model_name)
                    try:
                        img = Image.open(filepath)
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Lỗi khi load ảnh: {e}")
            else:
                with col:
                    st.warning(f"📌 {filename} không tìm thấy")
        
        # ===== HIỂN THỊ BẢNG SỐ LIỆU =====
        st.divider()
        st.subheader("📈 Bảng so sánh metrics")
        
        metrics_file = charts_dir / "comparison_metrics.csv"
        
        if metrics_file.exists():
            try:
                metrics_df = pd.read_csv(metrics_file)
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                
                # Hiển thị biểu đồ
                st.subheader("📊 Biểu đồ so sánh")
                
                if 'Accuracy' in metrics_df.columns:
                    chart_df = metrics_df[['Model', 'Accuracy']].set_index('Model')
                    st.bar_chart(chart_df)
                
            except Exception as e:
                st.error(f"❌ Lỗi khi đọc metrics: {e}")
        else:
            st.info("📌 File metrics chưa có")
        
        # ===== HIỂN THỊ SUMMARY =====
        st.divider()
        st.subheader("📋 Tóm tắt kết quả")
        
        summary_file = charts_dir / "comparison_summary.md"
        
        if summary_file.exists():
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    summary_content = f.read()
                st.markdown(summary_content)
            except Exception as e:
                st.error(f"❌ Lỗi khi đọc summary: {e}")
        else:
            st.info("📌 File summary chưa có")


# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
        <p>🤖 Phân loại báo chí tiếng Việt - Full-stack ML Pipeline</p>
        <p>Powered by Streamlit | ML Models: Naive Bayes, SVM, Decision Tree</p>
    </div>
""", unsafe_allow_html=True)
