# WexOpen

> 简约精致的 PC 微信多开助手 · 自动识别 · 免安装 / 安装版任选

![Python](https://img.shields.io/badge/Python-3.10+-07C160?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

<p align="center">
  <img src="assets/icon.png" alt="WexOpen" width="96">
</p>

**无需 Python · 无需配置路径 · 下载即用**

---

## 下载（推荐）

前往 **[Releases 发布页](https://github.com/aiyangdie/WexOpen/releases/latest)** 下载：

### 纯净版（推荐个人使用）

| 文件 | 说明 |
|------|------|
| `WexOpen-Portable.exe` | 免安装，无广告，双击即用 |
| `WexOpen-Portable.zip` | 同上，zip 格式 |
| `WexOpen-Setup.exe` | 安装版，自动创建桌面快捷方式 |

### 商业版（接广告 / 商务合作）

| 文件 | 说明 |
|------|------|
| `WexOpen-Business-Portable.exe` | 含商务合作广告位，免安装 |
| `WexOpen-Business-Portable.zip` | 同上，zip 格式 |

> 开发者：**aiyangdie** · 开源地址：[github.com/aiyangdie/WexOpen](https://github.com/aiyangdie/WexOpen)  
> 本软件仅供学习参考，商业合作联系：aike1015@qq.com

---

## 功能

- **自动检测微信** — 注册表 / 卸载信息 / 运行进程 / 常见目录，零配置
- **一键多开** — 双开 / 三开 / 四开 / 五开快捷按钮
- **自定义数量** — 输入 1–20，想开几个开几个
- **精致界面** — 简约浅色设计，开箱即用
- **全版本兼容** — 支持 `Weixin.exe` 与 `WeChat.exe`

## 使用说明

1. 下载并运行 `WexOpen-Portable.exe`（或安装 `WexOpen-Setup.exe`）
2. 程序自动检测本机微信
3. 选择数量，点击 **「启动微信」**
4. 未检测到微信？先安装 PC 版微信，再点 **「重新检测」**

## 开发者

### 从源码运行

```bash
git clone https://github.com/aiyangdie/WexOpen.git
cd WexOpen
pip install -r requirements.txt
python main.py
```

### 本地打包 exe

```bash
# 双击或命令行运行
build.bat
```

输出：
- `dist/WexOpen-Portable.exe` — 免安装单文件
- `dist/installer/WexOpen-Setup.exe` — 安装版（需 Inno Setup 6）

### 自动发布

推送 `v*` 标签即可触发 GitHub Actions 自动构建并上传到 Releases：

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 项目结构

```
WexOpen/
├── main.py                  # 入口
├── WexOpen.spec             # PyInstaller 配置
├── build.bat                # 一键打包
├── assets/                  # 图标资源
├── installer/WexOpen.iss    # Inno Setup 安装脚本
├── wexopen/
│   ├── finder.py            # 微信路径检测
│   ├── launcher.py          # 多开逻辑
│   └── app.py               # 图形界面
└── .github/workflows/       # 自动构建发布
```

## 常见问题

**Q: 点了启动但只开了一个？**  
A: 先完全退出所有微信，再用本工具启动。

**Q: 检测不到微信？**  
A: 确认已安装官方 PC 版微信，安装后点「重新检测」。

**Q: 杀毒软件报毒？**  
A: PyInstaller 打包的程序可能被误报，添加信任即可。也可自行 `build.bat` 编译。

## 许可证

MIT License

## 作者

[aiyangdie](https://github.com/aiyangdie)
