from core.data_handler import get_users, save_users, load_config
import hashlib
from datetime import datetime

class AuthManager:
    def __init__(self):
        self.config = load_config()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_login(self, username, password):
        # Kiểm tra admin account
        if username == self.config['admin_username'] and password == self.config['admin_password']:
            return {'username': username, 'role': 'admin'}
        
        # Kiểm tra user thông thường
        users = get_users()
        hashed_password = self.hash_password(password)
        
        for user in users:
            if user['username'] == username and user['password'] == hashed_password:
                return {'username': username, 'role': 'user'}
        
        return None
    
    def register_user(self, username, password, email, address, phone):
        users = get_users()
        
        # Kiểm tra username hoặc email đã tồn tại
        if any(user['username'] == username for user in users):
            return False, "Tên đăng nhập đã tồn tại"
        if any(user.get('email') == email for user in users):
            return False, "Email đã được sử dụng"
        
        # Tạo user mới
        new_user = {
            'username': username,
            'password': self.hash_password(password),
            'role': 'user',
            'email': email,
            'address': address,
            'phone': phone,
            'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users.append(new_user)
        save_users(users)
        return True, "Đăng ký thành công"