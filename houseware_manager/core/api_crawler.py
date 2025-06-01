import requests
from concurrent.futures import ThreadPoolExecutor
from core.data_handler import get_housewares, save_housewares, load_config
import time

class APICrawler:
    def __init__(self):
        self.config = load_config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_from_dummyjson(self):
        """Crawl từ dummyjson.com với phân trang"""
        base_url = "https://dummyjson.com/products/category/home-decoration"
        all_products = []
        
        try:
            # Lấy tổng số sản phẩm
            response = self.session.get(f"{base_url}?limit=0")
            total = response.json().get('total', 0)
            
            # Crawl song song với 4 luồng
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for skip in range(0, total, 30):  # 30 sản phẩm mỗi trang
                    url = f"{base_url}?limit=30&skip={skip}"
                    futures.append(executor.submit(self._fetch_page, url))
                
                for future in futures:
                    products = future.result()
                    if products:
                        all_products.extend(products)
            
            return all_products
        except Exception as e:
            print(f"Lỗi khi crawl từ dummyjson: {e}")
            return []

    def _fetch_page(self, url):
        """Lấy dữ liệu từ một trang cụ thể"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json().get('products', [])
        except Exception as e:
            print(f"Lỗi khi fetch {url}: {e}")
        return []


    def fetch_housewares(self):
        """Lấy dữ liệu đồ gia dụng từ API và chuyển đổi định dạng"""
        try:
            response = self.session.get(self.config['api_url'], timeout=10)
            if response.status_code == 200:
                api_data = response.json()
                
                # Chuyển đổi dữ liệu từ API sang định dạng của chúng ta
                processed_products = []
                for product in api_data.get('products', []):
                    processed_products.append({
                        'id': product['id'],
                        'tên': product['title'],
                        'giá': product['price'],
                        'mô tả': product['description'],
                        'thương hiệu': product['brand'],
                        'phân loại': product['category'],
                        'số lượng tồn kho': product.get('stock', 0)
                    })
                
                # Lấy dữ liệu hiện tại và kiểm tra trùng lặp
                current_data = get_housewares()
                current_ids = {item['id'] for item in current_data}
                
                # Chỉ thêm sản phẩm mới
                new_items = [
                    item for item in processed_products
                    if item['id'] not in current_ids
                ]
                
                if new_items:
                    current_data.extend(new_items)
                    save_housewares(current_data)
                    return True, f"Đã thêm {len(new_items)} sản phẩm mới"
                return True, "Không có sản phẩm mới nào"
            
            return False, f"Lỗi API: {response.status_code}"
        except Exception as e:
            return False, f"Lỗi khi crawl dữ liệu: {str(e)}"
        
    def process_products(self, products, source):
        """Xử lý và chuẩn hóa dữ liệu từ các nguồn khác nhau"""
        processed = []
        
        for p in products:
            if source == 'dummyjson':
                item = {
                    'id': p['id'],
                    'name': p['title'],
                    'price': p['price'],
                    'brand': p.get('brand', 'Unknown'),
                    'category': p['category'],
                    'description': p['description'],
                    'stock': p.get('stock', 0),
                    'thumbnail': p['thumbnail']
                }
            elif source == 'fakestoreapi':
                item = {
                    'id': p['id'] + 10000,
                    'name': p['title'],
                    'price': p['price'],
                    'brand': 'Unknown',
                    'category': p['category'],
                    'description': p['description'],
                    'stock': 100,
                    'thumbnail': p['image']
                }
            
            # Lọc sản phẩm không hợp lệ
            if all(key in item for key in ['id', 'name', 'price']):
                processed.append(item)
        
        return processed