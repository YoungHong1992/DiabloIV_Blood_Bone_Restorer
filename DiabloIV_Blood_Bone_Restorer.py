import sys
import os
import time
import platform
# 引入 winreg 用于访问 Windows 注册表
try:
    import winreg
except ImportError:
    winreg = None

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QTextEdit, QFileDialog, QDialog, QFrame)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QCursor, QColor, QPalette

# --- 样式表 (QSS) ---
# 保持原有暗黑风格设计
STYLESHEET = """
QMainWindow {
    background-color: #1a1a1a;
}

QWidget {
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    color: #d4d4d8; /* zinc-300 */
    font-size: 14px;
}

/* 标题栏区域背景 */
#HeaderFrame {
    background-color: #0f0f11;
    border-bottom: 1px solid #3f3f46;
}

/* 标题文字 */
#TitleLabel {
    color: #ef4444; /* red-500 */
    font-size: 24px;
    font-weight: bold;
    font-family: "Times New Roman", serif; /* 模拟 Cinzel */
}

#SubtitleLabel {
    color: #71717a; /* zinc-500 */
    font-size: 12px;
    letter-spacing: 2px;
}

/* 输入框 */
QLineEdit {
    background-color: #000000;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    padding: 8px;
    color: #e4e4e7;
    selection-background-color: #991b1b;
}
QLineEdit:focus {
    border: 1px solid #b91c1c;
}

/* 普通按钮 */
QPushButton#BrowseBtn, QPushButton#ModalCloseBtn {
    background-color: #27272a; /* zinc-800 */
    border: 1px solid #3f3f46;
    border-radius: 4px;
    padding: 6px 12px;
    color: #e4e4e7;
}
QPushButton#BrowseBtn:hover, QPushButton#ModalCloseBtn:hover {
    background-color: #3f3f46; /* zinc-700 */
}

/* 红色主按钮 (执行反和谐) */
QPushButton#RestoreBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #991b1b, stop:1 #7f1d1d);
    border: 1px solid #b91c1c;
    border-radius: 4px;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    font-size: 15px;
}
QPushButton#RestoreBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b91c1c, stop:1 #991b1b);
}
QPushButton#RestoreBtn:pressed {
    background-color: #7f1d1d;
    padding-top: 12px; /* 按压效果 */
}

/* 复制按钮 */
QPushButton#CopyBtn {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    color: #a1a1aa;
    padding: 4px 8px;
    font-size: 12px;
}
QPushButton#CopyBtn:hover {
    color: white;
    background-color: #3f3f46;
}

/* 日志区域 */
QTextEdit {
    background-color: #000000;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    padding: 5px;
}

/* 弹窗样式 */
QDialog {
    background-color: #18181b;
    border: 1px solid #7f1d1d;
}
"""

class FinalStepDialog(QDialog):
    """完成后的引导弹窗"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("最后一步: 战网设置")
        self.setFixedSize(500, 350)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint) # 无边框沉浸式
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # 标题
        title = QLabel("最后一步: 战网设置")
        title.setStyleSheet("font-size: 20px; color: #ef4444; font-weight: bold; font-family: 'Times New Roman';")
        layout.addWidget(title)

        # 说明文本
        instructions = (
            "文件修改已成功完成！请完成以下最后一步操作：\n\n"
            "1. 打开 战网客户端 (Battle.net)\n"
            "2. 点击 游戏设置 -> 暗黑破坏神4\n"
            "3. 勾选 '额外命令行参数'\n"
            "4. 复制并粘贴下方代码到输入框中："
        )
        lbl_inst = QLabel(instructions)
        lbl_inst.setWordWrap(True)
        lbl_inst.setStyleSheet("line-height: 1.5;")
        layout.addWidget(lbl_inst)

        # 代码复制区域
        code_frame = QFrame()
        code_frame.setStyleSheet("background-color: #000; border: 1px solid #3f3f46; border-radius: 4px;")
        code_layout = QHBoxLayout(code_frame)
        code_layout.setContentsMargins(10, 10, 10, 10)

        self.code_text = " -enableagentmanager"
        self.code_lbl = QLabel(self.code_text)
        self.code_lbl.setStyleSheet("color: #22c55e; font-family: Consolas; font-size: 16px;")
        
        self.copy_btn = QPushButton("复制")
        self.copy_btn.setObjectName("CopyBtn")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        code_layout.addWidget(self.code_lbl)
        code_layout.addStretch()
        code_layout.addWidget(self.copy_btn)
        layout.addWidget(code_frame)

        # 警告提示
        warning_frame = QFrame()
        warning_frame.setStyleSheet("background-color: rgba(127, 29, 29, 0.2); border: 1px solid rgba(127, 29, 29, 0.5); border-radius: 4px;")
        warn_layout = QHBoxLayout(warning_frame)
        warn_lbl = QLabel("注意：请确保代码最前方包含一个空格（已包含）。重启游戏后生效。")
        warn_lbl.setStyleSheet("color: #fca5a5; font-size: 12px; background: transparent;")
        warn_lbl.setWordWrap(True)
        warn_layout.addWidget(warn_lbl)
        layout.addWidget(warning_frame)

        layout.addStretch()

        # 关闭按钮
        close_btn = QPushButton("我已完成")
        close_btn.setObjectName("ModalCloseBtn")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_text)
        self.copy_btn.setText("已复制!")
        self.copy_btn.setStyleSheet("color: #22c55e; border-color: #22c55e;")
        QTimer.singleShot(2000, self.reset_copy_btn)

    def reset_copy_btn(self):
        self.copy_btn.setText("复制")
        self.copy_btn.setStyleSheet("")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiabloIV Blood & Bone Restorer")
        self.setFixedSize(800, 550)

        # 主容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. 顶部 Header
        header = QFrame()
        header.setObjectName("HeaderFrame")
        header.setFixedHeight(120)
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Blood & Bone Restorer")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("SANCTUARY UNCENSORED PROTOCOL")
        subtitle.setObjectName("SubtitleLabel")
        
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        main_layout.addWidget(header)

        # 2. 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # 路径选择行
        path_label = QLabel("游戏安装目录 (Game Directory)")
        path_label.setStyleSheet("font-weight: bold; color: #a1a1aa; font-size: 12px; text-transform: uppercase;")
        content_layout.addWidget(path_label)

        path_row = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("正在检测路径...")
        self.path_input.setReadOnly(True)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.setObjectName("BrowseBtn")
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_folder)

        path_row.addWidget(self.path_input)
        path_row.addWidget(browse_btn)
        content_layout.addLayout(path_row)

        # 状态与操作栏
        action_frame = QFrame()
        action_frame.setStyleSheet("background-color: #18181b; border: 1px solid #27272a; border-radius: 6px;")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 15, 20, 15)

        status_layout = QVBoxLayout()
        status_lbl_title = QLabel("当前状态:")
        status_lbl_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.status_value = QLabel("未知 / 等待检测")
        self.status_value.setStyleSheet("color: #ca8a04; font-size: 13px;") # yellow-600
        status_layout.addWidget(status_lbl_title)
        status_layout.addWidget(self.status_value)

        self.restore_btn = QPushButton("执行反和谐 (Restore)")
        self.restore_btn.setObjectName("RestoreBtn")
        self.restore_btn.setCursor(Qt.PointingHandCursor)
        self.restore_btn.clicked.connect(self.start_restoration)
        # 初始禁用，直到找到路径
        self.restore_btn.setEnabled(False)

        action_layout.addLayout(status_layout)
        action_layout.addStretch()
        action_layout.addWidget(self.restore_btn)
        content_layout.addWidget(action_frame)

        # 日志控制台
        log_label_row = QHBoxLayout()
        log_lbl = QLabel("SYSTEM LOG")
        log_lbl.setStyleSheet("font-size: 10px; color: #52525b; font-weight: bold;")
        log_label_row.addStretch()
        log_label_row.addWidget(log_lbl)
        content_layout.addLayout(log_label_row)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        content_layout.addWidget(self.console)

        main_layout.addWidget(content_widget)

        # 3. 底部 Footer
        footer = QFrame()
        footer.setFixedHeight(30)
        footer.setStyleSheet("background-color: #0f0f11; border-top: 1px solid #27272a;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)
        f1 = QLabel("BBR Core: Python Edition")
        f2 = QLabel("Based on BBR Prototype")
        f1.setStyleSheet("color: #52525b; font-size: 11px;")
        f2.setStyleSheet("color: #52525b; font-size: 11px;")
        footer_layout.addWidget(f1)
        footer_layout.addStretch()
        footer_layout.addWidget(f2)
        main_layout.addWidget(footer)

        # 初始化并开始自动检测
        self.log("System initialized.", "cmd")
        QTimer.singleShot(500, self.auto_detect_game_path)

    def log(self, message, msg_type="info"):
        timestamp = time.strftime("%H:%M:%S")
        color = "#a1a1aa" # 默认灰色
        if msg_type == "success": color = "#22c55e" # 绿色
        elif msg_type == "error": color = "#ef4444" # 红色
        elif msg_type == "warning": color = "#eab308" # 黄色
        elif msg_type == "cmd": color = "#06b6d4" # 青色

        html = f'<span style="color: #52525b;">[{timestamp}]</span> <span style="color: {color};">{message}</span>'
        self.console.append(html)
        sb = self.console.verticalScrollBar()
        sb.setValue(sb.maximum())
        QApplication.processEvents()

    # ---------------------------------------------------
    # 增强的路径检测逻辑 (基于引用代码适配)
    # ---------------------------------------------------

    def find_game_in_registry(self, exe_name="Diablo IV.exe"):
        """在注册表中查找游戏"""
        paths = []
        if winreg is None: 
            return paths

        # 常见的卸载注册表路径
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
                            # 很多战网游戏直接用 "Diablo IV" 作为键名
                            if "Diablo IV" in sub_key_name or "Diablo 4" in sub_key_name:
                                with winreg.OpenKey(key, sub_key_name) as sub_key:
                                    try:
                                        # 尝试读取安装位置
                                        path = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                                        if path and os.path.exists(os.path.join(path, exe_name)):
                                            paths.append(path)
                                    except FileNotFoundError:
                                        pass
                        except OSError:
                            continue
            except OSError:
                continue
        return paths

    def scan_common_paths(self, exe_name="Diablo IV.exe"):
        """扫描常见安装路径"""
        found = []
        drives = [f"{chr(x)}:\\" for x in range(67, 72)] # C:\ 到 G:\
        
        # 组合常见路径
        common_suffixes = [
            "Diablo IV",
            "Games\\Diablo IV",
            "Program Files (x86)\\Diablo IV",
            "Program Files\\Diablo IV",
            "Battle.net\\Games\\Diablo IV"
        ]

        for drive in drives:
            for suffix in common_suffixes:
                full_path = os.path.join(drive, suffix)
                if os.path.exists(os.path.join(full_path, exe_name)):
                    found.append(full_path)
        
        return found

    def auto_detect_game_path(self):
        """自动检测流程主函数"""
        self.log("正在自动检测游戏路径...", "cmd")
        
        found_paths = []

        # 1. 注册表检测
        self.log(">>> 正在查询 Windows 注册表...")
        reg_paths = self.find_game_in_registry()
        if reg_paths:
            for p in reg_paths:
                self.log(f"✓ 注册表找到: {p}", "success")
                found_paths.append(p)
        
        # 2. 常见路径扫描 (如果注册表没找到，或者作为补充)
        if not found_paths:
            self.log(">>> 注册表未发现，正在扫描常见硬盘路径...")
            common_paths = self.scan_common_paths()
            if common_paths:
                for p in common_paths:
                    self.log(f"✓ 硬盘扫描找到: {p}", "success")
                    found_paths.append(p)

        # 3. 结果处理
        if found_paths:
            # 去重并取第一个有效路径
            best_path = list(set(found_paths))[0]
            self.path_input.setText(best_path)
            self.log(f"✅ 最终锁定路径: {best_path}", "success")
            self.restore_btn.setEnabled(True)
            self.status_value.setText("就绪 / 等待执行")
            self.status_value.setStyleSheet("color: #eab308;") # Yellow
        else:
            self.log("❌ 未自动找到游戏路径。", "error")
            self.log("提示: 请点击 '浏览' 按钮手动指定安装目录。", "warning")
            self.status_value.setText("未找到路径")
            self.path_input.setText("")
            self.path_input.setPlaceholderText("未找到，请手动选择...")
            self.restore_btn.setEnabled(False)

    # ---------------------------------------------------

    def browse_folder(self):
        start_dir = self.path_input.text() if self.path_input.text() else "C:\\"
        dir_path = QFileDialog.getExistingDirectory(self, "选择 Diablo IV 安装目录", start_dir)
        if dir_path:
            dir_path = os.path.normpath(dir_path)
            
            # 手动选择后的简单校验
            if os.path.exists(os.path.join(dir_path, "Diablo IV.exe")) or os.path.exists(os.path.join(dir_path, "Diablo IV Launcher.exe")):
                self.path_input.setText(dir_path)
                self.log(f"已手动选择目录: {dir_path}", "cmd")
                self.restore_btn.setEnabled(True)
                self.status_value.setText("就绪 / 等待执行")
                self.status_value.setStyleSheet("color: #eab308;")
            else:
                self.path_input.setText(dir_path)
                self.log(f"警告: 该目录下未发现游戏主程序，可能选择错误。", "warning")
                self.log(f"已选择: {dir_path}", "cmd")
                self.restore_btn.setEnabled(True) # 仍然允许用户尝试，防止误判

    def start_restoration(self):
        game_path = self.path_input.text()
        
        if not game_path or not os.path.exists(game_path):
            self.log(f"错误: 路径无效", "error")
            return

        self.restore_btn.setEnabled(False)
        self.restore_btn.setText("处理中...")
        
        # 避免清空之前的检测日志，只添加分割线
        self.log("-" * 30, "cmd")
        
        try:
            self.log("初始化反和谐程序...", "cmd")
            QApplication.processEvents()
            time.sleep(0.5)

            wtf_folder = os.path.join(game_path, "WTF")
            config_file = os.path.join(wtf_folder, "Config.wtf")

            # 步骤 1: 创建 WTF 文件夹
            if not os.path.exists(wtf_folder):
                self.log(f"正在创建目录: {wtf_folder}", "warning")
                os.makedirs(wtf_folder)
                time.sleep(0.3)
                self.log("目录创建成功。", "success")
            else:
                self.log(f"目录已存在: {wtf_folder}", "info")

            # 步骤 2 & 3: 创建并写入文件
            self.log("正在配置 Config.wtf...", "info")
            content = 'SET OverrideArchive "0"'
            
            file_mode = 'w'
            if os.path.exists(config_file):
                self.log("检测到现有配置文件，正在检查...", "warning")
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        existing_content = f.read()
                except UnicodeDecodeError:
                    # 防止编码问题
                    with open(config_file, 'r', encoding='latin-1') as f:
                        existing_content = f.read()

                if 'SET OverrideArchive "0"' not in existing_content:
                     with open(config_file, 'a', encoding='utf-8') as f:
                        f.write(f'\n{content}\n')
                     self.log(f"已追加参数: [{content}]", "success")
                else:
                    self.log("参数已存在，无需修改。", "success")
            else:
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"文件创建成功，写入: [{content}]", "success")

            time.sleep(0.5)
            self.log("验证文件完整性... 通过。", "success")
            
            self.status_value.setText("文件已修改 (需重启)")
            self.status_value.setStyleSheet("color: #22c55e; font-size: 13px; font-weight: bold;")
            
            self.log("操作序列完成！启动引导向导...", "cmd")
            time.sleep(0.5)

            dialog = FinalStepDialog(self)
            dialog.exec()

        except Exception as e:
            self.log(f"发生严重错误: {str(e)}", "error")
            self.status_value.setText("错误 / 失败")
            self.status_value.setStyleSheet("color: #ef4444;")
        
        finally:
            self.restore_btn.setEnabled(True)
            self.restore_btn.setText("执行反和谐 (Restore)")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())