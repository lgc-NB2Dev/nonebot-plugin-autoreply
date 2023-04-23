import json
from pathlib import Path
from typing import Any, Dict, Generic, List, Literal, Tuple, TypeVar, Union

from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseModel

T = TypeVar("T")

DATA_PATH = Path.cwd() / "data" / "autoreply"
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)


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

    logger.opt(colors=True).info(
        "加载回复配置完毕，"
        f"<l><g>成功</g></l> <y>{success}</y> 个，"
        f"<l><r>失败</r></l> <y>{fail}</y> 个",
    )
    return success, fail


reload_replies()
