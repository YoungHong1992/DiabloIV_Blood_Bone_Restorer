import sys
import os
import time
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import webbrowser

__version__ = "1.0.0"

# 引入 winreg 用于访问 Windows 注册表
try:
    import winreg
except ImportError:
    winreg = None

class FinalStepDialog(tk.Toplevel):
    """完成后的引导弹窗"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("最后一步: 战网设置")
        self.withdraw()
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # 设置样式
        self.configure(bg="#18181b")
        
        # 创建主框架
        main_frame = tk.Frame(self, bg="#18181b")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 标题
        title = tk.Label(main_frame, text="最后一步: 战网设置", 
                        font=("Times New Roman", 20, "bold"), 
                        fg="#ef4444", bg="#18181b")
        title.pack(anchor=tk.W, pady=(0, 15))
        
        # 说明文本
        instructions = (
            "请务必完成以下操作以生效：\n\n"
            "1. 打开 战网客户端 (Battle.net)\n"
            "2. 点击 游戏设置 -> 暗黑破坏神4\n"
            "3. 勾选 '额外命令行参数'\n"
            "4. 复制并粘贴下方代码到输入框中："
        )
        lbl_inst = tk.Label(main_frame, text=instructions, 
                           font=(".", 12), 
                           fg="#d4d4d8", bg="#18181b", 
                           justify=tk.LEFT, wraplength=400)
        lbl_inst.pack(anchor=tk.W, pady=(0, 15))
        
        # 代码复制区域
        code_frame = tk.Frame(main_frame, bg="#000", bd=1, relief=tk.SOLID, highlightbackground="#3f3f46", highlightthickness=1)
        code_frame.pack(fill=tk.X, pady=(0, 15))
        
        code_layout = tk.Frame(code_frame, bg="#000")
        code_layout.pack(fill=tk.X, padx=10, pady=10)
        
        self.code_text = " -enableagentmanager"
        self.code_lbl = tk.Label(code_layout, text=self.code_text, 
                                font=("Consolas", 16), 
                                fg="#22c55e", bg="#000")
        self.code_lbl.pack(side=tk.LEFT, padx=5)
        
        self.copy_btn = tk.Button(code_layout, text="复制", 
                                 bg="#27272a", fg="#a1a1aa", 
                                 bd=1, relief=tk.SOLID, highlightbackground="#3f3f46", 
                                 font=(".", 12), 
                                 command=self.copy_to_clipboard, width=8)
        self.copy_btn.pack(side=tk.RIGHT, padx=5)
        
        # 警告提示
        warning_frame = tk.Frame(main_frame, bg="#2d1f1f", bd=1, relief=tk.SOLID, highlightbackground="#7f1d1d")
        warning_frame.pack(fill=tk.X, pady=(0, 15))
        
        warn_lbl = tk.Label(warning_frame, text="注意：请确保代码最前方包含一个空格（已包含）。重启游戏后生效。", 
                          font=(".", 12), 
                          fg="#fca5a5", bg="#2d1f1f", 
                          wraplength=400)
        warn_lbl.pack(padx=10, pady=10, anchor=tk.W)
        
        # 关闭按钮
        btn_frame = tk.Frame(main_frame, bg="#18181b")
        btn_frame.pack(side=tk.RIGHT, pady=(15, 0))
        
        close_btn = tk.Button(btn_frame, text="我已完成", 
                             bg="#27272a", fg="#e4e4e7", 
                             bd=1, relief=tk.SOLID, highlightbackground="#3f3f46", 
                             font=(".", 12), 
                             command=self.accept, width=12)
        close_btn.pack()

        # 自动调整大小并居中
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.code_text)
        self.copy_btn.config(text="已复制!", fg="#22c55e", highlightbackground="#22c55e")
        self.after(2000, self.reset_copy_btn)
    
    def reset_copy_btn(self):
        self.copy_btn.config(text="复制", fg="#a1a1aa", highlightbackground="#3f3f46")
    
    def accept(self):
        self.destroy()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DiabloIV Blood & Bone Restorer")
        self.geometry("800x550")
        self.resizable(False, False)
        
        # 窗口居中
        self.update_idletasks()
        width = 800
        height = 550
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # 设置样式
        self.configure(bg="#1a1a1a")
        
        # 创建样式
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 配置ttk样式
        self.style.configure("TButton", 
                           background="#27272a", 
                           foreground="#e4e4e7",
                           borderwidth=1)
        
        # 创建主布局
        self.create_widgets()
        
        # 启动自动检测
        self.after(500, self.auto_detect_game_path)
    
    def create_widgets(self):
        # 1. Header
        header = tk.Frame(self, bg="#0f0f11", height=120)
        header.pack(fill=tk.X, anchor=tk.N)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Blood & Bone Restorer", 
                        font=("Times New Roman", 24, "bold"), 
                        fg="#ef4444", bg="#0f0f11")
        title.pack(pady=(20, 5))
        
        subtitle = tk.Label(header, text="SANCTUARY UNCENSORED PROTOCOL", 
                          font=(".", 12), 
                          fg="#71717a", bg="#0f0f11")
        subtitle.pack()
        
        # 2. Content
        content_widget = tk.Frame(self, bg="#1a1a1a")
        content_widget.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Path Selection
        path_label = tk.Label(content_widget, text="游戏安装目录 (Game Directory)", 
                           font=(".", 12, "bold"), 
                           fg="#a1a1aa", bg="#1a1a1a")
        path_label.pack(anchor=tk.W, pady=(0, 10))
        
        path_row = tk.Frame(content_widget, bg="#1a1a1a")
        path_row.pack(fill=tk.X, anchor=tk.W)
        
        self.path_input = tk.Entry(path_row, 
                                  bg="#000", fg="#e4e4e7", 
                                  bd=1, relief=tk.SOLID, highlightbackground="#3f3f46", 
                                  font=(".", 14), 
                                  width=60)
        self.path_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.path_input.insert(0, "正在检测路径...")
        self.path_input.config(state="disabled")
        
        browse_btn = tk.Button(path_row, text="浏览...", 
                              bg="#27272a", fg="#e4e4e7", 
                              bd=1, relief=tk.SOLID, highlightbackground="#3f3f46", 
                              font=(".", 12), 
                              command=self.browse_folder, width=12)
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Action Bar
        action_frame = tk.Frame(content_widget, bg="#18181b", 
                               bd=1, relief=tk.SOLID, highlightbackground="#27272a")
        action_frame.pack(fill=tk.X, pady=20, padx=0)
        action_frame.pack_propagate(False)
        action_frame.configure(height=80)
        
        action_inner = tk.Frame(action_frame, bg="#18181b")
        action_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        status_layout = tk.Frame(action_inner, bg="#18181b")
        status_layout.pack(side=tk.LEFT, fill=tk.Y)
        
        status_lbl_title = tk.Label(status_layout, text="当前状态:", 
                                  font=(".", 13, "bold"), 
                                  fg="#d4d4d8", bg="#18181b")
        status_lbl_title.pack(anchor=tk.W)
        
        self.status_value = tk.Label(status_layout, text="未知 / 等待检测", 
                                   font=(".", 13), 
                                   fg="#ca8a04", bg="#18181b")
        self.status_value.pack(anchor=tk.W)
        
        self.restore_btn = tk.Button(action_inner, text="执行反和谐 (Restore)", 
                                   bg="#991b1b", fg="white", 
                                   bd=1, relief=tk.SOLID, highlightbackground="#b91c1c", 
                                   font=(".", 15, "bold"), 
                                   command=self.on_main_button_click, 
                                   width=20, height=2)
        self.restore_btn.pack(side=tk.RIGHT)
        self.restore_btn.config(state="disabled")
        
        # Log Console
        log_label_row = tk.Frame(content_widget, bg="#1a1a1a")
        log_label_row.pack(fill=tk.X, pady=(0, 10))
        
        log_lbl = tk.Label(log_label_row, text="SYSTEM LOG", 
                         font=(".", 10, "bold"), 
                         fg="#52525b", bg="#1a1a1a")
        log_lbl.pack(side=tk.RIGHT)
        
        # 日志文本框
        log_frame = tk.Frame(content_widget, bg="#000", 
                           bd=1, relief=tk.SOLID, highlightbackground="#3f3f46")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console = tk.Text(log_frame, 
                              bg="#000", fg="#a1a1aa", 
                              bd=0, 
                              font=("Consolas", 12), 
                              wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.console, orient=tk.VERTICAL, command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=scrollbar.set)
        self.console.config(state="disabled")
        
        # 3. Footer
        footer = tk.Frame(self, bg="#0f0f11", height=30)
        footer.pack(fill=tk.X, anchor=tk.S)
        footer.pack_propagate(False)
        
        f1 = tk.Label(footer, text="https://github.com/YoungHong1992/DiabloIV_Blood_Bone_Restorer", 
                     font=(".", 11, "underline"), 
                     fg="#3b82f6", bg="#0f0f11", cursor="hand2")
        f1.pack(side=tk.LEFT, padx=15)
        f1.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/YoungHong1992/DiabloIV_Blood_Bone_Restorer"))
        
        f2 = tk.Label(footer, text="Based on BBR Prototype", 
                     font=(".", 11), 
                     fg="#52525b", bg="#0f0f11")
        f2.pack(side=tk.RIGHT, padx=15)
    
    def log(self, message, msg_type="info"):
        timestamp = time.strftime("%H:%M:%S")
        color_code = {"success": "#22c55e", "error": "#ef4444", "warning": "#eab308", "cmd": "#06b6d4"}
        color = color_code.get(msg_type, "#a1a1aa")
        
        # 在tkinter中，我们使用标签来实现彩色文本
        self.console.config(state="normal")
        
        # 插入时间戳
        self.console.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # 插入消息
        self.console.insert(tk.END, f"{message}\n", msg_type)
        
        # 设置标签样式
        self.console.tag_config("timestamp", foreground="#52525b")
        self.console.tag_config("success", foreground="#22c55e")
        self.console.tag_config("error", foreground="#ef4444")
        self.console.tag_config("warning", foreground="#eab308")
        self.console.tag_config("cmd", foreground="#06b6d4")
        
        # 滚动到底部
        self.console.see(tk.END)
        self.console.config(state="disabled")
        
        # 处理事件
        self.update_idletasks()
    
    # --- Path Detection & Validation ---
    
    def find_game_in_registry(self, exe_name="Diablo IV.exe"):
        paths = []
        if winreg is None: return paths
        uninstall_keys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for base_key_path in uninstall_keys:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_key_path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            sub_key_name = winreg.EnumKey(key, i)
                            if "Diablo IV" in sub_key_name or "Diablo 4" in sub_key_name:
                                with winreg.OpenKey(key, sub_key_name) as sub_key:
                                    try:
                                        path = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                                        if path and os.path.exists(os.path.join(path, exe_name)):
                                            paths.append(path)
                                    except FileNotFoundError: pass
                        except OSError: continue
            except OSError: continue
        return paths
    
    def scan_common_paths(self, exe_name="Diablo IV.exe"):
        found = []
        drives = [f"{chr(x)}:\\" for x in range(67, 72)]
        common_suffixes = [
            "Diablo IV", "Games\\Diablo IV", "Program Files (x86)\\Diablo IV",
            "Program Files\\Diablo IV", "Battle.net\\Games\\Diablo IV"
        ]
        for drive in drives:
            for suffix in common_suffixes:
                full_path = os.path.join(drive, suffix)
                if os.path.exists(os.path.join(full_path, exe_name)):
                    found.append(full_path)
        return found
    
    def check_game_status(self, path):
        """
        核心功能：检测已选路径下的反和谐状态
        """
        if not path:
            return
        
        config_path = os.path.join(path, "WTF", "Config.wtf")
        is_valid = False
        
        # 检测文件内容
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'SET OverrideArchive "0"' in content:
                    is_valid = True
            except:
                try:
                    with open(config_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                    if 'SET OverrideArchive "0"' in content:
                        is_valid = True
                except: pass
        
        # 根据状态更新 UI
        if is_valid:
            self.status_value.config(text="已反和谐 (需配置启动参数)", fg="#22c55e")
            
            # 切换按钮为“查看指引”模式
            self.restore_btn.config(text="查看启动参数指引", bg="#064e3b", 
                                  fg="#a7f3d0", highlightbackground="#059669")
            self.restore_btn.config(state="normal")
            self.restore_btn.mode = "guide"
            
            self.log("检测结果: 配置文件完整且正确。", "success")
        else:
            self.status_value.config(text="未反和谐 / 文件缺失", fg="#eab308")
            
            # 切换按钮为“执行反和谐”模式
            self.restore_btn.config(text="执行反和谐 (Restore)", bg="#991b1b", 
                                  fg="white", highlightbackground="#b91c1c")
            self.restore_btn.config(state="normal")
            self.restore_btn.mode = "restore"
            
            if os.path.exists(config_path):
                self.log("检测结果: 配置文件存在但缺少参数。", "warning")
            else:
                self.log("检测结果: 未找到反和谐配置文件。", "warning")
    
    def auto_detect_game_path(self):
        def detect():
            self.log("正在自动检测游戏路径...", "cmd")
            found_paths = []
            
            self.log(">>> 查询 Windows 注册表...")
            reg_paths = self.find_game_in_registry()
            if reg_paths:
                for p in reg_paths: 
                    self.log(f"✓ 注册表找到: {p}", "success")
                    found_paths.append(p)
            
            if not found_paths:
                self.log(">>> 扫描常见硬盘路径...")
                common_paths = self.scan_common_paths()
                if common_paths:
                    for p in common_paths: 
                        self.log(f"✓ 硬盘扫描找到: {p}", "success")
                        found_paths.append(p)
            
            if found_paths:
                best_path = list(set(found_paths))[0]
                self.path_input.config(state="normal")
                self.path_input.delete(0, tk.END)
                self.path_input.insert(0, best_path)
                self.path_input.config(state="disabled")
                self.log(f"✅ 最终锁定路径: {best_path}", "success")
                # 检测该路径下的状态
                self.check_game_status(best_path)
            else:
                self.log("❌ 未自动找到游戏路径，请手动指定。", "error")
                self.path_input.config(state="normal")
                self.path_input.delete(0, tk.END)
                self.path_input.insert(0, "")
                self.path_input.config(state="normal")
                self.restore_btn.config(state="disabled")
        
        # 在新线程中运行检测，避免阻塞UI
        thread = threading.Thread(target=detect)
        thread.daemon = True
        thread.start()
    
    def browse_folder(self):
        start_dir = self.path_input.get() if self.path_input.get() else "C:/"
        dir_path = filedialog.askdirectory(parent=self, 
                                          title="选择 Diablo IV 安装目录", 
                                          initialdir=start_dir)
        
        if dir_path:
            dir_path = os.path.normpath(dir_path)
            # 简单校验
            if os.path.exists(os.path.join(dir_path, "Diablo IV.exe")) or os.path.exists(os.path.join(dir_path, "Diablo IV Launcher.exe")):
                self.path_input.config(state="normal")
                self.path_input.delete(0, tk.END)
                self.path_input.insert(0, dir_path)
                self.path_input.config(state="disabled")
                self.log(f"已手动选择目录: {dir_path}", "cmd")
                # 检测该路径下的状态
                self.check_game_status(dir_path)
            else:
                self.path_input.config(state="normal")
                self.path_input.delete(0, tk.END)
                self.path_input.insert(0, dir_path)
                self.path_input.config(state="normal")
                self.log(f"警告: 该目录下未发现游戏主程序。", "warning")
                # 依然允许尝试检测，防止文件名变动
                self.check_game_status(dir_path)
    
    def on_main_button_click(self):
        """主按钮点击处理，根据模式分发"""
        mode = getattr(self.restore_btn, 'mode', 'restore')
        if mode == "guide":
            # 仅显示指引
            dialog = FinalStepDialog(self)
            self.wait_window(dialog)
        else:
            # 执行反和谐
            self.run_restoration_logic()
    
    def run_restoration_logic(self):
        def restoration():
            game_path = self.path_input.get()
            if not game_path or not os.path.exists(game_path):
                self.log(f"错误: 路径无效", "error")
                return
        
            self.restore_btn.config(state="disabled")
            self.restore_btn.config(text="处理中...")
            self.log("-" * 30, "cmd")
            
            try:
                self.log("初始化反和谐程序...", "cmd")
                time.sleep(0.5)
                self.update_idletasks()
        
                wtf_folder = os.path.join(game_path, "WTF")
                config_file = os.path.join(wtf_folder, "Config.wtf")
        
                # 1. 创建文件夹
                if not os.path.exists(wtf_folder):
                    self.log(f"正在创建目录: {wtf_folder}", "warning")
                    os.makedirs(wtf_folder)
                    time.sleep(0.2)
                    self.update_idletasks()
                
                # 2. 写入文件
                content = 'SET OverrideArchive "0"'
        
                if os.path.exists(config_file):
                    self.log("更新现有配置文件...", "info")
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f: 
                            existing = f.read()
                    except: 
                        with open(config_file, 'r', encoding='latin-1') as f: 
                            existing = f.read()
                    
                    if 'SET OverrideArchive "0"' not in existing:
                         with open(config_file, 'a', encoding='utf-8') as f:
                            f.write(f'\n{content}\n')
                         self.log(f"参数已追加。", "success")
                else:
                    with open(config_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.log(f"文件创建成功。", "success")
        
                time.sleep(0.5)
                self.update_idletasks()
                self.log("操作完成。", "success")
                
                # 刷新状态
                self.check_game_status(game_path)
                
                # 弹出指引
                time.sleep(0.5)
                self.update_idletasks()
                dialog = FinalStepDialog(self)
                self.wait_window(dialog)
        
            except Exception as e:
                self.log(f"错误: {str(e)}", "error")
                self.restore_btn.config(text="执行反和谐 (Restore)")
                self.restore_btn.config(state="normal")
        
        # 在新线程中运行恢复逻辑，避免阻塞UI
        thread = threading.Thread(target=restoration)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
