import tkinter as tk
from gui.login_window import LoginWindow
from core.data_handler import initialize_data_files
import os

def main():
    # Khởi tạo file dữ liệu
    from core.data_handler import initialize_data_files
    initialize_data_files()
    
    # Tạo cửa sổ đăng nhập
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

print("Current working directory:", os.getcwd())
print("Data path:", os.path.abspath('data/housewares.json'))