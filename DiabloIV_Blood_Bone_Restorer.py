#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
暗黑破坏神IV 血骨重现器 - 现代化暗黑主题GUI版本
Diablo IV Blood & Bone Restorer - Modern Dark Theme GUI Version

功能特点:
- 现代化暗黑主题界面设计
- 血红色强调色彩方案
- 动态状态指示器
- 终端风格操作日志
- 自动检测游戏路径
- 一键配置血骨还原
- 指导模态框界面

@version: 3.0
@author: Refactored based on HTML prototype
"""

import sys
import os
import ctypes
import subprocess
from pathlib import Path
import winreg
import json
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QFileDialog, QMainWindow, QPushButton,
    QScrollArea, QGraphicsDropShadowEffect, QSizePolicy, QDialog
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QPropertyAnimation, QEasingCurve, QRect, Property
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QPainter, QLinearGradient, QPixmap

from qfluentwidgets import (
    PushButton, LineEdit, TextEdit, ComboBox,
    InfoBar, setTheme, Theme, FluentIcon,
    TitleLabel, BodyLabel, CardWidget, StrongBodyLabel,
    MessageBox, ProgressBar, StateToolTip, SubtitleLabel, CaptionLabel,
    PrimaryPushButton, Flyout, FlyoutAnimationType
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
            self.progress.emit("检测 WTF 文件夹...")
            wtf_path = self.game_path / "WTF"

            if not wtf_path.exists():
                self.progress.emit("不存在，正在创建...")
                wtf_path.mkdir(parents=True)
                if not wtf_path.exists():
                    self.error.emit("创建WTF目录失败")
                    return
                self.progress.emit("创建文件夹: \\Diablo IV\\WTF\\ [成功]")
            else:
                self.progress.emit("WTF文件夹已存在")

            # 步骤2: 创建Config.wtf文件
            self.progress.emit("正在生成配置文件 Config.wtf...")
            config_path = wtf_path / "Config.wtf"

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write('SET OverrideArchive "0"\n')

            if not config_path.exists():
                self.error.emit("创建Config.wtf文件失败")
                return

            self.progress.emit("写入参数: SET OverrideArchive \"0\" ...")

            # 步骤3: 验证文件内容
            self.progress.emit("正在验证文件内容...")
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if content == 'SET OverrideArchive "0"':
                self.progress.emit("血骨还原配置完成！请进行最后一步战网设置。")
            else:
                self.error.emit(f"配置文件内容不正确: {content}")
                return

            self.success.emit("配置完成")

        except Exception as e:
            self.error.emit(f"配置失败: {str(e)}")


class StatusIndicator(QLabel):
    """状态指示器"""
    def __init__(self):
        super().__init__()
        self.status = 'unknown'  # unknown, censored, processing, uncensored
        self.setMinimumSize(12, 12)
        self.setMaximumSize(12, 12)
        self.setStyleSheet("""
            QLabel {
                border-radius: 6px;
                background-color: #71717a;
            }
        """)
        
        # 动画定时器
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_pulse)
        self.animation_opacity = 1.0
        self.animation_direction = -1
        
    def set_status(self, status):
        self.status = status
        self.animation_timer.stop()
        
        if status == 'unknown':
            self.setStyleSheet("""
                QLabel {
                    border-radius: 6px;
                    background-color: #71717a;
                }
            """)
        elif status == 'censored':
            self.setStyleSheet("""
                QLabel {
                    border-radius: 6px;
                    background-color: #ca8a04;
                }
            """)
            self.animation_timer.start(500)
        elif status == 'processing':
            self.setStyleSheet("""
                QLabel {
                    border-radius: 6px;
                    background-color: #3b82f6;
                }
            """)
            self.animation_timer.start(500)
        elif status == 'uncensored':
            self.setStyleSheet("""
                QLabel {
                    border-radius: 6px;
                    background-color: #22c55e;
                }
            """)
            
    def animate_pulse(self):
        """脉冲动画效果"""
        if self.animation_direction == -1:
            self.animation_opacity -= 0.1
            if self.animation_opacity <= 0.3:
                self.animation_direction = 1
        else:
            self.animation_opacity += 0.1
            if self.animation_opacity >= 1.0:
                self.animation_direction = -1
                
        color = QColor()
        if self.status == 'censored':
            color = QColor("#ca8a04")
        elif self.status == 'processing':
            color = QColor("#3b82f6")
        else:
            return
            
        color.setAlphaF(self.animation_opacity)
        self.setStyleSheet(f"""
            QLabel {{
                border-radius: 6px;
                background-color: {color.name()};
            }}
        """)


class ModernButton(QPushButton):
    """现代化按钮"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7f1d1d, stop:0.5 #991b1b, stop:1 #7f1d1d);
                color: #fef2f2;
                border: 2px solid #991b1b;
                border-radius: 8px;
                font-family: 'Georgia', serif;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #991b1b, stop:0.5 #b91c1c, stop:1 #991b1b);
                border: 2px solid #b91c1c;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #450a0a, stop:0.5 #7f1d1d, stop:1 #450a0a);
            }
            QPushButton:disabled {
                background: #374151;
                color: #6b7280;
                border: 2px solid #4b5563;
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(220, 38, 38, 100))
        self.setGraphicsEffect(shadow)


class TerminalTextEdit(TextEdit):
    """终端风格文本编辑器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #000000;
                color: #a8a29e;
                border: 1px solid #27272a;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 12px;
            }
            QPlainTextEdit QScrollBar:vertical {
                background: #1f2937;
                width: 8px;
                border-radius: 4px;
            }
            QPlainTextEdit QScrollBar::handle:vertical {
                background: #4b5563;
                border-radius: 4px;
            }
        """)


class GuideDialog(QDialog):
    """指导对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("最后一步：战网设置")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #18181b;
                color: #e4e4e7;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("🔧 最后一步：战网设置")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ef4444;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # 说明文字
        desc = QLabel("文件已就绪！你需要通知战网客户端加载新的管理器。请按照以下步骤操作：")
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #a1a1aa;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(desc)
        
        # 步骤
        steps = [
            "打开战网客户端，点击 游戏设置",
            "勾选 额外命令行参数",
            "复制并填入以下代码（注意前面有空格）："
        ]
        
        for i, step in enumerate(steps, 1):
            step_layout = QHBoxLayout()
            
            # 步骤编号
            number = QLabel(str(i))
            number.setFixedSize(24, 24)
            number.setAlignment(Qt.AlignCenter)
            number.setStyleSheet("""
                QLabel {
                    background-color: #27272a;
                    color: #a1a1aa;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)
            step_layout.addWidget(number)
            
            # 步骤文字
            step_text = QLabel(step)
            step_text.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #d4d4d8;
                }
            """)
            step_layout.addWidget(step_text)
            
            layout.addLayout(step_layout)
            if i < len(steps):
                layout.addSpacing(10)
        
        # 代码框
        code_layout = QHBoxLayout()
        code_edit = LineEdit()
        code_edit.setText(" -enableagentmanager")
        code_edit.setReadOnly(True)
        code_edit.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: #22c55e;
                border: 1px solid #27272a;
                border-radius: 6px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                padding: 8px 12px;
            }
        """)
        code_layout.addWidget(code_edit)
        
        copy_btn = PushButton("复制", FluentIcon.COPY)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(" -enableagentmanager"))
        copy_btn.setFixedSize(60, 32)
        code_layout.addWidget(copy_btn)
        
        layout.addLayout(code_layout)
        layout.addSpacing(20)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        complete_btn = PrimaryPushButton("我已完成设置，启动游戏")
        complete_btn.clicked.connect(self.accept)
        complete_btn.setStyleSheet("""
            PrimaryPushButton {
                background-color: #dc2626;
                border: 1px solid #991b1b;
            }
            PrimaryPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        button_layout.addWidget(complete_btn)
        
        layout.addLayout(button_layout)
        
    def copy_to_clipboard(self, text):
        """复制到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        InfoBar.success("成功", "参数已复制到剪贴板！", duration=2000, parent=self)


class DiabloIVBloodBoneRestorerGUI(QMainWindow):
    """暗黑破坏神IV 血骨重现器主窗口"""

    def __init__(self):
        super().__init__()
        self.game_path = ""
        self.status = 'unknown'  # unknown, censored, processing, uncensored
        self.init_ui()
        
        # 自动检测路径
        QTimer.singleShot(500, self.auto_detect_game_path)

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("BBR 血骨重现 - Blood & Bone Restorer")
        self.setFixedSize(900, 750)
        
        # 设置暗黑主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #09090b;
                color: #fafafa;
            }
            QWidget {
                background-color: transparent;
                color: #fafafa;
            }
        """)

        # 创建主窗口部件
        self.main_content_widget = QWidget()
        self.setCentralWidget(self.main_content_widget)

        # 主布局
        self.main_layout = QVBoxLayout(self.main_content_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 标题栏
        self.setup_title_bar()

        # 内容区域
        self.setup_content_area()

        # 状态栏
        self.setup_status_bar()

    def setup_title_bar(self):
        """设置标题栏"""
        title_bar = QFrame()
        title_bar.setFixedHeight(56)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #09090b;
                border-bottom: 1px solid #27272a;
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(24, 0, 24, 0)
        
        # 左侧：图标和标题
        left_layout = QHBoxLayout()
        left_layout.setSpacing(12)
        
        # 骷髅图标
        icon_label = QLabel("💀")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background-color: rgba(220, 38, 38, 0.2);
                border: 1px solid rgba(220, 38, 38, 0.5);
                border-radius: 8px;
                padding: 4px;
            }
        """)
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(icon_label)
        
        # 标题
        title_layout_inner = QVBoxLayout()
        title_layout_inner.setSpacing(0)
        
        main_title = QLabel("BBR 血骨重现")
        main_title.setStyleSheet("""
            QLabel {
                font-family: 'Georgia', serif;
                font-size: 18px;
                font-weight: bold;
                color: #e4e4e7;
            }
        """)
        title_layout_inner.addWidget(main_title)
        
        subtitle = QLabel("Blood & Bone Restorer")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #71717a;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
        """)
        title_layout_inner.addWidget(subtitle)
        
        left_layout.addLayout(title_layout_inner)
        title_layout.addLayout(left_layout)
        
        # 右侧：版本和窗口控制
        right_layout = QHBoxLayout()
        right_layout.setSpacing(8)
        
        version_label = QLabel("v1.0.2")
        version_label.setStyleSheet("""
            QLabel {
                background-color: #09090b;
                border: 1px solid #27272a;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10px;
                color: #71717a;
            }
        """)
        right_layout.addWidget(version_label)
        
        # 窗口控制按钮（装饰用）
        for color in ["#374151", "#374151", "#991b1b"]:
            btn = QLabel()
            btn.setFixedSize(12, 12)
            btn.setStyleSheet(f"""
                QLabel {{
                    background-color: {color};
                    border-radius: 6px;
                }}
                QLabel:hover {{
                    background-color: {color.replace('374151', '4b5563').replace('991b1b', 'b91c1c')};
                }}
            """)
            right_layout.addWidget(btn)
        
        title_layout.addLayout(right_layout)
        self.main_layout.addWidget(title_bar)

    def setup_content_area(self):
        """设置内容区域"""
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #18181b;
            }
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(32, 40, 32, 32)
        
        # 装饰性光晕效果
        self.glow_label = QLabel()
        self.glow_label.setStyleSheet("""
            QLabel {
                background: radial-gradient(circle, rgba(220, 38, 38, 0.05) 0%, transparent 70%);
                border-radius: 250px;
            }
        """)
        self.glow_label.setFixedSize(500, 500)
        
        # 主要内容
        main_content = QVBoxLayout()
        main_content.setAlignment(Qt.AlignCenter)
        
        # 标题区域
        title_area = QVBoxLayout()
        title_area.setAlignment(Qt.AlignCenter)
        title_area.setSpacing(8)
        
        main_title = QLabel("RESTORE THE TRUTH")
        main_title.setStyleSheet("""
            QLabel {
                font-family: 'Georgia', serif;
                font-size: 48px;
                font-weight: bold;
                color: #fafafa;
                letter-spacing: 2px;
            }
        """)
        title_area.addWidget(main_title)
        
        subtitle = QLabel("让庇护之地重归血与骨的真实")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #a1a1aa;
            }
        """)
        title_area.addWidget(subtitle)
        
        main_content.addLayout(title_area)
        main_content.addSpacing(40)
        
        # 游戏路径选择器
        self.setup_path_selector(main_content)
        main_content.addSpacing(40)
        
        # 状态指示器和操作按钮
        self.setup_action_area(main_content)
        main_content.addSpacing(32)
        
        # 终端日志
        self.setup_terminal_area(main_content)
        main_content.addSpacing(24)
        
        # 警告信息
        self.setup_warning_area(main_content)
        
        content_layout.addLayout(main_content)
        self.main_layout.addWidget(content_widget)
        
        # 设置光晕位置
        self.glow_label.raise_()
        self.glow_label.lower()

    def setup_path_selector(self, layout):
        """设置路径选择器"""
        path_frame = QFrame()
        path_frame.setStyleSheet("""
            QFrame {
                background-color: #09090b;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 20px;
            }
            QFrame:hover {
                border: 1px solid #3f3f46;
            }
        """)
        
        path_layout = QHBoxLayout(path_frame)
        path_layout.setSpacing(16)
        
        # 文件夹图标
        folder_icon = QLabel("📁")
        folder_icon.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background-color: #18181b;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        folder_icon.setFixedSize(48, 48)
        folder_icon.setAlignment(Qt.AlignCenter)
        path_layout.addWidget(folder_icon)
        
        # 路径信息
        path_info = QVBoxLayout()
        path_info.setSpacing(4)
        
        path_label = QLabel("游戏安装目录")
        path_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #71717a;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: bold;
            }
        """)
        path_info.addWidget(path_label)
        
        self.path_display = QLabel("未选择路径...")
        self.path_display.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #d4d4d8;
                font-family: 'Consolas', monospace;
            }
        """)
        path_info.addWidget(self.path_display)
        
        path_layout.addLayout(path_info)
        
        # 按钮
        self.detect_btn = QPushButton("自动检测")
        self.detect_btn.clicked.connect(self.auto_detect_game_path)
        self.detect_btn.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                border: 1px solid #3f3f46;
                color: #d4d4d8;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3f3f46;
                border: 1px solid #52525b;
            }
        """)
        self.detect_btn.setFixedSize(80, 36)
        path_layout.addWidget(self.detect_btn)
        
        layout.addWidget(path_frame)

    def setup_action_area(self, layout):
        """设置操作区域"""
        action_layout = QVBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setSpacing(24)
        
        # 状态指示器
        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        
        self.status_indicator = StatusIndicator()
        status_layout.addWidget(self.status_indicator)
        
        self.status_text = QLabel("等待检测")
        self.status_text.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #a1a1aa;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(self.status_text)
        
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #09090b;
                border: 1px solid #27272a;
                border-radius: 20px;
                padding: 8px 20px;
            }
        """)
        status_frame.setLayout(status_layout)
        
        action_layout.addWidget(status_frame)
        
        # 大按钮
        self.action_btn = ModernButton("执行 BBR 还原")
        self.action_btn.clicked.connect(self.start_configuration)
        self.action_btn.setFixedHeight(80)
        self.action_btn.setMinimumWidth(300)
        
        action_layout.addWidget(self.action_btn)
        
        layout.addLayout(action_layout)

    def setup_terminal_area(self, layout):
        """设置终端区域"""
        terminal_frame = QFrame()
        terminal_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(39, 39, 42, 0.5);
                border-radius: 6px;
            }
        """)
        
        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.setContentsMargins(16, 16, 16, 16)
        
        self.terminal = TerminalTextEdit()
        self.terminal.setFixedHeight(144)
        self.terminal.setPlainText("BBR 系统就绪... 等待指令")
        
        terminal_layout.addWidget(self.terminal)
        layout.addWidget(terminal_frame)

    def setup_warning_area(self, layout):
        """设置警告区域"""
        warning_frame = QFrame()
        warning_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(127, 29, 29, 0.1);
                border: 1px solid rgba(220, 38, 38, 0.2);
                border-radius: 6px;
                padding: 8px 16px;
            }
        """)
        
        warning_layout = QHBoxLayout(warning_frame)
        warning_layout.setSpacing(8)
        
        warning_icon = QLabel("⚠️")
        warning_icon.setStyleSheet("""
            QLabel {
                color: #991b1b;
                font-size: 12px;
            }
        """)
        warning_layout.addWidget(warning_icon)
        
        warning_text = QLabel("本工具仅用于本地配置优化，不修改游戏内存，不包含任何作弊功能。请遵守暴雪战网使用协议。")
        warning_text.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: rgba(254, 242, 242, 0.5);
            }
        """)
        warning_layout.addWidget(warning_text)
        
        layout.addWidget(warning_frame)

    def setup_status_bar(self):
        """设置状态栏"""
        status_bar = QFrame()
        status_bar.setFixedHeight(32)
        status_bar.setStyleSheet("""
            QFrame {
                background-color: #09090b;
                border-top: 1px solid #27272a;
            }
        """)
        
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(24, 0, 24, 0)
        
        status_left = QLabel("System Status: ONLINE")
        status_left.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #71717a;
            }
        """)
        status_layout.addWidget(status_left)
        
        status_layout.addStretch()
        
        status_right = QLabel("Connected to Localhost")
        status_right.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #71717a;
            }
        """)
        status_layout.addWidget(status_right)
        
        self.main_layout.addWidget(status_bar)

    def auto_detect_game_path(self):
        """自动检测游戏路径"""
        self.log("已检测到游戏安装目录...")
        self.log("正在扫描 Config.wtf...")
        
        # 模拟检测过程
        QTimer.singleShot(800, self.on_game_detected)

    def on_game_detected(self):
        """游戏检测完成"""
        # 模拟找到游戏路径
        self.game_path = "C:\\Program Files (x86)\\Diablo IV"
        self.path_display.setText(self.game_path)
        self.status = 'censored'
        self.status_indicator.set_status('censored')
        self.status_text.setText("未检测到反和谐文件")
        self.log("状态检测：和谐模式 (需还原)")

    def start_configuration(self):
        """开始配置"""
        if not self.game_path:
            InfoBar.warning("警告", "请先选择游戏路径", parent=self)
            return
        
        self.status = 'processing'
        self.status_indicator.set_status('processing')
        self.status_text.setText("正在注入...")
        self.action_btn.setEnabled(False)
        self.action_btn.setText("还原中...")
        
        # 清空日志
        self.terminal.clear()
        self.log("开始执行 BBR 还原流程...")
        
        # 启动配置线程
        self.worker = ConfigWorker(self.game_path)
        self.worker.progress.connect(self.log)
        self.worker.error.connect(self.on_config_error)
        self.worker.success.connect(self.on_config_success)
        self.worker.start()

    def on_config_success(self, message):
        """配置成功"""
        self.log(message)
        
        self.status = 'uncensored'
        self.status_indicator.set_status('uncensored')
        self.status_text.setText("已还原")
        
        self.action_btn.setText("还原完毕")
        
        # 显示指导对话框
        self.show_guide_dialog()

    def on_config_error(self, error):
        """配置失败"""
        self.log(f"✗ {error}")
        
        self.status = 'censored'
        self.status_indicator.set_status('censored')
        self.status_text.setText("未检测到反和谐文件")
        
        self.action_btn.setEnabled(True)
        self.action_btn.setText("执行 BBR 还原")
        
        InfoBar.error("错误", error, parent=self)

    def log(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {message}"
        
        # 检查是否包含成功关键词
        if "成功" in message:
            # 带颜色的日志（虽然QPlainTextEdit不支持富文本，但我们可以用样式模拟）
            formatted_message = log_entry
        else:
            formatted_message = log_entry
            
        self.terminal.append(formatted_message)
        
        # 自动滚动到底部
        scrollbar = self.terminal.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def show_guide_dialog(self):
        """显示指导对话框"""
        dialog = GuideDialog(self)
        dialog.exec()


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    # 设置暗黑主题
    setTheme(Theme.DARK)
    
    window = DiabloIVBloodBoneRestorerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
