<!-- markdownlint-disable MD024 MD033 MD036 -->

# 配置文档

插件的配置文件位于 `data/autoreply` 下，下面是插件支持的配置格式以及他们的特点：

- **YAML** - 后缀名为 `.yml` 或 `.yaml`，结构较清晰，功能强大，推荐熟悉该格式的用户作为首选格式使用
- **JSON** - 后缀名为 `.json`，结构简明清晰，推荐小白使用

直接在插件配置文件夹下新建对应后缀名的文本文件即可开始配置，插件会自动寻找并加载

> Tip: 文档较长，善用侧边栏导航功能

## 配置结构

请根据下面的注释来编辑配置文件

<!-- tabs:start -->

### **YAML**

```yml
# 注意整个 yml 文件是一个数组，里面包含了多个回复规则

- # 该组配置是否阻塞其他回复配置
  # 可以不填，默认为 `true`
  block: true

  # 该组配置的优先级，越大越高
  # 可以不填，默认为 1
  priority: 1

  # 消息的匹配规则，是数组，可以放置多个
  matches:
    - # 匹配模式，可选 `full`(完全匹配)、`fuzzy`(模糊匹配)、`regex`(正则匹配)、`poke`(双击头像戳一戳)
      #
      # 使用 `poke` 匹配时，除了 `possibility` 和 `to_me` 条件，其他的匹配条件都会被忽略
      # 注意：`poke` 会匹配所有戳一戳事件，如果你只想要匹配 Bot 被戳的事件，请将 `to_me` 设为 `true`
      #
      # 可以不填，默认为 `fuzzy`
      type: fuzzy

      # 该匹配触发的概率，范围在 0 ~ 1 之间
      # 可以不填，默认为 1.0
      possibility: 1

      # 用于匹配消息的文本
      match: '测试'

      # 是否需要 at 机器人才能触发（叫机器人昵称也可以）
      # 当匹配模式为 `poke` 时，只有 被戳 的对象是 Bot，事件才会匹配成功
      # 可以不填，默认为 `false`
      to_me: false

      # 是否忽略大小写
      # 可以不填，默认为 `true`
      ignore_case: true

      # 是否去掉消息前后的空格再匹配
      # 可以不填，默认为 `true`
      strip: true

      # 当带 CQ 码的消息匹配失败时，是否使用去掉 CQ 码的消息再匹配一遍
      # 可以不填，默认为 `true`
      allow_plaintext: true

    # 如果规则为一个字符串，则会转换为一个 除 `match` 外 其他属性全部默认 的规则来匹配
    - '测试2'

  # 匹配成功后，回复的消息
  # 是数组，如果有多个，将随机抽取一个回复
  replies:
    # type=normal 时，message 需要为字符串，会解析 message 中的 CQ 码并发送
    - type: normal
      message: '这是一条消息，可以使用CQ码[CQ:image,file=https://pixiv.re/103981177.png]'

    # 直接写字符串也能表示 type=normal
    - '这是一条消息，可以使用CQ码[CQ:image,file=https://pixiv.re/103981177.png]'

    # type=plain 时，message 需要为字符串，但是 message 中的 CQ 码不会被解析
    - type: plain
      message: '这条消息后面的CQ码会以原样发送[CQ:at,qq=3076823485]'

    # 直接写 @ 开头的字符串也能表示 type=plain
    - '@这条消息后面的CQ码也会以原样发送[CQ:at,qq=3076823485]'

    # type=array 时，message 中需要填 CQ 码的 json 格式
    - type: array
      message:
        - type: text
          data:
            text: '我后面带了一张图片哦'
        - type: image
          data:
            file: 'https://pixiv.re/103981177.png'

    # 直接写数组也能代表 type=array
    # 注意这里在 replies 数组里嵌套了一个数组
    - - type: text
        data:
          text: '我可以正常发送哦'

    # type=multi 时，message 需要为上面提到的消息类型的数组
    # 会按顺序发送 message 中的所有内容
    # message 中不允许嵌套其他的 type=multi 类型的回复
    - type: multi

      # delay 是每条消息发送成功后的延时，格式为 [最低延时, 最高延时]
      # 单位为毫秒（1000 毫秒 = 1 秒），可以不填，默认为 [0, 0]
      delay: [1000, 1500]

      # 当 delay 值仅为一个整数时，代表固定延时发送，等同 [delay, delay]
      # delay: 1000

      # 是否打乱 message 数组发送
      # 可以不填，默认为 `false`
      shuffle: false

      # 要发送的多条消息
      message:
        # normal 类型
        - 'hello! 一会给你发张图哦~'
        - '[CQ:image,file=https://pixiv.re/103981177.png]一会给你分享首歌哦awa~'

        # array 类型
        - - type: music
            data:
              type: 163
              id: 2008994667

  # 过滤指定群聊
  # 可以不填，默认为空的黑名单
  groups:
    # 黑名单类型，可选 `black`(黑名单)、`white`(白名单)
    type: black

    # 要过滤的群号
    values:
      - 123456789
      - 987654321

  # 过滤指定用户
  # 可以不填，默认为空的黑名单
  users:
    # 结构同上
    type: black
    values:
      - 1145141919
      - 9191415411
```

### **JSON**

**实际 JSON 配置文件内不可以包含注释**

```json
[
  {
    // 该组配置是否阻塞其他回复配置
    // 可以不填，默认为 `true`
    "block": true,

    // 该组配置的优先级，越大越高
    // 可以不填，默认为 1
    "priority": 1,

    // 消息的匹配规则，可以放置多个
    "matches": [
      {
        // 匹配模式，可选 `full`(完全匹配)、`fuzzy`(模糊匹配)、`regex`(正则匹配)、`poke`(双击头像戳一戳)
        //
        // 使用 `poke` 匹配时，除了 `possibility` 和 `to_me` 条件，其他的匹配条件都会被忽略
        // 注意：`poke` 会匹配所有戳一戳事件，如果你只想要匹配 Bot 被戳的事件，请将 `to_me` 设为 `true`
        //
        // 可以不填，默认为 `fuzzy`
        "type": "fuzzy",

        // 该匹配触发的概率，范围在 0 ~ 1 之间
        // 可以不填，默认为 1.0
        "possibility": 1.0,

        // 用于匹配消息的文本
        // 在正则匹配下，注意使用 `\\` 在 json 里的正则表达式里表示 `\`，因为 json 解析时本身就会将 `\` 作为转义字符
        "match": "测试",

        // 是否需要 at 机器人才能触发（叫机器人昵称也可以）
        // 当匹配模式为 `poke` 时，只有 被戳 的对象是 Bot，事件才会匹配成功
        // 可以不填，默认为 `false`
        "to_me": false,

        // 是否忽略大小写
        // 可以不填，默认为 `true`
        "ignore_case": true,

        // 是否去掉消息前后的空格再匹配
        // 可以不填，默认为 `true`
        "strip": true,

        // 当带 CQ 码的消息匹配失败时，是否使用去掉 CQ 码的消息再匹配一遍
        // 可以不填，默认为 `true`
        "allow_plaintext": true
      },

      // 如果规则为一个字符串，则会转换为一个属性全部默认的 `match` 来匹配
      "测试2"

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

      // 直接写 @ 开头的字符串也能表示 type=plain
      "@这条消息后面的CQ码也会以原样发送[CQ:at,qq=3076823485]",

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
        "delay": [1000, 1500],

        // 当 delay 值仅为一个整数时，代表固定延时发送，等同 [delay, delay]
        // "delay": 1000,

        // 是否打乱 message 数组发送
        // 可以不填，默认为 `false`
        "shuffle": false,

        // 要发送的多条消息
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

<!-- tabs:end -->

## 关于变量

配置文件中的变量使用 [MessageTemplate.format_map()](https://v2.nonebot.dev/docs/tutorial/message#%E4%BD%BF%E7%94%A8%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF) 替换；  
非 `type=text` 的 `array` 类型消息则使用 `str.format()` 替换

下面两种类型变量的使用场景：

- 普通变量可以在 `normal` 和 `array` 类型的消息中使用
- 特殊变量只能在 `normal` 和 `type=text` 的 `array` 类型消息中使用
- `plain` 类型消息则无法使用变量
- `multi` 类型中嵌套的上述类型消息遵循同样的规则

### 变量列表

#### 普通变量

- `{bs}` - “`{`”，转义用 _（`bracket start` 的缩写）_
- `{be}` - “`}`”，转义用 _（`bracket end` 的缩写）_
- `{self_id}` - 机器人 QQ
- `{message_id}` - 消息 ID _（当 `match` 的 `type` 为 `poke` 时为 `None`）_
- `{user_id}` - 发送者 QQ
- `{group_id}` - 消息来源群号 _（私聊等为 `None`）_
- `{target_id}` - 被戳者 QQ _（仅当 `match` 的 `type` 为 `poke` 时有值，其他情况为 `None`）_
- `{nickname}` - 发送者昵称
- `{card}` - 发送者群名片
- `{display_name}` - 发送者显示名称 _（优先群名片，当群名片为空时为昵称）_

#### 特殊变量

- `{at}` - 艾特发送者
- `{reply}` - 回复发送者 _（当 `match` 的 `type` 为 `poke` 时为 `None`）_

### 示例

下面放出几个示例，帮助大家更好的理解如何使用变量

<!-- tabs:start -->

#### **YAML**

```yml
# 注意整个 yml 文件是一个数组，里面包含了多个回复规则

- matches:
    - match: '^(@|at|艾特)我$'
      type: regex

  replies:
    # 在 normal 类型消息中使用
    - '[normal] At了 [CQ:at,qq={user_id}]'

    # 在 array 类型消息中使用，注意插件只会替换 data 中值类型为 字符串 其中的变量
    # 注意这里在 replies 数组里嵌套了一个数组
    - - type: text
        data:
          text: '[array] At了 '

      - type: at
        data:
          qq: '{user_id}'

    # 在 multi 类型消息中使用
    - type: multi
      message:
        # 嵌套的 array 类型消息
        - - type: at
            data:
              qq: '{user_id}'

        # 嵌套的 normal 类型消息
        - '[multi] 我刚刚 At 了一下你哦~ 收到了吗？'

    # 无法在 plain 类型消息中使用，{user_id}、{nickname} 会原样显示
    - '@[plain] [CQ:at,qq={user_id}] 啊咧？怎么 At 不了 {nickname}？'

    # 可以在消息中使用 {bs｝ 和 {be} 来转义大括号
    # 前面的 {bs}user_id{be} 会转义成 {user_id} 发送
    # 而后面的 {nickname} 会被替换为发送者昵称
    - '[normal] [CQ:at,qq={bs}user_id{be}] 啊咧？怎么 At 不了 {nickname}？'
```

#### **JSON**

**实际 JSON 配置文件内不可以包含注释**

```json
[
  {
    "matches": [
      {
        "match": "^(@|at|艾特)我$",
        "type": "regex"
      }
    ],
    "replies": [
      // 在 normal 类型消息中使用
      "[normal] At了 [CQ:at,qq={user_id}]",

      // 在 array 类型消息中使用，注意插件只会替换 data 中值类型为 字符串 其中的变量
      [
        {
          "type": "text",
          "data": {
            "text": "[array] At了 "
          }
        },
        {
          "type": "at",
          "data": {
            "qq": "{user_id}"
          }
        }
      ],

      // 在 multi 类型消息中使用
      {
        "type": "multi",
        "message": [
          // 嵌套的 array 类型消息
          [
            {
              "type": "at",
              "data": {
                "qq": "{user_id}"
              }
            }
          ],

          // 嵌套的 normal 类型消息
          "[multi] 我刚刚 At 了一下你哦~ 收到了吗？"
        ]
      },

      // 无法在 plain 类型消息中使用，{user_id}、{nickname} 会原样显示
      "@[plain] [CQ:at,qq={user_id}] 啊咧？怎么 At 不了 {nickname}？",

      // 可以在消息中使用 {bs｝ 和 {be} 来转义大括号
      // 前面的 {bs}user_id{be} 会转义成 {user_id} 发送
      // 而后面的 {nickname} 会被替换为发送者昵称
      "[normal] [CQ:at,qq={bs}user_id{be}] 啊咧？怎么 At 不了 {nickname}？"
    ]
  }
]
```

<!-- tabs:end -->
