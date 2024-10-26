import tkinter as tk
from tkinter import ttk
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("文件浏览器")
        self.geometry("800x600")

        # 按钮框架
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        # 回退按钮
        self.back_button = tk.Button(self.button_frame, text="回退", command=self.go_back)
        self.back_button.pack(side=tk.LEFT)

        # 向上按钮
        self.up_button = tk.Button(self.button_frame, text="向上", command=self.go_up)
        self.up_button.pack(side=tk.LEFT)

        # 回到根目录按钮
        self.root_button = tk.Button(self.button_frame, text="回到根目录", command=self.go_root)
        self.root_button.pack(side=tk.LEFT)

        # 左侧文件列表
        self.file_list = tk.Listbox(self)
        self.file_list.pack(side=tk.LEFT, fill=tk.Y)

        # 右侧内容显示区域
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.content_label = tk.Label(self.content_frame, text="请选择一个文件")
        self.content_label.pack(expand=True)

        # 获取盘符并添加到列表中
        self.current_path = ""
        self.update_file_list(self.get_drives())

        # 绑定选择事件
        self.file_list.bind("<<ListboxSelect>>", self.on_file_select)

    def get_drives(self):
        if os.name == 'nt':
            import string
            drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        else:
            drives = ["/"]
        return drives

    def on_file_select(self, event):
        selected = self.file_list.get(self.file_list.curselection())
        if selected == "..":
            self.go_up()
        elif os.path.isdir(selected):
            self.current_path = selected
            self.update_file_list(os.listdir(selected))
        else:
            self.content_label.config(text=f"打开文件: {selected}")

    def update_file_list(self, items):
        self.file_list.delete(0, tk.END)
        if self.current_path:
            self.file_list.insert(tk.END, "..")
        for item in items:
            self.file_list.insert(tk.END, os.path.join(self.current_path, item))

    def go_back(self):
        # 实现回退功能
        pass

    def go_up(self):
        if self.current_path:
            self.current_path = os.path.dirname(self.current_path)
            self.update_file_list(os.listdir(self.current_path) if self.current_path else self.get_drives())

    def go_root(self):
        self.current_path = ""
        self.update_file_list(self.get_drives())

if __name__ == "__main__":
    app = App()
    app.mainloop()
