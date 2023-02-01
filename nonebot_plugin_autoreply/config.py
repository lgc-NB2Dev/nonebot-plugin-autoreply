import json
from pathlib import Path
from typing import Any, Dict, Generic, List, Literal, TypedDict, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")

DATA_PATH = Path.cwd() / "data" / "autoreply"
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)

REPLY_JSON_PATH = DATA_PATH / "replies.json"
if not REPLY_JSON_PATH.exists():
    REPLY_JSON_PATH.write_text("[]", encoding="u8")


class ReplyEntry(BaseModel):
    class Match(BaseModel):
        match: str
        type: Literal["full", "fuzzy", "regex"] = "fuzzy"
        to_me: bool = False
        ignore_case: bool = True
        strip: bool = True
        allow_plaintext: bool = True

    class ReplyDict(TypedDict):
        type: str
        data: Dict[str, Any]

    class Filter(BaseModel, Generic[T]):
        type: Literal["black", "white"] = "black"
        values: List[T]

    matches: List[Match]
    replies: List[Union[str, List[ReplyDict]]]
    groups: Filter[int] = Filter(values=[])
    users: Filter[int] = Filter(values=[])


replies = [
    ReplyEntry(**x) for x in json.loads(REPLY_JSON_PATH.read_text(encoding="u8"))
]
