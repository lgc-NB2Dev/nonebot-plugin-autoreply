<!-- markdownlint-disable MD033 MD036 MD041 -->

<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# NoneBot-Plugin-AutoReply

_✨ 自动回复 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/lgc2333/nonebot-plugin-autoreply.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-autoreply">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-autoreply.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pypi.python.org/pypi/nonebot-plugin-autoreply">
    <img src="https://img.shields.io/pypi/dm/nonebot-plugin-autoreply" alt="pypi download">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/3eb869b8-2edf-46dd-b325-916d9f8a4888">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/3eb869b8-2edf-46dd-b325-916d9f8a4888.svg" alt="wakatime">
</a>
</div>

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

插件的配置文件位于 `data/autoreply/replies.json` 下  
因为把这种东西写在 env 里会太紧凑不易读，所以我单独弄出来了

请根据下面的注释来编辑配置文件，实际配置文件内不要有注释

```jsonc
[
  {
    // 消息的匹配规则，可以放置多个
    "matches": [
      {
        // 用于匹配消息的文本
        "match": "测试",

        // 匹配模式，可选 `full`(完全匹配)、`fuzzy`(模糊匹配)、`regex`(正则匹配)
        // 在正则匹配下，请使用 `\\` 在 json 里的正则表达式里表示 `\`，因为 json 解析时本身就会将 `\` 作为转义字符
        // 可以不填，默认为 `fuzzy`
        "type": "fuzzy",

        // 是否需要 at 机器人才能触发（叫机器人昵称也可以）
        // 可以不填，默认为 `false`
        "to_me": false,

        // 是否忽略大小写
        // 可以不填，默认为 `true`
        "ignore_case": true,

        // 是否去掉消息前后的空格再匹配
        // 可以不填，默认为 `true`
        "strip": true,

        // 当带 cq 码的消息匹配失败时，是否使用去掉 cq 码的消息再匹配一遍
        // 可以不填，默认为 `true`
        "allow_plaintext": true
      }

      // 更多匹配规则...
    ],

    // 匹配成功后，回复的消息
    // 如果有多个，将随机抽取一个回复
    "replies": [
      // type=normal 时，message 需要为字符串，会解析 message 中的 CQ 码并发送
      {
        "type": "normal",
        "message": "这是一条消息，可以使用CQ码[CQ:image,file=https://pixiv.re/103981177.png]"
      },

      // 直接写字符串也能表示 type=normal
      "这是一条消息，可以使用CQ码[CQ:image,file=https://pixiv.re/103981177.png]",

      // type=plain 时，message 需要为字符串，但是 message 中的 CQ 码不会被解析
      {
        "type": "plain",
        "message": "这条消息后面的CQ码会以原样发送[CQ:at,qq=3076823485]"
      },

      // type=array 时，message 中需要填 CQ 码的 json 格式
      {
        "type": "array",
        "message": [
          {
            "type": "text",
            "data": {
              "text": "我后面带了一张图片哦"
            }
          },
          {
            "type": "image",
            "data": {
              "file": "https://pixiv.re/103981177.png"
            }
          }
        ]
      },

      // 直接写数组也能代表 type=array
      [
        {
          "type": "text",
          "data": {
            "text": "我可以正常发送哦"
          }
        }
      ],

      // type=multi 时，message 需要为上面提到的消息类型的数组
      // 会按顺序发送 message 中的所有内容
      // message 中不允许嵌套其他的 type=multi 类型的回复
      {
        "type": "multi",
        // delay 是每条消息发送成功后的延时，格式为 [最低延时, 最高延时]
        // 单位为毫秒（1000 毫秒 = 1 秒），可以不填，默认为 [0, 0]
        "delay": [1000, 1000],
        "message": [
          "hello! 一会给你发张图哦~",
          "[CQ:image,file=https://pixiv.re/103981177.png]一会给你分享首歌哦awa~",
          [
            {
              "type": "music",
              "data": {
                "type": "163",
                "id": "2008994667"
              }
            }
          ]
        ]
      }

      // 更多消息...
    ],

    // 过滤指定群聊
    // 可以不填，默认为空的黑名单
    "groups": {
      // 黑名单类型，可选 `black`(黑名单)、`white`(白名单)
      "type": "black",

      // 要过滤的群号
      "values": [
        123456789, 987654321
        // 更多群号...
      ]
    },

    // 过滤指定用户
    // 可以不填，默认为空的黑名单
    "users": {
      // 黑名单类型，可选 `black`(黑名单)、`white`(白名单)
      "type": "black",

      // 要过滤的QQ号
      "values": [
        1145141919, 9191415411
        // 更多QQ号...
      ]
    }
  }

  // ...
]
```

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

### 0.2.1

- 修复多 `match` 无法使用的问题

### 0.2.0

- 使用 `rule` 匹配消息，避免日志刷屏
- 支持一次回复多条消息，调整配置文件结构
- 增加了两个 `.env` 配置项
- 增加热重载配置文件的指令
