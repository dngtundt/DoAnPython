import tkinter as tk
from tkinter import ttk, messagebox
from core.houseware import HousewareManager
from core.data_handler import get_users, save_users
from core.auth_manager import AuthManager

class UserWindow:
    def __init__(self, master, login_window, username):
        self.master = master
        self.login_window = login_window
        self.username = username
        self.user_data = self.get_user_data()
        self.master.title(f"Quản lý đồ gia dụng - {self.username}")
        self.master.geometry("1500x500")
        
        self.houseware_manager = HousewareManager()
        self.create_widgets()
        self.load_housewares()
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
        self.tooltip = tk.Toplevel(self.master)
        self.tooltip.withdraw()  # Ẩn tooltip mặc định
        self.tooltip.overrideredirect(True)  # Loại bỏ viền cửa sổ
        self.tooltip_label = tk.Label(self.tooltip, text="", background="yellow", relief=tk.SOLID, borderwidth=1, padx=5, pady=2)
        self.tooltip_label.pack()

    def get_user_data(self):
        users = get_users()
        for user in users:
            if user['username'] == self.username:
                return user
        return None

    def on_close(self):
        self.login_window.deiconify()
        self.master.destroy()
        
    def create_widgets(self):
        # Xóa toàn bộ widget cũ trước khi vẽ lại
        for widget in self.master.winfo_children():
            widget.destroy()

        # Tạo frame chính với 2 phần: thông tin user và danh sách sản phẩm
        self.main_frame = tk.Frame(self.master, bg="#00CED1")  # Xanh ngọc
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame thông tin user (bên trái)
        user_info_frame = tk.Frame(self.main_frame, width=350, padx=10, pady=10, relief=tk.RIDGE, bd=2, bg="#483D8B")  # Tím xanh đậm
        user_info_frame.pack(side=tk.LEFT, fill=tk.Y)
        user_info_frame.pack_propagate(False)

        tk.Label(user_info_frame, text="THÔNG TIN CÁ NHÂN", font=('Arial', 12, 'bold'), bg="#483D8B", fg="white").pack(pady=5)

        # Hiển thị thông tin user
        info_labels = [
            ("Tên đăng nhập:", self.user_data['username']),
            ("Email:", self.user_data.get('email', 'Chưa cập nhật')),
            ("Địa chỉ:", self.user_data.get('address', 'Chưa cập nhật')),
            ("Số điện thoại:", self.user_data.get('phone', 'Chưa cập nhật')),
            ("Ngày đăng ký:", self.user_data.get('registration_date', 'Chưa cập nhật'))
        ]
        
        for label, value in info_labels:
            frame = tk.Frame(user_info_frame, bg="#483D8B")  # Tím xanh đậm
            frame.pack(fill=tk.X, pady=2)
            tk.Label(frame, text=label, width=15, anchor='w', bg="#483D8B", fg="white").pack(side=tk.LEFT)
            tk.Label(frame, text=value, anchor='w', bg="#483D8B", fg="white").pack(side=tk.LEFT, fill=tk.X, expand=True)
        

        # Nút chỉnh sửa thông tin
        btn_edit = tk.Button(user_info_frame, text="Chỉnh sửa thông tin", command=self.edit_profile, bg="#00CED1", fg="black")
        btn_edit.pack(pady=10)
        btn_edit.bind("<Enter>", self.on_hover)
        btn_edit.bind("<Leave>", self.on_leave)

        # Frame danh sách sản phẩm (bên phải)
        product_frame = tk.Frame(self.main_frame, bg="#00CED1")  # Xanh ngọc
        product_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame tìm kiếm
        search_frame = tk.Frame(product_frame, bg="#483D8B")  # Tím xanh đậm
        search_frame.pack(fill=tk.X, pady=5)

        tk.Label(search_frame, text="Tìm kiếm:", bg="#483D8B", fg="white").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        btn_search = tk.Button(search_frame, text="Tìm", command=self.search_housewares, bg="#00CED1", fg="black")
        btn_search.pack(side=tk.LEFT)
        btn_search.bind("<Enter>", self.on_hover)
        btn_search.bind("<Leave>", self.on_leave)

        btn_refresh = tk.Button(search_frame, text="Làm mới", command=self.load_housewares, bg="#00CED1", fg="black")
        btn_refresh.pack(side=tk.LEFT, padx=5)
        btn_refresh.bind("<Enter>", self.on_hover)
        btn_refresh.bind("<Leave>", self.on_leave)

        # Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(product_frame, columns=('ID', 'Tên', 'Giá', 'Phân loại', 'Thương hiệu', 'Tồn kho'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tên', text='Tên')
        self.tree.heading('Giá', text='Giá')
        self.tree.heading('Phân loại', text='Phân loại')
        self.tree.heading('Thương hiệu', text='Thương hiệu')
        self.tree.heading('Tồn kho', text='Tồn kho')

        self.tree.column('ID', width=30)
        self.tree.column('Tên', width=200)
        self.tree.column('Giá', width=100)
        self.tree.column('Phân loại', width=150)
        self.tree.column('Thương hiệu', width=150)
        self.tree.column('Tồn kho', width=10)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Nút chức năng
        button_frame = tk.Frame(product_frame, bg="#483D8B")  # Tím xanh đậm
        button_frame.pack(fill=tk.X)

        btn_details = tk.Button(button_frame, text="Xem chi tiết", command=self.show_details, bg="#00CED1", fg="black")
        btn_details.pack(side=tk.LEFT, padx=5)
        btn_details.bind("<Enter>", self.on_hover)
        btn_details.bind("<Leave>", self.on_leave)

        btn_logout = tk.Button(button_frame, text="Đăng xuất", command=self.on_close, bg="#1E00CA", fg="white")
        btn_logout.pack(side=tk.RIGHT)
        btn_logout.bind("<Enter>", self.on_hover)
        btn_logout.bind("<Leave>", self.on_leave)

        # Thêm menu sắp xếp
        sort_frame = tk.Frame(product_frame, bg="#00CED1")  # Xanh ngọc
        sort_frame.pack(fill=tk.X, pady=5)

        tk.Label(sort_frame, text="Sắp xếp:", bg="#00CED1", fg="black").pack(side=tk.LEFT)

        self.sort_var = tk.StringVar(value="id_asc")
        self.sort_options = {
            "ID (tăng dần)": "id_asc",
            "ID (giảm dần)": "id_desc",
            "Giá (thấp đến cao)": "price_asc",
            "Giá (cao đến thấp)": "price_desc",
            "Tên (A-Z)": "name_asc",
            "Tên (Z-A)": "name_desc"
        }

        sort_menu = tk.OptionMenu(sort_frame, self.sort_var, *self.sort_options.values(), command=self.sort_housewares)
        sort_menu.config(width=20, bg="#483D8B", fg="white", highlightbackground="#483D8B")  # Tím xanh đậm
        sort_menu.pack(side=tk.LEFT, padx=5)

        # Đổi tên hiển thị cho đẹp
        menu = sort_menu["menu"]
        menu.delete(0, "end")
        for text, value in self.sort_options.items():
            menu.add_command(label=text, command=lambda v=value: self.sort_var.set(v) or self.sort_housewares(v))

        # Gắn sự kiện hover vào Treeview
        self.tree.bind("<Motion>", self.show_tooltip)  # Hiển thị tooltip khi di chuột
        self.tree.bind("<Leave>", self.hide_tooltip)  # Ẩn tooltip khi rời chuột

        # Tải dữ liệu sản phẩm
        self.load_housewares()
    
    def edit_profile(self):
        # Tạo cửa sổ chỉnh sửa thông tin
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Chỉnh sửa thông tin")
        edit_window.geometry("500x400")  # Tăng kích thước cửa sổ
        edit_window.configure(bg="#00CED1")  # Xanh ngọc

        # Tiêu đề
        tk.Label(edit_window, text="CHỈNH SỬA THÔNG TIN", font=("Arial", 16, "bold"), bg="#00CED1", fg="#483D8B").grid(row=0, columnspan=2, pady=20)

        # Tạo các trường nhập liệu
        tk.Label(edit_window, text="Email:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=1, column=0, sticky='e', padx=20, pady=10)
        email_entry = tk.Entry(edit_window, width=40)
        email_entry.grid(row=1, column=1, padx=20, pady=10)
        email_entry.insert(0, self.user_data.get('email', ''))

        tk.Label(edit_window, text="Địa chỉ:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=2, column=0, sticky='e', padx=20, pady=10)
        address_entry = tk.Entry(edit_window, width=40)
        address_entry.grid(row=2, column=1, padx=20, pady=10)
        address_entry.insert(0, self.user_data.get('address', ''))

        tk.Label(edit_window, text="Số điện thoại:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=3, column=0, sticky='e', padx=20, pady=10)
        phone_entry = tk.Entry(edit_window, width=40)
        phone_entry.grid(row=3, column=1, padx=20, pady=10)
        phone_entry.insert(0, self.user_data.get('phone', ''))

        # Hiệu ứng hover cho nút
        def on_hover(event):
            event.widget.config(bg="#8B4513", fg="#FFFFFF")  # Nâu và chữ trắng

        def on_leave(event):
            event.widget.config(bg="#483D8B", fg="#FFFFFF")  # Tím xanh đậm và chữ trắng

        # Nút lưu
        def save_changes():
            # Cập nhật thông tin
            users = get_users()
            for user in users:
                if user['username'] == self.username:
                    user['email'] = email_entry.get()
                    user['address'] = address_entry.get()
                    user['phone'] = phone_entry.get()
                    break

            save_users(users)
            self.user_data = self.get_user_data()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin")
            edit_window.destroy()
            self.update_user_info()  # Chỉ cập nhật phần thông tin người dùng

        btn_save = tk.Button(edit_window, text="Lưu", command=save_changes, bg="#483D8B", fg="#FFFFFF", width=15)
        btn_save.grid(row=4, column=1, pady=20)
        btn_save.bind("<Enter>", on_hover)
        btn_save.bind("<Leave>", on_leave)

        # Nút hủy
        btn_cancel = tk.Button(edit_window, text="Hủy", command=edit_window.destroy, bg="#483D8B", fg="#FFFFFF", width=15)
        btn_cancel.grid(row=4, column=0, pady=20, padx=40)
        btn_cancel.bind("<Enter>", on_hover)
        btn_cancel.bind("<Leave>", on_leave)
        
    def sort_housewares(self, sort_type):
        """Xử lý sự kiện sắp xếp"""
        try:
            self.houseware_manager.sort_housewares(sort_type)
            self.load_housewares()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sắp xếp: {str(e)}")

    def load_housewares(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        housewares = self.houseware_manager.get_all_housewares()
        for item in housewares:
            self.tree.insert('', 'end', values=(
                item['id'],
                item['tên'],
                f"{item['giá']:,.0f} VND",
                item['thương hiệu'],
                item['phân loại'],
                item['số lượng tồn kho']
            ))

    def search_housewares(self):
        """Tìm kiếm sản phẩm"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.load_housewares()
            return
        
        results = self.houseware_manager.search_housewares(keyword)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for item in results:
            self.tree.insert('', tk.END, values=(
                item['id'],
                item['tên'],
                f"${item['giá']:.2f}",
                item['thương hiệu'],
                item['số lượng tồn kho']
            ))
    
    def show_details(self):
        """Hiển thị chi tiết sản phẩm"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm")
            return
        
        item_id = int(self.tree.item(selected[0], 'values')[0])
        item = self.houseware_manager.get_houseware_by_id(item_id)
        
        if not item:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm")
            return
        
        dialog = tk.Toplevel(self.master)
        dialog.title(f"Chi tiết: {item['tên']}")
        dialog.geometry("500x400")
        
        # Hiển thị thông tin sản phẩm
        tk.Label(dialog, text=f"Tên: {item['tên']}").pack(anchor='w', pady=2)
        tk.Label(dialog, text=f"Giá: {item['giá']:,.0f} VND").pack(anchor='w', pady=2)
        tk.Label(dialog, text=f"Thương hiệu: {item['thương hiệu']}").pack(anchor='w', pady=2)
        tk.Label(dialog, text=f"Phân loại: {item['phân loại']}").pack(anchor='w', pady=2)
        tk.Label(dialog, text=f"Tồn kho: {item['số lượng tồn kho']}").pack(anchor='w', pady=2)
        
        # Frame mô tả
        desc_frame = tk.LabelFrame(dialog, text="Mô tả", padx=5, pady=5)
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=5)
        desc_text.insert(tk.END, item['mô tả'])
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        # Nút đóng
        tk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=10)
    
    def show_tooltip(self, event):
        """Hiển thị tooltip khi hover"""
        item = self.tree.identify_row(event.y)  # Lấy ID của hàng được hover
        if item:  # Nếu hover vào một hàng
            try:
                item_id = int(self.tree.item(item, 'values')[0])  # Lấy ID sản phẩm
                product = self.houseware_manager.get_houseware_by_id(item_id)  # Lấy thông tin sản phẩm

                if product:
                    # Nội dung tooltip
                    text = f"{product['tên']}\nGiá: {product['giá']:,.0f} VND\nTồn kho: {product['số lượng tồn kho']}"

                    self.tooltip_label.config(text=text)
                    self.tooltip.update_idletasks()

                    # Vị trí tooltip
                    x = self.tree.winfo_rootx() + event.x + 20
                    y = self.tree.winfo_rooty() + event.y + 20
                    self.tooltip.geometry(f"+{x}+{y}")
                    self.tooltip.deiconify()  # Hiển thị tooltip
            except Exception as e:
                print(f"Lỗi khi hiển thị tooltip: {e}")
                self.hide_tooltip(event)  # Ẩn tooltip nếu có lỗi
        else:
            self.hide_tooltip(event)  # Ẩn tooltip khi rời chuột
    
    def hide_tooltip(self, event):
        """Ẩn tooltip"""
        self.tooltip.withdraw()

    def on_hover(self, event):
        """Thay đổi màu nút khi hover"""
        event.widget.config(bg="#8B4513", fg="#FFFFFF")  # Nâu và chữ trắng

    def on_leave(self, event):
        """Khôi phục màu nút khi rời chuột"""
        event.widget.config(bg="#00CED1", fg="black")  # Xanh ngọc và chữ đen

    def update_user_info(self):
        """Cập nhật phần thông tin người dùng trên giao diện."""
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_width() == 350:  # Frame thông tin user
                for child in widget.winfo_children():
                    child.destroy()

                tk.Label(widget, text="THÔNG TIN CÁ NHÂN", font=('Arial', 12, 'bold'), bg="#483D8B", fg="white").pack(pady=5)

                info_labels = [
                    ("Tên đăng nhập:", self.user_data['username']),
                    ("Email:", self.user_data.get('email', 'Chưa cập nhật')),
                    ("Địa chỉ:", self.user_data.get('address', 'Chưa cập nhật')),
                    ("Số điện thoại:", self.user_data.get('phone', 'Chưa cập nhật')),
                    ("Ngày đăng ký:", self.user_data.get('registration_date', 'Chưa cập nhật'))
                ]

                for label, value in info_labels:
                    frame = tk.Frame(widget, bg="#483D8B")  # Tím xanh đậm
                    frame.pack(fill=tk.X, pady=2)
                    tk.Label(frame, text=label, width=15, anchor='w', bg="#483D8B", fg="white").pack(side=tk.LEFT)
                    tk.Label(frame, text=value, anchor='w', bg="#483D8B", fg="white").pack(side=tk.LEFT, fill=tk.X, expand=True)

                tk.Button(widget, text="Chỉnh sửa thông tin", command=self.edit_profile, bg="#00CED1", fg="black").pack(pady=10)
                break
