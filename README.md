# WexOpen

> 简约风格的 PC 微信多开助手 · 自动识别安装路径 · 想开几个开几个

![Python](https://img.shields.io/badge/Python-3.10+-07C160?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

## 功能

- **自动检测微信** — 读取注册表、卸载信息、运行进程、常见安装目录，无需手动配置路径
- **一键多开** — 大按钮启动，支持双开 / 三开 / 四开快捷操作
- **自定义数量** — 输入 1–20，想开几个开几个
- **简约界面** — 浅色极简设计，开箱即用
- **通用兼容** — 支持新版 `Weixin.exe` 与旧版 `WeChat.exe`

## 快速开始

### 方式一：双击启动（推荐）

1. 确保已安装 [Python 3.10+](https://www.python.org/downloads/)
2. 双击 **`启动.bat`**
3. 首次运行会自动创建虚拟环境并安装依赖

### 方式二：命令行

```bash
git clone https://github.com/aiyangdie/WexOpen.git
cd WexOpen
pip install -r requirements.txt
python main.py
```

## 使用说明

1. 打开程序后会自动检测本机微信安装位置
2. 在数量框输入想打开的窗口数（默认 2）
3. 点击 **「启动微信」**，或使用 **双开 / 三开 / 四开** 快捷按钮
4. 若未检测到微信，请先安装 PC 版微信，再点 **「重新检测」**

## 检测原理

程序按以下顺序自动查找微信，找到即停：

| 优先级 | 方式 |
|--------|------|
| 1 | 注册表 `InstallPath`（Weixin / WeChat） |
| 2 | 卸载信息注册表 |
| 3 | 当前正在运行的微信进程 |
| 4 | 常见安装目录（Program Files 等） |
| 5 | 系统 PATH 环境变量 |

换电脑、重装微信、升级版本都**不需要改任何配置**。

## 项目结构

```
WexOpen/
├── main.py              # 程序入口
├── 启动.bat              # Windows 一键启动
├── requirements.txt
├── wexopen/
│   ├── finder.py        # 微信路径自动检测
│   ├── launcher.py      # 多开启动逻辑
│   └── app.py           # 图形界面
└── README.md
```

## 常见问题

**Q: 点了启动但只开了一个？**  
A: 请先完全退出所有微信窗口，再用本工具启动。已有微信在运行时，部分版本会阻止新实例。

**Q: 检测不到微信？**  
A: 确认已安装官方 PC 版微信。若刚安装完，点「重新检测」即可。

**Q: 最多能开几个？**  
A: 默认上限 20 个，可在 `wexopen/launcher.py` 中调整 `MAX_INSTANCES`。

## 许可证

MIT License — 自由使用、修改与分发。

## 作者

[aiyangdie](https://github.com/aiyangdie)
