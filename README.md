<p align="center"><img src="assets/covers/05-WexOpen.jpg" alt="WexOpen 项目封面" width="100%"></p>

<h1 align="center">WexOpen · PC 微信多开助手</h1>

<p align="center">自动识别微信安装路径，免安装双击即用，纯净版与商业版可选</p>

<p align="center">
  <a href="https://github.com/aiyangdie/WexOpen/releases/latest">下载最新版</a> ·
  <a href="LICENSE">MIT 许可</a>
</p>

## 简介

Windows 上的微信多开小工具。不需要手动找安装目录，程序会读取注册表、卸载信息、运行进程和常见路径，同时兼容新版 `Weixin.exe` 与旧版 `WeChat.exe`。打包为免安装 exe，机器上不需要 Python。

## 功能

- **零配置**：自动定位微信安装路径，换电脑不用改配置
- **快捷多开**：双开、三开、四开、五开一键启动
- **自定义数量**：支持 1–20 个窗口
- **全版本兼容**：新版与旧版微信客户端都能识别
- **两套界面**：纯净版只保留多开功能；商业版额外带关于页、作者与开源链接

## 使用

1. 从 [Releases](https://github.com/aiyangdie/WexOpen/releases) 下载对应 exe（纯净版 `WexOpen-Portable.exe`，商业版 `WexOpen-Business-Portable.exe`）
2. 双击运行，等待自动检测完成
3. 选择数量或点快捷按钮，再点「启动微信」
4. 提示未检测到微信时，先安装 [PC 版微信](https://weixin.qq.com/)，再点「重新检测」

建议先把已开的微信全部退出，再多开更稳定。历史版本在 Releases 页面往下滚动展开。

## 从源码运行

```bash
git clone https://github.com/aiyangdie/WexOpen.git
cd WexOpen
pip install -r requirements.txt

python main.py            # 纯净版
python main_business.py   # 商业版
```

打包：`build.bat`，产物在 `dist/`（免安装 exe、安装包）。推送 `v*` 标签会触发 GitHub Actions 自动构建并上传 Releases。

## 项目结构

```
main.py / main_business.py   两个版本入口
wexopen/
  theme.py       设计系统（颜色、字体）
  app.py         主界面
  finder.py      微信路径自动检测
  launcher.py    多开启动逻辑
  about.py / meta.py
WexOpen.spec     PyInstaller 打包配置
installer/       Inno Setup 安装脚本
```

## 常见问题

- **点了启动只开一个**：先把所有微信窗口关掉再启动
- **检测不到微信**：确认已装官方 PC 版，装完点「重新检测」
- **杀毒软件报毒**：PyInstaller 打包的常见误报，可加信任或自行编译源码

## 免责声明

本软件开源免费，仅供个人学习与研究参考，请勿用于违法用途。

## 许可证

[MIT](LICENSE) ｜ 作者 [aiyangdie](https://github.com/aiyangdie) · aike1015@qq.com
