# 在吗？

作者：[student_2333](https://lgc2333.top)

![在](https://img.shields.io/badge/-在-green?style=flat)
![在吗](https://img.shields.io/badge/-在吗-green?style=flat)

> @Bot 在吗 回复

<hr />

<!-- markdownlint-disable MD041 -->

## 介绍

本回复规则会在用户 `@Bot` 并发送 `在(吗)` 时向用户作回应答


## 配置内容

```json
[
  {
    "matches": [
      {
        "match": "在吗?\\s*(？|\\?)?",
        "type": "regex",
        "to_me": true
      }
    ],
    "replies": ["Bot 在哦~"]
  }
]

```