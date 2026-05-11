# -*- coding: utf-8 -*-
"""
Module crawl bài báo từ VnExpress RSS feed.

Cấp các hàm/class để cào dữ liệu bài báo từ VnExpress, hỗ trợ:
- Crawl theo danh mục (RSS feed)
- Crawl theo từ khóa tìm kiếm
- Trả về dữ liệu dưới dạng Dictionary hoặc DataFrame

Tác giả: Full-stack AI/ML Engineer
"""

import time
import re
from typing import Dict, List, Optional
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd


class VnExpressCrawler:
    """
    Class để crawl bài báo từ VnExpress.
    
    Hỗ trợ 2 chế độ:
    1. Crawl từ RSS feed theo danh mục
    2. Crawl từ trang web tìm kiếm
    """
    
    # Danh sách chuyên mục RSS có sẵn
    RSS_SOURCES = {
        "Giáo dục": "https://vnexpress.net/rss/giao-duc.rss",
        "Thể thao": "https://vnexpress.net/rss/the-thao.rss",
        "Kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
        "Giải trí": "https://vnexpress.net/rss/giai-tri.rss",
        "Khoa học công nghệ": "https://vnexpress.net/rss/khoa-hoc-cong-nghe.rss",
        "Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
        "Sức khỏe": "https://vnexpress.net/rss/suc-khoe.rss",
    }
    
    def __init__(self, timeout: int = 10, delay: float = 0.5):
        """
        Khởi tạo crawler.
        
        Args:
            timeout: Thời gian chờ kết nối (giây)
            delay: Thời gian delay giữa các request (giây)
        """
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def crawl_rss(self, category_name: str, rss_url: str, 
                  max_items: Optional[int] = None) -> List[Dict]:
        """
        Crawl bài báo từ RSS feed của một chuyên mục.
        
        Args:
            category_name: Tên chuyên mục (ký dùng làm nhãn/label)
            rss_url: URL RSS feed
            max_items: Số bài tối đa cần lấy (None = lấy tất cả)
        
        Returns:
            Danh sách bài báo dưới dạng dict với keys: title, summary, link, category
        
        Raises:
            Exception: Nếu lỗi khi truy cập RSS feed
        """
        try:
            articles = []
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print(f"⚠️  {category_name}: Không lấy được bài nào từ RSS")
                return articles
            
            for idx, entry in enumerate(feed.entries):
                if max_items and idx >= max_items:
                    break
                
                # Xử lý trường hợp entry không có đủ trường
                article = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "category": category_name,
                    "published": entry.get("published", "")
                }
                articles.append(article)
            
            print(f"✅ {category_name}: Lấy được {len(articles)} bài báo")
            time.sleep(self.delay)  # Tránh spam
            return articles
            
        except Exception as e:
            print(f"❌ Lỗi khi crawl {category_name}: {str(e)}")
            return []
    
    def crawl_multiple_categories(self, categories: Optional[List[str]] = None,
                                  max_items_per_category: Optional[int] = None) -> List[Dict]:
        """
        Crawl bài báo từ nhiều chuyên mục cùng lúc.
        
        Args:
            categories: Danh sách tên chuyên mục cần crawl (None = crawl tất cả)
            max_items_per_category: Số bài tối đa mỗi chuyên mục
        
        Returns:
            Danh sách tất cả bài báo từ các chuyên mục
        """
        all_articles = []
        
        # Nếu không chỉ định categories, crawl tất cả
        if categories is None:
            categories = list(self.RSS_SOURCES.keys())
        
        for category in categories:
            if category not in self.RSS_SOURCES:
                print(f"⚠️  '{category}' không có trong danh sách RSS. Bỏ qua.")
                continue
            
            rss_url = self.RSS_SOURCES[category]
            articles = self.crawl_rss(category, rss_url, max_items_per_category)
            all_articles.extend(articles)
        
        print(f"\n📰 Tổng số bài báo lấy được: {len(all_articles)}")
        return all_articles
    
    def crawl_from_url(self, url: str, title: str = "") -> Optional[Dict]:
        """
        Crawl nội dung bài báo từ một URL cụ thể.
        
        Args:
            url: URL của bài báo VnExpress
            title: Tiêu đề bài báo (nếu có)
        
        Returns:
            Dictionary chứa title, content, url hoặc None nếu lỗi
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Thử lấy tiêu đề nếu chưa có
            if not title:
                title_tag = soup.find('h1', class_='title-detail')
                if title_tag:
                    title = title_tag.get_text(strip=True)
            
            # Lấy nội dung bài báo
            content_div = soup.find('article') or soup.find('div', class_='content-detail')
            content = ""
            if content_div:
                paragraphs = content_div.find_all('p')
                content = "\n".join([p.get_text(strip=True) for p in paragraphs])
            
            # Lấy category từ URL nếu có
            category = self._extract_category_from_url(url)
            
            return {
                "title": title,
                "content": content,
                "summary": content[:500],  # Lấy 500 ký tự đầu làm summary
                "link": url,
                "category": category
            }
            
        except Exception as e:
            print(f"❌ Lỗi khi crawl URL {url}: {str(e)}")
            return None
    
    def _extract_category_from_url(self, url: str) -> str:
        """
        Trích xuất tên danh mục từ URL VnExpress.
        
        Args:
            url: URL của bài báo
        
        Returns:
            Tên danh mục hoặc chuỗi trống nếu không tìm được
        """
        for category, rss_url in self.RSS_SOURCES.items():
            # Trích xuất tên slug từ RSS URL
            slug = rss_url.split('/rss/')[-1].replace('.rss', '')
            if slug in url:
                return category
        return ""
    
    def to_dataframe(self, articles: List[Dict]) -> pd.DataFrame:
        """
        Chuyển đổi danh sách bài báo sang DataFrame.
        
        Args:
            articles: Danh sách bài báo
        
        Returns:
            DataFrame với các cột: title, summary, link, category, published
        """
        if not articles:
            return pd.DataFrame()
        
        df = pd.DataFrame(articles)
        return df
    
    def save_to_csv(self, articles: List[Dict], filepath: str = "articles.csv") -> None:
        """
        Lưu danh sách bài báo vào file CSV.
        
        Args:
            articles: Danh sách bài báo
            filepath: Đường dẫn file CSV cần lưu
        """
        try:
            df = self.to_dataframe(articles)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"💾 Đã lưu {len(articles)} bài báo vào: {filepath}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu file: {str(e)}")


# Hàm tiện ích cấp cao
def crawl_articles_by_category(category: str, max_items: Optional[int] = None) -> List[Dict]:
    """
    Hàm tiện ích: crawl bài báo từ một chuyên mục.
    
    Args:
        category: Tên chuyên mục
        max_items: Số bài tối đa
    
    Returns:
        Danh sách bài báo
    """
    crawler = VnExpressCrawler()
    if category not in crawler.RSS_SOURCES:
        print(f"❌ Chuyên mục '{category}' không tồn tại")
        return []
    
    rss_url = crawler.RSS_SOURCES[category]
    return crawler.crawl_rss(category, rss_url, max_items)


def crawl_from_link(url: str) -> Optional[Dict]:
    """
    Hàm tiện ích: crawl bài báo từ một link cụ thể.
    
    Args:
        url: URL của bài báo
    
    Returns:
        Dictionary chứa thông tin bài báo hoặc None nếu lỗi
    """
    crawler = VnExpressCrawler()
    return crawler.crawl_from_url(url)


if __name__ == "__main__":
    # Ví dụ sử dụng
    crawler = VnExpressCrawler()
    
    # Crawl từ một chuyên mục
    print("=== Test crawl từ RSS ===")
    articles = crawler.crawl_multiple_categories(
        categories=["Giáo dục", "Thể thao"],
        max_items_per_category=5
    )
    
    print(f"\nLấy được {len(articles)} bài")
    if articles:
        print("\nBài đầu tiên:")
        print(f"  Tiêu đề: {articles[0]['title']}")
        print(f"  Danh mục: {articles[0]['category']}")
