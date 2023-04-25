from typing import Any, Dict, Iterable, List, Union

from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    PokeNotifyEvent,
)

from .config import MessageSegmentModel


async def get_var_dict(
    bot: Bot,
    event: Union[MessageEvent, PokeNotifyEvent],
) -> Dict[str, Any]:
    is_message = isinstance(event, MessageEvent)
    is_group = isinstance(event, GroupMessageEvent)
    is_poke = isinstance(event, PokeNotifyEvent)

    user_id = event.user_id
    group_id = event.group_id if is_group or is_poke else None

    if is_poke:
        sender = (
            await bot.get_group_member_info(group_id=group_id, user_id=user_id)
            if group_id
            else await bot.get_stranger_info(user_id=user_id)
        )
        nickname = sender["nickname"]
        card = sender.get("card")

    else:
        sender = event.sender
        nickname = sender.nickname
        card = sender.card

    return {
        "self_id": event.self_id,
        "message_id": event.message_id if is_message else None,
        "user_id": user_id,
        "group_id": group_id,
        "target_id": event.target_id if is_poke else None,
        "nickname": nickname,
        "card": card,
        "display_name": card or nickname,
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
