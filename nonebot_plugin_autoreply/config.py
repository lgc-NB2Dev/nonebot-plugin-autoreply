import json
from pathlib import Path
from typing import Any, Dict, Generic, List, Literal, Optional, Tuple, TypeVar, Union

from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseModel

T = TypeVar("T")

DATA_PATH = Path.cwd() / "data" / "autoreply"
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)


MatchType = Union[str, "MatchModel"]
ReplyType = Union[str, List["MessageSegmentModel"], "ReplyModel"]
MessageType = Union[str, List["MessageSegmentModel"], List[ReplyType]]


class MatchModel(BaseModel):
    type: Literal["full", "fuzzy", "regex", "poke"] = "fuzzy"  # noqa: A003
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
    delay: Tuple[int, int] = (0, 0)


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
config = ConfigModel.parse_obj(get_driver().config)


def reload_replies() -> Tuple[int, int]:
    replies.clear()

    success = 0
    fail = 0

    for json_path in DATA_PATH.glob("*.json"):
        file_name = json_path.name

        try:
            replies.extend(
                [
                    ReplyEntryModel(**x)
                    for x in json.loads(json_path.read_text(encoding="u8"))
                ],
            )

        except Exception:
            logger.opt(colors=True).exception(
                f"加载回复配置 <y>{file_name}</y> <l><r>失败</r></l>",
            )
            fail += 1

        else:
            logger.opt(colors=True).info(f"加载回复配置 <y>{file_name}</y> <l><g>成功</g></l>")
            success += 1

    replies.sort(key=lambda x: x.priority)
    logger.opt(colors=True).info(
        "加载回复配置完毕，"
        f"<l><g>成功</g></l> <y>{success}</y> 个，"
        f"<l><r>失败</r></l> <y>{fail}</y> 个",
    )
    return success, fail


reload_replies()
