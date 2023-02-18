import asyncio
import random
import re
from itertools import starmap
from typing import Callable, Iterable, List, Optional, Tuple, TypeVar, cast

from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from typing_extensions import TypeVarTuple, Unpack

from .config import (
    FilterModel,
    MatchModel,
    MessageSegmentModel,
    ReplyModel,
    ReplyType,
    config,
    reload_replies,
    replies,
)

T = TypeVar("T")
TArgs = TypeVarTuple("TArgs")


def check_list(
    function: Callable[[Unpack[TArgs]], bool],
    will_check: Iterable[tuple[Unpack[TArgs]]],
    is_any: bool = False,
) -> bool:
    # 感谢 nb2 群内 Bryan不可思议 佬的帮助！！
    iterator = starmap(function, will_check)
    return any(iterator) if is_any else all(iterator)


def check_filter(filter: FilterModel[T], val: Optional[T]) -> bool:
    # 判断黑名单 值不在列表中ok
    ok = val not in filter.values
    if filter.type == "white":  # 白名单则反过来
        ok = not ok
    return ok


def check_match(match: MatchModel, event: MessageEvent) -> bool:
    if match.to_me and (not event.is_tome()):
        return False

    msg_str = str(event.message)
    msg_plaintext = event.message.extract_plain_text()
    match_template = match.match

    if match.strip:
        msg_str = msg_str.strip()
        msg_plaintext = msg_plaintext.strip()

    if match.type == "regex":
        flag = re.I if match.ignore_case else 0
        return bool(
            (re.search(match_template, msg_str, flag))
            or (
                re.search(match_template, msg_plaintext, flag)
                if match.allow_plaintext
                else False
            )
        )

    if match.ignore_case:
        # regex 匹配已经处理过了，这边不需要管
        msg_str = msg_str.lower()
        match_template = match_template.lower()

    if match.type == "full":
        return (msg_str == match_template) or (
            msg_plaintext == match_template if match.allow_plaintext else False
        )

    # default fuzzy
    if (not msg_str) or (match.allow_plaintext and (not msg_plaintext)):
        return False
    return (match_template in msg_str) or (
        (match_template in msg_plaintext) if match.allow_plaintext else False
    )


async def message_checker(event: MessageEvent, state: T_State) -> bool:
    group = event.group_id if isinstance(event, GroupMessageEvent) else None

    for reply in replies:
        filter_checks = [(reply.groups, group), (reply.users, event.user_id)]
        match_checks = [(x, event) for x in reply.matches]

        if not (
            check_list(check_filter, filter_checks)
            and check_list(check_match, match_checks, True)
        ):
            continue

        state["reply"] = random.choice(reply.replies)
        return True

    return False


def get_reply_msgs(
    reply: ReplyType, refuse_multi: bool = False
) -> Tuple[List[Message], Optional[Tuple[int, int]]]:
    if isinstance(reply, str):
        reply = ReplyModel(type="normal", message=reply)
    elif isinstance(reply, list):
        reply = ReplyModel(type="array", message=reply)

    rt = reply.type
    msg = reply.message

    if rt == "plain":
        return [Message() + cast(str, msg)], None

    if rt == "array":
        return [
            Message(
                [
                    MessageSegment(type=x.type, data=x.data)
                    for x in cast(List[MessageSegmentModel], msg)
                ]
            )
        ], None

    if rt == "multi":
        if refuse_multi:
            raise ValueError("Nested `multi` is not allowed")
        return [
            get_reply_msgs(x, True)[0][0] for x in cast(List[ReplyModel], msg)
        ], reply.delay

    # default normal
    return [Message(cast(str, msg))], None


autoreply_matcher = on_message(
    rule=message_checker,
    block=config.autoreply_block,
    priority=config.autoreply_priority,
)


@autoreply_matcher.handle()
async def _(matcher: Matcher, state: T_State):
    reply: ReplyType = state["reply"]

    msg, delay = get_reply_msgs(reply)
    for m in msg:
        await matcher.send(m)

        if delay:
            await asyncio.sleep(random.randint(*delay) / 1000)


reload_matcher = on_command("重载自动回复", permission=SUPERUSER)


@reload_matcher.handle()
async def _(matcher: Matcher):
    try:
        reload_replies()
    except:
        logger.exception("重载配置失败")
        await matcher.finish("重载失败，请检查后台输出")
    else:
        await matcher.finish("重载自动回复配置成功~")
