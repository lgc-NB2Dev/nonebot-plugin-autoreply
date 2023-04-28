<!-- markdownlint-disable -->
# 在吗？

作者：[student_2333](https://lgc2333.top)

![在](https://img.shields.io/badge/-在-brightgreen?style=flat-square) ![在吗](https://img.shields.io/badge/-在吗-brightgreen?style=flat-square)

> @Bot 并带上“在吗”时回复

<hr />

<!-- markdownlint-disable MD041 -->

## 介绍

本回复规则会在以下情况向用户作回应答：

- 用户 `@Bot` 并发送 `在(吗)(？)` / `zai(ma)(?)` 时
- 用户 `@Bot` 并不带任何参数时

其中，`@Bot` 可以换成 Bot 昵称

## 触发示例

- `@Bot 在吗`
- `@Bot zai ma`
- `@Bot`


## 配置内容

[右键点击我，选择 “链接另存为...” 即可下载](https://autoreply.lgc2333.top/replies/are_you_here/reply.yml)

<details>
<summary>点击展开</summary>

```yml
- matches:
    # @Bot 在/在吗/zai ma
    - match: '^(，|,)?\s*(在吗?|zai(\s*ma)?)\s*(？|\?)?$'
      type: regex
      to_me: true

    # 只 @Bot 不带任何文本
    - match: ''
      type: full
      to_me: true
      allow_plaintext: false

  replies:
    - '{at}在哦~'
    - '{at}有什么事吗？'
    - '{at}需要帮助吗？'
    - '{at}来了！'

```
</details>