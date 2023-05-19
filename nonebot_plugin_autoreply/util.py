from typing import Any, Dict, Tuple, Union, cast

from anyio import Path
from nonebot.adapters.onebot.utils import f2s
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PokeNotifyEvent,
)

VarDictType = Tuple[Dict[str, Any], Dict[str, Any]]


async def get_var_dict(
    bot: Bot,
    event: Union[MessageEvent, PokeNotifyEvent],
) -> VarDictType:
    is_message = isinstance(event, MessageEvent)
    is_group = isinstance(event, GroupMessageEvent)
    is_poke = isinstance(event, PokeNotifyEvent)

    message = event.get_message() if is_message else None
    plaintext = event.get_plaintext() if is_message else None
    message_id = event.message_id if is_message else None
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

    normal_var = {
        "bs": "{",
        "be": "}",
        "self_id": event.self_id,
        "message_id": message_id,
        "user_id": user_id,
        "group_id": group_id,
        "target_id": event.target_id if is_poke else None,
        "nickname": nickname,
        "card": card,
        "display_name": card or nickname,
        "plaintext": plaintext,
    }
    seg_var = {
        "at": MessageSegment.at(user_id),
        "reply": MessageSegment.reply(message_id) if message_id else None,
        "message": message,
    }
    return normal_var, seg_var


async def replace_message_var(message: Message, var_dict: VarDictType) -> Message:
    normal_var, seg_var = var_dict
    message = cast(
        Message,
        Message.template(message).format_map({**normal_var, **seg_var}),
    )

    for seg in message:
        if not seg.is_text():
            for k, v in seg.data.items():
                if isinstance(v, str):
                    seg.data[k] = v.format(**normal_var)

        if seg.type in ("image", "record"):
            file = seg.data.get("file")
            if isinstance(file, str) and file.startswith("file:///"):
                seg.data["file"] = f2s(await Path(file[8:]).read_bytes())

    return message
