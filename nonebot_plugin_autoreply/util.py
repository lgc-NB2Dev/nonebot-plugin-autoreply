from typing import Any, Dict, Union, cast

from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PokeNotifyEvent,
)


async def get_var_dict(
    bot: Bot,
    event: Union[MessageEvent, PokeNotifyEvent],
) -> Dict[str, Any]:
    is_message = isinstance(event, MessageEvent)
    is_group = isinstance(event, GroupMessageEvent)
    is_poke = isinstance(event, PokeNotifyEvent)

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

    return {
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
        "at": MessageSegment.at(user_id),
        "reply": MessageSegment.reply(message_id) if message_id else None,
    }


def replace_message_var(message: Message, var_dict: Dict[str, Any]) -> Message:
    return cast(Message, Message.template(message).format_map(var_dict))
