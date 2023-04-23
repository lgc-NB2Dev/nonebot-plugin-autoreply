from typing import Any, Dict, Iterable, List

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent

from .config import MessageSegmentModel


def get_var_dict(event: MessageEvent) -> Dict[str, Any]:
    is_group = isinstance(event, GroupMessageEvent)
    return {
        "self_id": event.self_id,
        "message_id": event.message_id,
        "user_id": event.user_id,
        "nickname": event.sender.nickname,
        "card": event.sender.card,
        "group_id": event.group_id if is_group else None,
    }


def replace_str_var(string: str, var_dict: Dict[str, Any]) -> str:
    return string.format(**var_dict)


def replace_segment_var(
    segments: Iterable[MessageSegmentModel],
    var_dict: Dict[str, Any],
) -> List[MessageSegmentModel]:
    segments = [x.copy(deep=True) for x in segments]

    for seg in segments:
        for k, v in seg.data.items():
            if isinstance(v, str):
                seg.data[k] = replace_str_var(v, var_dict)

    return segments
