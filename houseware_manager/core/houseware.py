from core.data_handler import get_housewares, save_housewares

class HousewareManager:
    def __init__(self):
        self.housewares = self.load_housewares()
    
    def load_housewares(self):
        """Load housewares from the data source"""
        return get_housewares()

    def refresh_data(self):
        self.housewares = self.load_housewares()
    
    def get_all_housewares(self):
        """Lấy toàn bộ danh sách đồ gia dụng"""
        return [{
            'id': item['id'],
            'tên': item['tên'],
            'giá': item['giá'],
            'mô tả': item['mô tả'],
            'thương hiệu': item['thương hiệu'],
            'phân loại': item['phân loại'],
            'số lượng tồn kho': item['số lượng tồn kho']
        } for item in self.housewares]
    
    def get_houseware_by_id(self, houseware_id):
        for item in self.housewares:
            if isinstance(item, dict) and item.get('id') == houseware_id:
                return item
        return None
    
    def add_houseware(self, houseware_data):
        try:
            new_id = self.generate_new_id()
            houseware_data['id'] = new_id
            self.housewares.append(houseware_data)
            save_housewares(self.housewares)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm sản phẩm: {e}")
            return False
    
    def update_houseware(self, houseware_id, updated_data):
        for i, item in enumerate(self.housewares):
            if item['id'] == houseware_id:
                updated_data['id'] = houseware_id
                self.housewares[i] = updated_data
                save_housewares(self.housewares)
                return True
        return False
    
    def delete_houseware(self, houseware_id):
        self.housewares = [item for item in self.housewares if item['id'] != houseware_id]
        save_housewares(self.housewares)
        return True
    
    def search_housewares(self, keyword):
        keyword = keyword.lower()
        return [
            item for item in self.housewares
            if (keyword in item['tên'].lower() or 
                keyword in item['mô tả'].lower() or
                keyword in item['thương hiệu'].lower())
        ]
    
    def sort_housewares(self, sort_type="id_asc"):
        """Sắp xếp sản phẩm theo các tiêu chí"""
        reverse_order = sort_type.endswith("_desc")
        
        if sort_type.startswith("id"):
            self.housewares.sort(key=lambda x: x['id'], reverse=reverse_order)
        elif sort_type.startswith("price"):
            self.housewares.sort(key=lambda x: x['giá'], reverse=reverse_order)
        elif sort_type.startswith("name"):
            self.housewares.sort(key=lambda x: x['tên'].lower(), reverse=reverse_order)
        elif sort_type.startswith("brand"):
            self.housewares.sort(key=lambda x: x['thương hiệu'].lower(), reverse=reverse_order)
        elif sort_type.startswith("category"):
            self.housewares.sort(key=lambda x: x['phân loại'].lower(), reverse=reverse_order)
        
        save_housewares(self.housewares)
        return self.housewares
    
    def generate_new_id(self):
        """Tạo ID mới dựa trên ID lớn nhất hiện có"""
        if not self.housewares:
            return 1  # Nếu danh sách sản phẩm rỗng, bắt đầu từ ID 1
        max_id = max(item['id'] for item in self.housewares)
        return max_id + 1