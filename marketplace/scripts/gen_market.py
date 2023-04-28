import json
from dataclasses import dataclass
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
REPLIES_PATH = ROOT_PATH / "replies"
REPLIES_INDEX_PATH = ROOT_PATH / "replies" / "index.json"
MARKET_ROOT_PATH = ROOT_PATH / "market"
MARKET_REPLY_PATH = MARKET_ROOT_PATH / "replies"
SIDEBAR_MD_PATH = MARKET_ROOT_PATH / "_sidebar.md"

ALLOWED_SUFFIXES = (".json", ".yml", ".yaml")


@dataclass
class ReplyMeta:
    name: str
    desc: str
    author: str
    author_link: str
    tags: list[str]


def find_reply_file(path: Path) -> Path:
    for suffix in ALLOWED_SUFFIXES:
        file_path = path / f"reply{suffix}"

        if file_path.exists():
            return file_path

    raise ValueError


def main():
    reply_paths = [x for x in REPLIES_PATH.iterdir() if x.is_dir()]

    reply_index = []
    main_readme = [
        "<!-- markdownlint-disable -->",
        "# 市场列表\n",
        "这里可以看到大家分享的回复配置！\n",
        "想提交自己的回复？来看看 [贡献指南](market/contributing)！\n",
        "| 名称 | 作者 | 介绍 | 标签 |",
        "| :- | :- | :- | :- |",
    ]
    sidebar = [
        "<!-- markdownlint-disable -->",
        "- [回复市场](market/)",
        "  - [贡献指南](market/contributing)",
        "  - [市场列表](market/replies/)",
    ]

    for path in reply_paths:
        dir_name = path.name

        meta_path = path / "meta.json"
        reply_path = find_reply_file(path)
        info_readme_path = path / "info.md"

        meta = ReplyMeta(**json.loads(meta_path.read_text(encoding="u8")))
        reply = reply_path.read_text(encoding="u8")

        tags = " ".join(
            [
                f"![{x}](https://img.shields.io/badge/-{x}-brightgreen?style=flat-square)"
                for x in meta.tags
            ],
        )
        desc = "".join([f"> {x}" for x in meta.desc.splitlines()])

        readme = (
            "<!-- markdownlint-disable -->\n"
            f"# {meta.name}\n"
            "\n"
            f"作者：[{meta.author}]({meta.author_link})\n"
            "\n"
            f"{tags}\n"
            "\n"
            f"{desc}"
            "\n\n<hr />\n\n"
        )

        if info_readme_path.exists():
            info = info_readme_path.read_text(encoding="u8")
            readme = f"{readme}{info}"

        readme = (
            f"{readme}\n"
            "\n"
            "## 配置内容\n"
            "\n"
            f"[右键点击我，选择 “链接另存为...” 即可下载](https://autoreply.lgc2333.top/replies/{dir_name}/{reply_path.name})\n"
            "\n"
            f"```{reply_path.suffix[1:]}\n"
            f"{reply}\n"
            "```"
        )

        sidebar.append(
            f'    - [{meta.name}](market/replies/{dir_name} "{meta.name} | AutoReply 回复市场")',
        )
        br_desc = meta.desc.replace("\n", "<br />")
        main_readme.append(
            f"| [{meta.name}](market/replies/{dir_name}) "
            f"| [{meta.author}]({meta.author_link}) "
            f"| {br_desc} "
            f"| {tags} |",
        )

        reply_index.append(
            {"dir": dir_name, "filename": reply_path.name, **meta.__dict__},
        )
        readme_path = MARKET_REPLY_PATH / f"{dir_name}.md"
        readme_path.write_text(readme, encoding="u8")
        main_readme_path = MARKET_REPLY_PATH / "README.md"
        main_readme_path.write_text("\n".join(main_readme), encoding="u8")

        print(f"OK - {dir_name} - {meta.name}")

    SIDEBAR_MD_PATH.write_text("\n".join(sidebar), encoding="u8")
    # REPLIES_INDEX_PATH.write_text(json.dumps(reply_index), encoding="u8")


if __name__ == "__main__":
    main()
