<!-- markdownlint-disable MD031 -->

# 贡献指南

1. Fork 本仓库

2. 在仓库 `marketplace/replies` 文件夹下新建一个文件夹，文件夹名称要求和你的配置内容相关，且只允许小写字母、数字和下划线

3. 在你新创建的文件夹内，新建下述文件

   - `reply.json` - 回复配置本体

   - `meta.json` - 该回复配置的元信息，具体内容：

     ```json
     {
       // 该配置在侧边栏中的显示名称，以及介绍页面中显示的标题
       "name": "测试",

       // 该配置在介绍页面中显示的简介
       "desc": "这是一个简介",

       // 该配置的作者在介绍页面中的显示名称
       "author": "student_2333",

       // 该配置的作者在介绍页面的显示名称点击后进入的链接
       // 建议填写 GitHub 个人资料页 或 个人主页
       "author_link": "https://lgc2333.top",

       // 该配置的标签，会显示在介绍页面
       "tags": ["在", "在吗"]
     }
     ```

   - _(可选)_ `info.md` - 该回复配置的详细说明，使用 Markdown 格式  
     这部分内容会夹在介绍页插件元信息和配置内容的中间，建议第一层标题使用 `##` 开头

4. 文件提交完成后，向仓库提交 Pull Request 等待合并即可 :wink:

如果有疑问，请看 [这个](https://github.com/lgc-NB2Dev/nonebot-plugin-autoreply/tree/master/marketplace/replies/are_you_here) 示例
