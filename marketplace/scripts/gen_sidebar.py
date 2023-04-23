import json
from pathlib import Path

from attr import dataclass

REPLIES_PATH = Path(__file__).parent.parent / "replies"
SIDEBAR_MD_PATH = REPLIES_PATH / "_sidebar.md"


@dataclass
class ReplyMeta:
    name: str
    desc: str
    author: str
    author_link: str
    tags: list[str]


def main():
    reply_paths = [x for x in REPLIES_PATH.iterdir() if x.is_dir()]

    sidebar = []

    for path in reply_paths:
        meta_path = path / "meta.json"
        reply_path = path / "reply.json"
        info_readme_path = path / "info.md"
        readme_path = path / "README.md"
        meta = ReplyMeta(**json.loads(meta_path.read_text(encoding="u8")))
        reply = reply_path.read_text(encoding="u8")

        sidebar.append(f"- [{meta.name}](replies/{path.name}/)")

        tags = "\n".join(
            [
                f"![{x}](https://img.shields.io/badge/-{x}-green?style=flat)"
                for x in meta.tags
            ],
        )
        desc = "".join([f"> {x}" for x in meta.desc.splitlines()])

        readme = (
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

        readme = f"{readme}\n\n## 配置内容\n\n```json\n{reply}\n```"

        readme_path.write_text(readme, encoding="u8")

    SIDEBAR_MD_PATH.write_text("\n".join(sidebar), encoding="u8")


if __name__ == "__main__":
    main()
