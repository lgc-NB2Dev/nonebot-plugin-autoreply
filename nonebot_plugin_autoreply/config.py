import json
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

import yaml
from nonebot import get_plugin_config
from nonebot.log import logger
from pydantic import BaseModel

T = TypeVar("T")

DATA_PATH = Path.cwd() / "data" / "autoreply"
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)

ALLOWED_SUFFIXES = (".json", ".yml", ".yaml")

MatchType = Union[str, "MatchModel"]
ReplyType = Union[str, List["MessageSegmentModel"], "ReplyModel"]
MessageType = Union[str, List["MessageSegmentModel"], List[ReplyType]]


class MatchModel(BaseModel):
    type: Literal[  # noqa: A003
        "full",
        "fuzzy",
        "start",
        "end",
        "regex",
        "poke",
    ] = "fuzzy"
    possibility: float = 1.0

    match: Optional[str] = None
    to_me: bool = False
    ignore_case: bool = True
    strip: bool = True
    allow_plaintext: bool = True


class MessageSegmentModel(BaseModel):
    type: str  # noqa: A003
    data: Dict[str, Any]


class ReplyModel(BaseModel):
    type: Literal["normal", "plain", "array", "multi"]  # noqa: A003
    message: MessageType
    shuffle: bool = False
    delay: Union[Tuple[int, int], int] = (0, 0)


class FilterModel(BaseModel, Generic[T]):
    type: Literal["black", "white"] = "black"  # noqa: A003
    values: List[T]


# TODO cool down
# class CoolDownModel(BaseModel):
#     type: Literal["user", "group"] = "group"  # noqa: A003
#     """cd类型，user为每个人的cd，group为每个群的cd"""
#     time: float
#     """cd时长，单位秒"""
#     tip: Optional[str] = None
#     """正在cd中的提示，None或空字符串为不提示"""


class ReplyEntryModel(BaseModel):
    block: bool = True
    priority: int = 1
    # cool_down: Optional[CoolDownModel] = None
    matches: List[MatchType]
    replies: List[ReplyType]
    groups: FilterModel[int] = FilterModel(values=[])
    users: FilterModel[int] = FilterModel(values=[])


# TODO class ResolvedReplyEntryModel
# 在配置项载入的之后就规范化配置项模型，减少运行时开销


class ConfigModel(BaseModel):
    autoreply_block: bool = False
    autoreply_priority: int = 99


replies: List[ReplyEntryModel] = []
config = get_plugin_config(ConfigModel)


def iter_config_path(root_path: Path = DATA_PATH) -> Iterator[Path]:
    for path in root_path.iterdir():
        if path.is_dir():
            yield from iter_config_path(path)

        if path.is_file() and (path.suffix in ALLOWED_SUFFIXES):
            yield path


def load_config(path: Path) -> List[ReplyEntryModel]:
    content = path.read_text(encoding="u8")

    if path.suffix in (".yml", ".yaml"):
        obj: list = yaml.safe_load(content)
    else:
        obj: list = json.loads(content)

    return [ReplyEntryModel(**x) for x in obj]


def reload_replies() -> Tuple[int, int]:
    replies.clear()

    success = 0
    fail = 0

    for path in iter_config_path():
        file_name = path.name

        try:
            replies.extend(load_config(path))

        except Exception:
            logger.opt(colors=True).exception(
                f"加载回复配置 <y>{file_name}</y> <l><r>失败</r></l>",
            )
            fail += 1

        else:
            logger.opt(colors=True).info(
                f"加载回复配置 <y>{file_name}</y> <l><g>成功</g></l>",
            )
            success += 1

    replies.sort(key=lambda x: x.priority)
    logger.opt(colors=True).info(
        f"加载回复配置完毕，<l>成功 <g>{success}</g> 个，失败 <r>{fail}</r> 个</l>",
    )
    return success, fail


reload_replies()
