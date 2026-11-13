<p align="center"><img src="assets/covers/05-WexOpen.jpg" alt="WexOpen 项目封面" width="100%"></p>

# WexOpen

<p align="center">
  <img src="assets/icon.png" alt="WexOpen" width="96">
</p>

<p align="center">
  <strong>简约精致的 PC 微信多开助手</strong><br>
  自动识别安装路径 · 免安装即用 · 纯净版 / 商业版任选
</p>

<p align="center">
  <img src="https://img.shields.io/badge/版本-2.3.0-07C160?style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="platform">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="license">
</p>

---

## 下载

前往 **[Releases 发布页](https://github.com/aiyangdie/WexOpen/releases/latest)**，在页面下方 **Assets** 区域按需下载。

### 纯净版

适合个人日常使用，**只有多开功能，界面干净无附加内容**。

| 文件 | 说明 |
|------|------|
| [WexOpen-Portable.exe](https://github.com/aiyangdie/WexOpen/releases/latest/download/WexOpen-Portable.exe) | 免安装单文件，**推荐** |
| [WexOpen-Portable.zip](https://github.com/aiyangdie/WexOpen/releases/latest/download/WexOpen-Portable.zip) | 压缩包 |
| [WexOpen-Setup.exe](https://github.com/aiyangdie/WexOpen/releases/latest/download/WexOpen-Setup.exe) | 安装版，自动创建桌面快捷方式 |

### 商业版

适合商业化场景，**含商务合作广告位、关于页面、作者信息与开源链接**。

| 文件 | 说明 |
|------|------|
| [WexOpen-Business-Portable.exe](https://github.com/aiyangdie/WexOpen/releases/latest/download/WexOpen-Business-Portable.exe) | 免安装单文件，**推荐** |
| [WexOpen-Business-Portable.zip](https://github.com/aiyangdie/WexOpen/releases/latest/download/WexOpen-Business-Portable.zip) | 压缩包 |

> 两个版本都在同一个 Releases 页面，无需 Python，下载后双击即可使用。

### 如何查看 / 下载历史版本？

GitHub 的 Releases 页面**默认只展开最新版**，历史版本需要往下翻：

1. 打开 **[全部 Releases](https://github.com/aiyangdie/WexOpen/releases)**（不要只停在 Latest）
2. 在 **v2.3.0** 下方继续滚动，可看到 **v2.2.1、v2.2.0、v2.0.1…** 等历史条目
3. 点击某一版本的标题（如 `v2.2.0`）展开，在 **Assets** 里下载该版本的 exe

也可直接查看 **[CHANGELOG 更新日志](CHANGELOG.md)**，每个版本都有说明和下载直链。

### 源码怎么下载？

每个版本的 Releases 里都有源码，有两种方式：

| 方式 | 说明 |
|------|------|
| **GitHub 自动生成** | 在 Assets 最下方有 `Source code (zip)` 和 `Source code (tar.gz)`，每个历史版本都有 |
| **命名源码包** | 从 **v2.3.1** 起额外提供 `WexOpen-vX.X.X-source.zip`，更方便识别 |

旧版本若没有命名源码包，可用直链下载，例如：

- v2.3.0 源码：https://github.com/aiyangdie/WexOpen/archive/refs/tags/v2.3.0.zip
- v2.2.0 源码：https://github.com/aiyangdie/WexOpen/archive/refs/tags/v2.2.0.zip

或执行：`git clone https://github.com/aiyangdie/WexOpen.git` 后 `git checkout v2.3.0`

| 版本 | 发布页 |
|------|--------|
| **v2.3.0**（当前最新） | [下载](https://github.com/aiyangdie/WexOpen/releases/tag/v2.3.0) |
| v2.2.1 | [下载](https://github.com/aiyangdie/WexOpen/releases/tag/v2.2.1) |
| v2.2.0 | [下载](https://github.com/aiyangdie/WexOpen/releases/tag/v2.2.0) |
| v2.0.1 | [下载](https://github.com/aiyangdie/WexOpen/releases/tag/v2.0.1) |
| v2.0.0 | [下载](https://github.com/aiyangdie/WexOpen/releases/tag/v2.0.0) |
| v1.0.0 | [下载](https://github.com/aiyangdie/WexOpen/releases/tag/v1.0.0) |

### 版本对比

| | 纯净版 | 商业版 |
|---|:---:|:---:|
| 微信多开 | ✅ | ✅ |
| 自动检测路径 | ✅ | ✅ |
| 双开 / 三开 / 四开 / 五开 | ✅ | ✅ |
| 自定义 1–20 个窗口 | ✅ | ✅ |
| 商务合作 / 广告位 | — | ✅ |
| 关于 / 作者 / 开源链接 | — | ✅ |

---

## 功能

- **零配置** — 自动读取注册表、卸载信息、运行进程、常见安装目录，换电脑不用改路径
- **快捷多开** — 双开 / 三开 / 四开 / 五开一键操作
- **自定义数量** — 支持 1–20 个窗口，想开几个开几个
- **全版本兼容** — 同时支持新版 `Weixin.exe` 与旧版 `WeChat.exe`
- **精致界面** — v2.3 极简 UI 重设计，单面板布局、更少边框噪音

---

## 使用说明

1. 下载对应版本的 `.exe` 文件
2. 双击运行，程序自动检测本机微信安装位置
3. 输入数量或点击快捷按钮，再点 **「启动微信」**
4. 若提示未检测到微信，请先安装 [PC 版微信](https://weixin.qq.com/)，再点 **「重新检测」**

> 建议先完全退出已有微信，再用本工具启动，多开效果更稳定。

---

## 常见问题

**Q：点了启动但只开了一个？**  
A：请先关闭所有微信窗口，再用本工具重新启动。

**Q：检测不到微信？**  
A：确认已安装官方 PC 版微信，安装完成后点击「重新检测」。

**Q：杀毒软件报毒？**  
A：PyInstaller 打包的程序可能被误报，添加信任即可，也可自行编译源码。

**Q：纯净版和商业版有什么区别？**  
A：功能完全相同。纯净版界面干净；商业版额外展示商务合作广告位与作者 / 开源信息。

---

## 开发者

### 从源码运行

```bash
git clone https://github.com/aiyangdie/WexOpen.git
cd WexOpen
pip install -r requirements.txt

# 纯净版
python main.py

# 商业版
python main_business.py
```

### 本地打包

```bash
build.bat
```

输出文件：

| 路径 | 说明 |
|------|------|
| `dist/WexOpen-Portable.exe` | 纯净版免安装 |
| `dist/WexOpen-Business-Portable.exe` | 商业版免安装 |
| `dist/installer/WexOpen-Setup.exe` | 纯净版安装包 |

### 自动发布

推送 `v*` 标签即可触发 GitHub Actions 自动构建并上传到 Releases：

```bash
git tag v2.2.1
git push origin v2.2.1
```

---

## 项目结构

```
WexOpen/
├── main.py                    # 纯净版入口
├── main_business.py           # 商业版入口
├── WexOpen.spec               # PyInstaller 打包配置
├── build.bat                  # 一键打包脚本
├── RELEASE_NOTES.md           # 发布说明模板
├── assets/                    # 图标资源
├── installer/WexOpen.iss      # Inno Setup 安装脚本
├── wexopen/
│   ├── theme.py               # 设计系统（颜色 / 字体）
│   ├── app.py                 # 主界面
│   ├── about.py               # 关于对话框
│   ├── meta.py                # 作者与项目信息
│   ├── finder.py              # 微信路径自动检测
│   └── launcher.py            # 多开启动逻辑
└── .github/workflows/         # CI 自动构建发布
```

---

## 免责声明

本软件开源免费，**仅供个人学习与研究参考**，请勿用于任何违法用途。

---

## 作者

**[aiyangdie](https://github.com/aiyangdie)**

- 邮箱：aike1015@qq.com
- 开源仓库：https://github.com/aiyangdie/WexOpen
- 商务合作：请下载商业版或发送邮件联系

---

## 许可证

[MIT License](LICENSE)
