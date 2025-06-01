import tkinter as tk
from tkinter import messagebox
from core.auth_manager import AuthManager
from gui.admin_window import AdminWindow
from gui.user_window import UserWindow

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng nhập hệ thống")
        self.master.geometry("400x300")
        
        self.auth_manager = AuthManager()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame chính
        self.main_frame = tk.Frame(self.master, padx=20, pady=20, bg="#00CED1")  # Xanh ngọc
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tiêu đề
        tk.Label(self.main_frame, text="ĐĂNG NHẬP HỆ THỐNG", 
                 font=("Arial", 16, "bold"), bg="#00CED1", fg="#483D8B").pack(pady=10)
        
        # Form đăng nhập
        tk.Label(self.main_frame, text="Tên đăng nhập:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W)
        self.username_entry = tk.Entry(self.main_frame, width=30)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Mật khẩu:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W)
        self.password_entry = tk.Entry(self.main_frame, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Nút đăng nhập
        tk.Button(self.main_frame, text="Đăng nhập", 
                  command=self.login, width=15, bg="#483D8B", fg="#FFFFFF").pack(pady=10)
        
        # Nút đăng ký
        tk.Button(self.main_frame, text="Đăng ký tài khoản", 
                  command=self.show_register, width=15, bg="#483D8B", fg="#FFFFFF").pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        user_info = self.auth_manager.validate_login(username, password)
        
        if user_info:
            self.master.withdraw()  # Ẩn cửa sổ đăng nhập
            
            if user_info['role'] == 'admin':
                admin_window = tk.Toplevel(self.master)
                AdminWindow(admin_window, self.master)
            else:
                user_window = tk.Toplevel(self.master)
                UserWindow(user_window, self.master, user_info['username'])
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    def show_register(self):
        register_window = tk.Toplevel(self.master)
        register_window.title("Đăng ký tài khoản")
        register_window.geometry("400x400")
        register_window.configure(bg="#00CED1")  # Xanh ngọc

        # Tiêu đề
        tk.Label(register_window, text="ĐĂNG KÝ TÀI KHOẢN", font=("Arial", 16, "bold"), bg="#00CED1", fg="#483D8B").pack(pady=10)

        # Form đăng ký
        tk.Label(register_window, text="Tên đăng nhập:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W, padx=20)
        username_entry = tk.Entry(register_window, width=30)
        username_entry.pack(pady=5)

        tk.Label(register_window, text="Mật khẩu:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W, padx=20)
        password_entry = tk.Entry(register_window, width=30, show="*")
        password_entry.pack(pady=5)

        tk.Label(register_window, text="Email:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W, padx=20)
        email_entry = tk.Entry(register_window, width=30)
        email_entry.pack(pady=5)

        tk.Label(register_window, text="Địa chỉ:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W, padx=20)
        address_entry = tk.Entry(register_window, width=30)
        address_entry.pack(pady=5)

        tk.Label(register_window, text="Số điện thoại:", bg="#00CED1", fg="#483D8B").pack(anchor=tk.W, padx=20)
        phone_entry = tk.Entry(register_window, width=30)
        phone_entry.pack(pady=5)

        def register():
            # Validate input
            if not all([username_entry.get(), password_entry.get(), email_entry.get(), phone_entry.get()]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
                return

            # Validate email
            if "@" not in email_entry.get() or "." not in email_entry.get():
                messagebox.showerror("Lỗi", "Email không hợp lệ")
                return

            # Validate phone number
            if not phone_entry.get().isdigit() or len(phone_entry.get()) < 10:
                messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ")
                return

            success, message = self.auth_manager.register_user(
                username_entry.get(),
                password_entry.get(),
                email_entry.get(),
                address_entry.get(),
                phone_entry.get()
            )

            if success:
                messagebox.showinfo("Thành công", message)
                register_window.destroy()
            else:
                messagebox.showerror("Lỗi", message)

        # Nút đăng ký
        tk.Button(register_window, text="Đăng ký", command=register, bg="#483D8B", fg="#FFFFFF", width=15).pack(pady=10)

        # Nút hủy
        tk.Button(register_window, text="Hủy", command=register_window.destroy, bg="#483D8B", fg="#FFFFFF", width=15).pack(pady=5)