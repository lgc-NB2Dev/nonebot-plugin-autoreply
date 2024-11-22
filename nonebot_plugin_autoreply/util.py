import mimetypes
import random
from typing import Any, Dict, Optional, Tuple, Union, cast

from anyio import Path
from nonebot import logger
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


SEG_MIMETYPES = {
    "image": "image/",
    "record": "audio/",
}


async def process_res_seg(seg: MessageSegment):
    file = seg.data.get("file")
    if not (isinstance(file, str) and file.startswith("file:///")):
        return

    path = Path(file[8:])
    if await path.is_dir():
        f = await get_random_file(path, SEG_MIMETYPES[seg.type])
        if not f:
            logger.warning(f"No files matched expected file type for {seg.type}")
            return
        path = f

    try:
        seg.data["file"] = f2s(await path.read_bytes())
    except Exception as e:
        logger.error(f"Failed to read file {path}: {type(e).__name__}: {e}")
        logger.opt(exception=e).debug("Stacktrace")


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
            await process_res_seg(seg)

    return message


async def get_random_file(base_path: Path, mime_pfx: str) -> Optional[Path]:
    async def inner(p: Path):
        async for x in p.iterdir():
            if await x.is_dir():
                async for y in inner(x):
                    yield y

            mime = mimetypes.guess_type(x.name)[0]
            if mime and mime.startswith(mime_pfx):
                yield x

    return random.choice([x async for x in inner(base_path)])
