<!-- markdownlint-disable -->
# 在吗？

作者：[student_2333](https://lgc2333.top)

![在](https://img.shields.io/badge/-在-brightgreen?style=flat-square) ![在吗](https://img.shields.io/badge/-在吗-brightgreen?style=flat-square)

> @Bot 在吗 回复

<hr />

<!-- markdownlint-disable MD041 -->

## 介绍

本回复规则会在用户 `@Bot` 并发送 `在(吗)` 时向用户作回应答


## 配置内容

[右键点击我，选择 `链接另存为...` 即可下载](https://autoreply.lgc2333.top/replies/are_you_here/reply.json)

```yml
- matches:
    - match: 在吗?\s*(？|\?)?
      type: regex
      to_me: true

  replies:
    - - type: at
        data:
          qq: '{user_id}'
      - type: text
        data:
          text: Bot 在哦~

```