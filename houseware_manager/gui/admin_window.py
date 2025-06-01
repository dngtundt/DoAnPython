import tkinter as tk
from tkinter import ttk, messagebox
from core.houseware import HousewareManager
from core.api_crawler import APICrawler

class AdminWindow:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        self.master.title("Quản lý đồ gia dụng - Admin")
        self.master.geometry("1300x500")
        
        # Khởi tạo các thành phần quan trọng trước
        self.houseware_manager = HousewareManager()
        self.api_crawler = APICrawler()
        
        # Tạo các widget giao diện
        self.create_widgets()  # Phải gọi hàm này trước khi bind sự kiện
        
        # Sau khi đã tạo treeview mới bind sự kiện
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Load dữ liệu ban đầu
        self.load_housewares()
        
        # Xử lý sự kiện đóng cửa sổ
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        self.login_window.deiconify()  # Hiển thị lại cửa sổ đăng nhập
        self.master.destroy()
    
    def create_widgets(self):
        # Frame chính
        self.main_frame = tk.Frame(self.master, bg="#00CED1")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame tìm kiếm
        search_frame = tk.Frame(self.main_frame, bg="#483D8B")
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

        btn_crawl = tk.Button(search_frame, text="Crawl dữ liệu", command=self.crawl_data, bg="#00CED1", fg="black")
        btn_crawl.pack(side=tk.RIGHT)
        btn_crawl.bind("<Enter>", self.on_hover)
        btn_crawl.bind("<Leave>", self.on_leave)

        # Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Tên', 'Giá', 'Phân loại', 'Thương hiệu', 'Tồn kho'), show='headings')
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
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=30)
        
        # Frame nút chức năng
        button_frame = tk.Frame(self.main_frame, bg="#483D8B")  # Tím xanh đậm
        button_frame.pack(fill=tk.X)

        btn_add = tk.Button(button_frame, text="Thêm mới", command=self.show_add_dialog, bg="#00CED1", fg="black")
        btn_add.pack(side=tk.LEFT, padx=5)
        btn_add.bind("<Enter>", self.on_hover)
        btn_add.bind("<Leave>", self.on_leave)

        btn_delete = tk.Button(button_frame, text="Xóa", command=self.delete_houseware, bg="#00CED1", fg="black")
        btn_delete.pack(side=tk.LEFT, padx=5)
        btn_delete.bind("<Enter>", self.on_hover)
        btn_delete.bind("<Leave>", self.on_leave)

        btn_logout = tk.Button(button_frame, text="Đăng xuất", command=self.on_close, bg="#1E00CA", fg="white")
        btn_logout.pack(side=tk.RIGHT)
        btn_logout.bind("<Enter>", self.on_hover)
        btn_logout.bind("<Leave>", self.on_leave)
    
            # Tooltip khi hover
        self.tooltip = tk.Toplevel(self.master)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip_label = tk.Label(self.tooltip, bg='lightyellow', relief='solid', borderwidth=1)
        self.tooltip_label.pack()
        self.tree.bind("<Motion>", self.show_tooltip)
        self.tree.bind("<Leave>", self.hide_tooltip)

            # Thêm nút và menu sắp xếp
        sort_frame = tk.Frame(self.main_frame, bg="#00CED1")  # Xanh ngọc
        sort_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(sort_frame, text="Sắp xếp:", bg="#00CED1", fg="#FFFFFF").pack(side=tk.LEFT)
        
        self.sort_var = tk.StringVar(value="id_asc")
        
        sort_options = {
            "ID (tăng dần)": "id_asc",
            "ID (giảm dần)": "id_desc",
            "Giá (thấp đến cao)": "price_asc",
            "Giá (cao đến thấp)": "price_desc",
            "Tên (A-Z)": "name_asc",
            "Tên (Z-A)": "name_desc",
            "Thương hiệu (A-Z)": "brand_asc",
            "Thương hiệu (Z-A)": "brand_desc",
            "Phân loại (A-Z)": "category_asc",
            "Phân loại (Z-A)": "category_desc"
        }
        
        sort_menu = tk.OptionMenu(sort_frame, self.sort_var, *sort_options.values(), command=self.sort_housewares)
        sort_menu.config(width=20, bg="#483D8B", fg="#FFFFFF", highlightbackground="#483D8B")  # Tím xanh đậm
        sort_menu.pack(side=tk.LEFT, padx=5)
        
        # Đổi tên hiển thị cho đẹp
        menu = sort_menu["menu"]
        menu.delete(0, "end")
        for text, value in sort_options.items():
            menu.add_command(label=text, command=lambda v=value: self.sort_var.set(v) or self.sort_housewares(v))

    def sort_housewares(self, sort_type):
        """Xử lý sự kiện sắp xếp"""
        try:
            self.houseware_manager.sort_housewares(sort_type)
            self.load_housewares()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sắp xếp: {str(e)}")

    def setup_context_menu(self):
        """Tạo menu ngữ cảnh khi right-click"""
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Xem chi tiết", command=self.show_selected_details)
        self.context_menu.add_command(label="Chỉnh sửa", command=self.edit_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Xóa", command=self.delete_houseware)
        
        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Hiển thị menu ngữ cảnh"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def show_selected_details(self):
        """Hiển thị chi tiết sản phẩm được chọn"""
        selected = self.tree.selection()
        if selected:
            item_id = int(self.tree.item(selected[0], 'values')[0])
            self.show_edit_dialog(item_id)

    def edit_selected(self):
        """Chỉnh sửa sản phẩm được chọn"""
        selected = self.tree.selection()
        if selected:
            item_id = int(self.tree.item(selected[0], 'values')[0])
            self.show_edit_dialog(item_id, immediate=True)

    def load_housewares(self):
        """Tải lại danh sách sản phẩm vào Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy danh sách sản phẩm từ HousewareManager
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
        """Tìm kiếm sản phẩm theo từ khóa"""
        keyword = self.search_entry.get().strip()

        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Nếu không có từ khóa, tải lại toàn bộ danh sách
        if not keyword:
            self.load_housewares()
            return

        # Tìm kiếm sản phẩm
        results = self.houseware_manager.search_housewares(keyword)

        # Nếu không tìm thấy kết quả, hiển thị thông báo
        if not results:
            messagebox.showinfo("Thông báo", "Không tìm thấy sản phẩm phù hợp")
            self.load_housewares()  # Tải lại toàn bộ danh sách
            return

        # Hiển thị kết quả tìm kiếm trong Treeview
        for item in results:
            self.tree.insert('', tk.END, values=(
                item.get('id', 0),
                item.get('tên', ''),
                f"{item.get('giá', 0):,.0f} VND",
                item.get('thương hiệu', ''),
                item.get('phân loại', ''),
                item.get('số lượng tồn kho', 0)
            ))
    
    def crawl_data(self):
        """Crawl dữ liệu và tự động làm mới giao diện"""
        success, message = self.api_crawler.fetch_housewares()
        if success:
            # Làm mới dữ liệu và giao diện
            self.houseware_manager.refresh_data()
            self.load_housewares()
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)
    
    def show_add_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Thêm sản phẩm mới")
        dialog.geometry("500x600")
        dialog.configure(bg="#00CED1")  # Xanh ngọc

        # Frame chính
        frame = tk.Frame(dialog, padx=10, pady=10, bg="#00CED1")  # Xanh ngọc
        frame.pack(fill=tk.BOTH, expand=True)

        # Các trường nhập liệu
        tk.Label(frame, text="Tên sản phẩm:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        name_entry = tk.Entry(frame, width=40)
        name_entry.pack(pady=5)

        tk.Label(frame, text="Giá:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        price_entry = tk.Entry(frame, width=40)
        price_entry.pack(pady=5)

        tk.Label(frame, text="Thương hiệu:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        brand_entry = tk.Entry(frame, width=40)
        brand_entry.pack(pady=5)

        tk.Label(frame, text="Danh mục:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        category_entry = tk.Entry(frame, width=40)
        category_entry.pack(pady=5)

        tk.Label(frame, text="Mô tả:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        description_entry = tk.Text(frame, width=40, height=4)
        description_entry.pack(pady=5)

        tk.Label(frame, text="Số lượng tồn kho:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        stock_entry = tk.Entry(frame, width=40)
        stock_entry.pack(pady=5)

        # Nút lưu
        def save():
            try:
                new_item = {
                    'id': self.houseware_manager.generate_new_id(),  # Tạo ID mới cho sản phẩm
                    'tên': name_entry.get(),
                    'giá': float(price_entry.get()),
                    'thương hiệu': brand_entry.get(),
                    'phân loại': category_entry.get(),
                    'mô tả': description_entry.get("1.0", tk.END).strip(),
                    'số lượng tồn kho': int(stock_entry.get())
                }

                if self.houseware_manager.add_houseware(new_item):
                    messagebox.showinfo("Thành công", "Thêm sản phẩm mới thành công!")
                    dialog.destroy()
                    self.load_housewares()  # Cập nhật lại danh sách sản phẩm
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm sản phẩm!")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng dữ liệu!")

        # Frame nút
        btn_frame = tk.Frame(frame, bg="#00CED1")  # Xanh ngọc
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Lưu", command=save, bg="#483D8B", fg="#FFFFFF", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Hủy", command=dialog.destroy, bg="#483D8B", fg="#FFFFFF", width=15).pack(side=tk.LEFT, padx=5)
    
    def show_edit_dialog(self, item_id):
        """Hiển thị dialog chỉnh sửa sản phẩm"""
        try:
            item_data = self.houseware_manager.get_houseware_by_id(item_id)
            if not item_data:
                messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm!")
                return

            dialog = tk.Toplevel(self.master)
            dialog.title(f"Chỉnh sửa: {item_data['tên']}")
            dialog.geometry("600x500")
            dialog.configure(bg="#00CED1")  # Xanh ngọc

            # Frame chính
            frame = tk.Frame(dialog, padx=10, pady=10, bg="#00CED1")  # Xanh ngọc
            frame.pack(fill=tk.BOTH, expand=True)

            # Các trường nhập liệu
            tk.Label(frame, text="Tên sản phẩm:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=0, column=0, sticky='w', padx=10, pady=5)
            name_entry = tk.Entry(frame, width=40)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            name_entry.insert(0, item_data['tên'])

            tk.Label(frame, text="Giá (VND):", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=1, column=0, sticky='w', padx=10, pady=5)
            price_entry = tk.Entry(frame, width=40)
            price_entry.grid(row=1, column=1, padx=10, pady=5)
            price_entry.insert(0, str(item_data['giá']))

            tk.Label(frame, text="Thương hiệu:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=2, column=0, sticky='w', padx=10, pady=5)
            brand_entry = tk.Entry(frame, width=40)
            brand_entry.grid(row=2, column=1, padx=10, pady=5)
            brand_entry.insert(0, item_data['thương hiệu'])

            tk.Label(frame, text="Phân loại:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=3, column=0, sticky='w', padx=10, pady=5)
            category_entry = tk.Entry(frame, width=40)
            category_entry.grid(row=3, column=1, padx=10, pady=5)
            category_entry.insert(0, item_data['phân loại'])

            tk.Label(frame, text="Số lượng tồn kho:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=4, column=0, sticky='w', padx=10, pady=5)
            stock_entry = tk.Entry(frame, width=40)
            stock_entry.grid(row=4, column=1, padx=10, pady=5)
            stock_entry.insert(0, str(item_data['số lượng tồn kho']))

            tk.Label(frame, text="Mô tả:", bg="#00CED1", fg="#483D8B", font=("Arial", 12)).grid(row=5, column=0, sticky='nw', padx=10, pady=5)
            desc_text = tk.Text(frame, width=40, height=5, wrap='word')
            desc_text.grid(row=5, column=1, padx=10, pady=5)
            desc_text.insert('1.0', item_data['mô tả'])

            # Hiệu ứng hover cho nút
            def on_hover(event):
                event.widget.config(bg="#8B4513", fg="#FFFFFF")  # Nâu và chữ trắng

            def on_leave(event):
                event.widget.config(bg="#483D8B", fg="#FFFFFF")  # Tím xanh đậm và chữ trắng

            # Nút lưu
            def save_changes():
                new_data = {
                    'id': item_id,
                    'tên': name_entry.get(),
                    'giá': float(price_entry.get()),
                    'thương hiệu': brand_entry.get(),
                    'phân loại': category_entry.get(),
                    'mô tả': desc_text.get("1.0", tk.END).strip(),
                    'số lượng tồn kho': int(stock_entry.get())
                }

                if self.houseware_manager.update_houseware(item_id, new_data):
                    messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm!")
                    self.load_housewares()
                    dialog.destroy()
                else:
                    messagebox.showerror("Lỗi", "Cập nhật thất bại!")

            # Frame nút
            btn_frame = tk.Frame(frame, bg="#00CED1")  # Xanh ngọc
            btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

            btn_save = tk.Button(btn_frame, text="Lưu", command=save_changes, bg="#483D8B", fg="#FFFFFF", width=15)
            btn_save.pack(side='left', padx=5)
            btn_save.bind("<Enter>", on_hover)
            btn_save.bind("<Leave>", on_leave)

            btn_cancel = tk.Button(btn_frame, text="Hủy", command=dialog.destroy, bg="#483D8B", fg="#FFFFFF", width=15)
            btn_cancel.pack(side='left', padx=5)
            btn_cancel.bind("<Enter>", on_hover)
            btn_cancel.bind("<Leave>", on_leave)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở dialog: {str(e)}")

    def delete_houseware(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa")
            return
        
        selected_item = selected_items[0]
        item_id = int(self.tree.item(selected_item, 'values')[0])
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?"):
            if self.houseware_manager.delete_houseware(item_id):
                messagebox.showinfo("Thành công", "Đã xóa sản phẩm thành công")
                self.load_housewares()  # Cập nhật lại danh sách
            else:
                messagebox.showerror("Lỗi", "Không thể xóa sản phẩm")

    def on_double_click(self, event):
        """Xử lý sự kiện double click"""
        try:
            item = self.tree.selection()[0]
            item_id = int(self.tree.item(item, 'values')[0])
            self.show_edit_dialog(item_id)
        except IndexError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở chi tiết: {str(e)}")

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