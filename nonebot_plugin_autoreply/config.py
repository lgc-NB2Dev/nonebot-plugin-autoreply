import json
from pathlib import Path
from typing import Any, Dict, Generic, List, Literal, Tuple, TypeVar, Union

from nonebot import get_driver
from pydantic import BaseModel

T = TypeVar("T")

DATA_PATH = Path.cwd() / "data" / "autoreply"
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)

REPLY_JSON_PATH = DATA_PATH / "replies.json"
if not REPLY_JSON_PATH.exists():
    REPLY_JSON_PATH.write_text("[]", encoding="u8")

MatchType = Union[str, "MatchModel"]
ReplyType = Union[str, List["MessageSegmentModel"], "ReplyModel"]


class MatchModel(BaseModel):
    match: str
    type: Literal["full", "fuzzy", "regex"] = "fuzzy"  # noqa: A003
    to_me: bool = False
    ignore_case: bool = True
    strip: bool = True
    allow_plaintext: bool = True


class MessageSegmentModel(BaseModel):
    type: str  # noqa: A003
    data: Dict[str, Any]


class ReplyModel(BaseModel):
    type: Literal["normal", "plain", "array", "multi"]  # noqa: A003
    message: Union[str, List[MessageSegmentModel], List[ReplyType]]
    delay: Tuple[int, int] = (0, 0)


class FilterModel(BaseModel, Generic[T]):
    type: Literal["black", "white"] = "black"  # noqa: A003
    values: List[T]


class ReplyEntryModel(BaseModel):
    matches: List[MatchType]
    replies: List[ReplyType]
    groups: FilterModel[int] = FilterModel(values=[])
    users: FilterModel[int] = FilterModel(values=[])


class ConfigModel(BaseModel):
    autoreply_block: bool = False
    autoreply_priority: int = 99


replies: List[ReplyEntryModel] = []
config = ConfigModel.parse_obj(get_driver().config)


def reload_replies():
    replies.clear()
    replies.extend(
        [
            ReplyEntryModel(**x)
            for x in json.loads(REPLY_JSON_PATH.read_text(encoding="u8"))
        ],
    )


reload_replies()
