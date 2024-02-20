<!-- markdownlint-disable MD033 MD036 MD041 -->

<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# NoneBot-Plugin-AutoReply

_✨ 自动回复 ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/3eb869b8-2edf-46dd-b325-916d9f8a4888">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/3eb869b8-2edf-46dd-b325-916d9f8a4888.svg" alt="wakatime">
</a>

<br />

<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v1-or-v2.json" alt="Pydantic Version 1 Or 2" >
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-autoreply.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-autoreply">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-autoreply.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-autoreply">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-autoreply" alt="pypi download">
</a>
</div>

## 🛒 回复市场

![market](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/autoreply/QQ截图20230423192951.png)

### [点击进入](https://autoreply.lgc2333.top)

我们的回复配置市场和文档站一起上线啦~  
在这里，你可以分享你的回复配置，也可以找到其他人分享的回复配置，欢迎各位使用！

_如果大家需要，我可以做一个直接使用指令下载安装市场中回复配置的功能 qwq_  
_想要的话就提个 issue 吧，没人想要的话就不做了（_

## 📖 介绍

一个简单的关键词自动回复插件，支持 模糊匹配、完全匹配 与 正则匹配，配置文件高度自定义  
因为商店里没有我想要的那种关键词回复，所以我就自己写了一个  
这个插件是从 [ShigureBot](https://github.com/lgc2333/ShigureBot/tree/main/src/plugins/shigure_bot/plugins/keyword_reply) 那边拆出来的，我重写了一下做成了单品插件

插件并没有经过深度测试，如果在使用中遇到任何问题请一定一定要过来发 issue 向我汇报，我会尽快解决  
如果有功能请求也可以直接发 issue 来 dd 我

## 💿 安装

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-autoreply
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-autoreply
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-autoreply
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-autoreply
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-autoreply
```

</details>

打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

```py
nonebot.load_plugin('nonebot_plugin_autoreply')
```

</details>

## ⚙️ 配置

### 回复配置

请访问 [配置文档](https://autoreply.lgc2333.top/#/configuring/)

### 常规配置

下方的配置皆为可选，如果不需要可以忽略不配置  
配置项请参考下面的文本

```ini
# matcher 是否阻断消息，默认 False
AUTOREPLY_BLOCK=False

# matcher 优先级
AUTOREPLY_PRIORITY=99
```

## 💬 指令

### `重载自动回复`

此命令用于重载自动回复配置，仅 `SUPERUSER` 可以执行

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

### 0.2.12

- 适配 Pydantic V1 & V2
- 修复 [#17](https://github.com/lgc-NB2Dev/nonebot-plugin-autoreply/issues/17)

### 0.2.11

- 🎉 NoneBot 2.0 🚀

### 0.2.10

- 新增了 `start`、`end` 匹配方式
- 添加变量 `message`、`plaintext`
- 可以使用变量获取 `regex` 类型的匹配结果

### 0.2.9

- 当回复中含有 `image` / `record` 类型的消息段（无论是 `normal` 还是 `array` 类型的消息），且其 `file` 属性为 `file:///` 开头时，插件将会读取该路径文件并转为 `base64` 发送
- `multi` 类型消息的 `delay` 支持了整数型值，会被解析为固定时长延时
- `multi` 类型新增 `shuffle` 属性，支持打乱消息顺序发送

### 0.2.8

- 支持解析 `yaml` 格式配置，会将 `.yml` 和 `.yaml` 的文件作为 `yaml` 格式配置加载
- 现在会寻找 `data/autoreply` 文件夹下所有子文件夹中的配置并加载
- 新增变量 `{at}`、`{reply}`
- 换用 `MessageTemplate` 格式化变量；由于这玩意不支持 `{{` 及 `}}` 转义，所以加入了变量 `{bs}` 和 `{be}`

### 0.2.7

- 新增了配置的 `block` 和 `priority` 属性
- 新增 `type` 为 `poke` (双击头像，戳一戳) 的 `match`
- 新增了 `match` 的 `possibility` 属性
- 新增了 `{target_id}` 与 `{display_name}` 变量

### 0.2.6

- 回复中可以使用变量了
- 新增配置市场

### 0.2.5

- 可以加载多个回复 Json

### 0.2.4

- 让字符串可以作为默认属性的 `match` 使用
- 让 `@` 开头的字符串 `reply` 解析为 `plain` 形式的回复

### 0.2.3

- 修复一处 py 3.8 无法使用的类型注解

### 0.2.2

- 修复群聊和用户过滤器无法正常使用的问题

### 0.2.1

- 修复多 `match` 无法使用的问题

### 0.2.0

- 使用 `rule` 匹配消息，避免日志刷屏
- 支持一次回复多条消息，调整配置文件结构
- 增加了两个 `.env` 配置项
- 增加热重载配置文件的指令
