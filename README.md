# DiabloIV_BBR(DiabloIV Blood & Bone Restorer)
# 暗黑四BBR(暗黑四血骨还原器/暗黑四反和谐工具)

![License](https://img.shields.io/github/license/YoungHong1992/DiabloIV_Blood_Bone_Restorer)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-win)
![Status](https://img.shields.io/badge/Status-Active-success)


> **⚠️ IMPORTANT / 重要提示**
>
> **English:** This project is free and open-source software licensed under **GNU GPL v3.0**. **If you paid for this software, you have been scammed.**
>
> **中文:** 本项目是基于 **GNU GPL v3.0** 协议的**免费开源软件**。**如果你是花钱买的，说明你被骗了。**

---

## 📖 Introduction (项目介绍)

### English
**DiabloIV Blood & Bone Restorer** is a safe, open-source desktop utility designed to manage the local configuration of Diablo IV. Its primary purpose is to restore the original visual fidelity (uncensored assets) for region-locked clients by managing the `Config.wtf` file.

### 中文
**DiabloIV Blood & Bone Restorer** 是一款安全、开源的桌面工具，专为暗黑破坏神4设计。它的主要功能是通过管理本地配置文件 (`Config.wtf`)，帮助锁区客户端（如国服/亚服）恢复原本的视觉保真度（即“反和谐”效果）。

---

## ✨ Key Features (核心功能)

### English
*   **Safety First:** Operates strictly via standard **File I/O**. It does **NOT** read/write game memory, inject code, or modify game executables (`.exe`). It is fully compliant with configuration editing standards.
*   **Auto Detection:** Automatically locates your game installation using Windows Registry scanning and smart disk search.
*   **One-Click Restore:** Safely appends the necessary parameter (`OverrideArchive`) to your local configuration file.
*   **Transparent:** The source code is fully open for community audit.

### 中文
*   **绝对安全**：仅进行标准的**文件读写**操作。**绝不**读取/修改游戏内存、不注入代码、也不修改游戏执行文件 (`.exe`)。完全符合修改配置文件的合规标准。
*   **自动检测**：利用 Windows 注册表和智能磁盘扫描，自动定位您的游戏安装路径。
*   **一键恢复**：安全地将必要的参数 (`OverrideArchive`) 添加到您的本地配置文件中。
*   **开源透明**：源代码完全公开，接受社区审查。

---

## 🚀 How to Use (使用方法)

### English
1.  **Download:** Get the latest executable from the [Releases Page](https://github.com/YoungHong1992/DiabloIV_Blood_Bone_Restorer/releases).
    *   *Note: If Windows SmartScreen warns you, click "More Info" -> "Run Anyway". (We are currently applying for Microsoft certification).*
2.  **Run:** Open the application. It will automatically detect your game path.
3.  **Restore:** Click the **"Execute Restore"** button. The tool will modify the config file.
4.  **Final Step (Crucial):**
    *   Open **Battle.net Launcher**.
    *   Go to **Game Settings** -> **Diablo IV**.
    *   Check **"Additional command line arguments"**.
    *   Enter: `-enableagentmanager`
    *   Launch the game.

### 中文
1.  **下载**：前往 [Releases 页面](https://github.com/YoungHong1992/DiabloIV_Blood_Bone_Restorer/releases) 下载最新的程序。
    *   *注意：如果 Windows SmartScreen 弹出拦截警告，请点击“更多信息” -> “仍要运行”。（我们正在申请微软安全认证）。*
2.  **运行**：打开程序，它会自动检测您的游戏路径。
3.  **执行**：点击 **“执行反和谐 (Restore)”** 按钮，工具将修改配置文件。
4.  **最后一步（关键）**：
    *   打开 **战网客户端 (Battle.net)**。
    *   点击 **“游戏设置”** -> **“暗黑破坏神 IV”**。
    *   勾选 **“额外命令行参数”**。
    *   输入： `-enableagentmanager`
    *   启动游戏即可生效。

---

## 🛠️ Build from Source (源码构建)

**English:**
If you are a developer, you can build the executable yourself to ensure safety.

**中文:**
如果您是开发者，您可以自行编译可执行文件以确信其安全性。

**Requirements:** Python 3.12+

```bash
# 1. Clone the repository / 克隆仓库
git clone https://github.com/YoungHong1992/DiabloIV_Blood_Bone_Restorer.git

# 2. Install dependencies / 安装依赖 (PyInstaller is only needed for building exe)
pip install pyinstaller

# 3. Build EXE / 编译 EXE
python -m PyInstaller --noconfirm --onefile --windowed --name "DiabloIV_BBR" DiabloIV_Blood_Bone_Restorer.py