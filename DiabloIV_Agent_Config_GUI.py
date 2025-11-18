#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
暗黑破坏神IV Agent模式配置器 - PySide6 Fluent-Widgets GUI版本
Diablo IV Agent Mode Configurator - PySide6 Fluent-Widgets GUI Version

功能特点:
- 现代化的Fluent Design用户界面
- 自动检测暗黑破坏神IV安装路径
- 一键配置Agent模式
- 多语言支持(中文/英文)
- 管理员权限检查
- 操作日志显示

@version: 2.0
@author: Gemini Pro
"""

import sys
import os
import ctypes
import subprocess
from pathlib import Path
import winreg
import json

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QFileDialog, QMainWindow
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon

from qfluentwidgets import (
    PushButton, LineEdit, TextEdit, ComboBox,
    InfoBar, setTheme, Theme, FluentIcon,
    TitleLabel, BodyLabel, CardWidget, StrongBodyLabel,
    MessageBox
)


class ConfigWorker(QThread):
    """后台配置工作线程"""
    progress = Signal(str)  # 进度信号
    error = Signal(str)     # 错误信号
    success = Signal(str)   # 成功信号

    def __init__(self, game_path):
        super().__init__()
        self.game_path = Path(game_path)

    def run(self):
        """执行配置操作"""
        try:
            # 步骤1: 创建WTF目录
            self.progress.emit("正在创建WTF目录...")
            wtf_path = self.game_path / "WTF"

            if not wtf_path.exists():
                wtf_path.mkdir(parents=True)
                if not wtf_path.exists():
                    self.error.emit("创建WTF目录失败")
                    return
                self.progress.emit("✓ WTF目录创建成功")
            else:
                self.progress.emit("✓ WTF目录已存在")

            # 步骤2: 创建Config.wtf文件
            self.progress.emit("正在创建Config.wtf配置文件...")
            config_path = wtf_path / "Config.wtf"

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write('SET OverrideArchive "0"\n')

            if not config_path.exists():
                self.error.emit("创建Config.wtf文件失败")
                return

            self.progress.emit("✓ Config.wtf文件创建成功")

            # 步骤3: 验证文件内容
            self.progress.emit("正在验证文件内容...")
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if content == 'SET OverrideArchive "0"':
                self.progress.emit("✓ 配置文件内容验证成功")
            else:
                self.error.emit(f"配置文件内容不正确: {content}")
                return

            self.success.emit("配置完成")

        except Exception as e:
            self.error.emit(f"配置失败: {str(e)}")


class DiabloIVAgentConfigGUI(QMainWindow):
    """暗黑破坏神IV Agent模式配置器主窗口"""

    def __init__(self):
        super().__init__()
        self.current_language = "zh"  # 默认中文
        self.game_path = ""

        # 管理员权限检查
        self.is_admin = self.check_admin_privilege()

        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(self.tr("暗黑破坏神IV Agent模式配置器"))
        self.setFixedSize(750, 680)

        # 创建主窗口部件
        self.main_content_widget = QWidget()
        self.setCentralWidget(self.main_content_widget)

        # 主布局
        self.main_layout = QVBoxLayout(self.main_content_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题区域
        self.setup_title_area(self.main_layout)

        # 语言选择
        self.setup_language_selector(self.main_layout)

        # 管理员权限警告
        if not self.is_admin:
            self.setup_admin_warning(self.main_layout)

        # 路径检测区域
        self.setup_path_area(self.main_layout)

        # 操作日志
        self.setup_log_area(self.main_layout)

        # 按钮区域
        self.setup_button_area(self.main_layout)

        # 自动检测路径
        self.auto_detect_game_path()

    def tr(self, text):
        """简单的国际化函数"""
        translations = {
            "zh": {
                "暗黑破坏神IV Agent模式配置器": "暗黑破坏神IV Agent模式配置器",
                "语言:": "语言:",
                "中文": "中文",
                "English": "English",
                "警告: 需要管理员权限": "警告: 需要管理员权限",
                "检测到非管理员权限运行，某些操作可能失败。\n建议右键点击程序，选择\"以管理员身份运行\"": "检测到非管理员权限运行，某些操作可能失败。\n建议右键点击程序，选择\"以管理员身份运行\"",
                "暗黑破坏神IV安装路径:": "暗黑破坏神IV安装路径:",
                "自动检测": "自动检测",
                "浏览": "浏览",
                "自动检测游戏路径...": "自动检测游戏路径...",
                "找到游戏目录: ": "找到游戏目录: ",
                "未找到自动检测到游戏安装目录": "未找到自动检测到游戏安装目录",
                "未找到暗黑破坏神IV安装目录": "未找到暗黑破坏神IV安装目录",
                "操作日志:": "操作日志:",
                "开始配置": "开始配置",
                "打开战网客户端": "打开战网客户端",
                "查看配置说明": "查看配置说明",
                "正在创建WTF目录...": "正在创建WTF目录...",
                "✓ WTF目录创建成功": "✓ WTF目录创建成功",
                "✓ WTF目录已存在": "✓ WTF目录已存在",
                "正在创建Config.wtf配置文件...": "正在创建Config.wtf配置文件...",
                "✓ Config.wtf文件创建成功": "✓ Config.wtf文件创建成功",
                "正在验证文件内容...": "正在验证文件内容...",
                "✓ 配置文件内容验证成功": "✓ 配置文件内容验证成功",
                "配置完成!": "配置完成!",
                "准备就绪": "准备就绪",
                "配置中...": "配置中...",
                "配置失败": "配置失败",
                "手动配置说明": "手动配置说明",
                "1. 打开战网客户端\n2. 进入: 游戏设置 > 暗黑破坏神IV\n3. 勾选: \"额外命令行参数\"\n4. 添加参数: -enableagentmanager\n5. 点击\"完成\"按钮":
                    "1. 打开战网客户端\n2. 进入: 游戏设置 > 暗黑破坏神IV\n3. 勾选: \"额外命令行参数\"\n4. 添加参数: -enableagentmanager\n5. 点击\"完成\"按钮",
                "暗黑破坏神IV Agent模式配置器\n\n本工具将帮您自动配置暗黑破坏神IV的Agent模式\n让您可以安全地使用游戏助手功能":
                    "暗黑破坏神IV Agent模式配置器\n\n本工具将帮您自动配置暗黑破坏神IV的Agent模式\n让您可以安全地使用游戏助手功能",
            },
            "en": {
                "暗黑破坏神IV Agent模式配置器": "Diablo IV Agent Mode Configurator",
                "语言:": "Language:",
                "中文": "Chinese",
                "English": "English",
                "警告: 需要管理员权限": "Warning: Administrator Privileges Required",
                "检测到非管理员权限运行，某些操作可能失败。\n建议右键点击程序，选择\"以管理员身份运行\"": "Non-administrator privileges detected. Some operations may fail.\nPlease right-click and select 'Run as administrator'",
                "暗黑破坏神IV安装路径:": "Diablo IV Installation Path:",
                "自动检测": "Auto Detect",
                "浏览": "Browse",
                "自动检测游戏路径...": "Auto-detecting game path...",
                "找到游戏目录: ": "Found game directory: ",
                "未找到暗黑破坏神IV安装目录": "Diablo IV installation directory not found",
                "操作日志:": "Operation Log:",
                "开始配置": "Start Configuration",
                "打开战网客户端": "Open Battle.net Client",
                "查看配置说明": "View Configuration Instructions",
                "正在创建WTF目录...": "Creating WTF directory...",
                "✓ WTF目录创建成功": "✓ WTF directory created successfully",
                "✓ WTF目录已存在": "✓ WTF directory already exists",
                "正在创建Config.wtf配置文件...": "Creating Config.wtf configuration file...",
                "✓ Config.wtf文件创建成功": "✓ Config.wtf file created successfully",
                "正在验证文件内容...": "Verifying file content...",
                "✓ 配置文件内容验证成功": "✓ Configuration file content verified successfully",
                "配置完成!": "Configuration complete!",
                "准备就绪": "Ready",
                "配置中...": "Configuring...",
                "配置失败": "Configuration failed",
                "手动配置说明": "Manual Configuration Instructions",
                "1. 打开战网客户端\n2. 进入: 游戏设置 > 暗黑破坏神IV\n3. 勾选: \"额外命令行参数\"\n4. 添加参数: -enableagentmanager\n5. 点击\"完成\"按钮":
                    "1. Open Battle.net client\n2. Navigate to: Game Settings > Diablo IV\n3. Check: \"Additional command line arguments\"\n4. Add parameter: -enableagentmanager\n5. Click \"Done\" button",
                "暗黑破坏神IV Agent模式配置器\n\n本工具将帮您自动配置暗黑破坏神IV的Agent模式\n让您可以安全地使用游戏助手功能":
                    "Diablo IV Agent Mode Configurator\n\nThis tool will automatically configure Agent mode for Diablo IV\nSo you can safely use game assistant features",
            }
        }
        return translations.get(self.current_language, {}).get(text, text)

    def check_admin_privilege(self):
        """检查是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def setup_title_area(self, layout):
        """设置标题区域"""
        title_label = TitleLabel(self.tr("暗黑破坏神IV Agent模式配置器"), self)
        layout.addWidget(title_label, 0, Qt.AlignCenter)

        desc_label = BodyLabel(self.tr(
            "暗黑破坏神IV Agent模式配置器\n\n本工具将帮您自动配置暗黑破坏神IV的Agent模式\n让您可以安全地使用游戏助手功能"
        ), self)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label, 0, Qt.AlignCenter)
        layout.addSpacing(10)

    def setup_language_selector(self, layout):
        """设置语言选择器"""
        lang_layout = QHBoxLayout()
        lang_label = BodyLabel(self.tr("语言:"), self)
        self.lang_combo = ComboBox(self)
        self.lang_combo.addItem(self.tr("中文"), "zh")
        self.lang_combo.addItem(self.tr("English"), "en")
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

    def setup_admin_warning(self, layout):
        """设置管理员权限警告"""
        InfoBar.warning(
            self.tr("警告: 需要管理员权限"),
            self.tr("检测到非管理员权限运行，某些操作可能失败。\n建议右键点击程序，选择\"以管理员身份运行\""),
            duration=-1,
            parent=self
        )

    def setup_path_area(self, layout):
        """设置路径选择区域"""
        path_card = CardWidget(self)
        path_layout = QVBoxLayout(path_card)
        path_layout.addWidget(StrongBodyLabel(self.tr("暗黑破坏神IV安装路径:"), self))

        path_input_layout = QHBoxLayout()
        self.path_edit = LineEdit(self)
        self.path_edit.setPlaceholderText("C:/Program Files/Battle.net/Diablo IV")
        self.path_edit.setReadOnly(True)
        path_input_layout.addWidget(self.path_edit)

        auto_detect_btn = PushButton(self.tr("自动检测"), self, FluentIcon.SEARCH)
        auto_detect_btn.clicked.connect(self.auto_detect_game_path)
        path_input_layout.addWidget(auto_detect_btn)

        browse_btn = PushButton(self.tr("浏览"), self, FluentIcon.FOLDER)
        browse_btn.clicked.connect(self.browse_game_directory)
        path_input_layout.addWidget(browse_btn)

        path_layout.addLayout(path_input_layout)
        layout.addWidget(path_card)

    def setup_log_area(self, layout):
        """设置日志显示区域"""
        log_card = CardWidget(self)
        log_layout = QVBoxLayout(log_card)
        log_layout.addWidget(StrongBodyLabel(self.tr("操作日志:"), self))

        self.log_text = TextEdit(self)
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(150)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_card)

    def setup_button_area(self, layout):
        """设置按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.config_btn = PushButton(self.tr("开始配置"), self, FluentIcon.PLAY)
        self.config_btn.clicked.connect(self.start_configuration)
        button_layout.addWidget(self.config_btn)

        battle_net_btn = PushButton(self.tr("打开战网客户端"), self, FluentIcon.GAME)
        battle_net_btn.clicked.connect(self.open_battle_net)
        button_layout.addWidget(battle_net_btn)

        instructions_btn = PushButton(self.tr("查看配置说明"), self, FluentIcon.HELP)
        instructions_btn.clicked.connect(self.show_instructions)
        button_layout.addWidget(instructions_btn)

        layout.addLayout(button_layout)

    def change_language(self, index):
        """切换语言"""
        lang_code = self.lang_combo.currentData()
        self.current_language = lang_code
        
        m = MessageBox(
            "Info", 
            "语言切换将在下次启动时生效\nLanguage change will take effect after restart", 
            self
        )
        m.exec()


    def auto_detect_game_path(self):
        """自动检测游戏路径 - 增强版"""
        self.log_text.clear()
        self.log("正在自动检测游戏路径...")

        found_paths = []

        # 方法1: 查询Windows注册表（最准确）
        self.log("=== 方法1: 查询注册表 ===")
        reg_paths = self.find_game_in_registry("DiabloIV.exe")
        if reg_paths:
            found_paths.extend(reg_paths)
            for path in reg_paths:
                self.log(f"✓ 注册表找到: {path}")

        # 方法2: 针对战网平台
        self.log("=== 方法2: 查找战网配置 ===")
        bn_path = self.find_battle_net_game()
        if bn_path:
            found_paths.append(bn_path)
            self.log(f"✓ 战网配置找到: {path}")

        # 方法3: 常见安装路径扫描
        self.log("=== 方法3: 常见路径扫描 ===")
        common_paths = self.scan_common_paths()
        if common_paths:
            found_paths.extend(common_paths)
            for path in common_paths:
                self.log(f"✓ 常见路径找到: {path}")

        # 处理结果
        if found_paths:
            # 去重并选择最佳路径
            unique_paths = list(set(found_paths))
            best_path = self.select_best_path(unique_paths)

            self.game_path = str(best_path)
            self.path_edit.setText(self.game_path)
            self.log(f"\n✅ 最终选择: {best_path}")

            if len(unique_paths) > 1:
                self.log(f"ℹ️ 找到 {len(unique_paths)} 个可能的位置，已选择最佳路径")
        else:
            self.log("❌ 未找到游戏，建议:")
            self.log("  1. 确保游戏已安装")
            self.log("  2. 以管理员身份运行脚本")
            self.log("  3. 手动指定游戏目录")

            InfoBar.warning("警告", "未找到暗黑破坏神IV安装目录，请手动指定", parent=self)

    def find_game_in_registry(self, game_exe="DiabloIV.exe"):
        """通过注册表查找游戏"""
        found_paths = []

        # 常见游戏注册表路径
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\Blizzard Entertainment",
            r"SOFTWARE\WOW6432Node\Blizzard Entertainment"
        ]

        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for reg_path in registry_paths:
                try:
                    key = winreg.OpenKey(hive, reg_path)
                    subkey_count = winreg.QueryInfoKey(key)[0]

                    for i in range(subkey_count):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)

                            # 尝试获取DisplayName和InstallLocation
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Diablo" in display_name and "IV" in display_name:
                                    install_loc = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    exe_path = os.path.join(install_loc, game_exe)
                                    if os.path.exists(exe_path):
                                        # 提取游戏目录路径（不含exe文件）
                                        game_dir = install_loc
                                        found_paths.append(game_dir)
                            except:
                                pass

                            subkey.Close()
                        except:
                            continue

                    key.Close()
                except:
                    continue

        return found_paths

    def find_battle_net_game(self):
        """查找战网安装的暗黑破坏神IV"""
        # 战网配置文件路径
        config_paths = [
            os.path.expandvars("%PROGRAMDATA%/Battle.net/Client/Battle.net.config"),
            os.path.expandvars("%APPDATA%/Battle.net/Battle.net.config"),
            os.path.expandvars("%USERPROFILE%/AppData/Local/Battle.net/Battle.net.config")
        ]

        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    # 尝试从战网配置中获取游戏安装信息
                    # 战网通常将游戏安装在Program Files下的Battle.net目录
                    battle_net_base = Path(os.path.expandvars("%PROGRAMFILES%")) / "Battle.net"
                    diablo_path = battle_net_base / "Diablo IV"

                    if diablo_path.exists():
                        return str(diablo_path)
                except Exception:
                    pass

        return None

    def scan_common_paths(self):
        """扫描常见的游戏安装路径"""
        common_paths = []
        search_locations = [
            os.path.expandvars("%ProgramFiles%"),
            os.path.expandvars("%ProgramFiles(x86)%"),
            "D:/Games",
            "E:/Games",
            "F:/Games"
        ]

        for base_path in search_locations:
            if base_path and os.path.exists(base_path):
                diablo_path = Path(base_path) / "Battle.net" / "Diablo IV"
                if diablo_path.exists():
                    common_paths.append(str(diablo_path))

                # 也检查直接在Games目录下
                diablo_direct = Path(base_path) / "Diablo IV"
                if diablo_direct.exists():
                    common_paths.append(str(diablo_direct))

        return common_paths

    def select_best_path(self, paths):
        """从多个路径中选择最佳路径"""
        if not paths:
            return None

        if len(paths) == 1:
            return paths[0]

        # 优先级排序
        priority_patterns = [
            os.path.expandvars("%ProgramFiles%") + "/Battle.net/Diablo IV",
            os.path.expandvars("%ProgramFiles(x86)%") + "/Battle.net/Diablo IV",
            "C:/Program Files/Battle.net/Diablo IV",
            "C:/Program Files (x86)/Battle.net/Diablo IV"
        ]

        # 检查是否有匹配优先级模式的路径
        for pattern in priority_patterns:
            for path in paths:
                if path.lower() == pattern.lower():
                    return path

        # 如果没有匹配的，返回第一个路径
        return paths[0]

    def browse_game_directory(self):
        """手动浏览选择游戏目录"""
        # 设置默认目录为Program Files下的Battle.net
        default_dir = os.path.expandvars("%ProgramFiles%/Battle.net")
        if not os.path.exists(default_dir):
            default_dir = os.path.expandvars("%ProgramFiles(x86)%/Battle.net")
        if not os.path.exists(default_dir):
            default_dir = "C:/"

        # 打开目录选择对话框
        selected_dir, _ = QFileDialog.getExistingDirectory(
            self, 
            self.tr("选择暗黑破坏神IV安装目录"), 
            default_dir
        )

        if selected_dir:
            # 验证选择的目录是否看起来像Diablo IV目录
            validation_result = self.validate_game_directory(selected_dir)

            if validation_result["valid"]:
                self.game_path = selected_dir
                self.path_edit.setText(selected_dir)
                self.log(f"✓ 已手动选择游戏目录: {selected_dir}")
                self.log(validation_result["message"])
            else:
                # 警告用户可能选择了错误的目录，但仍允许使用
                m = MessageBox(
                    self.tr("确认目录选择"), 
                    f"{validation_result['message']}\n\n{self.tr('是否仍要使用此目录？')}", 
                    self
                )
                if m.exec():
                    self.game_path = selected_dir
                    self.path_edit.setText(selected_dir)
                    self.log(f"⚠️ 用户确认使用目录: {selected_dir}")

    def validate_game_directory(self, path):
        """验证是否为有效的Diablo IV游戏目录"""
        if not os.path.exists(path):
            return {"valid": False, "message": "目录不存在"}

        # 检查目录名称是否包含"Diablo"
        dir_name = os.path.basename(path)
        if "Diablo" not in dir_name:
            return {
                "valid": False,
                "message": f"⚠️ 目录名称 '{dir_name}' 不包含'Diablo'，可能不是正确的游戏目录"
            }

        # 检查是否有常见的Diablo IV文件
        expected_files = ["DiabloIV.exe", "DiabloIV.exe.config"]
        found_files = []

        for file_name in expected_files:
            file_path = os.path.join(path, file_name)
            if os.path.exists(file_path):
                found_files.append(file_name)

        # 检查Data目录
        data_dir = os.path.join(path, "Data")
        has_data = os.path.exists(data_dir)

        if found_files and has_data:
            return {
                "valid": True,
                "message": f"✅ 验证通过！找到文件: {', '.join(found_files)} 和Data目录"
            }
        elif found_files:
            return {
                "valid": True,
                "message": f"✅ 验证通过！找到文件: {', '.join(found_files)}"
            }
        elif has_data:
            return {
                "valid": True,
                "message": "✅ 验证通过！找到Data目录"
            }
        else:
            return {
                "valid": False,
                "message": "⚠️ 未找到常见的Diablo IV文件，请确认选择了正确的目录"
            }

    def start_configuration(self):
        """开始配置"""
        if not self.game_path:
            InfoBar.warning("警告", "请先检测或输入游戏安装路径", parent=self)
            return

        # 确认路径存在
        game_path = Path(self.game_path)
        if not game_path.exists():
            InfoBar.error("错误", "指定的游戏路径不存在", parent=self)
            return

        # 禁用配置按钮
        self.config_btn.setEnabled(False)
        self.config_btn.setText(self.tr("配置中..."))

        # 清空日志
        self.log_text.clear()

        # 启动后台线程
        self.worker = ConfigWorker(self.game_path)
        self.worker.progress.connect(self.log)
        self.worker.error.connect(self.on_config_error)
        self.worker.success.connect(self.on_config_success)
        self.worker.start()

    def open_battle_net(self):
        """打开战网客户端"""
        # 可能的战网客户端路径
        battle_net_paths = [
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Battle.net" / "Battle.net.exe",
            Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Battle.net" / "Battle.net.exe",
        ]

        found = False
        for path in battle_net_paths:
            if path.exists():
                try:
                    subprocess.Popen([str(path)])
                    self.log(f"正在打开战网客户端: {path}")
                    found = True
                    break
                except Exception as e:
                    self.log(f"打开战网客户端失败: {e}")

        if not found:
            InfoBar.warning("警告", "未找到战网客户端，请手动打开", parent=self)

    def show_instructions(self):
        """显示手动配置说明"""
        instructions = self.tr(
            "1. 打开战网客户端\n"
            "2. 进入: 游戏设置 > 暗黑破坏神IV\n"
            "3. 勾选: \"额外命令行参数\"\n"
            "4. 添加参数: -enableagentmanager\n"
            "5. 点击\"完成\"按钮"
        )

        m = MessageBox(
            self.tr("手动配置说明"), 
            instructions,
            self
        )
        m.exec()


    def on_config_success(self, message):
        """配置成功回调"""
        self.log(f"✓ {message}")
        self.log("=" * 50)
        self.log("配置完成！请继续完成手动步骤:")
        self.log("1. 打开战网客户端")
        self.log("2. 设置命令行参数: -enableagentmanager")

        self.config_btn.setEnabled(True)
        self.config_btn.setText(self.tr("开始配置"))

        InfoBar.success("成功", "配置完成！请按说明完成手动步骤", parent=self)

    def on_config_error(self, error):
        """配置错误回调"""
        self.log(f"✗ 配置失败: {error}")

        self.config_btn.setEnabled(True)
        self.config_btn.setText(self.tr("开始配置"))

        InfoBar.error("错误", f"配置失败:\n{error}", parent=self)

    def log(self, message):
        """添加日志消息"""
        self.log_text.append(message)
        # 自动滚动到底部
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) # Deprecated
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps) # Deprecated

    app = QApplication(sys.argv)

    # 设置主题
    setTheme(Theme.DARK)

    window = DiabloIVAgentConfigGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
