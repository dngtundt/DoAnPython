import json
import os
from pathlib import Path

def initialize_data_files():
    """Khởi tạo các file dữ liệu nếu chưa tồn tại"""
    config = load_config()
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Tạo thư mục data nếu chưa có
    data_dir.mkdir(exist_ok=True)
    
    # Khởi tạo file users.json
    users_file = data_dir / 'users.json'
    if not users_file.exists():
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    # Khởi tạo file housewares.json
    housewares_file = data_dir / 'housewares.json'
    if not housewares_file.exists():
        with open(housewares_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    # Thêm tài khoản admin mặc định nếu chưa có
    users = get_users()
    admin_exists = any(user.get('username') == 'admin' for user in users)
    if not admin_exists:
        admin_user = {
            'username': 'admin',
            'password': 'admin123',  # Lưu ý: Trong thực tế nên mã hóa mật khẩu
            'role': 'admin'
        }
        users.append(admin_user)
        save_users(users)

def get_data_path(filename):
    """Lấy đường dẫn tuyệt đối tới file dữ liệu"""
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir / filename

def read_json(filename):
    file_path = get_data_path(filename)
    if not file_path.exists():
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filename, data):
    file_path = get_data_path(filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_housewares():
    return read_json('housewares.json')

def save_housewares(data):
    write_json('housewares.json', data)

def get_users():
    return read_json('users.json')

def save_users(data):
    write_json('users.json', data)

def load_config():
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def format_currency(amount):
    """Định dạng tiền tệ VND với dấu phẩy ngăn cách"""
    return f"{amount:,.0f} VND"